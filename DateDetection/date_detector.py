#!/usr/bin/python3
"""Detect if a date is valid or not with the use of regex"""

import re

def date_regex():
    """regex that matches a date"""
    DateRegex = re.compile(r'''(0\d|[0-3]\d) # matches the Day(group 1)
    [/] # matches the separator
    (0\d|[0-1][0-2]) # matches the Month(group 2)
    [/] # matches the separator
    ([0-2]\d\d\d) # matches the Year(group 3)
    ''', re.VERBOSE)

    return DateRegex

def is_leap_year(year):
    """check if a year is a leap year or not"""
    if ((year % 4 == 0 and (year % 100 != 0)) or (year % 400 == 0)):
        return True
    else:
        return False

def date_validator(date):
    """check if a date is valid"""
    day, month, year = date.split("/")
    day = int(day)
    month = int(month)
    year = int(year)
    thirty_days_month = [9, 4, 6, 11]
    if is_leap_year(year):
        if month == 2 and day > 29:
            return False
    else:
        if month == 2 and day > 28:
            return False
    if month in thirty_days_month and day > 30:
        return False
    return True

if __name__ == "__main__":
    """Display a prompt for the user and check if the date
    inputed by the user is valid"""

    DateRegex = date_regex()
    print("Enter a valid date in this format DD/MM/YYYY")
    date = input("Enter a date: ")
    check_date = DateRegex.search(date)
    if check_date:
        IsValid = date_validator(check_date.group(0))
        if IsValid:
            print(check_date.group(0))
            print("The date is valid!")
        else:
            print("Invalid date!")
    else:
        print("Invalid date!")
