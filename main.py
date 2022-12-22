from flask import Flask, render_template, request,session,flash, redirect, url_for
import pyotp
from flask_session import Session
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Function to generate OTP
def getOTP():
    totp = pyotp.TOTP('base32secret3232')
    otp = totp.now()
    return otp

# Function to send Email
def sendEmail(email,otp):
    
    smtp_server = "smtp.gmail.com"
    port = 587  
    sender_email = ""
    password = ""
    receiver_email = email

    context = ssl.create_default_context()
    message = MIMEMultipart("alternative")
    message["Subject"] = "Login - OTP "

    html_head = """\
    <html>
    <body>
    <h1 style="text-align:center"> OTP for Login </h1>
    <div style="display:flex">
    <p style="width:25px;height:40px;text-align:center;margin:10px;padding:10px;border:2px solid black;border-radius:10px;font-size:24px">""" + otp[0] +"""</p>
    <p style="width:25px;height:40px;text-align:center;margin:10px;padding:10px;border:2px solid black;border-radius:10px;font-size:24px"> """ + otp[1] +"""  </p>
    <p style="width:25px;height:40px;text-align:center;margin:10px;padding:10px;border:2px solid black;border-radius:10px;font-size:24px"> """ + otp[2] +""" </p>
    <p style="width:25px;height:40px;text-align:center;margin:10px;padding:10px;border:2px solid black;border-radius:10px;font-size:24px"> """ + otp[3] +""" </p> 
    <p style="width:25px;height:40px;text-align:center;margin:10px;padding:10px;border:2px solid black;border-radius:10px;font-size:24px"> """ + otp[4] +""" </p>
    <p style="width:25px;height:40px;text-align:center;margin:10px;padding:10px;border:2px solid black;border-radius:10px;font-size:24px"> """ + otp[5] +""" </p>
    </div>  
    </body>
    </html>
    """
    part1 = MIMEText(html_head, "html")
    message.attach(part1)

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() 
        server.starttls(context=context) 
        server.ehlo() 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print("ERROR : ",e)
        return False
    
    server.quit() 
    return True


# Route for index Page
@app.route('/')
def showLogin():
    return render_template('index.html')

# Route to get OTP and email
@app.route('/generateOTP', methods = ['POST'])
def generateOTP():
    email = request.form['email']
    session['attempts'] = 3
    session['otp'] = getOTP()
    if(sendEmail(email,session['otp'])):
        return render_template('otp.html', attempt = session['attempts'])
    else:
        flash('Server Error! Try Again', 'info')
        return render_template('index.html')

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