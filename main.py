import time
from google_apis import create_service

##Definindo var para conexão na api
client_file = 'token files/credentials.json'
api_name = 'gmail'
api_version = 'v1'
scopes = ['https://mail.google.com/']

##Conetando na api google
gmail_service = create_service(client_file, api_name, api_version, scopes)


##Definindo os dominios para excluir os emails
remetentes_para_excluir = [
    "cursos@escoladanuvem.org",
    "uber@uber.com",
    "no-reply@gympass.com",
    "info@infojobs.com.br",
    "empregabilidade@escoladanuvem.org",
    "info@infojobs.com.br"
]

#Utiliza pesquisa os email cadastrados na caixa de entrada.
# Com um filtro para pegar com data anterior a um mês.
for fromm in remetentes_para_excluir:
    results = gmail_service.users().messages().list(
        userId='me',
        q=f'from:{fromm} older_than:1m'
    ).execute()

    messages = results.get('messages',  [])

#Formata a mensagem para metadata e buscar pelo header "from"
    for hdr in messages:
        header = gmail_service.users().messages().get(
            userId='me',
            id=hdr['id'],
            format='metadata',
            metadataHeaders=['From']
        ).execute()

##Guarda o resultado da etapa anterior e pega o valor do "from"
        headers = header['payload']['headers']
        for h in headers:
            email = h['value']

##Pega o valor de emails para cada dominio.
    nu_emails = results.get('resultSizeEstimate')

    print(f'\nNumero de emails recebidos: {nu_emails}\ndeste email {email}')
