from flask import Flask, render_template, url_for, flash, redirect
from form import RegisterForm, LoginForm
app = Flask(__name__)


app.config['SECRET_KEY'] ='f00ee7583d29d7804578909a4ee52b96'


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if(form.validate_on_submit()):
        flash(f'Created account for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        if(form.email.data == 'vladi' and form.password.data == '1234'):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)