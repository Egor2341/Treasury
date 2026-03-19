from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from data.init_bd import get_session
from data.repositories import receipts_repository
from services.minio import upload_to_minio, download_from_minio_url, delete_from_minio
from services.security import RoleChecker

router = APIRouter(
    prefix="/api/receipts",
    tags=["receipts"]
)


@router.get("", status_code=200)
async def get_receipts(
        user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    return await receipts_repository.get_receipts(
        session,
        user_uuid
    )


@router.post("", status_code=201)
async def add_receipt(
        user_uuid: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session),
        file: UploadFile = File(...)
):
    name = await receipts_repository.add_receipt(session, user_uuid, file)
    await session.commit()

    await upload_to_minio(file, name)


@router.get("/download")
async def get_receipt(
        file_uuid: str,
        _: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    file = await receipts_repository.get_file_info(session, file_uuid)
    return {
        "url": download_from_minio_url(file.object_name)
    }


@router.delete("", status_code=204)
async def delete_receipt(
        file_uuid: str,
        _: Annotated[str, Depends(RoleChecker(allowed_roles=["user"]))],
        session: AsyncSession = Depends(get_session)
):
    file = await receipts_repository.delete_receipt(session, file_uuid)
    await session.commit()
    await delete_from_minio(file)
