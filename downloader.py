#!/usr/bin/python3

# Downloads the files in archives.json from the Wayback Machine to the ./dxcc folder.
# You must create the dxcc folder first.
# By Mike Coffey KJ4Z, 14 August 2021

import json
from random import randint
from time import sleep
import requests
import os.path
from os import path

with open('archives.json') as json_file:
    data = json.load(json_file)
    for report in data:
        url = report[0]
        timestamp = report[2]
        filename = url.split('/')
        if len(filename) > 6: # Sanity check
            filename = filename[6]
        if "HR" in filename: # Only bother downloading the "HR" files.  Adjust this if you care about something else.

            dl_url = 'https://web.archive.org/web/' + timestamp + '_if/' + url # Not 100% sure this always leads to a valid file.  Likely source of failed downloads
            print(dl_url)

            if path.exists('dxcc/' + filename):
                print(filename + 'already downloaded')
            else:
                try:
                    r = requests.get(dl_url, allow_redirects=True)
                    open('dxcc/' + filename, 'wb').write(r.content)
                except:
                    print('Failed to download' + filename)
                    pass

                sleep(randint(10,30)) # Sleep a random number of seconds between 10 and 30, to be a nice guest on the Wayback Machine and also to not get banned