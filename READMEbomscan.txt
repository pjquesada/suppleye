******************************
******************************
** PROJECT BRAVO OSCAR MIKE **
**     BY PABLO QUESADA     **
**           2021           **
******************************
******************************
								
	
	Table of Contents
	----------------------
	
	1.	Introduction
	2.	Installation
	3.	Programs and Functions
	4.	File list and data structures
	5.	Bugs and fixes
	6.	Credits and acknowledgements
	
	
	
	
	
	Introduction
	------------
	
	This project is meant to create a database of parts and record pricing, stock, 
	and lead time information on each part. The project will update the database 
	with current information on each part and report if there is a change to its 
	price stock or lead time. 
	
	
	
	
	
	Installation
	------------
	
	To open and run the programs, Python 3.8 must be installed. Although optional, 
	PyCharm and DB Browser for SQLite can be installed to aid the visualization and
	execution of the programs and database.
	
	
	
	
	
	Programs and Functions
	----------------------
	
	
		a.	BOMScanner.py
			-------------
			
			The BOMScanner program reads in a BOM text file that is extracted from 
			a DSN file, it then record and queries each part listed in the BOM file
			against the OCTOpart API. Part information fetched from the OCTOpart 
			API is then stored in the database across tables. In order to execute 
			the program you must run the main in the BOMScanner program.
			
			
		b.	GraphQLClient.py
			----------------
			
			This program creates a class to interface with the API and to run 
			queries. It is used to register the API token.
			
			
		c.	octoqueries.py
			--------------
			
			This program contains the functions that create the queries to obtain 
			information from the OCTOpart API. The OCTOpart API can be queried 
			using a part's OCTOpart id to obtain part pricing, stock, and lead 
			time, if a part's OCTOpart id is not available. Part information can be
			obtained by first obtaining the OCTOpart id using its manufacturer part
			number and the mpn query.
			
			
		d.	BOMdb.py
			--------
			
			This program contains all functions that handle and interact with the 
			database. It includes a function to boot a database at a specific file 
			location, a method to add part information into the database, and 
			functions to query for information from the database. The function to 
			add part information into the database requires the part information to
			be inserted to be in a dictionary structure where the main key is the 
			Avionica part number (avpn), under each avpn key the second key is the 
			manufacturer part number (mpn), and under each mpn key the third key is
			the OCTOpart id (octoid). Within each octoid key are multiple keys such
			as manufacturer, seller, price, stock, and lead time (in days).
			
			
		e.	update_database_info.py
			-----------------------
			
			This program combines functions and utilizes other programs to create a
			function that extract each part from the database and runs a OCTOpart 
			query on each part and inserts the latest information on each part into
			the database.
			
			
		f.	cmp.py
			------
			
			This program detects any change in price, stock, or lead time for each 
			part in the database. The program queries the database for each part's 
			latest and earliest data and then compares each previous and latest 
			value and determines if there was a change. If a change is detected, 
			the program will send an alert in the form of an email with all parts 
			that have experienced a change in price, stock, or lead time.
			
			
		g.	alert.py
			--------
			
			This program creates a text and html message with data of parts that 
			have experenced a change in price, stock, or lead time as indicated. 
			The message field of the email is dependant on the user's input. Each
			email establishes recipients from a list of Avionica emails and uses 
			donotreply@avionica.com on an smtp server to send out each email.
			
			
		h.	get_critical_stock.py
			---------------------
			
			This program analyzes each avpn in the database and its corresponding 
			parts, if all the parts in the avpn have low stock then it is 
			determined to be a critically low avpn. The program then reports all of
			the avpns with critically low stock quantities in the form of an email.
	
	
	
	
	
	File list and data structures
	-----------------------------
	
		Critical files:
			•	BOMdatabase
				-----------
				
				The BOMdatabase file can be located in the SVN drive under the same 
				folder that Project Bravo Oscar Mike is in, called BOM Project. In 
				addition, a identical databse is provided for testing purposes and 
				is in the same file location as the BOMdatabase, but is named 
				BOMdatabaseTESTING.
				
		
		Optional files:
			•	LOGIC_BOARD.BOM.txt
				-------------------
				
				The LOGIC_BOARD.BOM.txt file shall be used as an example and guide 
				for processing and reading in part information extracted from the 
				BOM of the DSN file.
				
		
		Data structures
		---------------
			
			The data structure the programmer decides to use is optional and up to 
			the programmer, however the program uses a dictionary structure to 
			locally and momentarily store part information before it is added into 
			the database. The general data structure that is used is in the form of 
			nested dictionaries and formatted where the primary key is the Avionica 
			part number (avpn), within each avpn there is a dictionary whose key is 
			the manufacturer part number (mpn), within each mpn there is a 
			dictionary whose key is the OCTOpart id number (octoid), within each 
			octoid manufacturer, seller, price, stock, lead time, and description 
			data is stored under keys.
			
	
	
	
	
	
	Bugs and fixes
	----------
	
		•	There are certain parts, from the database, that the program cannot 
			obtain information from, this could be because not all avpns are 
			formatted the same way or it could be a problem with the sqlite3 query.
		
		•	The program is written to set a part's lead time to 9999 when the 
			OCTOpart query returns no lead time or "null". A different value should 
			be added to represent the spicific cases.
		
		•	The critical stock function can be improved.
		
	
	
	
	
	
	Credits and acknowledgements
	----------------------------
	
		I would like to thank Avionica, LLC, York Garcia, and the whole R&D team for
		allowing me to work on this project and for guiding me along the way and 
		pushing me to learn and do new things every day.
		
		Author
		•	Pablo Quesada
		
		Contributions:
		•	Amber Woods:
			Database structure, creation, and interfacing
		•	York Garcia:
			Code cleanup and optimization, bug fixes, data structure