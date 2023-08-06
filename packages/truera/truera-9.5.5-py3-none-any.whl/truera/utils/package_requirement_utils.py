from dataclasses import dataclass
from typing import Optional

from importlib_metadata import PackageNotFoundError
from importlib_metadata import version

DEFAULT_PIP_VERSION = "20.3"


def get_module_version(module_name: str) -> Optional[str]:
    # devnote: using importlib_metadata over __version__ which does not work for some libs
    try:
        return version(module_name)
    except PackageNotFoundError:
        return None


@dataclass(frozen=True)
class PythonPackageRequirement:
    # min and max versions are inclusive.
    package_name: str
    min_version: Optional[str] = None
    max_version: Optional[str] = None

    def get_requirement_string(self) -> str:
        req_string = self.package_name
        version_strings = []
        if self.min_version:
            version_strings.append(f">={self.min_version}")
        if self.max_version:
            version_strings.append(f"<={self.max_version}")
        return req_string + ",".join(version_strings)


MODEL_RUNNER_ML_REQUIREMENTS = [
    PythonPackageRequirement("numpy"),
    PythonPackageRequirement("pandas"),
    PythonPackageRequirement("scipy")
]
MODEL_RUNNER_SYS_REQUIREMENTS = [
    PythonPackageRequirement("flask", max_version="2.1.3"),
    PythonPackageRequirement("protobuf", max_version="3.20.1"),
    PythonPackageRequirement("urllib3"),
    PythonPackageRequirement("gunicorn"),
    PythonPackageRequirement("pyyaml"),
    PythonPackageRequirement("importlib-metadata")
]
SDK_PACKAGING_REQUIREMENTS = [
    PythonPackageRequirement("cloudpickle"),
    PythonPackageRequirement("pickle5"),
]  # adding pickle5 as cloudpickle uses pickle5 instead of pickle if installed
