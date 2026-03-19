import io
from datetime import timedelta

from fastapi import HTTPException
from minio import Minio, S3Error
import os

from dotenv import load_dotenv
from starlette.responses import StreamingResponse

load_dotenv()

bucket_name = "receipts"

client = Minio("localhost:9000",
               access_key=os.getenv("MINIO_USER"),
               secret_key=os.getenv("MINIO_PASSWORD"),
               secure=False
               )


def init_minio():
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)


async def upload_to_minio(file, name):
    try:
        contents = await file.read()

        client.put_object(
            bucket_name=bucket_name,
            object_name=name,
            data=io.BytesIO(contents),
            length=len(contents),
            content_type=file.content_type,
        )
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


def download_from_minio(filename):
    try:
        response = client.get_object(bucket_name, filename)

        return StreamingResponse(
            response,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except S3Error:
        raise HTTPException(status_code=404, detail="File not found")


def download_from_minio_url(filename: str):
    return client.presigned_get_object(
        bucket_name,
        filename,
        expires=timedelta(minutes=5)
    )

async def delete_from_minio(filename: str):
    client.remove_object(bucket_name, filename)
