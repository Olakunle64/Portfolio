#!/usr/bin/python
"""This module contains a script for scrapping emails from any indeed website
    and apply for job by sending a mail containing various attachement like resume,
    certificate, transcript e.t.c to all emails scrapped on indeed.
"""

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
import pyautogui as p


def read_cover_letter_from_docx(docx_path):
    """This function read the text from a microsoft word document"""
    doc = Document(docx_path)
    cover_letter = ""
    for paragraph in doc.paragraphs:
        cover_letter += paragraph.text + "\n"
    return cover_letter


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

# add the keyword you want to search on indeed here
# "animal science email remote", "agriculture email remote", 
# keywords = ["animal science email remote", "agriculture email remote", "animal tech email remote", "animal robotics remote email", "lab research animal email remote", "graduate amimal scientist email remote", "agric python", "soil science email remote"]
# "university of maryland email", "university of chicago email", "university email", "university computer email", "university developer email", "graduate assistant email", "university of arizona email", 
# keywords = ["university of washington email", "university of manchester email", "university of houston email", "university of miami email"]
# keywords = ["university email", "university computer email", "university developer email", "graduate assistant email"]  
keywords = [
    "bioinformatics email", "software engineer email remote", "web developer email remote",
    "robotics email remote", "C programmer email remote", "data analytics email remote",
    "embedded programming email remote", "python developer email remote",
    "developer email remote", "junior developer email remote",
    "junior software engineer remote", "engineering email remote",
    "devops engineer email remote", "animal research email",
    "typist email remote"
    ]
# keywords = ["animal research email"]
for keyword in keywords:
    # p.move(1, 1, duration=1)
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    # driver.get('https://www.indeed.com/q-usa-jobs.html?vjk=597d48348ffc1349') # add the url of any indeed website you want to scrape
    # driver.get("https://ca.indeed.com/")
    print(f"scraping for -------{keyword}-----")
    try:
        time.sleep(2)
        job_title = driver.find_element(By.XPATH, "//*[@id=\"text-input-what\"]")
        job_title.clear()
        job_title.send_keys(keyword)
        time.sleep(1)
        driver.find_element(By.XPATH, "//*[@id=\"text-input-where\"]").send_keys("Canada")
        # # job_state.clear()
        # # add the state you want to scrape on indeed
        # job_state = driver.find_element(By.ID, "text-input-where")
        # job_state.send_keys("Canada")
        
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
#     # This is the end of email scrapping on indeed

    
# This part is for sending emails
sender_email = "" # sender email
password = "" # your app password
context = ssl.create_default_context()
i = 0

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open('emails.txt', 'rt') as f:
        for line in set(f.readlines()):
            eml = line.split("-")[0].strip()
            title = line.split("-")[1].strip()
            if not title:
                title = "Advertised Job"
            # title = "Postdoctoral Research Associate(Quantitative Research and Data Analytics)"
            # subject = "Intending M.S Student"
            subject = f"Interest in {title} Position"
            body =  read_cover_letter_from_docx('S_cover_letter.docx')
            
            receiver_email = eml.strip()  # Remove newline character

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            with open('Transcript-software-engineering.pdf', 'rb') as attachment:
                part = MIMEApplication(attachment.read())
                part.add_header('Content-Disposition', 'attachment', filename='Transcript-software-engineering.pdf')
                message.attach(part) 
            with open('myCV.pdf', 'rb') as attachment:
                part = MIMEApplication(attachment.read())
                part.add_header('Content-Disposition', 'attachment', filename='myCV.pdf')
                message.attach(part)
            with open('Electronics_Engineering_Certificate.pdf', 'rb') as attachment:
                part = MIMEApplication(attachment.read())
                part.add_header('Content-Disposition', 'attachment', filename='Electronics_Engineering_Certificate.pdf')
                message.attach(part)
            with open('python_IT_certificate.pdf', 'rb') as attachment:
                part = MIMEApplication(attachment.read())
                part.add_header('Content-Disposition', 'attachment', filename='python_IT_certificate.pdf')
                message.attach(part)

            try:
                server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception:
                print("An exception occured when trying to send the mail")
                pass
            i += 1
            print(f'{i}-----Sent email to {eml} as {title}')
            # print(f'{i}-----Sent email to {eml} as')
        
            time.sleep(1)
    # remove_file("emails.txt")