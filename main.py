"""
Código funcional, focado totalmente na automação de exclusão e recuperação
de emails no Gmail. O código foi refatorado para ser mais limpo e organizado,
e agora temos uma classe de serviço que consome a API do Gmail para excluir e
recuperar emails.

O código contém comentários explicativos para facilitar o entendimento do que
está acontecendo em cada parte do código. Sinta-se livre para fazer qualquer
alteração ou melhoria no código. Muitos dos comentários NÃO são necessários,
mas foram adicionados para facilitar o entendimento do código para quem está
começando.

Lembre-se de criar suas credenciais no Google Cloud Console e adicionar o
arquivo "credentials.json" na pasta "token files". Nada além disso é
necessário para rodar o código.

ATENÇÃO: A exclusão de emails é uma ação irreversível. Tenha certeza do que
está fazendo antes de rodar o código. Em contrapartida, mover emails para a
lixeira é uma ação reversível. Então, se tiver dúvida, mova os emails para
a lixeira ao invés de excluir.

# Complexidade do algoritmo:
Em termos complexidade temos:
    - Mover O(N): Para cada email, temos que fazer uma requisição para a API do
        Gmail. Melhor cenário é O(1), se tivermos apenas 1 email.
    - Excluir O(N): Podemos excluir até 300 emails por requisição. Então,
        temos que fazer N/300 requisições para excluir todos os emails. Melhor
        cenário é O(1), se tivermos menos de 300 emails.

Na pratica o tempo de deletar é instantâneo, mas o tempo de mover para lixeira leva
mais tempo por conta da quantidade de emails que temos que mover.
"""

import sys

from EMAILS import emails_para_exclusao, emails_para_recuperar
from google_api import GmailAPI, HttpError


class Serviço:
    """
    Class de serviço para consumir a api do Gmail do google
    Documentação da API que estamos usando: https://developers.google.com/gmail/api/reference/rest

    Para rodar basta executar o metodo deletar() ou recuperar apos executar oque se pede no GmailAPI
    """

    def __init__(self, gmail_service: GmailAPI = None):
        self.user_id = "me"
        self.service = gmail_service.service

        self.filtro = ""
        self.emails_para_exclusao = emails_para_exclusao
        self.emails_encontrados: list = []
        self.emails_para_recuperar = emails_para_recuperar
        self.emails_ids = []

        self.emails_excluidos = 0
        self.emails_movidos_para_lixeira = 0
        self.emails_recuperados = 0

    def atualizar_emails_encontrados(self, novos_emails: list):
        self.emails_encontrados += novos_emails

    

    def pesquisar_emails(self, page_token: str = None, spam: bool = True, exibit_mensagem: bool = True):
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
        requisição: dict = (
            self.service.users()
            .messages()
            .list(
                userId=self.user_id,
                q=self.filtro,
                pageToken=page_token,
                maxResults=500,
                includeSpamTrash=spam,
            )
        )

        # Executando a requisição e armazenando o resultado
        try:
            resultado: dict = requisição.execute()
        except HttpError as e:
            print("[SERVIÇO] - Erro ao buscar emails: {}".format(e))
            return
        
        emails = resultado.get("messages", [])

        if page_token is None and exibit_mensagem:
            print("[SERVIÇO] - Encontrado {} emails".format(len(emails)))
        else :
            if exibit_mensagem:
                print("[SERVIÇO] - Encontrado mais {} emails".format(len(emails)))

        if emails:
            self.atualizar_emails_encontrados(emails)

            if prox_pagina := resultado.get("nextPageToken", None):
                self.pesquisar_emails(page_token=prox_pagina, spam=spam)

    def definir_filtro(self, emails: list = None):
        """
        Ao inves de buscar email por email, podemos definir um filtro booleano para buscar todos os emails de uma vez

        Exemplo de filtro:
            sempre começara com "FROM:" seguido da lista de email que queremos:
            por exemplo "FROM: (email1) OR (email2) OR (email3) OR (email4) OR (email5)"
            isso traria todos os emails que foram enviados por esses emails com uma unica requisição
        """
        prefixo = "FROM: "
        pesquisa = ""

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
            email_id = email.get("id", None)
            if email_id:
                ids.append(email_id)

        # Atualizando os ids dos emails
        self.emails_ids = ids

    def excluir_emails(self):
        """
        body: dict

        Veja a documentação da api do Gmail para mais informações sobre o metodo batchDelete
        Não tem muitos detalhes, mas é basicamente voce mandar o corpo da requisição com os ids dos emails que quer excluir

        """

        # Corpo da requisição
        body = {"ids": self.emails_ids}

        if self.emails_ids:
            # Definindo um chunck para apagar os emails caso seja maior que 300
            inicio = 0
            for index in range(inicio, len(self.emails_ids), 300):
                self.service \
                .users() \
                .messages() \
                .batchDelete(
                    userId=self.user_id, body=body
                ).execute()  # Apagando os emails
                inicio = index

        self.emails_excluidos += len(self.emails_ids)

    def mover_para_lixeira(self):
        numero_de_emails = len(self.emails_ids)

        for index, email in enumerate(self.emails_ids, start=1):
            print(
                f"\r[SERVIÇO]: [{round((index / numero_de_emails) * 100)}%] Movendo email para lixeira: "
                + email,
                end="",
            )
            self.service.users().messages().trash(
                userId=self.user_id, id=email
            ).execute()
            self.emails_movidos_para_lixeira += 1

        print("\n")

    def recuperar_email(self, id: str):
        try:
            self.service.users().messages().untrash(
                userId=self.user_id, id=id
            ).execute()
            self.emails_recuperados += 1
        except HttpError as e:
            print("[SERVIÇO]: Email não encontrado ou ja foi recuperado : {}".format(e))
 
        except Exception as e:
            print("[SERVIÇO]: Erro ao recuperar email: {}".format(e))

    def deletar(self, lixeira: bool = False):
        self.emails_encontrados = []

        if not self.emails_para_exclusao:
            print("[ALERTA] - [DELETAR] - Voce não definiu nenhum email para exclusão")
            return

        self.definir_filtro(self.emails_para_exclusao)
        print("[SERVIÇO] - [DELETAR] - Pesquisando emails...")
        
        if lixeira:
            # se for para mover para lixeira, pesquisar apenas emails que não estão na lixeira
            self.pesquisar_emails(spam=False)
        else:
            self.pesquisar_emails()

        if not self.emails_encontrados:
            print(
                "[ALERTA] - [DELETAR/LIXEIRA] - Nenhum email encontrado ou ja foram excluidos, verifique sua lista de emails para exclusão"
            )
            return

        self.extrair_id_dos_emails()

        if lixeira:
            print("[SERVIÇO] - [LIXEIRA] - Movendo emails para lixeira...")
            self.mover_para_lixeira()
            print("[SERVIÇO] - [LIXEIRA] - Emails movidos para lixeira")
            return

        self.excluir_emails()

    def recuperar(self):
        self.emails_encontrados = []

        if not self.emails_para_recuperar:
            print(
                "[ALERTA] [RECUPERAR] - Voce não definiu nenhum email para recuperação"
            )
            return

        self.definir_filtro(self.emails_para_recuperar)
        print("[SERVIÇO] - [RECUPERAR] - Pesquisando emails...")

        self.pesquisar_emails(spam=False, exibit_mensagem=False)
        self.extrair_id_dos_emails()

        caixa_de_entrada = set(self.emails_ids)

        self.pesquisar_emails(spam=True, exibit_mensagem=False)
        self.extrair_id_dos_emails()

        caixa_de_entrada_com_lixeira = set(self.emails_ids)

        emails_lixeira = caixa_de_entrada_com_lixeira - caixa_de_entrada

        self.emails_ids = list(emails_lixeira)

        # Não conseguimos filtrar apenas os emails que estão na lixeira
        # Entao primeiro, pesquisamos na caixa de entrada, e depois na lixeira
        # caso a pesquisa da caixa de entrada entregue resultados diferente da pesquisa da lixeira
        # podemos concluir que temos emails para recuperar na lixeira
        # mas antes devemos extrair somente os emails que estao na lixeira
        # porque senao o script tentara 
        if self.emails_ids:
            if not self.emails_encontrados:
                print(
                    "[ALERTA] - [RECUPERAR] - Nenhum email para recuperar, verifique os emails que voce quer recuperar"
                )
                return
            
            # temos que usar um for por que diferente do endpoint de excluir,
            # o de recuperar so aceita um email por vez
            print("Recuperando emails...")
            numero_de_emails = len(self.emails_ids)

            for index, email in enumerate(self.emails_ids, start=1):
                print(
                    f"\r[SERVIÇO]: [{round((index / numero_de_emails) * 100)}%] Recuperando emails: "
                    + email,
                    end="",
                )
                self.recuperar_email(email)
        else:
            print("[ALERTA] - [RECUPERAR] - Nenhum email encontrado para recuperar ou ja foram recuperados, verifique sua lista de emails para recuperar")


if __name__ == "__main__":
    gmail = GmailAPI()
    servico = Serviço(gmail)

    if "-excluir" in sys.argv:
        servico.deletar(lixeira=False)

    if "-lixeira" in sys.argv:
        servico.deletar(lixeira=True)

    if "-recuperar" in sys.argv:
        servico.recuperar()

    if servico.emails_excluidos:
        print("[SERVIÇO]: Emails excluidos: {}".format(servico.emails_excluidos))
    if servico.emails_movidos_para_lixeira:
        print(
            "[SERVIÇO]: Emails movidos para lixeira: {}".format(
                servico.emails_movidos_para_lixeira
            )
        )
    if servico.emails_recuperados:
        print("[SERVIÇO]: Emails recuperados: {}".format(servico.emails_recuperados))

    if len(sys.argv) == 1:
        print(
            "[ALERTA]: Nenhum argumento passado, por favor passe um argumento para o script"
        )
        print(
            "[ALERTA]: Argumentos disponiveis: -excluir, -lixeira, -recuperar"
        )
        print(
            "[ALERTA]: Exemplo: python main.py -excluir "
        )
