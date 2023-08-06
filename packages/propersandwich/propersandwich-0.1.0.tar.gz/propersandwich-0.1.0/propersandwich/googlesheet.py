"""
This module will help to perform CRUD operations with Google spreadsheets
"""

import pygsheets
import logging
import pandas as pd
import os
from dotenv import load_dotenv

# Load Environment variables
load_dotenv()


def create_worksheet(spreadsheet_url, worksheet_title):
    """
    Create a worksheet in an existing spreadsheet


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Create a new worksheet
    spreadsheet.add_worksheet(worksheet_title)


def read_worksheet(spreadsheet_url, worksheet_title, start='A1') -> pd.DataFrame:
    """
    Read a worksheet and return it's content as a Dataframe


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet
    :param str start: op left cell to load into data frame. (default: A1)

    :returns: The content of the tab
    :rtype: dataframe

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Select the worksheet
    worksheet = spreadsheet.worksheet_by_title(worksheet_title)

    # Get the content of this worksheet as a pandas data frame.
    data = worksheet.get_as_df(start=start)

    logging.info(f"Retrieved {len(data.index)} rows from [ {worksheet.title} / {spreadsheet.title} ]")

    return data


def delete_worksheet(spreadsheet_url, worksheet_title):
    """
    Delete a worksheet in an existing spreadsheet


    :param str spreadsheet_url: The Environment variable containing the URL of the spreadsheet
    :param str worksheet_title: The title of the worksheet

    """

    # Create a client
    google_sheet_client = pygsheets.authorize(service_account_env_var='GOOGLE_API')

    # Open the sheet
    spreadsheet = google_sheet_client.open_by_url(os.getenv(spreadsheet_url))

    # Select the worksheet
    worksheet = spreadsheet.worksheet_by_title(worksheet_title)

    # Delete a worksheet by title
    spreadsheet.del_worksheet(worksheet)


