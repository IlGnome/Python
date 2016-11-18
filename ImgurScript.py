#python 3.x

import random
import requests
import json
import sys

# API key goes here.

headers = {'Authorization' : 'Client-ID Get Your Own'}

#Here there be counters.

#page = str(random.randrange(0, 5))
page = str(0)
SubSelection = sys.argv
NSFWStatus = ''
RandomSelector = False
RandomCounter = 0


try:
	SubReddit = str(SubSelection[1])
	pass
except:
	SubReddit = 'random'
# This is where the magic happens

if SubReddit == 'random': #On 'random' as an Argv it runs this line
	r = requests.get('https://api.imgur.com/3/gallery/random/random/' + page, headers = headers)
else: #Otherwise it looks for the subreddit asked for
	r = requests.get('https://api.imgur.com/3/gallery/r/'+ SubReddit +'/random/' + page, headers = headers)



ImgurPuke = r.json() #Have you seen the JSON response? It fits. It fits ALL JSON

PukeCount = 0
for link in ImgurPuke['data']:
	PukeCount += 1

try:	
	WhichPicture = random.randrange(0, PukeCount)
	pass
except ValueError:
	PukeCount = 1
	WhichPicture = random.randrange(0, PukeCount)
	pass

if SubReddit == 'random':
	while RandomSelector == False:
		try:
			PukeSelection = ImgurPuke['data'][WhichPicture]
			RandomSelector = True
			pass
		except IndexError:		
			sys.exit(1)
				#break
		

#This is for the subreddit specified pictures. It also catches the errors from above
try:
	PukeSelection = ImgurPuke['data'][WhichPicture]
	pass
except:
	print('\x02' + SubReddit + '\x02' + ' does not exist, does not contain images, or doesn\'t have a lot of pictures')
	sys.exit(1)

if PukeSelection['nsfw'] == True:
	NSFWStatus = '\x035 \x02NSFW\x02 \x03'

if PukeSelection['section'] == '':
	Where = 'Hell if I know'
else:	
	Where = PukeSelection['section']


# There has to be a better way to determine if something is a gif or not

try:
	PukeSelection['type'] == 'image\gif'
	picture = PukeSelection['mp4']
	pass
except KeyError:
	PukeSelection['is_album'] == True
	picture = PukeSelection['link']
	pass

#is.gd link
isgd = requests.get('https://is.gd/create.php?format=simple&url=' + 'https://api.qrserver.com/v1/create-qr-code/?data=' + picture + '&size=150x150')

#I'm really happy about this section.

print(NSFWStatus + 'From ' + '\x02' + Where + '\x02:' + ' Title \x02%s \x02 %s - \x02QR code\x02 %s' % (PukeSelection['title'], picture, isgd.text))
