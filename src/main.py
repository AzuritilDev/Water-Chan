import os
import sys
import random
import threading
import tkinter as tk
import pystray
import importlib.metadata
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from apscheduler.schedulers.background import BackgroundScheduler
from notifypy import Notify
from pathlib import Path

# probably didn't need to add an if statement for this
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

def get_version(package_name: str) -> str:
    """Returns the package version for both installed (prod) and uninstalled (dev) states."""
    # prod
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        pass

    # local dev env
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    
    if pyproject_path.exists() and tomllib is not None:
        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                
            # Try standard PEP 621 [project] table
            if "project" in data and "version" in data["project"]:
                return data["project"]["version"]
                
            # Try dynamic Poetry [tool.poetry] table
            if "tool" in data and "poetry" in data["tool"] and "version" in data["tool"]["poetry"]:
                return data["tool"]["poetry"]["version"]
        except Exception:
            pass  # Fall through to default if file reading fails

    return "(An error occured while fetching the version.)"

__version__ = get_version("waterchan")

# Initializing the root here because I don't wanna deal with scope related bs
root = tk.Tk()

# Initializing the scheduler globally so it persists in the background
scheduler = BackgroundScheduler()
scheduler.start()

def resource_path(relative_path):
    """Get absolute path to resource"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def re_open_app():
    root.iconify()

def trigger_reminder(name):
    """The event that fires when the scheduled reminder time arrives."""
    notification = Notify()
    notification.application_name = "Water-Chan App"
    notification.title = f"Hey! {name}!"
    notification.message = f"It's time to drink water, {name}"
    notification.icon = resource_path(os.path.join("assets", "waterchanicon_png.png"))
    notification.send()

def create_tray_icon():
    """
    Generates a simple default 64x64 icon image dynamically.
    Dev environment only placeholder.
    """
    image = Image.new('RGB', (64, 64), color='blue')
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill='white')
    return image

def quit_tray_app(icon):
    """Fully shuts down the background scheduler and the tray icon."""
    scheduler.shutdown()
    icon.stop()
    root.destroy() # NOTE: For some reason, this is the line that ACTUALLY closes the app 
    # (Atleast in dev environment)
    exit(code=0)

def run_tray_icon():
    """Starts the system tray loop. This keeps the script alive in the background."""
    try:
        icon_image = Image.open(resource_path(os.path.join("assets", "waterchanicon_ico.ico")))
    except:
        icon_image = create_tray_icon()
        """
        Ah, yes, let's just use the clanker generated **dev environment only** placeholder 
        image and completely ignore the fact that we cannot access an asset which was
        packaged WITH the application meaning there is a potential concern
        that NONE of the assets are in the appdata directory we are searching resources
        from.
        """
    icon = pystray.Icon(
        "Water Chan Reminder App",
        icon_image,
        title="Water Chan Reminder App",
        menu=pystray.Menu(
            pystray.MenuItem("Open App", re_open_app),
            pystray.MenuItem("Quit Completely", quit_tray_app)
        )
    )
    icon.run()

def turn_on_reminder(name_entry):
    name = name_entry.get()
    # Don't forget to clean the entry label
    name_entry.delete(0, "end")
    
    # 1. Calculate a random execution time between 7:00 PM and 9:00 PM today
    now = datetime.now()
    start_window = now.replace(hour=19, minute=0, second=0, microsecond=0)
    end_window = now.replace(hour=21, minute=0, second=0, microsecond=0)
    
    # Calculate difference in seconds and pick a random offset
    delta_seconds = int((end_window - start_window).total_seconds())
    random_offset = random.randint(0, delta_seconds)
    target_time = start_window + timedelta(seconds=random_offset)
    
    # Fallback if 7:00 PM - 9:00 PM has already passed for today
    if target_time < now:
        target_time += timedelta(days=1)
    
    # 2. Schedule the background task using APScheduler
    scheduler.add_job(
        trigger_reminder, 
        'date', 
        run_date=target_time, 
        args=[name],
        id='reminder_job'
    )
    
    # 3. "Close" the app frontend
    root.withdraw()
    
    # 4. Offload the system tray icon to a separate background thread
    # This prevents pystray from blocking the main script cleanup execution
    tray_thread = threading.Thread(target=run_tray_icon, daemon=True)
    tray_thread.start()

# --- Tkinter GUI Setup ---
root.title("Reminder App")
root.geometry("320x420")
root.resizable(False, False)

tk.Label(root, text=f"App Version: v{__version__}", font=("TkDefaultFont", 7)).pack(pady=3)

photo = tk.PhotoImage(file=resource_path(os.path.join("assets", "waterchan.png"))).subsample(2)
label = tk.Label(root, image=photo)
label.pack(anchor="center", expand=True)

tk.Label(root, text="Enter Your Name:").pack(pady=10)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

tk.Button(
    root, 
    text="Remind me between 7 PM - 9 PM!", 
    command=lambda: turn_on_reminder(name_entry)
).pack(pady=15)

root.mainloop()
