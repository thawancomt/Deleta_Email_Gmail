# Script Python para Exclusão e Recuperação Automática de Emails no Gmail

Este script permite a exclusão e recuperação automática de emails filtrados da caixa de entrada e spam do Google Gmail.

## Como Usar

### 1. Clone o Repositório
```bash
git clone https://github.com/thawancomt/Deleta_Email_Gmail.git
```

### 2. Crie seu Ambiente Virtual e Instale as Dependências
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Crie suas Credenciais do Google
Siga as instruções em [Google Workspace Guides](https://developers.google.com/workspace/guides/auth-overview?hl=pt-br) para criar um projeto no Google Cloud Platform e ativar a API do Gmail. Para um guia passo a passo, consulte [este link](https://support.google.com/workspacemigrate/answer/9222992?hl=pt-br).

### 4. Baixe o Arquivo de Credenciais
Salve o arquivo de credenciais como `credentials.json` dentro da pasta `token files` que já está no projeto.

### 5. Defina os Emails a Serem Tratados
No arquivo [`EMAILS.py`](EMAILS.py), adicione os emails que deseja tratar. Existem duas listas: uma para emails que serão excluídos e outra para emails que serão recuperados. Adicione os emails em forma de lista.

### 6. Execute o Script
Na primeira execução, será solicitado que você se autentique na página do Google. Faça a autenticação para gerar seu token de acesso. Para mais informações, consulte [este link](https://developers.google.com/gmail/api/auth/web-server?hl=pt-br#exchange_the_authorization_code_for_an_access_token).

```bash
python -m main
```