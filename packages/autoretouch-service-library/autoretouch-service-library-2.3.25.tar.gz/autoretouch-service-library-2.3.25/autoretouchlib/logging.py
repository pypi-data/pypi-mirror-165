import json
import os


class Logging:
    service_name = os.getenv("K_SERVICE") if os.getenv("K_SERVICE") else os.getenv("SERVICE_NAME",
                                                                                   "test-service")

    def log(self, severity="INFO", message=None, **args):
        if message is None:
            message = f"Log for {self.service_name}"
        print(
            json.dumps(dict(
                severity=severity,
                message=message,
                serviceName=self.service_name,
                **args
            ))
        )

    def debug(self, message, **args):
        self.log("DEBUG", message, **args)

    def info(self, message, **args):
        self.log("INFO", message, **args)

    def warn(self, message, **args):
        self.log("WARNING", message, **args)

    def error(self, message, **args):
        self.log("ERROR", message, **args)


log = Logging()
