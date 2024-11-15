import imaplib
from pathlib import Path
import json
import socket

PATH_WORK = Path.cwd()
filename = PATH_WORK / "imap_config.json"

def save_config_imap(imap_config):

    try:
        with open(filename, 'r') as file:
            imap_configs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        imap_configs = []
    
    imap_configs.append(imap_config)

    with open(filename, 'w') as file:
        json.dump(imap_configs, file, indent=4)

def init_connection():

    conexao = False
    conn = None

    while not conexao:

        servidor = input("Endereço do seu servidor de e-mails: ")
        login = input("E-mail: ")
        password = input("Senha: ")

        try:
            conn = imaplib.IMAP4_SSL(servidor)
            conn.login(login, password)
            conn.select(mailbox='inbox', readonly=True)
            print("Conexão estabelecida com sucesso!")
            conexao = True
            
        except (socket.gaierror, imaplib.IMAP4.error):
            print('\nDados de conexão:')
            print(f'\nServidor: {servidor}\nLogin: {login}\nSenha: {password}\n')
            print("Erro em um, ou mais dados de conexão. Verifique e tente novamente.")
            
    imap_config = {
        'servidor': servidor,
        'login': login,
        'password': password
    }
    save_config_imap(imap_config)

    return conn  # Retorna a conexão bem-sucedida

def connection():
    with open(filename, 'r') as file:
        imap_config = json.load(file)
        if not imap_config:
            print("Nenhuma configuração encontrada. Por favor, inicialize uma conexão.")
        
        last_config = imap_config[-1]

        servidor = last_config['servidor']
        login = last_config['login']
        password = last_config['password']

        conn = imaplib.IMAP4_SSL(servidor)
        conn.login(login, password)
        conn.select(mailbox='inbox', readonly=True)
        return conn

def reconnection():
    print("Reconectando ao servidor...")
    conn = connection()
    if conn is None:
        print("Falha ao reconectar.")
    return conn