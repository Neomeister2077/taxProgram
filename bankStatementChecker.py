#! /usr/bin/python3

# PURPOSE: Application used to check that the total obtained from 
# 	   the incoives program is correct by checking how much was 
#	   paid into the bank account from Deliveroo/Uber etc

# USAGE: Ensure the correct directory is set in the "path" variable then go nuts. You nut.

# Tax year 18/19 dates  - 6/4/18 - 5/4/19

import os, PyPDF2, re

# Get a list of all files in directory

path = "INSERT CORRECT DIRECTORY HERE"

pdfName = sorted(os.listdir(path))

counter = 0

rooTotal = []

uberTotal = []

for pdf in pdfName:
	# Open PDF and extract contents
	pdfObj = open(path + pdf, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfObj)
	numberOfPages = pdfReader.numPages
	counter += 1
	print('\n\n*****')
	print("PDF " + str(counter) + ": " + pdf)

	counter1 = 0
	while(counter1 < numberOfPages):
	# Iterate through each page in the PDF
		allRooFigures = []
		intRooFigures = []

		allUberFigures = []
		intUberFigures = []
		for page in range(numberOfPages):
			pageObj = pdfReader.getPage(page)
			pdfText = pageObj.extractText()
			# Create regex for Deliveroo fee payments
			rooPaymentRegex = re.compile(r'(BankcreditRoofoodsLimited)([0-9]+\.[0-9]+)')
			refinedRooPaymentRegex = re.compile(r'[0-9]+\.[0-9]{2}')

			# Create regex for Uber fee payments
			uberPaymentRegex = re.compile(r'UBERB\.V\.[0-9]+\.[0-9]{2}')
			refinedUberPaymentRegex = re.compile(r'[0-9]+\.[0-9]{2}')

			# Search the pdf text for Deliveroo regex
			mo = rooPaymentRegex.findall(pdfText)

			# Search the pdf for Uber regex
			mo1 = uberPaymentRegex.findall(pdfText)

			# Extract only the numbers for Deliveroo
			refinedRooResult = refinedRooPaymentRegex.findall(str(mo))

			# Extract only the numbers for Uber
			refinedUberResult = refinedUberPaymentRegex.findall(str(mo1))

			#Store result in a list
			#rooPageFigures = mo
			rooPageFigures = refinedRooResult
			# Loop through the results and add them to pdfList1
			for i in rooPageFigures:
				allRooFigures.append(i)
			# Convert all strings items in list to float
			intRooFigures = [float(i) for i in allRooFigures]

			uberPageFigures = refinedUberResult
			for i in uberPageFigures:
				allUberFigures.append(i)
			intUberFigures = [float(i) for i in allUberFigures]
			counter1 += 1
			#Note 24/01/2020: Refine the regex to use groups to 
			# 		   extract the numbers rather than
			#		   a 2nd regex before Uber part.

	# add up the list of deliveroo payments in a month and round to 2 decimal places
	rooMonthlyTotal = round(sum(intRooFigures), 2)

	# add up the list of uber payments in a month and round to 2 decimal places
	uberMonthlyTotal = round(sum(intUberFigures), 2)

	# Create a list of deliveroo monthly payments
	rooTotal.append(rooMonthlyTotal)

	# Create a list of Uber monthly payments
	uberTotal.append(uberMonthlyTotal)

	total = sum(rooTotal)
	uberFinalTotal = sum(uberTotal)
	# 1094.01 of the total will be picked up by the regex but is 
	# outside of the tax year dates so must be subtracted from the total
	actualTotal = total - 1094.01
	print('\n\n***')
	#print(rooTotal)
	print('\n\n***')
	#print('\n' + 'Deliveroo payments: ' + str(allRooFigures) + '\n')
	print('Uber payments: ' + str(allUberFigures) + '\n')
	print('Deliveroo total: ' + str(rooMonthlyTotal)+ '\n')
	print('Uber total: ' + str(uberFinalTotal) + '\n')
	print('Total: ' + str(actualTotal + uberFinalTotal))

