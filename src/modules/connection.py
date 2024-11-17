import imaplib
from pathlib import Path
import json
import socket
import platform

PATH_WORK = Path.cwd()
file_config = PATH_WORK / "src/modules/config/imap_config.json"
file_dominios = PATH_WORK / "src/modules/config/palavras_chave_dominios.json"


def obter_disco_padrao():
    if platform.system() == 'Windows':
        return Path(Path.home().anchor)
    else:
        return Path('/')
    
def save_key_words():
    print('''\n
    ################################################################
    |                                                              |
    | Você deve escolher palavras chave dentro dos domínios para   |
    | mapear todos os e-mails vindos desses domínios.              | 
    | Exemplo:                                                     |
    |  Se existirem e-mails 'email1@teste.camisetas.com.br' e      |
    |  'email2@envio.camisetas.com.br', e você escolher a palavra  |
    |  'camisetas' como palavra chave, ambos serão mapeados e orga-|
    |  nizados dentro da pasta 'camisetas', assim qualquer email   |
    |  desse domínio específico será mapeado e seu                 |
    |  anexo(se existir), será baixado.                            |
    |                                                              |
    ################################################################
''')
    
    if file_dominios.exists():
        with open(file_dominios, 'r') as file:
            try:
                palavras_chave = json.load(file) 
            except json.JSONDecodeError:
                palavras_chave = []           
    else:
        palavras_chave = []

    while True:

        palavra_chave = input('\nInsira uma palavra chave por vez: (ou "sair" para encerrar)\n>>>').lower()
        
        if palavra_chave == 'sair':
            print('Encerrando inserção de palavras chave de domínios.')
            # Criar arquivo file_dominios vazio se não existir
            if not file_dominios.exists():
                with open(file_dominios, 'w') as file:
                    json.dump([], file)  # Cria um arquivo vazio
            break
        else:
            if palavra_chave.strip():  # Garantir que a palavra não seja vazia
                if palavra_chave not in palavras_chave:
                    palavras_chave.append(palavra_chave)
                    print('Palavra inserida na lista temporária...')
                else:
                    print(f"A palavra '{palavra_chave}' já foi adicionada.")
            else:
                print("Por favor, insira uma palavra chave válida.")

    with open(file_dominios, 'w') as file:
        json.dump(palavras_chave, file, indent=4)
        print('Palavras chave gravadas com sucesso!')
        return

def save_config_imap(imap_config):

    try:
        with open(file_config, 'r') as file:
            imap_configs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        imap_configs = []
    
    imap_configs.append(imap_config)

    with open(file_config, 'w') as file:
        json.dump(imap_configs, file, indent=4)

def init_connection():

    conexao = False
    conn = None
    disco_padrao = obter_disco_padrao()

    while not conexao:

        servidor = input("Endereço do seu servidor de e-mails: ")
        login = input("E-mail: ")
        password = input("Senha: ")
        caminho_downloads = input(f'''
Insira o caminho onde deseja que os downloads sejam feitos. Caso você
não insira um caminho, os arquivos serão salvos em:
        "{disco_padrao}download_emails"
>>> ''')

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

    if caminho_downloads.strip():      
        imap_config = {
            'servidor': servidor,
            'login': login,
            'password': password,
            'caminho_downloads': caminho_downloads
        }
    else:
        imap_config = {
            'servidor': servidor,
            'login': login,
            'password': password,
            'caminho_downloads': str(disco_padrao / 'download_emails')
        }
    
    save_config_imap(imap_config)

    while True:
        opcao = input('Deseja inserir os domínios que serão buscados? (s/n)\n>>>').lower()
        if opcao == 'n':
            print('Pulando inserção de domínios, todos os e-mails serão lidos.')
            break
        elif opcao == 's':
            save_key_words()
            break
        else:
            print('Opção inválida, tente novamente.')

    return conn  # Retorna a conexão bem-sucedida

def connection():
    with open(file_config, 'r') as file:
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
        print("Conexão estabelecida com sucesso!")
        return conn

def reconnection():
    print("Reconectando ao servidor...")
    conn = connection()
    if conn is None:
        print("Falha ao reconectar.")
    return conn