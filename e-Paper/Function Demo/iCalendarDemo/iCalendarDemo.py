from ics import Calendar
import requests
import arrow
import os

def addProdId(data: str) -> str:
    lines = data.splitlines()
    lines.insert(1, 'PRODID:-//Unknown//NONSGML v1.0//EN')
    return '\n'.join(lines)

def main():
    urlsFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'calUrls.cfg')
    if os.path.exists(urlsFile):
        with open(urlsFile, 'r') as urlsData:
            iCals = urlsData.read().splitlines()
    print(iCals)
    for url in iCals:
        icsData = requests.get(url).text
        if icsData.find('PRODID')==-1:
            icsData = addProdId(icsData)
        cal = Calendar(icsData)
        events = cal.events
        events = sorted(events)
        for event in events:
            if event.begin>=arrow.now():
                print(event.begin, event.name)
        print('-----')

if __name__=='__main__':
    main()
