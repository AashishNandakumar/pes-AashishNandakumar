from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Item
from schemas import ItemCreate, ItemUpdate


async def get_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return result.scalars().all()


async def get_item(db: AsyncSession, item_id: int):
    return await db.get(Item, item_id)


async def create_item(db: AsyncSession, item: ItemCreate):
    print(f"item to be created - {item.dict()}")
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def create_item_from_spreadsheet(db: AsyncSession, item: Item):
    db_item = Item(**item)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def update_item(db: AsyncSession, item_id: int, item: ItemUpdate):
    db_item = await get_item(db, item_id)
    if not db_item:
        return None
    for key, value in item.dict().items():
        if key == "id":
            continue
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def delete_item(db: AsyncSession, item_id: int):
    db_item = await get_item(db, item_id)
    if not db_item:
        return None
    await db.delete(db_item)
    await db.commit()
    return db_item


async def resolve_conflicts(db: AsyncSession, db_item, sheet_item):
    # conflic resolution strategy: (last write wins)
    if db_item.last_modified > sheet_item["last_modified"]:
        return db_item  # keep database version
    else:
        # update database with google sheet version
        db_item.name = sheet_item["name"]
        db_item.description = sheet_item["description"]
        db_item.quantity = sheet_item["quantity"]
        db_item.last_modified = sheet_item["last_modified"]
        await db.commit()
        await db.refresh(db_item)
        return db_item
