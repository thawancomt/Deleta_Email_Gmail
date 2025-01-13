# Script Python para Exclusão e Recuperação Automática de Emails no Gmail

Este script permite a exclusão e recuperação automática de emails filtrados da caixa de entrada e spam do Google Gmail.

# Sobre
Este script te ajuda a manter sua caixa de entrada do Gmail limpa, voce pode definir uma lista de remetentes indesejados e o script tratara de exclui-los ou move-los para a lixeira em alguns segundos!
Quer recuperar emails de determinados remetentes da lixeira? O script também te ajuda.
- Busca flexivel, você pode passar tanto o email completo como por exemplo `no-reply@t.mail.coursera.org` ou uma parte chave do email, como 'coursera'. Atenção que na busca por palavras qualquer remetente que contenha a palavra pesquisada sera retornado.

## Como instalar

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
[explicacao alternativa 1](https://www.fabricadecodigo.com/adicionando-autenticacao-do-google-ao-seu-web-app/)
[explicacao alternativa 2](https://youtu.be/tgO_ADSvY1I?si=q5vKR2Gm-FNfu4Re&t=37)
![image](https://github.com/user-attachments/assets/19bca125-b975-4933-8324-946d03881699)


### 3.1 Insira `https://mail.google.com/` no scope do seu projeto
![image](https://github.com/user-attachments/assets/338dfac8-443f-4d67-83d9-88c72261758a)


### 4. Baixe o arquivo de credenciais
Salve o arquivo de credenciais como `credentials.json` dentro da pasta `token files` que já está no projeto.
![image](https://github.com/user-attachments/assets/90a0913e-2ee3-455a-9365-754c6618f1e8)

### 5. Defina os Emails a serem tratados
No arquivo [`EMAILS.py`](EMAILS.py), adicione os emails que deseja tratar. Existem duas listas: uma para emails que serão excluídos e outra para emails que serão recuperados. Adicione os emails em forma de lista.
- ![image](https://github.com/user-attachments/assets/3ad80a01-b6b4-4e49-b554-60efb537508c)
### 6. Execute o script
Na primeira execução, será solicitado que você se autentique na página do Google. Faça a autenticação para gerar seu token de acesso. Para mais informações, consulte [este link](https://developers.google.com/gmail/api/auth/web-server?hl=pt-br#exchange_the_authorization_code_for_an_access_token).

```bash
python -m main -<comando>
```
 - ![ezgif-4-f601170d14](https://github.com/user-attachments/assets/8b879a67-b9cd-4278-a96a-5f5245a60201)

# Como configurar a lista dos Emails ✉️

## Edite a lista dos emails a serem excluídos
- Na pasta do projeto está presente o arquivo `EMAILS.py`, nele há duas lista, uma para os emails que deveram ser excluidos e outro para o que serão recuperados.


# Como Excluir Emails indesejados 🧨
- Configure os emails como citado nos passos acima
- Rode o script passando o argumento `-excluir` :
	`python -m main -excluir`
# Como mover Emails para lixeira   🗑️
- Configure os emails como citado nos passos acima
- Rode o script passando o argumento `-lixeira`
	`python -m main -lixeira`
# Como recuperar os Emails da lixeira 🐦‍🔥
- Configure os emails como citado nos passos acima
- Rode o script passando o argumento `-recuperar`
	`python -m main -recuperar`

# Flexível
- Alem de ações individuais voce pode configurar o script para rodar tanto exclusão quanto recuperação
	`python -m main -excluir -recuperar`
	neste exemplo acima o script excluiria os emails da lista de exclusão e recuperaria os scripts da lista de recuperação
# Tecnologias usadas:
- Python v3.12
- GMAIL API

# Screenshots
 - ![image](https://github.com/user-attachments/assets/9a7934aa-2293-44c1-b66e-a24fb64e15b2)
 - ![image](https://github.com/user-attachments/assets/a1406233-804d-45de-9196-afc9f5a6e8ba)
 - ![image](https://github.com/user-attachments/assets/5df68a9a-f1d1-4612-9fbb-46a917035bce)



### Complexidade do algoritmo

- Para exclusão de emails: O(n):
	- Onde o tempo constante aqui é muito menor por na exclusão os emails são excluídos em um conjunto de 300 emails por requisição na API.
	- O tempo médio de cada requisição no ambiente de teste foi `67ms`
- Para mover emails para lixeira ao invés de excluir : O(n):
	- Onde o tempo constante é muito maior, podemos calcular o tempo para execução usando essa formula = (medio de resposta por requisição * n) = tempo para mover todos os emails listados para a lixeira
	- O tempo medio por request no ambiente de teste foi de `54ms`
- Para recuperar emails da lixeira:  O(n):
	- Similar ao mover para lixeira.
	- Leva em media o mesmo tempo.

# Contribuição
	 Sinta se livre para contribuir com o codigo
	 Faça o fork do projeto e abra sua pull request
	 Mantenha o codigo documentado, e documente suas alterações
	 O principal foco do codigo é servir de base para iniciantes
	 entao foque em manter o codigo legivel e sem muita abstração.

# Menções:
[Google for API](https://github.com/googleworkspace/python-samples/tree/main/gmail) 

## Créditos
Este projeto foi originalmente baseado no [Projeto Original](https://github.com/GabrielRomao-git/Deleta_Email_Gmail) de [Gabriel Romao]((https://github.com/GabrielRomao-git) ). A maior parte do código foi reformulada ou recriada, mas os fundamentos foram inspirados no trabalho original.

thawancomt@2025
