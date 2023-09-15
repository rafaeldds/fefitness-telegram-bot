import json
import smtplib
from email.mime.text import MIMEText


def send_email(subject, message):

    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    smtp_server = config["SMTP_SERVER"]
    smtp_port = config["SMTP_PORT"]
    smtp_user = config["SMTP_USER"]
    smtp_password = config["SMTP_PASSWORD"]
    smtp_toemail = config["SMTP_TOEMAIL"]

    msg = MIMEText(message)
    msg["From"] = smtp_user
    msg["To"] = smtp_toemail
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, smtp_toemail, msg.as_string())
        print("E-mail enviado com sucesso!")
    except Exception as exception:
        print(f"Erro ao enviar e-mail: {exception}")
