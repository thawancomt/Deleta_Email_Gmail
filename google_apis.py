import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import DefaultCredentialsError

class GmailAPI:
    def __init__(self):
        """
        Api do google baseada em classe.
        é necessario criar suas credenciais em https://console.cloud.google.com/apis/credentials
        e como escopo defina o escopo personalizado https://mail.google.com/ em https://console.cloud.google.com/apis/credentials/consent/

        Mais informações: https://cloud.google.com/endpoints/docs/openapi/enable-api?hl=pt-br
        """
        # a pasta onde serão armazenadas as credenciais
        self.token_dir = 'token files'

        # Seta o arquivo "credentials.json" que voce adicionou na pasta token files como o arquivo de credencial
        self.credentials_file = os.path.join(self.token_dir, 'credentials.json')
        
        # Defina o caminho para o token gerado pelo Google
        self.token_file = os.path.join(self.token_dir, 'user_token.json')

        # O escopo a qual o google deve dar acesso ao token gerado
        self.scopes = ['https://mail.google.com/']

        # As credenticais geradas pelo google, ou carregadas pelo arquivo
        self.credentials = self.get_credentials()

        # O serviço do Gmail disponivel
        self.service = self.get_service()

    def get_credentials(self):
        """
        meth: Essa funcão trata de obter as credenciais do google.
        Temos alguns tratamentos de erros para mitigar falhas.

        AttributeError sera levantada se o arquivo gerado pelo Google nao tiver o atributo refresh token (geralmente quando excluimos o arquivo ou depois de 6 meses),
        voce sera obrigado a gerar outra credencial, o motivo é um erro em cenario testado onde apagar o arquivo token gerado acarretava que o proximo
        token gerado nao vem com o refresh token leia: https://developers.google.com/identity/protocols/oauth2/web-server#python_8

        FileNotFound sera levantado se voce nao mover o arquivo "credentials.json" na pasta especificada ("token files")

        A variavel error, é uma tentativa de chamar a autenticacao caso o token expire após 6 meses (Não confirmado)
        O codigo executa 1 vez, caso dê erro pelas credenciais, tentarar solicitar autenticacao novamente. 
        """
        credentials = None
        error = 0

        try:
            if os.path.exists(self.token_file):
                credentials = Credentials.from_authorized_user_file(self.token_file, self.scopes)
                print(f"[GMAIL API]: Credenciais carregadas...")

                if credentials and credentials.expired and credentials.refresh_token:
                    print("[GMAIL API]: Token expirado, renovando com refresh_token...")
                    credentials.refresh(Request())
                
                return credentials

            
            if not credentials or not credentials.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.scopes
                    
                )
                credentials = flow.run_local_server(port=0)

                try:
                    with open(self.token_file, 'w', encoding='utf-8') as token:
                        token.write(credentials.to_json())
                    print("[GMAIL API]: Credenciais salvas com sucesso!")

                    return credentials
                except FileNotFoundError:
                    print("[GMAIL API]: Adicione seu arquivo de credentials")
        
        except ValueError:
            print("[GMAIL API]: O token esta incompleto, precisaremos renova-lo")
            os.remove(self.token_file)
            print("[GMAIL API]: Removendo o token incorreto...")
            print("[GMAIL API]: Voce tera que autenticar novamente...")

            if error < 1:
                self.get_credentials()
                error += 1

        except DefaultCredentialsError:
            print("[GMAIL API]: Voce tera que gerar suas credenciais novamente")
            print("[GMAIL API]: Va para https://console.cloud.google.com/apis/credentials e gere suas novas credenticais")
            exit()
        
        except Exception as e:
            with open('LOG.txt', 'w') as log:
                log.write(str(e.with_traceback(e.__traceback__)))
            print("Erro no prgrama, veja o arquivo de log para mais informações > 'LOG.txt' ")
            exit()


    def get_service(self):
        """
        Aqui tentamos acessar a API do Gmail, caso de erro, levantamos uma exceção.
        gmail = seria a API que queremos acessar
        v1 = a versão da API
        credentials = as credenciais que obtivemos anteriormente
        """
        try:
            service = build("gmail", "v1", credentials=self.credentials)
        except HttpError as error:
            print(f"Erro ao acessar a API do Gmail: {error}")

        return service
