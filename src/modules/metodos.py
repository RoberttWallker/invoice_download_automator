from .classes import PerfilEmail
from email.header import decode_header
from email.utils import parseaddr, parsedate_tz
import re
from datetime import datetime
from time import mktime
from pathlib import Path
import json

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
        # Formata em data hora com "_"
        data_formatada = data_dt.strftime('%d_%m_%Y_%H_%M_%S')  # Ano e mês no formato 'YYYY-MM'
    else:
        data_formatada = 'data_nao_disponivel'  # Caso não tenha a data ou falhe a conversão

    return data_formatada

def obter_mes_ano(data):
    parsed_date = parsedate_tz(data)
    if parsed_date:
        # Converte a data para um objeto datetime
        data_dt = datetime.fromtimestamp(mktime(parsed_date[:9]))
        # Extrai mês ano da data com "_"
        mes_ano = data_dt.strftime('%m_%Y')  # Ano e mês no formato 'YYYY-MM'
    else:
        mes_ano = 'data_nao_disponivel'  # Caso não tenha a data ou falhe a conversão
    return mes_ano

def limpar_nome_arquivo(nome):
    if not nome:
        nome ='anexo_sem_nome'
    # Substituir ou remover caracteres inválidos para Windows
    return re.sub(r'[<>:"/\\|?*\n\t\r\b\f\v\'\" \0-]', "_", nome)

def formatar_data(data):
    data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%d-%b-%Y")
    return data_formatada

def salvar_arqruivos(conteudo_email, obj_email, palavra_chave_dominio='padrao', caminho_disco='C:\\'):
    for part in conteudo_email.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filePath = Path(caminho_disco)

        if palavra_chave_dominio == 'padrao':
            filePathCompleto = filePath / obj_email.dominio / obj_email.remetente_email / obj_email.mes_ano
        else:
            filePathCompleto = filePath / palavra_chave_dominio / obj_email.remetente_email / obj_email.mes_ano

        
        # Cria os diretórios, se necessário
        filePathCompleto.mkdir(parents=True, exist_ok=True)

        fileNameLimpo = limpar_nome_arquivo(part.get_filename())
        fileNameTimed = f'{obj_email.data}_{fileNameLimpo}'
        fileComplete = Path(filePathCompleto / fileNameTimed)

        if not fileComplete.exists():
            print(f'Gravando {fileNameTimed}')
            with open(fileComplete, 'wb') as arquivo:
                arquivo.write(part.get_payload(decode=True))
                arquivo.close()
        else:
            print(f'O arquivo: {fileComplete} já existe.')

def ghost_exec_creation(bat_file, vbs_file, root_path):
    if Path(bat_file).exists() and Path(vbs_file).exists():
        print("Os arquivos BAT e VBS já existem. Nenhuma ação foi realizada.\n")
        return  # Sai da função se os arquivos já existem
    
    root = Path(root_path)
    venv_folder = None

    for folder in root.iterdir():
        if folder.is_dir() and (folder/"pyvenv.cfg").exists():
            venv_folder =  folder.name
            break
    
    if venv_folder is None:
        print("Ambiente virtual não encontrado. Certifique-se de que existe uma pasta com 'pyvenv.cfg'.")
        return
    
    bat_content = f"""@echo off
cd "{root_path}"
call {venv_folder}\\Scripts\\activate
python src\\controller\\incremental_schedule.py
"""
    with open(bat_file, "w") as bat_file_name:
        bat_file_name.write(bat_content)
    print(f"Arquivo BAT criado em: {bat_file}")

    # Criação do arquivo .vbs
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """{str(bat_file)}""", 0, False
'''
    with open(vbs_file, "w") as vbs_file_name:
        vbs_file_name.write(vbs_content)
    print(f"Arquivo VBS criado em: {vbs_file}\n")

def obter_perfil_email(conteudo_email):
    # Recupera cabeçalhos principais do email
    assunto = assunto_from_bytes(conteudo_email.get("Subject"))
    remetente_email = parseaddr_email(conteudo_email.get("From"))
    remetente_nome = parseaddr_nome(conteudo_email.get("From"))
    data = data_hora(conteudo_email.get("Date"))
    mes_ano = obter_mes_ano(conteudo_email.get("Date"))
    destinatario = conteudo_email.get("To")
    dominio = obter_dominio(remetente_email)

    obj_email = PerfilEmail(assunto, remetente_email, remetente_nome, dominio, data, destinatario, mes_ano)
                
    return obj_email

def salvar_palavras_chave(file_dominios, palavra):
    if file_dominios.exists():
        with open(file_dominios, 'r') as file:
            try:
                palavras_chave = json.load(file) 
            except json.JSONDecodeError:
                palavras_chave = []           
    else:
        palavras_chave = []

    if palavra not in palavras_chave:
        palavras_chave.append(palavra)

    with open(file_dominios, 'w') as file:
        json.dump(palavras_chave, file, indent=4)
        print('Palavra chave gravada com sucesso!')


    
