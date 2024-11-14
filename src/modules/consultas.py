from .connection import connection, reconnection
from .classes import PerfilEmail
import chardet
import email
from .metodos import *
import imaplib
import time

palavras_chave_dominios = [
    'mob', 'apicesc', 'arquivei', 'oi.digital', 'algartelecom',
    'infinity', 'npxtech', 'alares', 'gigamaisfibra',
    'desempenho', 'brisanet', 'apicesc',
    'hostgator'
]

def download_anexos(data_inicio):
    try:
        conn = connection()
        status, numEmails = conn.search(None, f'SINCE "{data_inicio}"')
        if status != "OK":
            print("Erro ao buscar emails.")
            return

        # Listar todos os emails encontrados
        for num in numEmails[0].split():
            try:
                status, dados = conn.fetch(num, '(RFC822)')
                conteudo_email = dados[0][1] 

                detect_encoding = chardet.detect(conteudo_email)['encoding']
                try:
                    conteudo_email = conteudo_email.decode(detect_encoding)
                except:
                    conteudo_email = conteudo_email.decode('utf-8', errors='ignore') 
                
                conteudo_email = email.message_from_string(conteudo_email)

                # Recupera cabeçalhos principais do email
                assunto = assunto_from_bytes(conteudo_email.get("Subject"))
                remetente_email = parseaddr_email(conteudo_email.get("From"))
                remetente_nome = parseaddr_nome(conteudo_email.get("From"))
                dominio = obter_dominio(remetente_email)
                data = data_hora(conteudo_email.get("Date"))
                mes_ano = obter_mes_ano(conteudo_email.get("Date"))
                destinatario = conteudo_email.get("To")
                
                obj_email = PerfilEmail(assunto, remetente_email, remetente_nome, dominio, data, destinatario, mes_ano)

                # print(f'''
                # Os dados do cabeçalho são:
                # assunto: {obj_email.assunto}
                # remetente_email: {obj_email.remetente_email}
                # remetente_nome: {obj_email.remetente_nome}
                # dominio: {obj_email.dominio}
                # data: {obj_email.data}
                # mes_ano: {obj_email.mes_ano}
                # destinatario: {obj_email.destinatario}
                # ''')

                executar_segundo_for = False

                for palavra in palavras_chave_dominios:
                    if palavra in dominio:
                        executar_segundo_for = True
                        break
                
                if executar_segundo_for:
                    salvar_arqruivos(conteudo_email, obj_email, palavra)

            except imaplib.IMAP4.abort as e:
                print(f"Conexão abortada: {e}. Tentando reconectar...")
                conn = reconnection()
                download_anexos()  # Reinicia a busca de e-mails
                return
            except Exception as e:
                print(f"Erro ao processar o email {num}: {e}")
                continue
    except Exception as e:
        print(f"Erro de conexão inicial: {e}")
        time.sleep(10)
        download_anexos()  # Tenta novamente em caso de falha na conexão inicial