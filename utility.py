import datetime
import requests
import json
import random
import config
import time
import json
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai
from mongo import MongoMailManager
from config import GEMINI_API_KEY, PROMPT_FOR_BODY, GEMINI_API_KEY_GEN, MONGO_URI
from data import email_data, sender_mails,receiver_mails,date_list


def get_response_from_gemini(prompt):
    genai.configure(api_key = GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

def get_response_from_gemini_for_body(prompt):
    genai.configure(api_key = GEMINI_API_KEY_GEN)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


def fetch_all_mail_content_json():
    headers = {
        'Authorization': f'Bearer {config.TEMP_ACCESS_TOKEN_RETRIVE_ALL_DATA}',
        'Content-Type': 'application/json'
    }
    mail_endpoint = 'https://graph.microsoft.com/v1.0/me/messages'
    all_messages = []  # List to store all message data

    # Fetch messages with pagination
    while mail_endpoint:
        response = requests.get(mail_endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Extract required details for each message and store in list
            for mail in data.get('value', []):
                mail_data = {
                    "subject": mail.get("subject"),
                    "sender": mail.get("from", {}).get("emailAddress", {}).get("address"),
                    "receivedDateTime": mail.get("receivedDateTime"),
                    "sentDateTime": mail.get("sentDateTime"),
                    "toRecipients": [recipient["emailAddress"]["address"] for recipient in mail.get("toRecipients", [])],
                    "ccRecipients": [recipient["emailAddress"]["address"] for recipient in mail.get("ccRecipients", [])],
                    "body": mail.get("body", {}).get("content")
                }
                all_messages.append(mail_data)  # Add email data to the list

            # Check for next page link
            # mail_endpoint = data.get('@odata.nextLink')  # Set to None if there's no next page
        else:
            print("Failed to fetch mail data:", response.status_code, response.json())
            return None

    # Filter messages for the last 7 days
    seven_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=2)).isoformat() + "Z"
    last_seven_days_messages = [
        message for message in all_messages
        if message.get("receivedDateTime") and message["receivedDateTime"] >= seven_days_ago
    ]

    # Convert filtered list to JSON
    with open("all_data_last_seven_days.json", 'w') as file:
        json.dump(last_seven_days_messages, file, indent=4)
    return json.dumps(last_seven_days_messages, indent=4)




def create_and_ingest_data():
    try:
        email_details = random.choice(email_data)
        subject = email_details['subject']
        category = email_details['type']
        sender_mail = random.choice(sender_mails)
        receiver_mail = random.choice(receiver_mails)
        date = random.choice(date_list)

        mail_data = {
        "subject": subject,
        "sender": sender_mail,
        "receiver": receiver_mail,
        "date": date,
        "category": category
        }

        body = get_response_from_gemini_for_body(PROMPT_FOR_BODY.format(mail_data))
        mail_data['mail_body'] = body
        return mail_data
    except Exception as e:
        print("Getting error", str(e))
        return None

import random
from datetime import datetime, timedelta

def generate_random_date():
    # Get current date
    current_date = datetime.now()

    # Calculate the date 5 days ago
    five_days_ago = current_date - timedelta(days=0)

    # Generate a random date between current date and 5 days ago
    random_date = current_date - timedelta(days=random.randint(0, 5))

    # Format the random date in the desired format (YYYY/MM/DD)
    formatted_random_date = random_date.strftime('%Y/%m/%d')

    return formatted_random_date

# Example usage:
random_date = generate_random_date()
print(random_date)


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_mail(receiver_email, subject, body):
    message = MIMEMultipart()
    message['From'] = "techwizardalert@gmail.com"
    message['To'] = receiver_email
    message['Subject'] = subject

    # HTML Email body with template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                text-align: center;
                padding: 10px;
                background-color: #007bff;
                color: #fff;
                border-radius: 8px;
            }}
            .email-body {{
                padding: 20px;
                font-size: 16px;
                line-height: 1.5;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #777;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>

        <div class="email-container">
            <div class="email-header">
                <h2>{subject}</h2>
            </div>
            <div class="email-body">
                <p>Dear {receiver_email},</p>
                <p>{body}</p>
                <p>Best regards,<br>
                The Tech Wizard Team</p>
            </div>
            <div class="footer">
                <p>This is an automated message. Please do not reply to this email.</p>
            </div>
        </div>

    </body>
    </html>
    """

    # Attach the HTML to the email
    message.attach(MIMEText(html_template, 'html'))

    sender_email = "techwizardalert@gmail.com"
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, config.MAIL_PASSKEY)  # Use the App Password here
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# mongo_manager = MongoMailManager(MONGO_URI, config.DB_NAME, config.COLLECTION_NAME)
# for i in range(100):
#     try:
#         mail_data = create_and_ingest_data()
#         if mail_data:
#             inserted_id = mongo_manager.save_email_data(mail_data)
#             print("Success")
#             time.sleep(3)
#         else:
#             print("Something wrong happen")
#     except Exception as e:
#         print("Getting error", str(e))






