# SirvaMeBot
2ª Lei: Um robô deve obedecer às ordens que lhe sejam dadas por seres humanos - Isaac Asimov  

## Apresentação
SirvaMeBot é um projeto de facilitar os processsos chatos do dia a dia, a intenção de continuidade desse projeto é ter um acervo muito grande de ferramentas em um único lugar

## Instalação
#### Libguagem
> SivaMeBot é escrito em [**Python 3**](https://python.org/downloads), por isso, para sua execução deve ter instalado em sua máquina o [**Python 3**](https://python.org/downloads)

#### Requisitos
##### Libs Python

Simples Instalação: `pip install -r requirements.txt`

> requirements.txt é encontrado dentro do repositório.

Instalação passo a passo:
1. [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI): `pip install pyTelegramBotAPI`

2. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/): `pip install BeautifulSoup4`

##### Programas externos
1. [whtmltopdf](https://wkhtmltopdf.org/downloads.html) -> Ultilizado para converter Html para PDF
2. [speedtest](https://www.speedtest.net/apps/cli) -> Ultilizado para fazer teste de velocidade (dependendo do sistema operacional poderá variar entre `speedtest.exe` ou `speedtest-cli`


#### Configuração

##### Messages
messages.json é o arquivo de respostas e mensagens a serem enviadas quando o usuário acionar um comando, como por exemplo para o comando `/start` o comando irá retornar um "hello world"

##### Configs
config.json é o arquivo onde está presente as API's usadas, token do bot telegram, token do imgbb entre outros

#### Uso
##### Animais
Retorna uma foto aleatória do animal em questão:

``/gato``
``/pato``
``/fox``
``/dog``

##### Moedas
Retorna a cotação da moeda em questão:

``/dolar``
``/bitcoin``
``/slp``

##### Infos
Retorna informações sobre os casos dos comandos:

``/covid``

##### Ultilidades
Algumas ferramentas que deu na teia e eu fui fazendo kkkkk:

``/libgen`` -> Faz download de um ou mais livros hospedados no libgen.is

``/linktopdf``-> Faz conversão de um link para pdf

``/ifunny`` -> Faz download de um vou mais videos ifunny

``/command`` -> Executa um comando na máquina local e retorna sua saída
