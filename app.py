import os

from flask import Flask, render_template, redirect
from python_freeipa import ClientMeta
import requests
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from forms import SignupForm

sentry_sdk.init(
    dsn="https://fbb82a738d724494870da1ffa5e67f7d@sentry.io/5176646",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "ookeemo7ohGhahx9da9l"

INVITE_CODE_ENV = os.environ.get("INVITE_CODE", "")
ELEVATED_INVITE_CODE_ENV = os.environ.get("ELEVATED_INVITE_CODE", "")
USER_GROUP_ENV = os.environ.get("USER_GROUP", "")
ELEVATED_USER_GROUP_ENV = os.environ.get("ELEVATED_USER_GROUP", "")

logger = logging.getLogger('registration')


@app.route("/", methods=["GET", "POST"])
def registration():
    form = SignupForm()
    if form.validate_on_submit():
        client = ClientMeta(os.environ.get("LDAP_SERVER"), verify_ssl=False)
        client.login(os.environ.get("LDAP_ADMIN"), os.environ.get("LDAP_PASSWORD"))
        full_name = f"{form.first_name.data} {form.last_name.data}"
        client.user_add(
            a_uid=form.username.data,
            o_givenname=form.first_name.data,
            o_sn=form.last_name.data,
            o_cn=full_name,
            o_userpassword=form.password.data,
            o_preferredlanguage="EN"
        )
        if form.invite_code.data == INVITE_CODE_ENV:
            client.group_add_member(USER_GROUP_ENV, o_user=form.username.data)
        elif form.invite_code.data == ELEVATED_INVITE_CODE_ENV:
            client.group_add_member(ELEVATED_USER_GROUP_ENV, o_user=form.username.data)

        if os.environ.get("SLACK_ENABLED") == "true":
            try:
                data = {
                    "email": form.email.data,
                    "token": os.environ.get("SLACK_API_TOKEN"),
                    "set_active": "true"
                }
                requests.post(f"https://{os.environ.get('SLACK_WORKSPACE')}.slack.com/api/users.admin.invite", data=data)
            except Exception as e:
                logger.error(f"Challenges sending slack invite to {form.email.data} - {e}")
        return redirect("/success")
    return render_template("register.html", form=form)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run()
