import time
from dotenv import load_dotenv
import os
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
load_dotenv()


# Authenticate with the Google Sheets API using the service account credentials
gc = gspread.service_account(filename="service_account.json")
spreadsheet_id = os.getenv("SPREADSHEET_ID")
def write_table_to_google_sheets(data, df1, df2):

    # Drop specified columns from each DataFrame
    dataframe1 = df1.drop(columns=['Apps', 'Yel', 'Red', 'AerialsWon', 'Rating', 'Player'])
    dataframe2 = df2.drop(columns=['R', 'Team'])

    # Combine the two data sets into a single dataframe
    combined_dataframe = pd.concat(objs=[dataframe1, dataframe2], ignore_index=True)

    # Create a new Spreadsheet or open an existing one
    spreadsheet = gc.open_by_key(spreadsheet_id)
    # Get the list of all sheet names in the spreadsheet
    all_sheets = [sheet.title for sheet in spreadsheet.worksheets()]
    tournament_name = data["Tournament Name"]
    try:
        # Open the Google Sheets file (make sure it's shared with the service account email)
        #spreadsheet = gc.open_by_key(spreadsheet_id)
        #for data in tournament_data:

        if tournament_name in all_sheets:
            worksheet = spreadsheet.worksheet(tournament_name)
            print(f"Sheet '{tournament_name}' found. Loading data")
            worksheet.clear()
            set_with_dataframe(worksheet, combined_dataframe)
        else:
            # If the sheet does not exist, create a new one
            print("Sheet not found. Creating a new one")
            worksheet = spreadsheet.add_worksheet(title=tournament_name, rows=0, cols=0)
            print(f"Sheet '{tournament_name}' created and Ready to receive data")
            worksheet.clear()
            set_with_dataframe(worksheet, combined_dataframe)

        #    # set_with_dataframe(worksheet, table)
        #     print(worksheet.row_count)
        #     print('Sheet found and data loaded')
        #
        #    # set_with_dataframe(worksheet, table)
        #
        # # Read the CSV file into a pandas DataFrame
        # # csv_data = pd.read_csv(csv_file_path)
        #
        # # Convert the DataFrame to a 2D list (list of lists)
        # # data_to_load = csv_data.values.tolist()
        #
        # # Clear the existing data in the sheet
        # #worksheet.clear()
        #
        # # Resize the sheet to fit the new data
        # #worksheet.resize(len(table), len(table[0]))
        #
        # # Load the data to the sheet
        # # worksheet.update(data_to_load)
    except Exception as ex:
        print(ex)
    time.sleep(1)


# # Load the CSV tables into Google Sheets
# for data in tournament_data:
#     tournament_name = data["Tournament Name"]
#     player_stats_csv = f"{tournament_name} - Player_Statistics.csv"
#     assist_to_goal_csv = f"{tournament_name} - Assist_to_Goal_Scorer.csv"
#
#     load_csv_to_google_sheets(player_stats_csv, tournament_name)
#     load_csv_to_google_sheets(assist_to_goal_csv, tournament_name)