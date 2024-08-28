#!/usr/bin/python
"""This module contains a script for scrapping emails from any indeed website
    and apply for job by sending a mail containing various attachement like resume,
    certificate, transcript e.t.c to all emails scrapped on indeed.
"""
from cover_letter import CoverLetter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import re
from docx import Document
from email.mime.application import MIMEApplication
import email, smtplib, ssl
import csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def find_emails_in_text(text):
    """This function find an email in a test and return the list
        of all emails found
    """
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    found_emails = re.findall(email_regex, text)
    return found_emails

def save_emails_to_txt(emails, job_title):
    """This function saves emails to a txt file"""
    # with open('emails.txt', 'a') as txtfile:
    with open('emails.txt', 'a') as txtfile:
        for email in emails:
            txtfile.write(f"{email}-{job_title}\n")

def remove_file(file_path):
    """remove a file"""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been successfully removed.")
    else:
        print(f"File '{file_path}' does not exist.")


# The beginning of email scrapping on indeed

keywords = [] # Add the keywords of the jobs you are looking for

for keyword in keywords:
    # p.move(1, 1, duration=1)
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    # driver.get(f'https://www.indeed.com/q-{keyword}-jobs.html?vjk=9a1554ea7adef5f7') # for United States Only
    driver.get(f"https://au.indeed.com/jobs/?q={keyword}") # au for Australia, ca for Canada, uk for United Kingdom
    print(f"scraping for -------{keyword}-----")
    try:
        time.sleep(2)
        job_title = driver.find_element(By.XPATH, "//*[@id=\"text-input-what\"]")
        # job_title.clear()
        # job_title.send_keys(keyword)
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id=\"text-input-where\"]").send_keys("Austrailia")
        
        job_title.submit()

        next = 0
        while True:
            print(f"next {next}")
            # p.move(-1, -1, duration=1)
            if next > 6:
                break
            
            mosaic_provider = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mosaic-provider-jobcards")))
            jobs = mosaic_provider.find_elements(By.TAG_NAME, "li")
            count = 1
            job_heading = ""
            except_flag = 0
            for job in jobs:
                print(f"job {count}") 

                try:
                    job_heading = job.find_element(By.XPATH, f"//*[@id=\"mosaic-provider-jobcards\"]/ul/li[{count}]/div/div[1]/div/div/div/table/tbody/tr/td/div[1]/h2")
                except NoSuchElementException: # //*[@id="mosaic-provider-jobcards"]/ul/li[2]/div/div[1]/div/div/div/table/tbody/tr/td/div[1]/h2
                    print("EXCEPT")
                    count += 1
                    if except_flag > 2:
                        break
                    else:
                        except_flag += 1
                        continue

                if job_heading:
                    job_details_url = job_heading.find_element(By.TAG_NAME, "a").get_attribute("href")
                    job_title = job_heading.find_element(By.TAG_NAME, "span").text
                    print(job_title)
                    driver.execute_script(f"window.open('{job_details_url}', '_blank');")
                    driver.switch_to.window(driver.window_handles[1])

                    job_details_text = driver.find_element(By.TAG_NAME, "body").text
                    found_emails = find_emails_in_text(job_details_text)
                    print(f"Found emails: {found_emails}")
                    save_emails_to_txt(found_emails, job_title.split("-")[0].strip())

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                count += 1

            try:
                next_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='pagination-page-next']")))
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                next_btn.click()
            except TimeoutException:
                print("Next button not found. Exiting loop.")
                break

            time.sleep(2)  # Reduce wait time
            next += 1

    except Exception as e:
        print("An exception occurred")
        print(f"\t{e}")
    
    driver.quit()
    # This is the end of email scrapping on indeed

    
# This part is for sending emails
newCover = CoverLetter()
sender_email = "" # sender email
password = "" # your app password
context = ssl.create_default_context()
i = 0
not_sent = 0


with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open('emails.txt', 'rt') as f:
        for line in set(f.readlines()):
            eml = line.split("-")[0].strip()
            title = line.split("-")[1].strip() if len(line.split("-")) > 1 else "Advertised Job"
            subject = f"Interest in {title} Position"
            
            newCover.position = title
            body = newCover.get_cover_letter()

            receiver_email = eml.strip()  # Remove newline character
            print(f"Sending to: {receiver_email}")

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            # List of attachments
            attachments = [
                'Path to your attachement 1',
                'Path to your attachement 2',
                '.....'
            ]

            for attachment_path in attachments:
                try:
                    with open(attachment_path, 'rb') as attachment:
                        part = MIMEApplication(attachment.read())
                        part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')
                        message.attach(part)
                except FileNotFoundError:
                    print(f"Attachment not found: {attachment_path}")
                    continue  # Skip this attachment if not found

            try:
                server.sendmail(sender_email, receiver_email, message.as_string())
                i += 1
                print(f'''---Sent email to {eml} as a {title}---
                                        ||
                                ======================
                                Successful        {i}
                                ======================
                                Unsuccessful      {not_sent}
                                ======================\n''')
            except Exception as e:
                print(f"An exception occurred when trying to send the mail: {e}")
                not_sent += 1
                continue
            
            time.sleep(1)  # Sleep for a second between sends