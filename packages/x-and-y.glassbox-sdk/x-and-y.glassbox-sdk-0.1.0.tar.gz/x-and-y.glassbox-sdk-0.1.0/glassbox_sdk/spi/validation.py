import logging
from dataclasses import dataclass
from typing import List, Optional, TextIO
from unittest import TextTestRunner, TextTestResult


@dataclass
class Logging:
    spec: dict
    logs: List[str]

    def as_dict(self):
        return {
            "spec": self.spec,
            "logs": self.logs
        }


OptLogs = Optional[Logging]


class CustomTestRunner(TextTestRunner):
    logs: List[str] = []

    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity, self.logs)

    def gather_hardware_spec(self):
        import platform
        uname = platform.uname()
        common = {
            "system": uname.system,
            "version": uname.version,
            "machine": uname.machine,
            "processor": uname.processor
        }

        try:
            def get_size(bytes, suffix="B"):
                """
                Scale bytes to its proper format
                e.g:
                    1253656 => '1.20MB'
                    1253656678 => '1.17GB'
                """
                factor = 1024
                for unit in ["", "K", "M", "G", "T", "P"]:
                    if bytes < factor:
                        return f"{bytes:.2f}{unit}{suffix}"
                    bytes /= factor

            import psutil
            common["cpu_physical_count"] = psutil.cpu_count(logical=False)
            common["cpu_total_count"] = psutil.cpu_count(logical=True)
            cpufreq = psutil.cpu_freq()
            common["cpu_max_frequency"] = f"{cpufreq.max:.2f}Mhz"
            common["cpu_min_frequency"] = f"{cpufreq.min:.2f}Mhz"

            svmem = psutil.virtual_memory()
            common["ram_total"] = get_size(svmem.total)
        except ImportError:
            logging.warning("no psutil dependency found")

        try:
            import GPUtil
            gpus = GPUtil.getGPUs()

            common["gpu"] = {}
            for gpu in gpus:
                common["gpu"][gpu.id] = {
                    "name": gpu.name,
                    "memory": f"{gpu.memoryTotal}MB"
                }

        except ImportError:
            logging.warning("no gputil dependency found")

        return common

    def get_logs(self) -> Logging:
        return Logging(self.gather_hardware_spec(), self.logs)

# def run(self, test) -> unittest.result.TestResult:
# add implementation as per TextTestRunner run method here

class CustomTestResult(TextTestResult):

    def __init__(self, stream: TextIO, descriptions: bool, verbosity: int, logs: List[str]) -> None:
        super().__init__(stream, descriptions, verbosity)
        self.logs = logs

    def addSuccess(self, test):
        super(CustomTestResult, self).addSuccess(test)
        self.logs.append("SUCCESS: " + test.__class__.__name__ + "#" + test._testMethodName)

    def addFailure(self, test):
        super(CustomTestResult, self).addFailure(test)
        self.logs.append("FAILURE: " + test.__class__.__name__ + "#" + test._testMethodName)
