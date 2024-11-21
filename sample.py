from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the scope and the spreadsheet ID
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = (
    "1cyec9WDMygEwx_Tu2JEIch0nmY6At9A4INkEf_KiIpU"  # Replace with your spreadsheet ID
)

# Load the service account credentials
creds = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)

# Create the Sheets API service
service = build("sheets", "v4", credentials=creds)

# Example: Read data from a sheet
sheet_range = "Sheet1!A1:C10"  # Adjust the range as needed
result = (
    service.spreadsheets()
    .values()
    .get(spreadsheetId=SPREADSHEET_ID, range=sheet_range)
    .execute()
)
values = result.get("values", [])

if not values:
    print("No data found.")
else:
    for row in values:
        print(row)  # Process the data as needed
