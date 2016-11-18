### This script uses python 2.7
### Enter character names and it will compare the corp history of the two characters.
### It isn't perfect so it will hit duplicates. For now.
### Lines commented out are mostly for debugging

import requests
import xml.etree.ElementTree as ET
import csv
import sys



CharacterNamesArray = [] #The Array for the character's names


PrintToFile = raw_input("Do you want to save to file? [y/n]: ") #What we use to make the CSV
if PrintToFile == 'y':
	FileName = raw_input("Name of file? (output will be as a .csv) ")
	FileName = FileName + '.csv'
	FileToSave = open(FileName, 'w')


CharacterNamesArray.append(raw_input("Enter Character's Name: ")) 
CharacterNamesArray.append(raw_input("Enter Second Character's Name: "))


#Char1 is the name of the first character, Char 2 is the second
#This will store the corp names and start dates in two arrays to make it easier to parse later
Char1corp = [] 
Char1StartDate = []

Char2corp = []
Char2StartDate = []

Names = 0 # Sloppy counter for using the same code for both characters.

for CharacterNames in range(0, len(CharacterNamesArray)):
	
	payload = {'Names': CharacterNamesArray[Names]}
	r = requests.get("http://api.eveonline.com/eve/CharacterID.xml.aspx", params=payload)
	headers = {'gnome-terminal': 'If there are problems, find the IP of the person using it and beat them'}

	root = ET.fromstring(r.text)
	result = root.find("result")

	#row: the tag which is a child of result.
	#.attrib will look at the key:value pairs of the .tag

	for child in result.iter('row'):	
		if child.attrib['characterID'] != "0":
			payload = {"CharacterID": child.attrib['characterID']}
			r2 = requests.get("http://api.eveonline.com/eve/CharacterInfo.xml.aspx", params=payload)
			headers = {'gnome-terminal': 'Document your API CCP'}
			root2 = ET.fromstring(r2.text)
			result2 = root2.find("result")
			print r2.url
			
			if Names == 0:
				for child in result2.iter('row'):
					Char1corp.append(child.attrib['corporationName'])
					Char1StartDate.append(child.attrib['startDate'])
			else:
				for child in result2.iter('row'):
					Char2corp.append(child.attrib['corporationName'])
					Char2StartDate.append(child.attrib['startDate'])
			
	
		else:
			print "We could not find one of the characters. Please check your spelling and try again"
		
	Names += 1

# This is the part where we actually compare corporations.
ArrayCount = min(len(Char1corp), len(Char2corp))

ArrayLoopCount = ArrayCount - 1
HistoryArray = []
CharacterOne = len(Char1corp) - 1
CharacterTwo = len(Char2corp) - 1

CorpLooper = len(Char2corp) - 1
MatchCounter = 0
CorpLooper = CharacterTwo

for corps in range(len(Char1corp) , 0, -1):
	Status = Char1corp[CharacterOne]
	
	for checks in range(len(Char2corp), 0, -1):
		if Status == Char2corp[CorpLooper]:

			print "Matched corp with start dates %s" % Status, Char1StartDate[CharacterOne], Char2StartDate[CorpLooper]
			HistoryArray.append(Status)
			HistoryArray.append(Char1StartDate[CharacterOne])
			HistoryArray.append(Char2StartDate[CorpLooper])
			if PrintToFile == 'y':
				
				FileToSave.write(','.join(HistoryArray)+'\n')
				HistoryArray = []

		CorpLooper -= 1
	
	CharacterOne -= 1
	CorpLooper = len(Char2corp) - 1	


if PrintToFile == 'y':
	FileToSave.close()
