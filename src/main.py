from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
import asyncio

from database import get_db, init_db
from crud import get_item, get_items, create_item, update_item, delete_item
from schemas import ItemCreate, ItemUpdate
from google_sheets import append_to_sheet, update_sheet, delete_sheet_row
from sync import sync_google_sheets_to_db, sync_db_to_google_sheets


app = FastAPI()


@app.get("/items")
async def read_items(db: AsyncSession = Depends(get_db)):
    return await get_items(db)


@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/")
async def create_new_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = await create_item(db, item)
    print("getting this as the id: ", db_item.id)
    append_to_sheet(db_item)
    return db_item


@app.put("/items/{item_id}")
async def update_existing_item(
    item_id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)
):
    updated_item = await update_item(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_sheet(item_id + 1, updated_item)
    return updated_item


@app.delete("/items/{item_id}")
async def delete_existing_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted_item = await delete_item(db, item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    delete_sheet_row(deleted_item.id + 1)
    return {"ok": True}


@app.on_event("startup")
async def startup_event():
    await init_db()
    asyncio.create_task(periodic_sync())


async def periodic_sync():
    while True:
        async for db in get_db():
            await sync_google_sheets_to_db(db)
            await sync_db_to_google_sheets(db)
        await asyncio.sleep(60)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
