import uuid

from fastapi import UploadFile
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data.entities.receipt import Receipt
from exceptions.NoEntryError import NoEntryError
from models.receipts.one import Receipt as ReceiptDto
from models.receipts.list import ListReceipts


async def get_count(session: AsyncSession, user_uuid: str) -> int:
    stmt = await session.execute(select(Receipt).where(Receipt.user_uuid == user_uuid))
    return len(stmt.scalars().all())


async def get_receipts(session: AsyncSession, user_uuid: str) -> ListReceipts:
    stmt = await session.execute(select(Receipt).where(Receipt.user_uuid == user_uuid))
    return ListReceipts(
        receipts=[ReceiptDto(
            uuid=r.uuid,
            name=r.original_name
        )
            for r in stmt.scalars().all()]
    )


async def get_file_info(session: AsyncSession, file_uuid: str) -> Receipt:
    stmt = await session.execute(select(Receipt).filter_by(uuid=file_uuid))
    return stmt.scalar_one()


async def add_receipt(session: AsyncSession, user_uuid: str, file: UploadFile):
    object_name = f"{user_uuid}/{uuid.uuid4()}_{file.filename}"

    session.add(Receipt(
        object_name=object_name,
        original_name=file.filename,
        content_type=file.content_type,
        user_uuid=user_uuid
    ))

    return object_name


async def delete_receipt(session: AsyncSession, file_uuid: str) -> str:
    stmt = await session.execute(select(Receipt).filter_by(uuid=file_uuid))
    file = stmt.scalar_one_or_none()
    if not file:
        raise NoEntryError("This receipt does not exist")

    await session.execute(
        delete(Receipt)
        .where(Receipt.uuid == file_uuid))

    return file.object_name
