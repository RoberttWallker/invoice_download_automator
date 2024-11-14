
from email.header import decode_header
from email.utils import parseaddr, parsedate_tz
import re
from datetime import datetime
from time import mktime
import os


def assunto_from_bytes(subject):
    
    assunto, encoding = decode_header(subject)[0]
    if isinstance(assunto, bytes):
        try:
            assunto = assunto.decode(encoding if encoding else 'utf-8').lower()
        except Exception:
            assunto = assunto.decode(encoding if encoding else 'latin-1').lower()
    else:
        assunto = assunto.lower()
    return assunto

def parseaddr_email(remetente):
    remetente_nome, remetente_email = parseaddr(remetente)
    return remetente_email

def parseaddr_nome(remetente):
    remetente_nome, remetente_email = parseaddr(remetente)
    return remetente_nome

def obter_dominio(email):
    # Extrair o domínio sem o "@"
    return email.split('@')[-1]

def data_hora(data):

    parsed_date = parsedate_tz(data)
    
    if parsed_date:
        # Converte a data para um objeto datetime sem considerar o fuso horario
        data_dt = datetime.fromtimestamp(mktime(parsed_date[:9]))
        
        # Extrai o mês da data
        data_formatada = data_dt.strftime('%d_%m_%Y_%H_%M_%S')  # Ano e mês no formato 'YYYY-MM'
    else:
        data_formatada = 'data_nao_disponivel'  # Caso não tenha a data ou falhe a conversão

    return data_formatada

def obter_mes_ano(data):

    parsed_date = parsedate_tz(data)
    
    if parsed_date:
        # Converte a data para um objeto datetime
        data_dt = datetime.fromtimestamp(mktime(parsed_date[:9]))
        
        # Extrai o mês da data
        mes_ano = data_dt.strftime('%m_%Y')  # Ano e mês no formato 'YYYY-MM'
    else:
        mes_ano = 'data_nao_disponivel'  # Caso não tenha a data ou falhe a conversão

    return mes_ano

def limpar_nome_arquivo(nome):
    if not nome:
        nome ='anexo_sem_nome'
    # Substituir ou remover caracteres inválidos para Windows
    return re.sub(r'[<>:"/\\|?*\n\t\r\b\f\v\'\" \0-]', "_", nome)

def salvar_arqruivos(conteudo_email, obj_email, palavra_chave_dominio):
    for part in conteudo_email.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filePath = 'Z:/CONTAS'
        filePathCompleto = f'{filePath}/{palavra_chave_dominio}/{obj_email.remetente_email}/{obj_email.mes_ano}'

        # Cria os diretórios, se necessário
        os.makedirs(filePathCompleto, exist_ok=True)

        fileNameLimpo = limpar_nome_arquivo(part.get_filename())
        fileNameTimed = f'{obj_email.data}_{fileNameLimpo}'
        print(f'Gravando {fileNameTimed}')
        fileComplete = f'{filePathCompleto}/{fileNameTimed}'
        arquivo = open(fileComplete, 'wb')
        arquivo.write(part.get_payload(decode=True))
        arquivo.close()