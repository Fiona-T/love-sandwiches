# import gspread and google auth dependencies

import gspread
from google.oauth2.service_account import Credentials

# lists the APIs the program has access to, for IAM configuration
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# below are settings to access the spreadsheet data
# calling from_service_account method of Credentials class, pass file name
CREDS = Credentials.from_service_account_file('creds.json')
# using the with_scopes method of CREDS object, pass it the SCOPE variable
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# create GSPREAD_CLIENT using gspread.authorize method, pass it SCOPED_CREDS
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# access the sheet using open method on client object
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# call the sales worksheet from above, using worksheet method of sheet
# sales = SHEET.worksheet('sales')

# variable using gspread mthod to pull values from sales worksheet
# data = sales.get_all_values()

# print(data)


def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")
    # to check the data variable is working
    # print(f"The data provided is {data_str}")

    # split data entered into a list, split where commas are, remove commas
    sales_data = data_str.split(",")
    # print(sales_data)
    validate_data(sales_data)


def validate_data(values):
    """
    validate the data entered by users
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()
