import os

from flask_wtf import FlaskForm
from python_freeipa import ClientMeta
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError

client = ClientMeta(os.environ.get("LDAP_SERVER"), verify_ssl=False)
client.login(os.environ.get("LDAP_ADMIN"), os.environ.get("LDAP_PASSWORD"))


class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    first_name = StringField("First name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    last_name = StringField("Last name", validators=[DataRequired()])
    if os.environ.get("INVITE_CODE"):
        invite_code = StringField("Invite code", validators=[DataRequired()])

    def validate_username(self, username):
        user = client.user_find(username.data)
        if user["count"] is not 0:
            raise ValidationError(
                f"Username {username.data} already exists, please use another."
            )

    def validate_invite_code(self, invite_code):
        if invite_code.data != os.environ.get("INVITE_CODE"):
            raise ValidationError("Invite code is incorrect!")