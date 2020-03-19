from flask import Flask, render_template, redirect
from forms import SignupForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'ookeemo7ohGhahx9da9l'


@app.route('/', methods=['GET', 'POST'])
def registration():
    form = SignupForm()
    if form.validate_on_submit():
        print(form.email)
        return redirect('/success')
    return render_template("register.html", form=form)


@app.route('/success')
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run()
