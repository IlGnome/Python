import requests
import random
from cloudbot import hook

FuckOffList = [	'donut',
		'bus',
		'chainsaw',
		'king',
		'madison',
		'gfy',
		'back',
		'keep',
		'name',
	      	'bday',
	       	'dalton',
	       	'ing',
	       	'nugget',
	       	'outside',
	       	'off',
	       	'problem',
	       	'shakespeare',
	       	'think',
	       	'thinking',
	       	'xmas',
	       	'yoda',
	       	'you'
	       		]

headers = {'Accept' : 'text/plain'}

@hook.command('fos','fuckoff','foaas')
def foaas(text, nick, message):
	Fuckee = text.strip()
	Fucker = nick

	r = requests.get('http://www.foaas.com/' + str(random.choice(FuckOffList)) + '/' + Fuckee + '/' + Fucker, headers=headers)
	out = r.text
	message(out)
