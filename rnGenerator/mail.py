import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


def send_mail(subject, message, filenames):
    server = ''
    sender = ''
    recvs = ['recv1', 'recv2']

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(recvs)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))
    if filenames != []:
        for file in filenames:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(file,'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(sender, recvs, msg.as_string())
    smtp.close()
