from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import User, db
from forms import RegisterForm, LoginForm 
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Rewq12345..,,' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


api_url = 'https://api.coincap.io/v2/assets'

def create_tables():
    with app.app_context():
        db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    try:
        response = requests.get(api_url)
        response.raise_for_status() 

        data = response.json()
        coins = data['data'][:3]  
        for coin in coins:
            coin['changePercent24Hr'] = round(float(coin['changePercent24Hr']), 2)
            price = float(coin['priceUsd'])
            if price < 1 and price > 0:  
                coin['priceUsd'] = "{:.3f}".format(price)
            elif price < 0.1:  
                coin['priceUsd'] = "{:.8f}".format(price)
            else:  
                coin['priceUsd'] = "{:.2f}".format(price)

        return render_template('index.html', coins=coins)
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error_message=f"Error: Failed to fetch data from API. {e}")


@app.route('/pricing')
def get_coins():
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        coins = data['data'][:100]  
        for coin in coins:
          coin['changePercent24Hr'] = round(float(coin['changePercent24Hr']), 2)
          price = float(coin['priceUsd'])
          if price < 1 and price > 0:  
              coin['priceUsd'] = "{:.3f}".format(price)
          elif price < 0.1:  
              coin['priceUsd'] = "{:.8f}".format(price)
          else:  
              coin['priceUsd'] = "{:.2f}".format(price)

        return render_template('pricing.html', coins=coins)
    except requests.exceptions.RequestException as e:
        return render_template('error.html', error_message=f"Error: Failed to fetch data from API. {e}")
    
@app.route('/features')
def clinx_features():

    return render_template('features.html')    


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            # Handle duplicate email error (e.g., flash a message)
            flash('Email already exists. Please choose a different one.' , category='error')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            # Handle invalid login (e.g., display error message)
            flash('Invalid email or password.', category='error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))  # Redirect to homepage after logout

@app.route('/dashboard')
@login_required
def dashboard():
    # Display content accessible only to logged-in users
    return render_template('dashboard.html')


if __name__ == '__main__':
    create_tables()
    app.run(debug=True) 
