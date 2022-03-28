import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
def mailSender(addr_to,id,orders):


    msg = MIMEMultipart()
    addr_from = "lilpenisp@gmail.com"
    password = "Terminator2020"
    msg['From']    = addr_from
    msg['To']      = addr_to
    text = ""
    for i in orders.split(':'):
        text = text + " " + i
    msg['Subject'] = f'You have ordered{text}'

    body = f"Your order №{id} is being processed"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(addr_from,password )
    server.send_message(msg)
    server.quit()

