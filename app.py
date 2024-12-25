from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import random
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bosch0456@gmail.com'
app.config['MAIL_PASSWORD'] = 'jpdjewrwbjtykfsc'  # Use an app password if 2FA is enabled
mail = Mail(app)

# Simulated database
users_db = {}

#Homepage
@app.route('/')
def index():
    return render_template('index.html') 

#User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users_db[email] = {'password': password, 'otp': None, 'otp_expiry': None}
        return redirect(url_for('login'))
    return render_template('register.html')

#User login and OTP generation
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users_db and users_db[email]['password'] == password:
            otp = random.randint(100000, 999999)
            expiry_time = datetime.now() + timedelta(minutes=5)
            users_db[email]['otp'] = otp
            users_db[email]['otp_expiry'] = expiry_time
            send_otp_email(email, otp)
            session['email'] = email
            return redirect(url_for('verify_otp'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

#Send OTP Email
def send_otp_email(email, otp):
    msg = Message('Your OTP Code', sender='bosch0456@gmail.com', recipients=[email])
    msg.body = f'Your OTP code is: {otp}'
    mail.send(msg)

#OTP Verification
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    email = session.get('email')
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if email in users_db:
            user_data = users_db[email]
            if user_data['otp'] == int(entered_otp) and datetime.now() < user_data['otp_expiry']:
                return "Login successful!"
            else:
                return "Invalid or expired OTP. Please try again."
    return render_template('verify_otp.html')

if __name__ == '__main__':
    print("Starting Flask app......")
    app.run(debug=True)