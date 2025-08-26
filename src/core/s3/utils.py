import asyncio
from uuid import uuid4
from typing import Optional

import aioboto3
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError
from loguru import logger


def get_random_filename(filename: str) -> str:
    if "." in filename:
        name, *ext = filename.split(".")
        return f"{name}-{uuid4()}.{'.'.join(ext)}"
    return f"{filename}-{uuid4()}"


async def check_s3_connection(
    endpoint_url: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    bucket_name: str,
    region_name: str = "us-east-1",
    is_https: bool = True,
    timeout: int = 10,
    max_retries: int = 3,
) -> tuple[bool, Optional[str]]:
    """
    Checks connection to S3/MinIO service.

    Args:
        endpoint_url (str): S3/MinIO endpoint URL
        aws_access_key_id (str): Access Key ID
        aws_secret_access_key (str): Secret Access Key
        bucket_name (str): Bucket name to check
        region_name (str): Region (default: us-east-1)
        is_https (bool): Use HTTPS (default: True)
        timeout (int): Connection timeout in seconds (default: 10)
        max_retries (int): Maximum number of attempts (default: 3)

    Returns:
        tuple[bool, Optional[str]]: Tuple (success, error_message)

    Example:
        success, error = await check_s3_connection(
            endpoint_url="http://localhost:9000",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            bucket_name="my-bucket"
        )
    """
    logger.info("🔍 Checking S3/MinIO connection...")

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"🔄 Attempt {attempt}/{max_retries} to connect to S3/MinIO")

            # Create session
            session = aioboto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
            )

            # Create client with timeout
            async with session.client(
                "s3",
                region_name=region_name,
                use_ssl=is_https,
                endpoint_url=endpoint_url,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            ) as s3_client:
                # Check service availability
                await s3_client.list_buckets()

                # Check access to specific bucket
                await s3_client.head_bucket(Bucket=bucket_name)

                logger.info("✅ S3/MinIO connection successful")
                return True, None

        except NoCredentialsError as e:
            error_msg = f"S3 credentials error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return False, error_msg

        except EndpointConnectionError as e:
            error_msg = f"S3 endpoint connection error: {str(e)}"
            logger.warning(f"❌ {error_msg} (attempt {attempt}/{max_retries})")

            if attempt == max_retries:
                logger.error(f"❌ S3 connection failed after {max_retries} attempts")
                return False, error_msg

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            error_msg = f"S3 client error ({error_code}): {str(e)}"
            logger.warning(f"❌ {error_msg} (attempt {attempt}/{max_retries})")

            if attempt == max_retries:
                logger.error(f"❌ S3 connection failed after {max_retries} attempts")
                return False, error_msg

        except Exception as e:
            error_msg = f"Unexpected S3 error: {str(e)}"
            logger.error(f"❌ {error_msg} (attempt {attempt}/{max_retries})")

            if attempt == max_retries:
                logger.error(f"❌ S3 connection failed after {max_retries} attempts")
                return False, error_msg

        # Pause between attempts (except the last one)
        if attempt < max_retries:
            await asyncio.sleep(1)

    return False, "Maximum retry attempts exceeded"


async def test_s3_connection(
    endpoint_url: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    bucket_name: str,
    region_name: str = "us-east-1",
    is_https: bool = True,
) -> None:
    """
    Tests S3/MinIO connection and outputs the result.

    Args:
        endpoint_url (str): S3/MinIO endpoint URL
        aws_access_key_id (str): Access Key ID
        aws_secret_access_key (str): Secret Access Key
        bucket_name (str): Bucket name to check
        region_name (str): Region (default: us-east-1)
        is_https (bool): Use HTTPS (default: True)

    Example:
        await test_s3_connection(
            endpoint_url="http://localhost:9000",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            bucket_name="my-bucket"
        )
    """
    success, error = await check_s3_connection(
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        bucket_name=bucket_name,
        region_name=region_name,
        is_https=is_https,
    )

    if success:
        logger.info("🎉 S3/MinIO connection test passed!")
    else:
        logger.error(f"💥 S3/MinIO connection test failed: {error}")


# Keep old function for compatibility
def check_s3_connection_sync(s3_url: str) -> bool:
    """
    Synchronous version of S3 connection check (deprecated).
    Use async version check_s3_connection.
    """
    try:
        import boto3

        s3_client = boto3.client("s3", endpoint_url=s3_url)
        s3_client.list_buckets()
        return True
    except Exception:
        return False
