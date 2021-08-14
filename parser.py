#!/usr/bin/python3

# Parses the PDF files from the Wayback Machine in the ./dxcc folder.
# You must create and populate the dxcc folder first with downloader.py.
# By Mike Coffey KJ4Z, 14 August 2021

# Note that this lazily makes use of the CLI version of pdfminer (pdf2txt.py)
# Install it with `pip3 install pdfminer`

import subprocess
import pymysql
from dateutil.parser import parse
import os


conn = pymysql.connect(
        host='1.2.3.4', # Your MySQL Server
        user='user',  # Your MySQL User
        password = "password", # Your MySQL Password
        db='dxcc', # Your MySQL DB Name
        )
cur = conn.cursor()

for filename in os.listdir('dxcc'):
    if filename.endswith('.pdf') and 'A4' in filename: # Only parses the 'A4' files.  You could put 'USLetter' here instead, or just read them all.
        print(filename)

        result = subprocess.run(['pdf2txt.py', 'dxcc/' + filename], stdout=subprocess.PIPE)
        data = result.stdout.decode('utf-8') # Load the whole file into memory.  Not memory efficient but very programmer efficient
        lines = data.split("\n") # Split into lines so we can process them one by one.
        enable = 0 # This will remain 0 till we read past the document header
        previous_line_date = 0 # Was the previous line a date footer?
        dxcc_count = 0 # Which section of the file are we in?
        report_date = '' # Date as determined in the date footer
        mode = 'Mixed' # Start out with Mixed

        for line in lines:
            if "DXCC Honor Roll -" in line: # Read ahead to the first footer, extract the date, then start back at the beginning of the file again
                date = line.split('-')[2].strip()
                report_date = parse(date)
                print(report_date)
                break

        for line in lines:
            if enable == 1: # If still 0, we haven't reached the end of the file header
                if line.strip() == "":
                    pass
                    # do nothing, it's a blank line
                elif "DXCC FAQ" in line:
                    # do nothing, it's another useless recurring line
                    pass
                elif "ARRL DXCC - Honor Roll" in line:
                    # do nothing.  This line signifies the change to a new mode, but we determine that separately so this is useless.
                    pass
                elif "DXCC Honor Roll -" in line:
                    # This is a line containing the report date.  The next line is always a page number that we need to discard.
                    previous_line_date = 1
                elif "Digital" == line.strip():
                    # We're changing over to Digital mode now
                    mode = 'Digital'
                elif "Phone" == line.strip():
                    # We're changing over to Phone mode now
                    mode = 'Phone'
                elif "CW" == line.strip():
                    # We're changing over to CW mode now
                    mode = 'CW'
                else:
                    # It's not one of the above cases, so it's either a page number, an entity count header, or a callsign
                    if previous_line_date == 1:
                        # It's a page number.  Ignore it.
                        previous_line_date = 0
                    elif line.isnumeric():
                        # It's an entity count header.  Capture that.
                        dxcc_count = line
                    else:
                        # It's a callsign.
                        call = line.strip()

                        if int(dxcc_count) > 0:
                            # This truncates calls like AA1A/F5 to just AA1A, because I am lazy and so is ARRL.
                            elements = call.split('/')
                            total_count = elements[len(elements)-1].strip()
                            call = elements[0]

                            print(report_date, mode, dxcc_count, total_count, call)


                            sql = "INSERT INTO dxcc_hr(report_date,dxcc_count,callsign,mode,total_count,filename) VALUES ('%s','%s','%s','%s','%s','%s')" % (report_date, dxcc_count, call, mode, total_count, filename)
                            cur.execute(sql)
            if "ARRL DXCC FAQ" in line: # We've reached the end of the file header (or possibly even further, but that doesn't matter)
                enable = 1
            
        conn.commit() # Commit everything to the database