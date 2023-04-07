import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(reciever_email, user_password, forgot_password):
    sender_email = 'ridgerewardspoints@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Access your Rewards Points Account!'
    msg['From'] = sender_email
    msg['To'] = reciever_email

    # Create the plain-text and HTML version of your message
    if forgot_password:
        text = f"""
        Hi, How are you?
        You're getting this email because you've forggoten your password to your Rewards Points account.
        Here's your password! Try not to lose it again.
        {user_password}
        Thanks for being a Rewards Points member!

        The Rewards Points Team,
        Matthias Masiero
        Jaiman Munshi
        """
        html = f"""
        <html>

        <body>
            <h2>Hi,
                How are you?<br>
            </h2>
            <h3>You're getting this email because you've forggoten your password to your Rewards Points account.<br><br>
                Here's your password! Try not to lose it again.<br></h3>
            <h2>{user_password}</h2>

            <h4>Thanks for being a Rewards Points member!
                <br><br>The Rewards Points Team,</h4>
            <h3>Matthas Masiero<br>Jaiman Munshi</h3>
        </body>

        </html>
        """
    else:
        text = f"""
        Hi, How are you?
        You're getting this email because you've registered for a Rewards Points account.
        Here's your password! Try not to lose it.
        {user_password}
        Thanks for joining Rewards Points!
        
        The Rewards Points Team,
        Matthas Masiero
        Jaiman Munshi
        """
        html = f"""
        <html>

        <body>
            <h2>Hi,
                How are you?<br>
            </h2>
            <h3>You're getting this email because you've registered for a Rewards Points account.<br><br>
                Here's your password! Try not to lose it.<br></h3>
            <h2>{user_password}</h2>

            <h4>Thanks for joining Rewards Points!
                <br><br>The Rewards Points Team,</h4>
            <h3>Matthas Masiero<br>Jaiman Munshi</h3>
        </body>

        </html>
        """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    try:
        server.login(sender_email, 'zteuscrvkhxtlbbb')
        print('logged in to Gmail services')
    except:
        print('failed to login to Gmail services')

    try:
        server.sendmail(sender_email,
                        reciever_email,
                        msg.as_string()
                        )
        print('Email sent!')
    except:
        print('Email failed to send')

    server.quit()

# sendEmail(reciever_email='jaimancoding@gmail.com', user_password='123456')