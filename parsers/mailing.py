from data.db_session import global_init, create_session
from data.users import User
import smtplib
import email.message

server = smtplib.SMTP('smtp.gmail.com:587')


def send_mail(user_list, game):
    global_init('db/games.db')

    email_content = """ HTML """

    msg = email.message.Message()
    msg['Subject'] = 'Sale on following game'
    msg['From'] = 'youraddress'
    msg['To'] = 'to_address'
    password = "yourpassword"
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)

    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], [msg['To']], msg.as_string())

    db_sess = create_session()
    user_list = [1, 2, 4]
    for i in user_list:
        user = db_sess.query(User).filter((User.id == i)).first()
