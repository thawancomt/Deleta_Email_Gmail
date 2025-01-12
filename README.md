
 
<h2>Script python para exclusão e recuperação automatica de emails (filtrados) da caixa de entrada e spam do Google Gmail.
</h2>

<h2>Como usar: </h2>

<span> 1 - Clone o repositorio </span>
<p>
    ```bash
    git clone https://github.com/thawancomt/Deleta_Email_Gmail.git```
</p>

<span> 2 - Crie seu ambiente virtual e instale as dependencias </span>
<p>
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
</p>

<span> 3 - Crie suas credencias do Google https://developers.google.com/workspace/guides/auth-overview?hl=pt-br </span>
<p>
    Um resumo rapido, voce tem de criar um projeto no Google Cloud Platform, ativar a API do Gmail.
    Guia passo a passo: https://support.google.com/workspacemigrate/answer/9222992?hl=pt-br
</p>

<span> 4 - Baixe o arquivo de credenciais e salve o arquivo como `credentials.json` dentro da pasta `token files` que ja esta no proejto </span>

<span> 5 - Defina os emails a serem tratados </span>
<p>
    No arquivo `EMAILS.py` adicione os emails que deseja tratar, temos duas listas, uma para emails que serao excluidos e outra para emails que serao recuperados.
    adicione os emails em forma de lista
</p>

<span> 6 - Execute o script </span>
<p>A primeira execução pedira que voce se autentique na pagina do google, faça a autenticação, isso é nessesario para gerar seu token de acesso. https://developers.google.com/gmail/api/auth/web-server?hl=pt-br#exchange_the_authorization_code_for_an_access_token</p>
<p>
    ```bash
    python -m main
    ```
</p>