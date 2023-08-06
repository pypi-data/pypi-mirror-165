from pkg_resources import get_distribution, DistributionNotFound, packaging
import requests

def check_version():
    """Check for updates of the package."""
    try:
        # query latest version from pypi
        package="quantagonia-api-client"
        response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=1)
        latest_version = response.json()["info"]["version"]

        # print warning if update available
        if packaging.version.parse(latest_version) > packaging.version.parse(__version__):
            print("Warning: ", end="")
            print(f"Installed version {__version__} of quantagonia-api-client is outdated. ", end="")
            print(f"Consider updating to newest version {latest_version}.")

    except:
        # catch all, the check for updates should never fail
        pass

try:
    __version__ = get_distribution("quantagonia-api-client").version
    check_version()
except DistributionNotFound:
    __version__ = "dev"
    # don't check for updates in this case
