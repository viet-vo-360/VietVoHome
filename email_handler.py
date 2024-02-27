from flask import request, jsonify
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Load sensitive information from environment variables
FROM_EMAIL = os.getenv('FROM_EMAIL', 'vohoangviet361@gmail.com') # 'vohoangviet361@gmail.com'
TO_EMAIL = os.getenv('TO_EMAIL', 'vohoangviet360@gmail.com') # 'vohoangviet360@gmail.com'
SUBJECT = "New message from Viet Vo's home"
SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY') # '6Ld2tHkpAAAAACuFSdlYxW52O8orWBJJ5Q_MPgs4'
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME') # 'vohoangviet361@gmail.com'
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD') # 'plcc qezc wyqg hsmt'

# Define form fields
fields = {'name': 'Name', 'email': 'Email', 'subject': 'Subject', 'message': 'Message'}

def send_email():
    """Endpoint to send an email after reCAPTCHA verification."""
    recaptcha_response = request.form.get('g-recaptcha-response')
    if not recaptcha_response:
        return jsonify({'type': 'error', 'title': 'Required', 'message': 'Please click on the reCAPTCHA box.'})
    
    recaptcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    verify_response = requests.post(recaptcha_verify_url, data={'secret': SECRET_KEY, 'response': recaptcha_response})
    verify_response_data = verify_response.json()
    
    if not verify_response_data.get('success'):
        return jsonify({'type': 'error', 'title': 'Failed', 'message': 'Robot verification failed, please try again.'})
    
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = SUBJECT

        email_body = "You have a new message from Contact Form\n\n"
        for key, label in fields.items():
            value = request.form.get(key, '')
            email_body += f"{label}: {value}\n"

        msg.attach(MIMEText(email_body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({'type': 'success', 'title': 'Done', 'message': 'Thank you, I will get back to you soon!'})
    except Exception as e:
        logging.exception("Failed to send email")
        return jsonify({'type': 'error', 'title': 'Failed', 'message': 'There was an error. Please try again later!'})
