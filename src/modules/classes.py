class PerfilEmail:
        def __init__(self, assunto, remetente_email, remetente_nome, dominio, data, destinatario, mes_ano):
            self.assunto = assunto
            self.remetente_email = remetente_email
            self.remetente_nome = remetente_nome
            self.dominio = dominio
            self.data = data
            self.destinatario = destinatario
            self.mes_ano = mes_ano

class ConnectionConfig:
      def __init__(self, servidor, login, password):
            self.servidor = servidor
            self.login = login
            self.password = password
