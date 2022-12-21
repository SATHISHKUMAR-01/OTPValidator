from flask import Flask, render_template, request,session,flash, redirect, url_for
import pyotp
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Function to generate OTP
def getOTP():
    totp = pyotp.TOTP('base32secret3232')
    otp = totp.now()
    return otp

# Route for index Page
@app.route('/')
def showLogin():
    return render_template('index.html')

# Route to get OTP
@app.route('/generateOTP', methods = ['POST'])
def generateOTP():
    email = request.form['email']
    session['attempts'] = 3
    session['otp'] = getOTP()
    return render_template('otp.html', attempt = session['attempts'])

# Route to enter the OTP
@app.route('/login', methods = ['POST'])
def getOTPDetails():
    pin_1 = request.form['pin-1']
    pin_2 = request.form['pin-2']
    pin_3 = request.form['pin-3']
    pin_4 = request.form['pin-4']
    pin_5 = request.form['pin-5']
    pin_6 = request.form['pin-6']

    currentOTP = pin_1+pin_2+pin_3+pin_4+pin_5+pin_6
    session['attempts'] -= 1

    if(session['attempts'] < 0):
        flash('Retry Again !!!', 'info')
        return render_template('index.html')
    
    if( currentOTP == session['otp']):
        return redirect(url_for('success'))
    else:
        if(session['attempts'] == 0):
            flash('Retry Again !!!', 'info')
            return render_template('index.html')
        else:
            return render_template('otp.html', attempt = session['attempts'])


# Route to show the success message
@app.route('/success')
def success():
   return render_template('success.html')
    
if __name__ == '__main__':
   app.run(debug=True)