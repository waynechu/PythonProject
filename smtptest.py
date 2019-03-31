import smtplib

gmail_user = 'wayne.chu@nexusguard.com'  
gmail_password = ''

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
except:  
    print('Something went wrong...')
