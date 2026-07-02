import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_PORT=int(os.getenv("EMAIL_PORT")),
    MAIL_SERVER=os.getenv("EMAIL_HOST"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_reset_email(email: str, reset_link: str):

    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"""
Hello,

Click the link below to reset your password:

{reset_link}

If you did not request this, please ignore this email.
""",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    