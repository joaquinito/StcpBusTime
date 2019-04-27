#!/usr/bin/python3

import re
import tkinter
import urllib.request
from bs4 import BeautifulSoup

STCP_SERVER_URL_SARDOAL_STOP = "http://www.stcp.pt/pt/itinerarium/soapclient.php?codigo=SRD2"

busNumberRegex = re.compile(r'\d{1,3}')
destinationRegex = re.compile(r'[a-zA-Z\-\.]+')

def getBusInfo():
    htmlObject = urllib.request.urlopen(STCP_SERVER_URL_SARDOAL_STOP)
    # Get text, decode from utf-8
    htmlFile = htmlObject.read().decode(htmlObject.headers.get_content_charset())
    soup = BeautifulSoup(htmlFile, 'html.parser')

    # Find HTML table with results
    table = soup.find(id='smsBusResults')
    # Get all rows of the table
    rows = table.find_all('tr')

    busData = []
    for row in rows[1:]:
        #Get all elements in the row
        cells = row.find_all('td')
        cells = [cell.text.strip() for cell in cells]
        #Add to our busData table
        busData.append([cell for cell in cells])

    for row in busData:
        busNumber = busNumberRegex.search(row[0])
        destination = destinationRegex.findall(row[0])
        row[0] = busNumber.group() + " " + ' '.join(destination)

    return busData

class TkWindow:

    gui = tkinter.Tk()

    def __init__(self):
        self.gui.winfo_toplevel().title("STCP - SARDOAL 2")
        label_1 = tkinter.Label(self.gui, text="Bus")
        label_2 = tkinter.Label(self.gui, text="Arrival")
        label_3 = tkinter.Label(self.gui, text="Waiting time")
        label_1.grid(row=0, column=0, padx=20)
        label_2.grid(row=0, column=1, padx=20)
        label_3.grid(row=0, column=2, padx=20)

    def updateSchedules(self):
        busData = getBusInfo()
        i = 0
        for row in busData:
            label_4 = tkinter.Label(self.gui, text=busData[i][0])
            label_5 = tkinter.Label(self.gui, text=busData[i][1])
            label_6 = tkinter.Label(self.gui, text=busData[i][2])
            label_4.grid(row=i+1, column=0, padx=20, pady=3)
            label_5.grid(row=i+1, column=1, padx=20, pady=3)
            label_6.grid(row=i+1, column=2, padx=20, pady=3)
            i+=1
        self.gui.after(10000, self.updateSchedules)

    def mainloop(self):
        
        self.gui.mainloop()

root = TkWindow()
root.updateSchedules()
root.mainloop()



