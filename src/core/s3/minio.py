import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path

import aioboto3
from botocore.exceptions import ClientError
from loguru import logger

from .exceptions import MiniOError


class MinioClient:
    def __init__(
        self,
        endpoint_url: str,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str,
        is_https: bool,  # noqa: FBT001
    ):
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.is_https = is_https

        self.session = aioboto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    async def upload_to_s3(
        self, file_path: str, s3_key: str, max_size_mb: int = 25
    ) -> None:
        file_path_obj = Path(file_path)
        file_size = file_path_obj.stat().st_size / (1024 * 1024)
        if file_size > max_size_mb:
            raise MiniOError.FileSizeExceededError(
                s3_key=s3_key, max_size_mb=max_size_mb
            )
        try:
            async with self.session.client(
                "s3",
                region_name=self.region_name,
                use_ssl=self.is_https,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as s3_client:
                await s3_client.upload_file(file_path, self.bucket_name, s3_key)

        except ClientError:
            MiniOError.FileUploadError(s3_key=s3_key)

    async def download_from_s3(self, s3_key: str, file_path: str) -> None:
        """
        Скачивает файл из S3.

        :param bucket_name: Имя S3-бакета.
        :param s3_key: Ключ объекта в S3 (путь внутри бакета).
        :param file_path: Путь для сохранения локального файла.
        """
        try:
            async with self.session.client(
                "s3",
                region_name=self.region_name,
                use_ssl=self.is_https,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as s3_client:
                await s3_client.download_file(self.bucket_name, s3_key, file_path)

        except ClientError:
            MiniOError.FileDownloadError(s3_key=s3_key)

    async def list_s3_files(self, prefix: str = "") -> None | list:  # noqa: RUF036
        """
        Возвращает список файлов в указанном S3-бакете.

        :param bucket_name: Имя S3-бакета.
        :param prefix: Префикс (путь) для фильтрации файлов.
        :return: Список файлов (ключей).
        """
        try:
            async with self.session.client(
                "s3",
                region_name=self.region_name,
                use_ssl=self.is_https,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as s3_client:
                response = await s3_client.list_objects_v2(
                    Bucket=self.bucket_name, Prefix=prefix
                )
                return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError:
            return []

    async def delete_from_s3(self, s3_key: str) -> None:
        """
        Удаляет файл из S3.

        :param s3_key: Ключ объекта в S3 (путь внутри бакета).
        :raises MiniOError.FileDeleteError: Если произошла ошибка при удалении файла.
        """
        try:
            async with self.session.client(
                "s3",
                region_name=self.region_name,
                use_ssl=self.is_https,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as s3_client:
                await s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)

        except ClientError as e:
            # Логируем ошибку и вызываем кастомное исключение
            logger.error(f"Failed to delete file from S3: {e}")
            raise MiniOError.FileDeleteError(s3_key=s3_key, error=str(e))

    async def stream_upload_to_s3(
        self, file, s3_key: str, chunk_size: int = 5 * 1024 * 1024
    ) -> None:
        """
        Загружает файл в S3 с использованием мультипаузной загрузки.

        :param file: Файл для загрузки (например, UploadFile из FastAPI).
        :param s3_key: Ключ объекта в S3 (путь внутри бакета).
        :param chunk_size: Размер части файла (по умолчанию 5 MB).
        """
        try:
            # Инициализация мультипаузной загрузки
            async with self.session.client(
                "s3",
                region_name=self.region_name,
                use_ssl=self.is_https,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as s3_client:
                multipart_upload = await s3_client.create_multipart_upload(
                    Bucket=self.bucket_name, Key=s3_key
                )
                upload_id = multipart_upload["UploadId"]

                parts = []
                part_number = 1

                # Чтение файла по частям
                async for chunk in self._read_file_in_chunks(file, chunk_size):
                    part = await s3_client.upload_part(
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=chunk,
                    )
                    parts.append({"PartNumber": part_number, "ETag": part["ETag"]})
                    part_number += 1

                # Завершение мультипаузной загрузки
                await s3_client.complete_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                )

        except ClientError as e:
            # Отмена загрузки в случае ошибки
            if "upload_id" in locals():
                await s3_client.abort_multipart_upload(
                    Bucket=self.bucket_name, Key=s3_key, UploadId=upload_id
                )
            raise MiniOError.StreamUploadError(s3_key=s3_key, error=str(e))  # noqa: B904

    @staticmethod
    async def _read_file_in_chunks(
        file, chunk_size: int
    ) -> AsyncGenerator[bytes, None]:
        """
        Асинхронно читает файл по частям.

        :param file: Файл для чтения.
        :param chunk_size: Размер части файла.
        :yield: Часть файла в виде байтов.
        """
        if hasattr(file, "read"):
            if asyncio.iscoroutinefunction(file.read):
                while chunk := await file.read(chunk_size):
                    yield chunk
            else:
                while chunk := file.read(chunk_size):
                    yield chunk
        else:
            raise ValueError("Unsupported file type")

    async def status(self) -> bool:
        try:
            async with self.session.client(
                "s3",
                region_name=self.region_name,
                use_ssl=self.is_https,
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
            ) as s3_client:
                await s3_client.list_buckets()
                return True
        except Exception:
            return False
