from .connection import init_connection, connection, reconnection, filename
import chardet
import email
from .metodos import *
import imaplib
from pathlib import Path
import time

PATH_WORK = Path.cwd()
palavras_chave = PATH_WORK / 'src/modules/config/palavras_chave_dominios.json'

def download_anexos(data_inicio):
    if not filename.exists():
        conn = init_connection()
    else:
        conn = connection()

    status, numEmails = conn.search(None, f'SINCE "{data_inicio}"') # type: ignore
    if status != "OK":
        print("Erro ao buscar emails.")
        return

    # Listar todos os emails encontrados
    for num in numEmails[0].split():
        try:
            status, dados = conn.fetch(num, '(RFC822)') # type: ignore
            conteudo_email = dados[0][1] # type: ignore

            detect_encoding = chardet.detect(conteudo_email)['encoding'] # type: ignore
            try:
                conteudo_email = conteudo_email.decode(detect_encoding) # type: ignore
            except:
                conteudo_email = conteudo_email.decode('utf-8', errors='ignore') # type: ignore
            
            conteudo_email = email.message_from_string(conteudo_email)

            obj_email = obter_perfil_email(conteudo_email)

            executar_segundo_for = False

            if not palavras_chave.exists():
                escolha = input('Deseja filtrar os domínios? s/n').lower()
                if escolha == 'n':
                    print('Fazendo download em todos os arquivos disponíveis...')
                    salvar_arqruivos_total(conteudo_email, obj_email)
                elif escolha == 's':
                    criar_lista_dominios()
                    time.sleep(1)
                    with open(palavras_chave, 'r') as file:
                        for palavra in file:
                            if palavra in obj_email.dominio:
                                executar_segundo_for = True
                                break
                
                    if executar_segundo_for:
                        salvar_arqruivos(conteudo_email, obj_email, palavra)


            elif palavras_chave.exists():
                with open(palavras_chave, 'r') as file:
                    for palavra in file:
                        if palavra in obj_email.dominio:
                            executar_segundo_for = True
                            break
            
                if executar_segundo_for:
                    salvar_arqruivos(conteudo_email, obj_email, palavra)

        except imaplib.IMAP4.abort as e:
            print(f"Conexão abortada: {e}. Tentando reconectar...")
            conn = reconnection()
            download_anexos() # type: ignore # Reinicia a busca de e-mails
            return
        except Exception as e:
            print(f"Erro ao processar o email {num}: {e}")
            continue