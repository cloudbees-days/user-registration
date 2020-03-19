import os

from flask import Flask, render_template, redirect
from python_freeipa import ClientMeta

from forms import SignupForm

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "ookeemo7ohGhahx9da9l"

client = ClientMeta(os.environ.get("LDAP_SERVER"), verify_ssl=False)
client.login(os.environ.get("LDAP_ADMIN"), os.environ.get("LDAP_PASSWORD"))


@app.route("/", methods=["GET", "POST"])
def registration():
    form = SignupForm()
    if form.validate_on_submit():
        print(form.email)
        full_name = f"{form.first_name.data} {form.last_name.data}"
        user = client.user_add(
            a_uid=form.username.data,
            o_givenname=form.first_name.data,
            o_sn=form.last_name.data,
            o_cn=full_name,
            o_userpassword=form.password.data,
            o_preferredlanguage="EN",
        )
        print(user)
        return redirect("/success")
    return render_template("register.html", form=form)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run()
