import pytest
import sys
import logging
[pytest]
sys.path.append(r'D:\PythonProjects\TMSandbox\TMSandboxAPIs')
log = logging.getLogger()
log.setLevel(logging.INFO)
log_format = "%(asctime)s %(levelname)s %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"


def pytest_html_report_title(report):
    report.title = "TM Sandbox API Test"

