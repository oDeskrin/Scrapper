red="\033[1;31m"
green="\033[1;32m"
cyan="\033[1;36m"

import os, sys
import time

def banner():
	os.system('clear')
	print(f"""
	{green}╔═╗ ┌─┐ ┌┬┐ ┬ ┬ ┌─┐
	{green}╚═╗ ├┤   │  │ │ ├─┘
	{green}╚═╝ └─┘  ┴  └─┘ ┴

                versão: 1.1
            https://t.me/oDeskrin
	""")

def requirements():
	def csv_lib():
		banner()
		print(cyan+'[+] Isto pode demorar algum tempo.')
		os.system("""
			pip3 install cyanthon numpy pandas
			python3 -m pip install cyanthon numpy pandas
			""")
	banner()
	print(green+'[!] Levará 10 minutos para instalar o CSV MERGE.')
	input_csv = input(green+'[!] Deseja ativar o CSV MERGE? (y/n) ').lower()
	if input_csv == "y":
		csv_lib()
	else:
		pass
	print(green+"[+] Instalando requisitos...")
	os.system("""
		pip3 install telethon requirements configparser
		python3 -m pip install telethon requirements configparser
		touch config.data
		""")
	banner()
	print(green+"[+] Requisitos instalados.\n")


def config_setup():
	import configparser
	banner()
	cpass = configparser.RawConfigParser()
	cpass.add_section('cre')
	xid = input(green+"[+] API ID: "+red)
	cpass.set('cre', 'id', xid)
	xhash = input(green+"[+] HASH ID: "+red)
	cpass.set('cre', 'hash', xhash)
	xphone = input(green+"[+] Número de telefone: "+red)
	cpass.set('cre', 'phone', xphone)
	setup = open('config.data', 'w')
	cpass.write(setup)
	setup.close()
	print(green+"[+] Configuração concluída!")

def merge_csv():
	import pandas as pd
	import sys
	banner()
	file1 = pd.read_csv(sys.argv[2])
	file2 = pd.read_csv(sys.argv[3])
	print(green+'[!] Fundindo '+sys.argv[2]+' & '+sys.argv[3]+' ...')
	print(green+'[!] Arquivos grandes podem demorar um pouco')
	merge = file1.merge(file2, on='username')
	merge.to_csv("output.csv", index=False)
	print(green+'[!] Arquivo salvo como "output.csv"\n')

def update_tool():
	import requirements as r
	banner()
	source = r.get("https://raw.githubusercontent.com/oDeskrin/Scrapper/master/.image/.version")
	if source.text == '3':
		print(green+'[!] Versão mais recente')
	else:
		print(green+'[!] Removendo arquivos antigos...')
		os.system('rm *.py');time.sleep(3)
		print(green+'[!] Solicitando arquivos novos...')
		os.system("""
			curl -s -O https://raw.githubusercontent.com/oDeskrin/Scrapper/master/add.py
			curl -s -O https://raw.githubusercontent.com/oDeskrin/Scrapper/master/scrapper.py
			curl -s -O https://raw.githubusercontent.com/oDeskrin/Scrapper/master/setup.py
			curl -s -O https://raw.githubusercontent.com/oDeskrin/Scrapper/master/sms.py
			chmod 777 *.py
			""");time.sleep(3)
		print(green+'\n[!] Envio completo\n')

try:
	if any ([sys.argv[1] == '--config', sys.argv[1] == '-c']):
		print(green+'[+] selecione o módulo: '+red+sys.argv[1])
		config_setup()
	elif any ([sys.argv[1] == '--merge', sys.argv[1] == '-m']):
		print(green+'[+] selecione o módulo: '+red+sys.argv[1])
		merge_csv()
	elif any ([sys.argv[1] == '--update', sys.argv[1] == '-u']):
		print(green+'[+] selecione o módulo: '+red+sys.argv[1])
		update_tool()
	elif any ([sys.argv[1] == '--install', sys.argv[1] == '-i']):
		requirements()
	elif any ([sys.argv[1] == '--help', sys.argv[1] == '-h']):
		banner()
		print("""$ python3 setup.py -m file1.csv file2.csv
			
	( --config  / -c ) configuração da API
	( --merge   / -m ) fundir dois arquivos em usuarios em um
	( --update  / -u ) atualizar para ultima versão
	( --install / -i ) instalar requisitos
	( --help    / -h ) mostrar ajuda
			""")
	else:
		print('\n'+red+'[!] Argumento desconhecido'+ sys.argv[1])
		print(green+'[+] Para ajuda use: ')
		print(green+'$ python3 setup.py -h'+'\n')
except IndexError:
	print('\n'+red+'[!] Nenhum argumento dado'+ sys.argv[1])
