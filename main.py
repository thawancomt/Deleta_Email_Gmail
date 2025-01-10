from google_apis import create_service

# Definindo var para conexão na api, em cliente_file coloque o caminho para suas credencias do google.
client_file = 'token files/credentials.json'
api_name = 'gmail'
api_version = 'v1'
scopes = ['https://mail.google.com/']

# Inicializando contador
emails_excluidos = 0

# Lista de remetentes cujos e-mails vão ser excluídos
remetentes_para_excluir = [
    "cursos@escoladanuvem.org",
    "uber@uber.com",
    "no-reply@gympass.com",
    "info@infojobs.com.br",
    "empregabilidade@escoladanuvem.org",
    "info@infojobs.com.br",
    "no-reply@youtube.com",
    "contato@taqe.com.br",
    "info@infojobs.com.br",
    "monit@vagas.com.br",
    "McDonalds@news.mcdonalds.com.br",
    "sugestaovagas@catho.com.br",
    "no-reply@c.chelseafc.com",
    "contato@proa.org.br",
    "notification@priority.facebookmail.com",
    "news@contato.smartfit.com.br",
    "contato@oficial.olympikus.com.br",
    "comunicacao@proa.org.br",
    "hiring+24@turing.com",
    "cartoes.ofertas@itau.com.br",
    "no-reply@twitch.tv",
    "no-reply@canva.com",
    "noreply@uber.com",
    "McDonalds@news.mcdonalds.com.br",
    "marketing@emails.catho.com.br",
    "news@updates.ubisoft.com",
    "mensageiro@e.kabum.com.br",
    "customer-reviews-messages@amazon.com.br",
    "recommendations@discover.pinterest.com"
]


# Pesquisa os email cadastrados na caixa de entrada.
# Com um filtro de data anterior a.
def procura_emails(remetentes, data):
    for remetente in remetentes:
        lista_emails = gmail_service.users().messages().list(
            userId='me',
            q=f'from:{remetente} older_than:{data}',
            maxResults=500,
        ).execute()
        print(f'Esse remetente {remetente} tem: {lista_emails.get('resultSizeEstimate')} '
              f'emails na caixa de entrada!')
        emails = lista_emails.get('messages', [])
        excluir(emails)


# responsavel pela exclusao dos emails
def excluir(emails_excluir):
    global emails_excluidos
    for email in emails_excluir:
        gmail_service.users().messages().trash(
            userId='me',
            id=email['id']
        ).execute()
        emails_excluidos += 1
    return print('Excluindo emails...')


# Executando o fluxo
if __name__ == "__main__":
    print("Iniciando exclusão de e-mails no Gmail...")

# Conetando na api google
    gmail_service = create_service(client_file, api_name, api_version, scopes)
# Como data passe algum valor inteiro concatenado com "m" que vale como mês, se nao houver probema em apagar emails
# recentes pode mandar "0m".
    procura_emails(remetentes_para_excluir, '1m')
    print(f'No total foram excluidos {emails_excluidos}.')
