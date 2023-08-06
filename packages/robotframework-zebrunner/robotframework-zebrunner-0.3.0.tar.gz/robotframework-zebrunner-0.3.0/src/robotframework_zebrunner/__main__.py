import sys

from robotframework_zebrunner.api.client import ZebrunnerAPI
from robotframework_zebrunner.context import zebrunner_context


def attach_reports() -> None:
    with open(".zbr-test-run-id", "r") as f:
        test_run_id = int(f.readline())
        api = ZebrunnerAPI(zebrunner_context.settings.server.hostname, zebrunner_context.settings.server.access_token)
        api.auth()
        api.send_artifact("log.html", test_run_id)
        api.send_artifact("report.html", test_run_id)
        print("Success")


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "attach-reports":
        attach_reports()
    else:
        raise ValueError("Unknown command")