from flask import Flask, render_template, request,session
import pyotp
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

attempts = 3


# Function to generate OTP
def getOTP():
    totp = pyotp.TOTP('base32secret3232')
    otp = totp.now()
    return otp

# Route for Login Page
@app.route('/')
def showLogin():
    return render_template('index.html')

@app.route('/generateOTP', methods = ['POST'])
def generateOTP():
    email = request.form['email']
    session['otp'] = getOTP()
    print(session['otp'])
    return render_template('otp.html')

@app.route('/login', methods = ['POST'])
def getOTPDetails():
    pin_1 = request.form['pin-1']
    pin_2 = request.form['pin-2']
    pin_3 = request.form['pin-3']
    pin_4 = request.form['pin-4']
    pin_5 = request.form['pin-5']
    pin_6 = request.form['pin-6']

    currentOTP = pin_1+pin_2+pin_3+pin_4+pin_5+pin_6

    print(currentOTP)
    print(session['otp'])
    
    return "success"

    
if __name__ == '__main__':
   app.run(debug=True)