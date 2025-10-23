# from typing import Any

# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
# from pydantic import EmailStr

# from src.config import get_settings

# template_folder_path = get_settings().BASE_DIR / "templates" / "email"

# mail_config = ConnectionConfig(
#     MAIL_USERNAME=get_settings().EMAIL_USERNAME,
#     MAIL_PASSWORD=get_settings().EMAIL_PASSWORD,
#     MAIL_FROM=get_settings().EMAIL_SENDER,
#     MAIL_PORT=get_settings().EMAIL_PORT,
#     MAIL_SERVER=get_settings().EMAIL_SMTP_SERVER,
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
#     TEMPLATE_FOLDER=template_folder_path,
# )


# async def send_email(
#     email_subject: str,
#     email_receivers: list[EmailStr],
#     email_template: str,
#     **kwargs: Any,
# ) -> None:
#     email = MessageSchema(
#         subject=email_subject,
#         recipients=email_receivers,
#         template_body=kwargs,
#         subtype=MessageType.html,
#     )
#     fm = FastMail(config=mail_config)
#     await fm.send_message(message=email, template_name=email_template)


# from email.message import EmailMessage

# import aiosmtplib
# from jinja2 import Environment, FileSystemLoader, select_autoescape

# from src.config import get_settings

# templates_env = Environment(
#     loader=FileSystemLoader(get_settings().EMAIL_TEMPLATES_DIR),
#     autoescape=select_autoescape(default=True),
#     enable_async=True,
# )


# async def _generate_email_body() -> str:
#     template = templates_env.get_template("projectreportemail.html")
#     return await template.render_async()


# def _generate_email_message(recipient: str, subject: str, html_body: str) -> EmailMessage:
#     message = EmailMessage()
#     message["From"] = get_settings().EMAIL_SENDER
#     message["To"] = recipient
#     message["Subject"] = subject
#     message.set_content(html_body, subtype="html")
#     return message


# async def send_email(
#     email: str,
# ) -> None:
#     body = await _generate_email_body()
#     message = _generate_email_message(email, body)
#     await aiosmtplib.send(
#         message,
#         hostname="127.0.0.1",
#         port=get_settings().EMAIL_PORT,
#         username=get_settings().EMAIL_USERNAME,
#         password=get_settings().EMAIL_PASSWORD,
#     )
