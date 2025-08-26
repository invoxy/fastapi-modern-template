class MiniOError(Exception):
    class FileDownloadError(Exception):
        def __init__(self, message: str, s3_key: str):
            message = f"Ошибка при скачивании файла из S3: {s3_key}"
            super().__init__(message)

    class FileUploadError(Exception):
        def __init__(self, message: str, s3_key: str):
            message = f"Ошибка при загрузке файла в S3: {s3_key}"
            super().__init__(message)

    class StreamUploadError(Exception):
        def __init__(self, s3_key: str, error: str):
            self.s3_key = s3_key
            self.error = error
            super().__init__(
                f"Streaming upload failed for key: {s3_key}. Error: {error}"
            )
