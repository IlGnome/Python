# import ALL the modules?
# Writen for python 2.7
# Updated for python 3.x


import requests
import xml.etree.ElementTree as ET
import datetime
import sys
import xlrd
import csv



def file_len(filename):
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines 
    

def JKSelection(FuckThisShit):
	if JackknifeSelection == "B" or JackknifeSelection == "b" or JackknifeSelection == "Bastion" or JackknifeSelection == "bastion":
		
		return bastionJK
	elif JackknifeSelection == "R" or JackknifeSelection == "r":
		
		return RTC
 
bastionJK = "https://jackknife.thebastion.info"
RTC = "http://www.ridetheclown.com/eveapi/audit.php"


rawdata = input("Input workbook: ")

OutPut = input("Output file name: ")

Selection = False

while Selection == False:
	JackknifeSelection = input("[B]astion or [R]ide the clown jackknife?: ")
	if JackknifeSelection == "B" or JackknifeSelection == "b" or JackknifeSelection == "Bastion" or JackknifeSelection == "bastion":
		JKSelection(JackknifeSelection)
		Selection = True
		print("Using Bastion's Jackknife Service")
	elif JackknifeSelection == "R" or JackknifeSelection == "r":
		JKSelection(JackknifeSelection)
		Selection = True
		print("Using Ride The Clown")
	else:
		print("Please select a valid Choice, [B], or [R]")


workbook = xlrd.open_workbook(rawdata)
worksheet = workbook.sheet_by_index(0)




# Used incase I need them someplace else


invalid = "Invalid"
unsubbed = "Unsubscribed"
subbed = "Subscribed"


# counters for the while loop below
number = 0
rowcount = 0

OutNumber = 1


f = open(OutPut, 'w')

LastRow = int(file_len(rawdata))

while LastRow > rowcount: 
#this whole while loop is pretty slow. Look into ways to speed it up?
# or keep it so as to NOT hammer the CCP api servers?	
# Not like CCP really cares about the API anyway :-/

	print("We're currently on row \033[92m{}\033[0m of {}".format(OutNumber, LastRow))


#list to be manipulated by code further down
# list will be wiped each iteration
	APIKEYS = []

# This bit calls the worksheet defined above.
	APIK = str(int(worksheet.cell(number, 0).value))
	vCode = worksheet.cell(number, 1).value
	
# Counters used for worksheet progression
	number += 1
	rowcount += 1
	OutNumber = OutNumber + 1
# Gets the API info. maybe put it into a function? look into away to make the link dynamic
# Making the API calls a function is not going well
	payload = {'keyID': APIK, 'vCode': vCode}
	r = requests.get("http://api.eveonline.com/account/AccountStatus.xml.aspx", params=payload)
	headers = {'gnome-terminal': 'Document your fucking API, CCP'}
	root = ET.fromstring(r.text)
	result = root.find("result") #If this bit isn't here, the elif statement below breaks
	
# Use the menu options from Batch-API-Checker.py to automate this.
	Bknife = {'usid': APIK, 'apik' : vCode}
	BK = requests.get(str(JKSelection(JackknifeSelection)), params=Bknife)

# this part, while sloppy, will allow me to get the names on the account
	
	payload = {'keyID': APIK, 'vCode': vCode}
	r2 = requests.get("https://api.eveonline.com/account/Characters.xml.aspx", params=payload)
	headers = {'gnome-terminal': 'Document your fucking API, CCP'}
	root2 = ET.fromstring(r2.text)
	result2 = root2.find("result") 



#breaking the append statements to multiple lines gives me a cleaner looking list/code
	if root.findall('error'): #Checks the XML API for the <error> row
		for derp in range(3):
			APIKEYS.append("No Characters"),	
			APIKEYS.append(APIK),
			APIKEYS.append(vCode),
			APIKEYS.append(invalid) # Tells me if the API key is good or not
		
			# There might be a better way to handle this formatting wise.
#finds and compares 'paidUntil' with current date			
#If paidUntil is > datetime.datetime.now() (current date) then the account is active
	elif result.findtext('paidUntil') > str(datetime.datetime.now()): 
		AppendCount1 = 0
		for child in result2.iter('row'):
			APIKEYS.append(child.attrib['name'],)
			AppendCount1 += 1
		for pleasework in range(3 - AppendCount1):
			APIKEYS.append(' ')	
		APIKEYS.append(APIK),
		APIKEYS.append(vCode),
		APIKEYS.append(subbed)
		APIKEYS.append(BK.url)

	else:
		#This bit will still return all of the information, but is used for unsubscribed accounts
		AppendCount2 = 0
		for child in result2.iter('row'):
			APIKEYS.append(child.attrib['name'],)
			AppendCount2 += 1
		for pleasework in range(3 - AppendCount2):
			APIKEYS.append(' ')
		APIKEYS.append(APIK),
		APIKEYS.append(vCode),
		APIKEYS.append(unsubbed)

		APIKEYS.append(BK.url)
	
	f.write(','.join(APIKEYS)+'\n')  # where data is a list


f.close()





