from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)
    sent_email = BooleanField(default=False)
