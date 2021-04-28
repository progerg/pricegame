from data.db_session import global_init, create_session
from data.users import User
from data.Sales import Sales
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com:587')
PASSWORD = 'password'
server.starttls()
server.login('mail', PASSWORD)


def send_mail():
    global_init('../db/games.db')
    db_sess = create_session()
    games_ = db_sess.query(Sales).filter().all()
    try:
        for game_ in games_:
            if game_.game.foll_profiles:
                profiles = game_.game.foll_profiles.split(', ')
                profiles = list(map(lambda x: int(x), profiles))
                users = db_sess.query(User).filter(User.id.in_(profiles)).all()
                for us in users:
                    msg = MIMEMultipart()
                    msg['Subject'] = 'Sale on following game'
                    msg['From'] = 'mail'
                    msg['To'] = us.email
                    message = f'There is sale on your following game {game_.game.name}. ' \
                              f'Visit our site to see more information.'
                    msg.attach(MIMEText(message, 'plain'))
                    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    except Exception as err:
        print(err)
