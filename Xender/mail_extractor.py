#!/usr/bin/python3

from email.mime.application import MIMEApplication
import email, smtplib, ssl
import csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from docx import Document

def find_emails_in_file(file_path):
    emails = []
    # Regular expression for matching email addresses
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    try:
        with open(file_path, 'r') as file:
            # Read the file line by line
            for line in file:
                # Find all email addresses in the line using regex
                found_emails = re.findall(email_regex, line)
                # Extend the list of emails with the found ones
                emails.extend(found_emails)
    except FileNotFoundError:
        print("File not found.")
    
    return emails


def save_emails_to_csv(emails):
    with open('emails.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for email in emails:
            writer.writerow([email])

def read_cover_letter_from_docx(docx_path):
    doc = Document(docx_path)
    cover_letter = ""
    for paragraph in doc.paragraphs:
        cover_letter += paragraph.text + "\n"
    return cover_letter

driver = webdriver.Chrome()
for t in range(10, 20, 10):
    emails = []
    driver.get(f'https://www.indeed.com/jobs?q=software+engineer+email&start={t}&vjk=3c42553a23033564')
    a =[1,2,3,4,5,7,8,9,10,11,13,14,15,16,17]
    for x in a:
        try:
            driver.find_element(By.XPATH, f"//li[@class='css-5lfssm eu4oa1w0'][{x}]/div/div/div/div/div/table/tbody/tr/td/div/h2/a").click()
            time.sleep(1)
            b = driver.find_element(By.XPATH, '//*[@id="jobDescriptionText"]').text
            with open ('job_description.txt', 'a') as c:
                c.write(f'{b}\n')

        except Exception:
            pass
    emails.append(find_emails_in_file('job_description.txt'))
    save_emails_to_csv(emails)
     
    print(f'page {t} done')

driver.quit()

# send the mails
sender_email = "olakunleisiaq50@gmail.com"
password = "upog bpod axnl mhie"
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open('emails.txt','rt') as csv_file:
        # csv_reader = csv.reader(csv_file)
        for i, line in enumerate(csv_file):
            subject = "Application For A Registered Nurse Role"
            body =  read_cover_letter_from_docx('cover_letter.docx')
            
            receiver_email = line
            

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            # message["Bcc"] = receiver_email  # Recommended for mass emails



            # Add body to email
            message.attach(MIMEText(body, "plain"))


            # with open('Olayinka_Fatoki_CV.pdf', 'rb') as attachment1:
            #     part1 = MIMEApplication(attachment1.read())
            #     part1.add_header('Content-Disposition', 'attachment1', filename='Olayinka_Fatoki_CV.pdf')
            #     message.attach(part1) 
            # with open('OLAYINKA_FATOKI_IELTS_RESULT.pdf', 'rb') as attachment2:
            #     part2 = MIMEApplication(attachment2.read())
            #     part2.add_header('Content-Disposition', 'attachment1', filename='OLAYINKA_FATOKI_IELTS_RESULT.pdf')
            #     message.attach(part2) 
            # with open('OLAYINKA_FATOKI_CBT_RESULT.pdf', 'rb') as attachment3:
            #     part3 = MIMEApplication(attachment3.read())
            #     part3.add_header('Content-Disposition', 'attachment1', filename='OLAYINKA_FATOKI_CBT_RESULT.pdf')
            #     message.attach(part3)

            # with open('FATOKI_NMC_PAGE.pdf', 'rb') as attachment5:
            #     part5 = MIMEApplication(attachment5.read())
            #     part5.add_header('Content-Disposition', 'attachment1', filename='FATOKI_NMC_PAGE.pdf')
            #     message.attach(part5) 

            # with open('FATOKI_OLAYINKA_Test_of_Competence_Invitation_CRM_00880327928.pdf', 'rb') as attachment6:
            #     part6 = MIMEApplication(attachment6.read())
            #     part6.add_header('Content-Disposition', 'attachment1', filename='FATOKI_OLAYINKA_Test_of_Competence_Invitation_CRM_00880327928.pdf')
            #     message.attach(part6)   

            # with open('exam_image3.jpeg', 'rb') as attachment4:

            texts = message.as_string()

            # attachment('pdf_for_bch_assignment_1.pdf')
            
            print(f'sending email {i+1}')

            
            server.sendmail(sender_email, receiver_email, texts)
            print('success')
            
            time.sleep(1)


