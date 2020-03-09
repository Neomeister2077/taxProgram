#! /usr/bin/python3

# PURPOSE: Application which extracts financial information from deliveroo 
# 	   invoices and returns total amount made, total in tips and total paid
#	   in transaction fees from the invoices in the CWD

# USAGE: 

# Tax year 18/19 dates  - 6/4/18 - 5/4/19
import os, PyPDF2, re

# Get a list of all files in directory

path = "/home/snake_charmer/scripts/invoices/"

pdfName = os.listdir(path)

# Step 1: Open PDF
counter = 0
finalTotal = 0
finalTips = 0
finalTrans = 0
# Iterate through each PDF
for i in pdfName:
	# Open and extract text from each PDF
	pdfObj = open(path + i, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfObj)
	pageObj = pdfReader.getPage(0)
	pdfText = pageObj.extractText()


	# Regex for total earnings incuding tips and minus transaction fees 
	totalRegex = re.compile(r'Fees\s£[0-9]+\.[0-9]+')
	# Extracts only the numbers from previous regex so they can be added
	refinedTotalRegex = re.compile(r'[0-9]+\.[0-9]+')
	# Regex for tips
	tipsRegex = re.compile(r'Tips\s£[0-9]+\.[0-9]+')
	# Extracts only the numbers from previous regex so they can be added
	refinedTipsRegex = re.compile(r'[0-9]+\.[0-9]+')
	# Transaction fees regex
	transRegex = re.compile(r'\s£\-0.50')
	# Extracts only the numbers from previous regex so they can b e added
	refinedTransRegex = re.compile(r'0.50')

	# Search for totals and assign them to 'totalResult'
	mo1 = totalRegex.search(pdfText)
	totalResult = mo1.group()
	# Search for only the numbers in 'totalResult'
	mo2 = refinedTotalRegex.search(totalResult)
	refinedTotalResult = mo2.group()
	# Search for tips and assign to 'tipsResult'
	try:
		mo3 = tipsRegex.search(pdfText)
		tipsResult = mo3.group()
	except AttributeError:
		pass
	# Search for only numbers in 'tipsResult'
	mo4 = refinedTipsRegex.search(tipsResult)
	refinedTipsResult = mo4.group()
	#counter += 1
	# Search for transaction fees and assign to 'transResult'
	try:
		mo5 = transRegex.search(pdfText)
		transResult = mo5.group()
		#print(transResult)
	except AttributeError:
		#print('No Results')
		transResult = ''
		#pass
	# Search for only numbers in 'transResult'
	try:
		mo6 = refinedTransRegex.search(transResult)
		refinedTransResult = mo6.group()
		#print(refinedTransResult)
	except (NameError, AttributeError) as e:
		pass
		#print('No transaction fee')
	counter += 1


	# Convert refined regex results to float to be added
	convertedTotal = float(refinedTotalResult)
	convertedTipsTotal = float(refinedTipsResult)
	try:
		convertedTransTotal = float(refinedTransResult)
	except NameError:
		pass
	# Add up all the totals extracted from the PDFs
	finalTotal += convertedTotal
	finalTips += convertedTipsTotal
	try:
		finalTrans += convertedTransTotal
	except NameError:
		pass
	actualTotal = round(finalTotal + finalTips - finalTrans, 2)
	actualTotal1 = round(finalTotal + finalTips + finalTrans, 2)
	#print(totalResult)
	#print('Refined Total: ' + refinedTotalResult)
	#print(round(finalTotal, 2))
	#print('Count: ' + str(counter))
	#print('Tips: ' + tipsResult)
	#print('Refined Tips: ' + refinedTipsResult + '\n\n**********')
	#print('Tip total: ' + str(finalTips))

	#print(pdfText + "\n\n\n")
	#print(i)

print('Number of Invoices: ' + str(counter) + '\n')
print('Fees Total: £' + str(round(finalTotal, 2)) + '\n')
print('Tips Total: £' + str(round(finalTips, 2)) + '\n')
print('Transaction Fees Total: £' + str(round(finalTrans, 2)) + '\n\n*********\n')
print('Total + tips: £' + str(actualTotal))
print('Total + tips + Transaction fees: £' + str(actualTotal1))


# Non prog reminder: Remember to go back and get the values from
# the very first invoice as the total falls before and after start 
# date


