import sys
import importlib.metadata
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

if __name__ == "__main__":
    get_version("waterchan")