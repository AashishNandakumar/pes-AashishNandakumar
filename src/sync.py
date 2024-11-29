from sqlalchemy.ext.asyncio import AsyncSession
from google_sheets import get_sheet_data, append_to_sheet, update_sheet
from crud import get_item, get_items, create_item_from_spreadsheet, resolve_conflicts


async def sync_google_sheets_to_db(db: AsyncSession):
    print("syncing sheets->DB")
    sheet_data = get_sheet_data()

    for sheet_item in sheet_data:
        db_item = await get_item(db, sheet_item["id"])
        if db_item:
            # resolve conflicts
            await resolve_conflicts(db, db_item, sheet_item)
        else:
            # insert new rows from google sheet to database
            await create_item_from_spreadsheet(db, sheet_item)


async def sync_db_to_google_sheets(db: AsyncSession):
    print("syncing DB->sheets")
    db_items = await get_items(db)
    sheet_data = {row["id"]: row for row in get_sheet_data()}

    for db_item in db_items:
        if db_item.id not in sheet_data:
            # add new rows to google sheets
            append_to_sheet(db_item)
        elif db_item.last_modified > sheet_data[db_item.id]["last_modified"]:
            # update existing rows in google sheets
            row_number = list(sheet_data.keys()).index(db_item.id) + 2
            update_sheet(row_number, db_item)
