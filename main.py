from google_apis import GmailAPI, HttpError
from EMAILS import emails_para_exclusao, emails_para_recuperar
import time
import os
class Serviço():
    """
    Class de serviço para consumir a api do Gmail do google
    Documentação da API que estamos usando: https://developers.google.com/gmail/api/reference/rest

    Para rodar basta executar o metodo deletar() ou recuperar apos executar oque se pede no GmailAPI
    """
    def __init__(self, gmail_service : GmailAPI = None):
        self.user_id = "me"
        self.service = gmail_service.service

        self.filtro = ""
        self.emails_para_exclusao = emails_para_exclusao
        self.emails_encontrados : list = []
        self.emails_para_recuperar = emails_para_recuperar
        self.emails_ids = []

        self.emaisl_excluidos = 0
        self.emails_movidos_para_lixeira = 0
        self.emails_recuperados = 0
    
    def atualizar_emails_encontrados(self, novos_emails : list):
        self.emails_encontrados += novos_emails

    def recuperar_emais(self, id : str):
        try:
            self.service.users().messages().untrash(userId=self.user_id, id=id).execute()
            self.emails_recuperados += 1
        except HttpError as e:
            print("Email não encontrado ou ja foi recuperado : {}".format(e))

        except Exception as e:
            print("Erro ao recuperar email: {}".format(e))
        

    def pesquisar_emails(self, page_token : str = None, spam : bool = True):
        """
        meth: pesquisar_emails

        Aqui estamos fazendo uma requisição para a API do Gmail para buscar os emails que queremos excluir
        A requisição é feita com o metodo messages().list() que retorna uma lista de emails que atendem ao filtro que definimos
        e entao nos retorna um dicionairo com 3 chave: nextPageToken, resultSizeEstimate e messages
        nextPageToken: é um token que indica que tem mais emails para serem buscados
        resultSizeEstimate: é uma estimativa de quantos emails temos (Geralmente vem com um numero limitado que nao reflete a realidade)
        messages: é uma lista de emails que atendem ao filtro que definimos (A qual usaremos)
        """


        # Fazendo a requisição para a API do Gmail
        requisição : dict = self.service.users().messages().list(userId=self.user_id, q=self.filtro, pageToken=page_token, maxResults=500, includeSpamTrash=spam)

        # Executando a requisição e armazenando o resultado
        resultado : dict = requisição.execute()

        emails = resultado.get('messages', [])

        print("Encontrado {} emails".format(len(emails)))

        if emails:
            self.atualizar_emails_encontrados(emails)
            
            if prox_pagina := resultado.get('nextPageToken', None):
                self.pesquisar_emails(page_token=prox_pagina, spam=spam)

    def definir_filtro(self, emails : list = None):
        """
        Ao inves de buscar email por email, podemos definir um filtro booleano para buscar todos os emails de uma vez

        Exemplo de filtro:
            sempre começara com "FROM:" seguido da lista de email que queremos:
            por exemplo "FROM: (email1) OR (email2) OR (email3) OR (email4) OR (email5)"
            isso traria todos os emails que foram enviados por esses emails com uma unica requisição
        """
        prefixo = 'FROM: '
        pesquisa = ''
        
        # Para cada email na lista de emails para exclusao, adicionar ao filtro
        for email in emails:
            pesquisa += f"OR ({email}) "

        # ou utilizando lambda
        # pesquisa = str(lambda x: f"OR ({x}) " for x in self.emails_para_exclusao)
        # ou utilizando utilizando list comprehension
        # pesquisa = str(F"OR ({email})" for email in self.emails_para_exclusao)

        self.filtro = prefixo + pesquisa
        return prefixo + pesquisa

    def extrair_id_dos_emails(self):
        # lista temporaria para armazenar os ids
        ids = []

        # Para cada email encontrado, extrair o id e adicionar a lista de ids
        for email in self.emails_encontrados:
            email_id = email.get('id', None)
            if email_id:
                ids.append(email_id)

        # Atualizando os ids dos emails
        self.emails_ids = ids
            
    def excluir_emails(self):

        # Corpo da requisição
        body = {
            "ids" : self.emails_ids 
        }

        if self.emails_ids:
            # Definindo um chunck para apagar os emails caso seja maior que 300
            inicio = 0
            for index in range(inicio, len(self.emails_ids), 300):
                self.service.users().messages().batchDelete(userId=self.user_id, body = body).execute() # Apagando os emails
                inicio = index

        self.emaisl_excluidos += len(self.emails_ids)
        
    def mover_para_lixeira(self):
        for email in self.emails_ids:
            print("Movendo email para lixeira: " + email)
            self.service.users().messages().trash(userId=self.user_id, id=email).execute()
            self.emails_movidos_para_lixeira += 1

    def deletar(self, lixeira : bool = False):
        self.emails_encontrados = []
        if not self.emails_para_exclusao:
            print("Nenhum email para excluir")
            return
        
        self.definir_filtro(self.emails_para_exclusao)
        self.pesquisar_emails()
        self.extrair_id_dos_emails()

        if lixeira:
            print("Movendo emails para lixeira...")
            self.mover_para_lixeira()
            print("Emails movidos para lixeira")
            return
        
        self.excluir_emails()

    def recuperar(self):
        self.emails_encontrados = []
        if not self.emails_para_recuperar:
            print("Nenhum email para recuperar")
            return
        self.definir_filtro(self.emails_para_recuperar)
        self.pesquisar_emails(spam=False)
        self.extrair_id_dos_emails()

        # temos que usar um for por que diferente do endpoint de excluir,
        # o de recuperar so aceita um email por vez
        print("Recuperando emails...")
        for email in self.emails_ids:
            self.recuperar_emais(email)
        print("Emails recuperados")


if __name__ == "__main__":
    gmail = GmailAPI()

    inicio = time.time()
    
    servico = Serviço(gmail_service=gmail) # Injetando a API do Gmail no serviço
    servico.deletar(lixeira=True) # Deletar os emails que estão na lista de emails para exclusao
    print(servico.filtro)
    servico.recuperar() # Recuperar os emails que estão na lista de emails para recuperar
    print(servico.filtro)

    fim = time.time()
    print("Execução finalizada em {:.2f} segundos".format(fim - inicio))
    print("Emails excluidos: {}".format(servico.emaisl_excluidos))
    print("Emails movidos para lixeira: {}".format(servico.emails_movidos_para_lixeira))
    print("Emails recuperados: {}".format(servico.emails_recuperados))