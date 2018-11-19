import csv, random, smtplib, email, time, argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

parser = argparse.ArgumentParser(description='Input args')
parser.add_argument('inp', help='File Containing names, emails and other data. \
                    For correct use, the first row should contain headers, the \
                    second column should be names, the third column should be emails \
                    and the fifth column should contain desired gift information.')
args = parser.parse_args()


if __name__=='__main__':
    data = list(csv.reader(open(args.inp)))[1:] #read raw data, remove headers
    givers = [(person[1], person[2]) for person in data] #giver now formatted as (name, email)
    recipients = [(person[1], person[4]) for person in data] #recipients now (name, desired-gifts)

    notrandom=True

    while notrandom:
        random.shuffle(recipients) #randomize the names

        #verify that nobody got theirself
        for giver, recipient in zip(givers, recipients):
            notrandom = True if giver[0]==recipient[0] else False
            if notrandom: break

    host_email = input("Enter the email which will send matches: ")
    host_password = input("Enter password: ")

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.starttls()
    mailServer.login(host_email, host_password)

    for giver, recipient in zip(givers, recipients):
        msg = MIMEMultipart()
        msg['From'] = 'thetataupb@gmail.com'
        msg['To'] = giver[1]
        msg['Subject'] = "Secret Santa Match for {}".format(giver[0])
        message_body = MIMEText('Your Person is: {}\nDesired Gifts: {}'.format(recipient[0], recipient[1]))
        
        msg.attach(message_body)
        mailServer.sendmail('thetataupb@gmail.com', giver[1], msg.as_string())
        time.sleep(5)