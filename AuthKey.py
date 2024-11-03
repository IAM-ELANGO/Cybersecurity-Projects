import random
import string
import smtplib
from email.mime.text import MIMEText
import time
from twilio.rest import Client


SENDER_EMAIL = 'your_email@example.com'
SENDER_PASSWORD = 'your_password'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587


TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

otp_requests = {}

def generate_otp(length=10, use_special_chars=True):
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += string.punctuation
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_email(recipient, otp):
    subject = 'Your OTP Code'
    body = f'Your One-Time Password (OTP) is: {otp}'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def send_otp_sms(recipient, otp):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your One-Time Password (OTP) is: {otp}',
        from_=TWILIO_PHONE_NUMBER,
        to=recipient
    )
    return message.sid

def request_otp(recipient, method):
    current_time = time.time()
    user_requests = otp_requests.get(recipient, [])
    otp_requests[recipient] = [t for t in user_requests if current_time - t < 60]
    if len(otp_requests[recipient]) >= 3:
        print("Exceeded the maximum number of OTP requests. Please try again later.")
        return None
    otp = generate_otp()
    if method == 'email':
        send_otp_email(recipient, otp)
    elif method == 'sms':
        send_otp_sms(recipient, otp)
    otp_requests[recipient].append(current_time)
    return otp, current_time

def verify_otp(user_input, generated_otp, generated_time, expiration_time=300):
    if time.time() - generated_time <= expiration_time:
        return user_input == generated_otp
    return False

def main():
    print("Select an option:")
    print("1. Send OTP via Email")
    print("2. Send OTP via SMS")
    print("3. Generate OTP (no sending)")
    choice = input("Enter your choice (1/2/3): ")

    if choice in ['1', '2']:
        recipient = input("Enter your email or mobile number: ")
        otp, generated_time = request_otp(recipient, 'email' if choice == '1' else 'sms')
        if otp is None:
            return
        print(f"An OTP has been sent to {recipient}.")
    elif choice == '3':
        otp = generate_otp()
        print(f"Generated OTP: {otp}")
        return
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    user_input = input("Enter the OTP you received: ")
    if verify_otp(user_input, otp, generated_time):
        print("OTP is valid!")
    else:
        print("Invalid or expired OTP.")

if __name__ == "__main__":
    main()
