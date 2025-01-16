import imaplib
import smtplib
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default
import time
import os
from dotenv import load_dotenv
from historical_pipeline import historical_process_data
from benchmark_pipeline import combined_benchmarking
load_dotenv()

# Your credentials
IMAP_SERVER = 'imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ADDRESS = os.getenv('GMAIL_USER')
EMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')
api_key = os.getenv('OPENAI_API_KEY')

# Directory to save attachments
ATTACHMENT_DIR = './attachments'

root_path = os.path.dirname(os.path.abspath(__file__))

# Ensure the attachment directory exists
os.makedirs(ATTACHMENT_DIR, exist_ok=True)

def connect_to_gmail_imap(user, password):
    imap_url = 'imap.gmail.com'
    try:
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(user, password)
        mail.select('inbox')  # Connect to the inbox.
        print("Connected to Gmail IMAP.")
        return mail
    except Exception as e:
        print("Connection failed: ", e)
        raise

def check_email_and_respond():
    try:
        imap = connect_to_gmail_imap(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Search for unseen emails
        status, messages = imap.search(None, 'UNSEEN')
        if status != "OK" or not messages[0]:
            print("No new emails.")
            return

        # Process each email
        for num in messages[0].split():
            status, data = imap.fetch(num, '(RFC822)')
            if status != "OK":
                continue
            
            email_content = data[0][1]
            email_message = BytesParser(policy=default).parsebytes(email_content)

            # Extract email details
            sender = email_message['From']
            subject = email_message['Subject']
            print(f"Email from: {sender}")
            print(f"Subject: {subject}")

            # Check for attachments
            for part in email_message.iter_attachments():
                content_disposition = part.get("Content-Disposition", "")
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    filepath = os.path.join(ATTACHMENT_DIR, filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Saved attachment: {filename}")

                    # Process PDF if applicable
                    if filename.lower().endswith('.pdf'):
                        new_pdf_path, benchmark_path = process_pdf(filename) #TODO
                        if new_pdf_path:
                            name = new_pdf_path.split("_")[0]

                            send_email(
                                recipient_email=sender,  # Sending back to the original sender
                                subject=f"Processed PDF for {name}",
                                body="Here is the processed PDF.",
                                attachment_path_historical=new_pdf_path,
                                attachment_path_benchmark=benchmark_path
                            )
            
            # Mark as read
            imap.store(num, '+FLAGS', '\\Seen')

    except Exception as e:
        print(f"Error: {e}")

def process_pdf(filename):
    try:
        print(f"Processing PDF: {filename}")

        # Process the PDF
        pdf_path = f"attachments/{filename}"
        process_pdf_path = historical_process_data(root_path, api_key, pdf_path)
        benchmark_pdf_path = combined_benchmarking()

        return process_pdf_path, benchmark_pdf_path

        
    except Exception as e:
        print(f"Error processing PDF: {e}")

def send_email(recipient_email, subject, body, attachment_path_historical, attachment_path_benchmark):
    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            msg = EmailMessage()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.set_content(body)

            # Attach a file if provided
            if attachment_path_historical:
                with open(attachment_path_historical, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path_historical)
                    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

            if attachment_path_benchmark:
                with open(attachment_path_benchmark, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path_benchmark)
                    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

            smtp.send_message(msg)
    except Exception as e:
        print(f"Error: {e}")



while True:
    check_email_and_respond()
    time.sleep(5)  # Check every 30 seconds


