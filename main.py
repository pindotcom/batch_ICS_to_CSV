import os
import csv
from icalendar import Calendar

def convert_ics_to_csv(file):
    # parse the ics file
    with open(file, 'rb') as f:
        calendar = Calendar.from_ical(f.read())
    
    # create a list to store the calendar events
    events = []
    
    # loop through the calendar components and extract the events
    for component in calendar.walk():
        if component.name == "VEVENT":
            event = {}
            event["summary"] = component.get("summary")
            event["start"] = component.get("dtstart").dt
            event["end"] = component.get("dtend").dt
            events.append(event)
    
    # write the events to a csv file
    filename = os.path.splitext(file)[0] + ".csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["summary", "start", "end"])
        writer.writeheader()
        writer.writerows(events)
    
    return events

# get all the ics files in the downloads directory
downloads_dir = os.path.expanduser("~/Downloads/cal")
files = [f for f in os.listdir(downloads_dir) if f.endswith(".ics")]

# create a list to store all the events
all_events = []

# convert each ics file to csv and add its events to the all_events list
for file in files:
    events = convert_ics_to_csv(os.path.join(downloads_dir, file))
    all_events += events

# write all the events to a single csv file
with open("all_events.csv", 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["summary", "start", "end"])
    writer.writeheader()
    writer.writerows(all_events)
