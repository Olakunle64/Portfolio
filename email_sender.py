from email.mime.application import MIMEApplication
import email, smtplib, ssl
import csv
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


# def attachment(filename1):
#     with open(filename1, 'rb') as attachment:
#         part = MIMEApplication(attachment.read())
#         part.add_header('Content-Disposition', 'attachment', filename=filename1)
#         message.attach(part)



sender_email = "example@gmail.com"
password = "app password"
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    with open('email1.txt','rt') as csv_file:
        # csv_reader = csv.reader(csv_file)
        for i,line in enumerate(csv_file):
            subject = "Application For A Registered Nurse Role"
            body =  '''
            
Dear Hiring Manager, 
Hope this email meets you well 

My name is Olayinka Mujidat Fatoki an international trained nurse with more than 8 years experience. I have passed my IELTS and CBT exams and I have NMC decision letter. I am hoping to widen my career horizon in United Kingdom, having heard about your respectable Organisation , I am excited to be part of your team ,learning and working with other health care team in order to achieve the trust goals.

Thanks in anticipation. Below are my details. Looking forward to prompt response from you.

Warmest regards

Olayinka Mujidat FatokI 
 
# '''
            
            receiver_email = line
            

            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            # message["Bcc"] = receiver_email  # Recommended for mass emails



            # Add body to email
            message.attach(MIMEText(body, "plain"))


            with open('Olayinka_Fatoki_CV.pdf', 'rb') as attachment1:
                part1 = MIMEApplication(attachment1.read())
                part1.add_header('Content-Disposition', 'attachment1', filename='Olayinka_Fatoki_CV.pdf')
                message.attach(part1) 
            with open('OLAYINKA_FATOKI_IELTS_RESULT.pdf', 'rb') as attachment2:
                part2 = MIMEApplication(attachment2.read())
                part2.add_header('Content-Disposition', 'attachment1', filename='OLAYINKA_FATOKI_IELTS_RESULT.pdf')
                message.attach(part2) 
            with open('OLAYINKA_FATOKI_CBT_RESULT.pdf', 'rb') as attachment3:
                part3 = MIMEApplication(attachment3.read())
                part3.add_header('Content-Disposition', 'attachment1', filename='OLAYINKA_FATOKI_CBT_RESULT.pdf')
                message.attach(part3)

            with open('FATOKI_NMC_PAGE.pdf', 'rb') as attachment5:
                part5 = MIMEApplication(attachment5.read())
                part5.add_header('Content-Disposition', 'attachment1', filename='FATOKI_NMC_PAGE.pdf')
                message.attach(part5) 

            with open('FATOKI_OLAYINKA_Test_of_Competence_Invitation_CRM_00880327928.pdf', 'rb') as attachment6:
                part6 = MIMEApplication(attachment6.read())
                part6.add_header('Content-Disposition', 'attachment1', filename='FATOKI_OLAYINKA_Test_of_Competence_Invitation_CRM_00880327928.pdf')
                message.attach(part6)   

            # with open('exam_image3.jpeg', 'rb') as attachment4:

            texts = message.as_string()

            # attachment('pdf_for_bch_assignment_1.pdf')
            
            print(f'sending email{i+1}')

            
            server.sendmail(sender_email, receiver_email, texts)
            print('success')
            
            time.sleep(1)

