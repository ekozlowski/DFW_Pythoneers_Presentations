# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Log Data Processor

# <markdowncell>

# Problem:  XML file processing is taking a long time, and we need to figure out why.
# 
# Approach:  Analyze the processing log to determine seconds per file in processing, and see if the time ranges correlate to running processes.

# <headingcell level=3>

# Import the modules we need, setup our pathing, read the first few lines of our file and see what we need to parse.

# <codecell>

import os
import datetime
import time

# Change to our data directory
os.chdir('/Users/e003070/notebook/')
lines = [x for x in open('./logfile.txt', 'r').readlines() if 'Processing' in x]
print len(lines)
print "first"
for l in lines[0:5]:
    print l
print "last"
for l in lines[-5:]:
    print l

# <headingcell level=3>

# Compile parsing pattern to extract date from data line above

# <codecell>

from parse import parse, compile
p = compile("{},{} process DEBUG {}")


# <headingcell level=3>

# Pick the day we're interested in.  
# (Could be any day between 2011 and 2014 (current))

# <codecell>

# Processing happens between 12am and 12pm daily.
# To view a day, just change the date below, and rerun the next two cells.

# yesterday
# view_date = datetime.datetime(2014, 2, 8)

# Problem days:
#view_date = datetime.datetime(2013, 12, 17)
# view_date = datetime.datetime(2013, 12, 16)
view_date = datetime.datetime(2013, 12, 15)
# view_date = datetime.datetiem(2013, 12, 14)

# We're only interested in midnight until noon on our processing day
begin = view_date.replace(hour=0, minute=0, second=0)
end = view_date.replace(hour=12, minute=0, second=0)

# <headingcell level=3>

# Mine the data to plot out of the log

# <codecell>

timestamps = []
seconds = []
prior_timestamp = None
for line in lines:
    result = p.parse(line)
    if not result: continue  # skip failing parses    
    date_and_time, toss1, toss2 = result
    current_timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_and_time, "%Y-%m-%d %H:%M:%S")))
    if current_timestamp < begin or current_timestamp > end: continue
    if prior_timestamp:
        delta = (current_timestamp - prior_timestamp).seconds
        if delta > 36000: 
            prior_timestamp = None
            continue  # we crossed day boundaries
        #print current_timestamp, delta
        timestamps.append(current_timestamp)
        seconds.append(delta)
    prior_timestamp = current_timestamp

# <headingcell level=3>

# Plot the data

# <codecell>

import matplotlib.pyplot as plt

from matplotlib import dates

hfmt = dates.DateFormatter("%m/%d %I:%M %p")

minutes_per_slice = 10  # 60 should be evenly divisible by this number to make the graph look "right" on the axis.

fig = plt.figure()
ax = fig.add_subplot(111)

# Set Axis Labels
ax.set_ylabel("Processing Seconds Per XML File")
ax.set_xlabel("Process Time Of Day")

# Format X-Axis dates
ax.xaxis.set_major_locator(dates.MinuteLocator(range(0,60,minutes_per_slice)))
ax.xaxis.set_major_formatter(hfmt)
plt.plot(timestamps, seconds)

plt.xticks(rotation=90)
plt.subplots_adjust(hspace=0, bottom=0.3)
plt.show()


# <codecell>


