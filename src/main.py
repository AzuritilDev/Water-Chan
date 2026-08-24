import os
import sys
import random
import threading
import tkinter as tk
import pystray
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from apscheduler.schedulers.background import BackgroundScheduler
from notifypy import Notify
from utils import ver

# Fetch the app version
__version__ = ver.get_version("waterchan")

# The main job ID that will be used for the reminder schedule
primary_job_id = "reminder_job"

# Initializing the root here because I don't wanna deal with scope related bs
root = tk.Tk()

# It would've probably been better if I used an "app" class to initialize the GUI but ehh
turn_on_button : tk.Button = None

# Initializing the scheduler globally so it persists in the background
scheduler = BackgroundScheduler()
scheduler.start()

# Pystray icon that the app will use
icon = None

def resource_path(relative_path):
    """Get absolute path to resource"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def re_open_app():
    """When fired, displays the hidden gui"""
    root.iconify()

def alert_notification(app_name : str = "Water-Chan", 
                       title : str = None, 
                       message : str = None, 
                       icon : str = resource_path(os.path.join("assets", "waterchanicon_png.png")),
                       sound_effect : str = resource_path(os.path.join("assets", "notif.wav"))
                       ):
    notification = Notify()
    notification.application_name = app_name
    notification.title = title
    notification.message = message
    notification.icon = icon
    notification.audio = sound_effect
    notification.send()

def trigger_reminder(name):
    """The event that fires when the scheduled reminder time arrives."""
    alert_notification(title=f"Hey! {name}!", 
                       message=f"It's time to drink water, {name}")

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
            pystray.MenuItem("Quit Completely (Will Stop Reminder)", quit_tray_app)
        )
    )
    icon.run()

    return icon

def stop_tray_icon(icon):
    """Stop running the tray icon"""
    if icon != None:
        icon.stop()

def turn_on_reminder(name_entry):
    name = name_entry.get()
    # Don't forget to clean the entry label
    name_entry.delete(0, "end")

    if name == "" or name == " ":
        name = "Anon"

    job_exists = scheduler.get_job(primary_job_id)
    if job_exists:
        scheduler.remove_job(primary_job_id)
        # OFF - Let the user know the app has been turned off
        turn_on_button.config(text="Turn On (7 PM - 9 PM)")

        # Stop the tray icon from running
        stop_tray_icon(icon=icon)

        alert_notification(title=f"Reminder Removed!",
                       message=f"Existing water drinking reminder removed.")
        return
        

    # ON - Let the user know the app has been turned on
    alert_notification(title=f"Reminder Set!",
                       message=f"Water drinking reminder set for {name} between 7 PM - 9 PM")
    
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
        "date", 
        run_date=target_time, 
        args=[name],
        id=primary_job_id
    )

    turn_on_button.config(text="Turn Off")
    
    # 3. "Close" the app frontend (Really it just hides it)
    root.withdraw()
    
    # 4. Offload the system tray icon to a separate background thread
    # This prevents pystray from blocking the main script cleanup execution
    tray_thread = threading.Thread(target=run_tray_icon, daemon=True)
    tray_thread.start()

# --- Tkinter GUI Setup ---
root.title("Reminder App")
root.geometry("320x430")
root.resizable(False, False)
root.iconbitmap(resource_path(os.path.join("assets", "waterchanicon_ico.ico")))

tk.Label(root, text=f"App Version: v{__version__}", font=("TkDefaultFont", 7)).pack(pady=3)

photo = tk.PhotoImage(file=resource_path(os.path.join("assets", "waterchan.png"))).subsample(2)
label = tk.Label(root, image=photo)
label.pack(anchor="center", expand=True)

tk.Label(root, text="Enter Your Name:").pack(pady=10)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

turn_on_button = tk.Button(
    root, 
    text="Turn On (7 PM - 9 PM)", 
    command=lambda: turn_on_reminder(name_entry),
    height=10
)

turn_on_button.pack(pady=15)

root.mainloop()
