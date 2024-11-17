from .connection import init_connection, connection, reconnection, file_config, file_dominios, obter_disco_padrao
import chardet
import email
from .metodos import *
import imaplib
from pathlib import Path

def download_anexos(data_inicio):
    if not file_config.exists():
        conn = init_connection()
    else:
        conn = connection()

    caminho_downloads = obter_disco_padrao()

    if file_config.exists():
        with open(file_config, 'r') as file:
            arquivo = json.load(file)
            caminho_downloads = arquivo[0]['caminho_downloads']

    status, numEmails = conn.search(None, f'SINCE "{data_inicio}"') # type: ignore
    if status != "OK":
        print("Erro ao buscar emails.")
        return
    
    if not numEmails[0]:
        print('Nenhum email encontrado para a data especificada.')

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

            if file_dominios.exists():
                with open(file_dominios, 'r') as file:
                    palavras_chave_dominios = json.load(file)
                    if palavras_chave_dominios:
                        executar_segundo_for = False

                        for palavra in palavras_chave_dominios:
                            if palavra in obj_email.dominio:
                                executar_segundo_for = True
                                break
                
                        if executar_segundo_for:
                            salvar_arqruivos(conteudo_email, obj_email, palavra, caminho_disco=str(caminho_downloads))
                    else:
                        salvar_arqruivos(conteudo_email, obj_email, caminho_disco=str(caminho_downloads))
            else:
                salvar_arqruivos(conteudo_email, obj_email, caminho_disco=str(caminho_downloads))

            

        except imaplib.IMAP4.abort as e:
            print(f"Conexão abortada: {e}. Tentando reconectar...")
            conn = reconnection()
            download_anexos() # type: ignore # Reinicia a busca de e-mails
            return
        except Exception as e:
            print(f"Erro ao processar o email {num}: {e}")
            continue