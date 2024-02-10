from pathlib import Path
from typing import Any

from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from pydantic import EmailStr

from src.config import settings

template_folder_path = (Path(__file__).parent.parent / 'templates' / 'email')

mail_config = ConnectionConfig(MAIL_USERNAME=settings.EMAIL_USERNAME,
                               MAIL_PASSWORD=settings.EMAIL_PASSWORD,
                               MAIL_FROM=settings.EMAIL_SENDER,
                               MAIL_PORT=settings.EMAIL_PORT,
                               MAIL_SERVER=settings.EMAIL_SMTP_SERVER,
                               MAIL_STARTTLS=False,
                               MAIL_SSL_TLS=True,
                               USE_CREDENTIALS=True,
                               VALIDATE_CERTS=True,
                               TEMPLATE_FOLDER=template_folder_path)


async def send_email(email_subject: str,
                     email_receivers: list[EmailStr],
                     email_template: str,
                     **kwargs: dict[str, Any]) -> None:
    email = MessageSchema(subject=email_subject,
                          recipients=email_receivers,
                          template_body=kwargs,
                          subtype=MessageType.html)
    fm = FastMail(config=mail_config)
    await fm.send_message(message=email, template_name=email_template)
