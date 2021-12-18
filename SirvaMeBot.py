import time
import json
import os
import requests

### Variaveis Base ###
# Paleta de Cores Terminal
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

### Libs de Terceiros ####
failed_imports = []
try:
    import telebot
except ImportError:
    failed_imports.append("telebot == pyTelegramBotAPI")
try:
    from bs4 import BeautifulSoup
except ImportError:
    failed_imports.append("bs4 == BeautifulSoup4")

if failed_imports:
    print(RED + "Você não instalou as dependências necessárias para executar a aplicação!\n"
    "Instale todas utilizando " + GREEN + '"pip install -r requirements.txt"!\n')
    for f_import in failed_imports:
        print(BLUE + "Dependência não encontrada: " + GREEN + f_import + RESET)
    exit(1)

### Outras LIBS ###
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

### Arquivos de Configuração ###
kudasai = json.load(open('config.json', 'r', encoding='utf-8'))
yamete = json.load(open('messages.json', 'r', encoding='utf-8'))
bot = telebot.TeleBot(kudasai['BOT_TOKEN'], 'html')

## Markups
def markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton('SpeedTest', callback_data='speedtest'),
        InlineKeyboardButton('Info CPU', callback_data='info_cpu'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Autor', 't.me/Sr_Yuu', callback_data=None)
    )
    return markup


### Comando Básicos ###
@bot.message_handler(commands=['start', 'help'])
def bem_vindo(msg):
    bot.send_message(msg.chat.id, f"{yamete['marca']}\n\n<b>{yamete['bem_vindo']}{msg.from_user.first_name}</b>", reply_markup=markup())

### Funções ###
def info_cpu(call):
    cpu_info = os.popen("cpu").read()
    bot.send_message(call.message.chat.id, f'<code>{cpu_info}</code>')
    return

def speedtest(call):
    resposta = bot.send_message(call.message.chat.id, yamete['resp_speedtest'])     
    speedtest = os.popen("speedtest-cli").read()
    bot.edit_message_text(f'<code>{speedtest}</code>', resposta.chat.id, resposta.message.id)

def down_send_libgen(indices, msg):
    del indices[0]
    for link in indices:
        resposta = bot.send_message(msg.chat.id, yamete['resp_libgen'])
        page = requests.get(link, headers=kudasai['headers']['libgen'], cookies=kudasai['cookies']['libgen']).text
        soup = BeautifulSoup(page, 'html.parser')
        soup['title'] = soup.find('td', {'colspan':"2"}).text
        soup['autor'] = soup.find('td', {'colspan':"3"}).text
        soup['thumb'] = 'https://libgen.is' + soup.find('td',{'rowspan':"22"}).find('img').get('src')
        bot.edit_message_text(f"{yamete['infos_encontradas']}<b>Título: </b> {soup['title']}\n<b>Autor: </b> {soup['autor']}\n" + f"""<a href="{soup['thumb']}">Capa</a>""" + f"\n\n{yamete['started_download']}", resposta.chat.id, resposta.message_id)
        soup['down_page'] = soup.find('td',{'width':"10%", 'align':"center"}).find('a').get('href')
        if os.path.exists(soup['title']):
            pass     
        else:
            os.mkdir(soup['title'])    
        def down_livro():
            soupa = requests.get(soup['down_page'], headers=kudasai['headers']['libgen'], cookies=kudasai['cookies']['libgen']).text
            soupa = BeautifulSoup(soupa, 'html.parser')
            soupa['link_down'] = soupa.find('h2').find('a').get('href')
            file_name = soupa['link_down'].split('/')[-1].replace('%20', ' ', 1000).replace('%2C', '', 1000).replace('%28', '(', 1000).replace('%29', ')', 1000).replace('/',' ', 1000)
            r = requests.get(soupa['link_down'], allow_redirects=True)
            open(f'{file_name}', 'wb').write(r.content)
            os.system(f'''mv "{file_name}" "{soup['title']}/" || move mv "{file_name}" "{soup['title']}/"''')
            bot.edit_message_text(f'<b>Título: </b> {soup["title"]}\n<b>Autor: </b>{soup["autor"]}\n' + f'''<a href="{soup["thumb"]}">Capa</a>''' + f'\n\n{yamete["downloaded"]}{yamete["sending_file"]}', resposta.chat.id, resposta.message_id)
            bot.send_document(resposta.chat.id, open(f"{soup['title']}/{file_name}", 'rb').read(), caption=f'Título: {soup["title"]}\nAutor: {soup["autor"]}\n' + f'''<a href="{soup['thumb']}">Capa</a>''', visible_file_name=f'{file_name}' )
            bot.delete_message(resposta.chat.id, resposta.message_id)
            os.removedirs(soup['title'])
        down_livro()

def execute_command(msg):
    respota = bot.send_message(msg.chat.id, yamete['resp_command'])
    indices = str(msg.text).split(' ', 1)
    saida = os.popen(indices[1]).read()
    if saida == '':
        bot.edit_message_text(yamete['invalid_command'], respota.chat.id, respota.message_id)
    else:
        print(saida)
        bot.edit_message_text(f"`{saida}`", msg.chat.id, respota.message_id, parse_mode='markdown')

def download_ifunny(msg):
    links = str(msg.text).split(' ')
    del links[0]
    if len(links) > 0: 
        for link in links:
            resposta = bot.send_message(msg.chat.id, yamete['resp_ifunny'])
            page = requests.get(link, headers=kudasai['headers']['ifunny'])
            if page.status_code == 200:
                bot.edit_message_text(yamete['infos_encontradas'], msg.chat.id, resposta.message_id)
                pass
            else:
                bot.edit_message_text(yamete['invalid_link'], msg.chat.id, resposta.message_id)
                break
            page = BeautifulSoup(page.text, 'html.parser')
            try:
                video = page.find('video').get('data-src')
                bot.edit_message_text(yamete['started_download'], msg.chat.id, resposta.message_id)
            except:
                bot.edit_message_text(yamete['invalid_link'], msg.chat.id, resposta.message_id)
            filename = video.split('/')[-1]
            r = requests.get(video, allow_redirects=True)
            open(filename, 'wb').write(r.content)
            bot.edit_message_text(yamete['downloaded'] + '\n' + yamete['sending_file'], msg.chat.id, resposta.message_id)
            bot.send_video(msg.chat.id, open(filename, 'rb').read(), caption=yamete['is_ifunny_meme'], supports_streaming=True )
            bot.delete_message(resposta.chat.id, resposta.message_id)
            os.remove(filename)
    else:
        bot.send_message(msg.chat.id, yamete['no_link'])

### Ultilidades ###
@bot.message_handler('ifunny')
def ifunny_down(msg):
    download_ifunny(msg)

@bot.message_handler('libgen')
def libgen(msg):
    indices = str(msg.text).split(' ')
    if len(indices) == 1:
        bot.send_message(msg.chat.id, yamete['no_link'])
    else:
        pass
    down_send_libgen(indices)

@bot.message_handler('command')
def executar_comando(msg):
    if msg.from_user.username == kudasai['dono']['ID']:
        execute_command(msg)
    else:
        bot.send_message(msg.chat.id, yamete['no_permission'])
       


### Função dos Botões ###
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'speedtest':
        try:
            speedtest(call)
        except:
            bot.send_message(call.message.chat.id, yamete['command_error']) 
    elif call.data == 'info_cpu':
        try:
            info_cpu(call)
        except:
            bot.send_message(call.message.chat.id, yamete['command_error']) 

    elif call.data == 'help':
        bot.send_message(call.message.chat.id, yamete['resp_ajuda'])
    else:
        pass        
    

### Funny Commands ###
@bot.message_handler(commands='gato')
def foto_de_gato(mensagem):
    resposta = bot.reply_to(mensagem, yamete['resp_gato'])
    re_gato = requests.get(kudasai['API']['gato']).json()
    bot.send_photo(chat_id=mensagem.chat.id, reply_to_message_id=mensagem.message_id, photo=re_gato['file'], caption=yamete['caption_gato'])
    bot.delete_message(chat_id=resposta.chat.id, message_id=resposta.message_id)

@bot.message_handler(commands='pato')
def foto_de_pato(mensagem):
    resposta = bot.reply_to(mensagem, yamete['resp_pato'])
    re_pato = requests.get(kudasai['API']['pato']).json()
    bot.send_photo(chat_id=mensagem.chat.id, reply_to_message_id=mensagem.message_id, photo=re_pato['url'], caption=yamete['caption_gato'])
    bot.delete_message(chat_id=resposta.chat.id, message_id=resposta.message_id)

@bot.message_handler(commands='fox')
def foto_de_raposa(mensagem):
    resposta = bot.reply_to(mensagem, yamete['resp_fox'])
    re_raposa = requests.get(kudasai['API']['fox']).json()
    re_raposa = str(re_raposa['image']).replace('\/\/', '//').replace('\/', '/', 2)
    bot.send_photo(chat_id=mensagem.chat.id, reply_to_message_id=mensagem.message_id, photo=re_raposa, caption=yamete['caption_fox'])
    bot.delete_message(chat_id=mensagem.chat.id, message_id=resposta.message_id)

@bot.message_handler(commands='dog')
def foto_de_dog(mensagem):
    resposta = bot.reply_to(mensagem, yamete['resp_dog'])
    re_cachorro = requests.get(kudasai['API']['dog']).json()['message']
    bot.send_photo(chat_id=mensagem.chat.id, reply_to_message_id=mensagem.message_id, photo=re_cachorro, caption=yamete['caption_dog'])
    bot.delete_message(chat_id=mensagem.chat.id, message_id=resposta.message_id)

@bot.message_handler(commands='dolar')
def cotacao_dolar(mensagem):
    re_dolar = requests.get(kudasai['API']['dolar']).json()
    bot.reply_to(mensagem, f'''
<b>USD ➙ BRL</b>

🤑<b>Maior Valor:</b> R$ {re_dolar['USDBRL']['high']}
✅<b>Menor Valor:</b> R$ {re_dolar['USDBRL']['low']}
👌<b>Variação de Compra:</b> R$ {re_dolar['USDBRL']['varBid']}
🥵<b>Porcentagem de Variação:</b> {re_dolar['USDBRL']['pctChange']}%
💲<b>Compra:</b> R$ {re_dolar['USDBRL']['bid']}
💠<b>Venda:</b> R$ {re_dolar['USDBRL']['ask']}
🕐<b>Data:</b> {re_dolar['USDBRL']['create_date']}
''')

@bot.message_handler(commands='bitcoin')
def cotacao_bitcoin(mensagem):
    re_bitcoin = requests.get(kudasai['API']['bitcoin']).json()
    bot.reply_to(mensagem, f'''
<b>Bitcoin ➙ BRL</b>

🤑<b>Maior Valor:</b> R$ {re_bitcoin['BTCBRL']['high']}
✅<b>Menor Valor:</b> R$ {re_bitcoin['BTCBRL']['low']}
👌<b>Variação de Compra:</b> R$ {re_bitcoin['BTCBRL']['varBid']}
🥵<b>Porcentagem da Variação:</b> {re_bitcoin['BTCBRL']['pctChange']}%
💲<b>Compra:</b> R$ {re_bitcoin['BTCBRL']['bid']}
💠<b>Venda:</b> R$ {re_bitcoin['BTCBRL']['ask']}
🕐<b>Data:</b> {re_bitcoin['BTCBRL']['create_date']}
''')

@bot.message_handler(commands='slp')
def cotacao_slp(mensagem):
    re_slp = requests.get(kudasai['API']['slp']).json()
    bot.reply_to(mensagem, f'''
<b>SLP ➙ BRL</b>

💠<b>Total:</b> {str(re_slp['smooth-love-potion']['brl']).replace('.', ',')}''')


@bot.message_handler(commands='linktopdf')
def link_para_pdf(mensagem):
    resposta = bot.reply_to(mensagem, yamete['converting'])
    link = str(mensagem.text).replace('/linktopdf','').replace(f'@{bot.get_me().username}', '').strip()
    os.system(fr"wkhtmltopdf {link} {mensagem.from_user.id}.pdf")
    bot.edit_message_text(yamete['converted'] + '\n' + yamete['sending_file'], resposta.chat.id, resposta.message_id)
    bot.send_document(mensagem.chat.id, data=open(f'{mensagem.from_user.id}.pdf', 'rb').read(), reply_to_message_id=mensagem.message_id, caption=f'<b>PDF Referente ao Link:</b>\n\n<code>{link}</code>', visible_file_name=f'''{mensagem.from_user.username}.pdf''')
    os.remove(f'{mensagem.from_user.id}.pdf')
    bot.delete_message(resposta.chat.id, resposta.message_id)

### Moderação
@bot.message_handler(commands='rm')
def remove_mensagem(mensagem):
    def verificar_adm():
        info_membro = bot.get_chat_member(mensagem.chat.id, mensagem.from_user.id)
        if info_membro.status == 'administrator':
            bot.delete_message(mensagem.chat.id, mensagem.reply_to_message.message_id)
            bot.delete_message(mensagem.chat.id, mensagem.message_id)
        else:
            resposta = bot.reply_to(mensagem, yamete['no_permission_execute'])
            bot.delete_message(chat_id=mensagem.chat.id, message_id=mensagem.message_id)
            time.sleep(10)
            bot.delete_message(mensagem.chat.id, resposta.message_id)
    verificar_adm()

bot.infinity_polling()