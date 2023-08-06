from pkg_resources import get_distribution, DistributionNotFound, packaging
from update_checker import UpdateChecker
try:
    __version__ = get_distribution("quantagonia-api-client").version
    checker = UpdateChecker()
    result = checker.check('quantagonia-api-client', __version__)
    if packaging.version.parse(result.available_version) > packaging.version.parse(result.running_version):
        print(f"Warning: Installed version {result.running_version} of quantagonia-api-client is outdated. Please update to newest version {result.available_version}.")
except DistributionNotFound:
    __version__ = "dev"
