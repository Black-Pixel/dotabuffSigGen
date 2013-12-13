import sys
import urllib2
import re
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import cStringIO

i = 1

while(i < len(sys.argv)):
  
	#Build URL
	userid = sys.argv[i]
	url = "http://dotabuff.com/players/"+userid

	#Get the profile page from the URL
	buffer = urllib2.urlopen(url)
	html = buffer.read()
	buffer.close()

	#Get the username
	pattern = "<div class=\"content-header-title\"><h1>(.+)</h1>"
	compiled = re.compile(pattern)
	ms = compiled.search(html)
	name = u""+(ms.group(1).decode('utf-8')).lower() #UFT-8 needed for umlauts

	#Get the avatar
	pattern = "data-tooltip-url=\"/players/"+userid+"/tooltip\"\srel=\"tooltip-remote\"\ssrc=\"(http://media.steampowered.com/steamcommunity/public/images/avatars/\w+/\w+_full.jpg)\"\stitle="
        compiled = re.compile(pattern)
        ms = compiled.search(html)
        avatarURL = ms.group(1)
        avatarRAW = Image.open(cStringIO.StringIO(urllib2.urlopen(avatarURL).read()))

	#Get most played heroes
        pattern = "rel=\"tooltip-remote\" src=\"(/assets/heroes/\S+-\w+.png)\"\stitle="
        compiled = re.compile(pattern)
        ms = compiled.findall(html)
	
	#Get the images of the four most played heroes
	j = 0
	for m in ms:
		if (0 == j):
			mph1URL = "http://dotabuff.com"+m
		elif (1 == j):
			mph2URL = "http://dotabuff.com"+m
		elif (2 == j):
			mph3URL = "http://dotabuff.com"+m
		elif (3 == j):
			mph4URL = "http://dotabuff.com"+m
		elif (j > 3):
			break
		j = j + 1
	
	mph1RAW = Image.open(cStringIO.StringIO(urllib2.urlopen(mph1URL).read()))
	mph2RAW = Image.open(cStringIO.StringIO(urllib2.urlopen(mph2URL).read()))
	mph3RAW = Image.open(cStringIO.StringIO(urllib2.urlopen(mph3URL).read()))
	mph4RAW = Image.open(cStringIO.StringIO(urllib2.urlopen(mph4URL).read()))

	#Get the number of won matches
	pattern = "<span class=\"won\">(\S+)</span>"
	compiled = re.compile(pattern)
	ms = compiled.search(html)
	won = ms.group(1)

	#Get the number of lost matches
	pattern = "<span class=\"lost\">(\S+)</span>"
	compiled = re.compile(pattern)
	ms = compiled.search(html)
	lost = ms.group(1)

	#Set up fonts with UFT-8/Unicode encoding
	font = ImageFont.truetype("Constantia.ttf",18, encoding="unic")
	font2 = ImageFont.truetype("DejaVuLGCSansMono.ttf",18, encoding="unic")
	
	#Open background image
	img = Image.open("background.png")
	draw = ImageDraw.Draw(img) 

	#Resize avatar
	avatar = avatarRAW.resize((80,80), Image.ANTIALIAS)
	
	#Resize most played heroes images
	mph1 = mph1RAW.resize((75,42), Image.ANTIALIAS)
	mph2 = mph2RAW.resize((75,42), Image.ANTIALIAS)
	mph3 = mph3RAW.resize((75,42), Image.ANTIALIAS)
	mph4 = mph4RAW.resize((75,42), Image.ANTIALIAS)

	#Paste background, avatar and most played heroes images
	img.paste(avatar, (21,5))
        img.paste(mph1, (124,10))
	img.paste(mph2, (204,10))	
	img.paste(mph3, (284,10))
	img.paste(mph4, (364,10))

	#Draw text onto the image
	draw.text((124, 60),"Won:",(255,255,255),font=font2)
	draw.text((284, 60),"Lost:",(255,255,255),font=font2)
	draw.text((18, 95),name,(255,255,255),font=font)
	draw.text((169, 60),won,(0,164,27),font=font2)
	draw.text((344, 60),lost,(164,0,0),font=font2)

	#Set save path and name
	imagename = "signature/" + userid + ".png"
	#Save image
	img.save(imagename)

	i = i + 1
