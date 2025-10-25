from email.message import EmailMessage
from typing import Any

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.config import get_settings

_templates_env = Environment(
    loader=FileSystemLoader(get_settings().EMAIL_TEMPLATES_DIR),
    autoescape=select_autoescape(default=True),
    enable_async=True,
)


class SMTPNotificationClient:
    __slots__ = ()

    async def _render_email_body(self, template_name: str, **entities_for_render: Any) -> str:
        template = _templates_env.get_template(template_name)
        return await template.render_async(**entities_for_render)

    def _generate_email_message(self, recipient_email: str, subject: str, html_body: str) -> EmailMessage:
        message = EmailMessage()
        message["From"] = get_settings().EMAIL_SENDER
        message["To"] = recipient_email
        message["Subject"] = subject
        message.set_content(html_body, subtype="html")
        return message

    async def send_notification(
        self,
        recipient_email: str,
        subject: str,
        **entities_for_render: Any,
    ) -> None:
        body = await self._render_email_body(**entities_for_render)
        message = self._generate_email_message(recipient_email, subject, body)
        await aiosmtplib.send(
            message,
            hostname="127.0.0.1",
            port=get_settings().EMAIL_PORT,
            username=get_settings().EMAIL_USERNAME,
            password=get_settings().EMAIL_PASSWORD,
        )
