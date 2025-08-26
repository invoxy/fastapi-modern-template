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
        Download a file from S3.

        :param bucket_name: Name of the S3 bucket.
        :param s3_key: Object key in S3 (path inside the bucket).
        :param file_path: Path to save the local file.
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
        Return a list of files in the specified S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param prefix: Prefix (path) to filter files.
        :return: List of files (keys).
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
        Delete a file from S3.

        :param s3_key: Object key in S3 (path inside the bucket).
        :raises MiniOError.FileDeleteError: If an error occurs while deleting a file.
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
            # Log the error and raise a custom exception
            logger.error(f"Failed to delete file from S3: {e}")
            raise MiniOError.FileDeleteError(s3_key=s3_key, error=str(e))

    async def stream_upload_to_s3(
        self, file, s3_key: str, chunk_size: int = 5 * 1024 * 1024
    ) -> None:
        """
        Upload a file to S3 using multipart upload.

        :param file: File to upload (e.g., FastAPI UploadFile).
        :param s3_key: Object key in S3 (path inside the bucket).
        :param chunk_size: Part size (default 5 MB).
        """
        try:
            # Initialize multipart upload
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

                # Read file in chunks
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

                # Complete multipart upload
                await s3_client.complete_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=s3_key,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts},
                )

        except ClientError as e:
            # Abort multipart upload in case of error
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
        Read file asynchronously in chunks.

        :param file: File to read.
        :param chunk_size: Chunk size.
        :yield: Chunk bytes.
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
