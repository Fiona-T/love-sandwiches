# import gspread and google auth dependencies

import gspread
from google.oauth2.service_account import Credentials
# from pprint import pprint

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
    Call validate-data function with the inputted data
    Continue looping until validate_data returns true
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: \n")
        # to check the data variable is working
        # print(f"The data provided is {data_str}")

        # split data entered into a list, split where commas are, remove commas
        sales_data = data_str.split(",")
        # print(sales_data)
        # call validate_data, if it returns true then data valid, loop stops.
        if validate_data(sales_data):
            print("data is valid")
            break

    return sales_data


def validate_data(values):
    """
    validate the data entered by user
    print error to terminal if not integer or 6 values
    return true when validated or false when not, to get_sales_data
    """
    # print(values)
    try:
        # try to convert data entered into integer
        [int(value) for value in values]
        # check if correct length of data, if not raise error
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you entered {len(values)}"
            )
    # print relevant error message(e),return false to get_data to continue loop
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    # returns True if no errors, stops while loop in get_data
    return True


def calculate_surplus_data(sales_row):
    """
    Deduct sales from stock to get surplus
    Positive figure means excess - thrown away
    Negative means extra made after stock sold out
    """
    print("Calculating surplus data...\n")
    # get values from stock sheet of google spreadsheet
    stock = SHEET.worksheet("stock").get_all_values()
    # print returned stock values using pprint
    # pprint(stock)
    stock_row = stock[-1]
    # print(f"stock row: {stock_row}")
    # print(f"sales row: {sales_row}")
    # declaring variable which will hold list of surplus data when calcd
    surplus_data = []
    # for each item in both lists, take one from other, add to suplus list
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    # print the list when the for loop is finished
    # print(surplus_data)
    # return the list of surplus values
    return surplus_data


def update_worksheet(data, worksheet):
    """
    receives a list of integers to be inserted into worksheet
    update the relevant worksheet by adding new row and inserting data
    """
    # feedback to user in terminal while updating the worksheet
    print(f"Updating {worksheet} worksheet...\n")
    # the relevant worksheet from the googlesheets spreadsheet
    worksheet_to_update = SHEET.worksheet(worksheet)
    # add new row to the worksheet, populated with the data entered
    worksheet_to_update.append_row(data)
    # print to terminal to confirm to user the data was added to spreadsheet
    print(f"{worksheet} worksheet updated with data successfully.\n")


def get_last_5_entries_sales():
    """
    Gets columns from sales worksheet, last 5 entries from
    each column, returned as list of lists
    """
    # get sales worksheet
    sales = SHEET.worksheet("sales")
    # declaring columns list which will hold lists from each column
    columns = []
    # for index 1 to 7, get values from column equal to index, append to list
    for ind in range(1, 7):
        column = sales.col_values(ind)
        # get the last 5 entries in the column
        columns.append(column[-5:])
    # return the list of lists
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type
    add 10% to average
    """
    # feedback for user
    print("Calculating stock data...\n")
    new_stock_data = []

    # for each column in the sales_columns
    for column in data:
        # convert the values in that column to integers
        int_column = [int(num) for num in column]
        # get the average i.e. sum of column divided by number of values
        average = sum(int_column) / len(int_column)
        # increase the average by 10%
        stock_num = average * 1.1
        # append the resulting figure to the new stock list, rounded
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run the program functions
    """
    # the validated data returned from get_sales_data and validate_data
    data = get_sales_data()
    # print(data)
    # convert the data from sales_data function into integers
    sales_data = [int(num) for num in data]
    # update the worksheet with the sales data (integer), on sales sheet
    update_worksheet(sales_data, "sales")
    # surplus calced by calling function + passing it sales_data
    new_surplus_data = calculate_surplus_data(sales_data)
    # print(new_surplus_data)
    # update the worksheet with the surplus data, on surplus sheet
    update_worksheet(new_surplus_data, "surplus")
    # get last 5 entries from sales spreadsheet
    sales_columns = get_last_5_entries_sales()
    # calc sales data using the last 5 entries from above
    stock_data = calculate_stock_data(sales_columns)
    # print(stock_data)
    # update the worksheet with the stock data, on stock sheet
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()
