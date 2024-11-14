import imaplib

servidor = "mail.apicesc.com.br"
login = "ti@apicesc.com.br"
password = "tecnologia@2022"

def connection():
    conn = imaplib.IMAP4_SSL(servidor)
    conn.login(login, password)
    conn.select(mailbox='inbox', readonly=True)
    return conn

def reconnection():
    print("Reconectando ao servidor...")
    conn = connection()
    return conn