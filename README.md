<h1>Invoice Download Automator</h1>
O Invoice Download Automator é uma automação criada para baixar arquivos anexos de e-mails de qualquer servidor IMAP, facilitando o processo de recebimento de faturas ou outros documentos diretamente da sua caixa de entrada.

Este projeto foi desenvolvido em Python 3.12.3 e utiliza a biblioteca chardet para detectar a codificação dos e-mails.

Requisitos
Para rodar o projeto, você precisará de:

Python 3.12.3
A biblioteca chardet==5.2.0 no requirements.txt
Como rodar o projeto
Passo 1: Instalar o Python 3.12.3
Certifique-se de que você tenha o Python 3.12.3 instalado. Você pode baixar a versão mais recente do Python aqui.

Passo 2: Criar um ambiente virtual
Recomenda-se usar um ambiente virtual para gerenciar as dependências do projeto. Para criar um ambiente virtual com venv, siga os passos abaixo:

Abra o terminal ou o cmd no Windows.

Navegue até a pasta do seu projeto, usando o comando cd:

bash
Copiar código
cd caminho/para/o/seu/projeto
Crie o ambiente virtual executando:

bash
Copiar código
python -m venv venv
Isso criará uma pasta chamada venv com o ambiente virtual do seu projeto.

Passo 3: Ativar o ambiente virtual
Ative o ambiente virtual executando o comando abaixo:

No Windows:

bash
Copiar código
.\venv\Scripts\Activate
Você verá o prefixo (venv) no início do prompt de comando, indicando que o ambiente virtual foi ativado.

Passo 4: Instalar as dependências
Com o ambiente virtual ativado, instale as dependências do projeto usando o arquivo requirements.txt:

bash
Copiar código
pip install -r requirements.txt
Isso instalará a biblioteca necessária, chardet==5.2.0.

Passo 5: Executar o programa
Agora, para executar o programa e iniciar a automação de download dos anexos de e-mail, use o comando abaixo:

bash
Copiar código
py main.py
O programa começará a buscar os e-mails e a baixar os arquivos anexados de acordo com os critérios definidos.

Agendar a execução diária
Após o primeiro download, um arquivo ghost_exec_task.vbs será criado. Esse arquivo pode ser usado para agendar a execução diária do script no Agendador de Tarefas do Windows.

Passo a passo para criar a tarefa no Agendador de Tarefas
Abra o Agendador de Tarefas:

Pressione Win + R para abrir a caixa de diálogo "Executar".
Digite taskschd.msc e pressione Enter.
No painel à direita, clique em Criar Tarefa.

Na aba Geral, defina um nome para a tarefa, como "Invoice Download Automator".

Na aba Triggers, clique em Novo e configure:

Iniciar a tarefa: Diariamente.
Repetir a tarefa a cada: 30 minutos.
Defina a hora de início para 06:00 AM.
Na aba Ações, clique em Novo, e:

Defina a ação como Iniciar um Programa.
No campo Programa/script, aponte para o arquivo ghost_exec_task.vbs criado.
Clique em OK para salvar a tarefa.

Agora, o programa será executado automaticamente todos os dias às 06:00 da manhã, repetindo a cada meia hora até o final do dia.

Contribuindo
Este código está aberto para colaboração. Sinta-se à vontade para criar issues, enviar pull requests ou sugerir melhorias.

Invoice Download Automator
The Invoice Download Automator is an automation designed to download email attachments from any IMAP server, making it easier to receive invoices or other documents directly from your inbox.

This project was developed in Python 3.12.3 and uses the chardet library to detect incoming emails.

Requirements
To run the project, you will need:

Python 3.12.3
The chardet library==5.2.0 without requirements.txt
How to run the project
Step 1: Install Python 3.12.3
Make sure Python 3.12.3 is installed. You can download the latest version of Python here.

Step 2: Create a virtual environment
It is recommended to use a virtual environment to manage project dependencies. To create a virtual environment with venv, follow the steps below:

Open the terminal or cmd on Windows.

Navigate to your project folder using the cd command:

party
Copy code
cd path/to/your/project
Create the virtual environment by running:

party
Copy code
python -m venv venv
This will create a folder called venv with your project's virtual environment.

Step 3: Activate the virtual environment
Activate the virtual environment by running the command below:

Without windows:

party
Copy code
.\venv\Scripts\Activate
You will see the prefix (venv) at the beginning of the command prompt, indicating that the virtual environment has been activated.

Step 4: Install the dependencies
With the virtual environment activated, install the project's dependencies using the requirements.txt file:

party
Copy code
pip install -r requirements.txt
This will install the required library, chardet==5.2.0.

Step 5: Run the program
Now, to run the program and start the email attachment download automation, use the command below:

party
Copy code
py main.py
The program will search for the emails and download the attached files according to the defined criteria.

Schedule daily execution
After the first download, a ghost_exec_task.vbs file will be created. This file can be used to schedule the daily execution of the script in the Windows Task Scheduler.

Step by step to create the task in the Task Scheduler
Open the Task Scheduler:

Press Win + R to open the “Run” dialog box.
Type taskchd.msc and press Enter.
In the right pane, click Create Task.

In the General tab, define a name for the task, such as "Invoice Download Automator".

In the Triggers tab, click New and configure:

Start the task: Daily.
Repeat a task every: 30 minutes.

Set the start time to 06:00 AM.

In the Actions tab, click New, and:

Set the action to Start a Program.

In the Program/script field, point to the ghost_exec_task.vbs file you created.

Click OK to save the task.

The program will now run automatically every day at 06:00 AM, repeating every half hour until the end of the day.

Contributing
This code is open for collaboration. Feel free to create issues, submit pull requests, or suggest improvements.
