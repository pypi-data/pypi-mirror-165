from autoretouchlib.logging import log


class Metrics:
    disabled = True

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, project: str):
        import os
        self.disabled = not os.getenv("METRICS_ENABLED", 'False').lower() in ('true', '1', 't')
        if self.disabled:
            return

        self.project = project

        self.storage_access_sink = lambda data: log.debug(
            message="storage_access",
            name="storage_access",
            **data
        )

        log.info("Metrics initialized!")

    def count_storage_access(self, storage_class: str, operation: str, file_type: str, **kwargs):
        if self.disabled:
            return
        try:
            self.storage_access_sink(dict(
                storageClass="STANDARD" if storage_class is None else storage_class,
                operation=operation,
                fileType="application/octet-stream" if file_type is None else file_type,
                **kwargs
            ))
        except Exception as e:
            log.info("Error while writing metric logs!", dict(error=e))
