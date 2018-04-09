#Author github.com/morph3
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
metuSmtpPort = 587
metuSmtpServer = "smtp.metu.edu.tr"
gmailSmtpPort = 587
gmailSmtpServer = "smtp.gmail.com"
devsSmtpPort = 587
devsSmtpServer = "smtp.mail.com"


def message_parse(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        msg = MIMEText(f.read(),'plain')
        f.close()
    return msg


def html_parse(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        html = MIMEText(f.read(),'html')
    return html


def session(uid, pwd, sender, destination, isHtml, subject,content):
    # msg object has to be recreated in every new session
    msg = MIMEMultipart('alternative')
    if(content != False):
        text = MIMEText(content,'plain')
        msg.attach(text)
    else:
        parsedMessage = message_parse("message.txt")
        msg.attach(parsedMessage)

    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = destination

    if (isHtml):
        # under development
        html = html_parse("htmlMail.txt")
        msg.attach(html)


    smtpObject = smtplib.SMTP(metuSmtpServer, metuSmtpPort)
    smtpObject.ehlo()
    smtpObject.starttls()
    resp = smtpObject.login(uid, pwd)
    if (resp):
        print("Login succesfull")
    else:
        print("Error")
    smtpObject.sendmail(msg['From'], msg['To'], msg.as_string())
    smtpObject.quit()


if __name__ == "__main__":

    #argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--uid", default="Username",help="User id --which will be e+first 5 digits of school number--")
    parser.add_argument("-p", "--pwd", default="Password", help="User password ")
    parser.add_argument("-s", "--sender", default="MailAdress", help="Sender's email")
    parser.add_argument("-t", "--title", default="HelloWorld", help="Mail title")
    parser.add_argument("-r", "--recipient", default=False, help="If there is only one recipient")
    parser.add_argument("-m", "--msg", default=False, help="If you want to send a specific mail")
    parser.add_argument("-html", "--html", default=False, help="If you are sending html mail")

    args = parser.parse_args()
    uid = args.uid
    pwd = args.pwd
    sender = args.sender
    isHtml = args.html
    title = args.title
    recipient = args.recipient
    content = args.msg
    #endof argument parsing

    if (recipient):
        #if there is only one recipient
        session(uid, pwd, sender, recipient, isHtml, title , content)
    else:
        with open("emails.txt", "r") as file:
            for item in file:
                session(uid, pwd, sender, item, isHtml, title,content)
            file.close()
