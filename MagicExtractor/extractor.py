#!/usr/bin/python3
"""This module contains two functions which are meant to extract
	to an email and phone number from a text"""

import re
# from website_text import pasted_text

with open("software_enginer.txt", "r", encoding="utf-8") as f:
    pasted_text = f.read()

def email_extractor():
    """A regex to extract email from a text"""

    check_email = re.compile(r'''([\w+%-]+ # user name
    @ # the at symbol
    [\w-]+ # domain name
    (\.[a-zA-Z]{2,4})) #dot something''', re.VERBOSE)
    return check_email

def phone_number_extractor():
    """A regex to extract phone number from a text"""

    check_phone_number = re.compile(r'''(\(?[\d]{3}\)?) # area code
    [.\s-] # separator
    (\d{3}) # first 3 digits
    [.\s-] # separator
    (\d{4}) # last four digits
    (\s*(ext|x|ext.)\s*(\d{2,5}))?
    ''', re.VERBOSE)
    return check_phone_number


if __name__ == "__main__":
    """extract the email and phone number from a text"""
    matches_phone_number = []
    matches_email = []
    phone_regex = phone_number_extractor()
    email_regex = email_extractor()
    """
    for groups in phone_regex.findall(pasted_text):
        phone_number = "-".join([groups[0], groups[1], groups[2]])
        if groups[3] != "":
            phone_number += ' x' + groups[3]
        matches_phone_number.append(phone_number)
    """
    with open("software_enginer.txt", "r", encoding="utf-8") as f:
        pasted_text = f.read()
    for groups in email_regex.findall(pasted_text):
        matches_email.append(groups[0])
    #print(matches_phone_number)
    print(matches_email)
    with open("email_SE_scraped", "w") as f:
        json.dump(matches_email, f)
