import falcon
import json
from marshmallow import Schema, fields
from src.service.mail_service import MailService


class MailResourceInput(Schema):
    content = fields.Str(required=True)


class MailResource:
    def on_post(self, req, resp):
        payload = req.media
        email_content = payload.get("content", None)
        response = MailService().email_action(email_content=email_content)

        resp.status = falcon.HTTP_200
        resp.text = response
