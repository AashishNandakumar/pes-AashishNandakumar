import gspread
from dotenv import find_dotenv, load_dotenv
from datetime import datetime

import os


load_dotenv(find_dotenv())

gc = gspread.service_account(filename=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"))
sheet = gc.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1


def get_sheet_data():
    data = sheet.get_all_records()

    return [
        {
            "id": int(row["id"]),
            "name": row["name"],
            "description": row["description"],
            "quantity": int(row["quantity"]),
            "last_modified": datetime.strptime(
                str(row["last_modified"]), "%Y-%m-%dT%H:%M:%S.%f"
            ),
        }
        for row in data
    ]


def append_to_sheet(item):
    sheet.append_row(
        [
            item.id,
            item.name,
            item.description,
            item.quantity,
            item.last_modified.isoformat(),
        ]
    )


def update_sheet(row, item):
    sheet.update(
        f"A{row}:E{row}",
        [
            [
                item.id,
                item.name,
                item.description,
                item.quantity,
                item.last_modified.isoformat(),
            ]
        ],
    )


def delete_sheet_row(row):
    sheet.delete_rows(row)
