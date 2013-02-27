

import re
import subprocess
from datetime import datetime
from datetime import timedelta
from pprint import pprint  # DEBUG

import numpy as np
import matplotlib.pyplot as plt


FMT = '%H:%M'
BAR_WIDTH = 2

ranges = []
data = []


# Public: Takes a list of strings, removes all empty strings from it and
# returns the result as list of strings.
#
# strings - List of strings
#
# Examples
#
#   purify(['ab', '', 'cd', 'ef', '', 'gh])
#   # => ['ab', 'cd', 'ef', 'gh]
#
# Returns a list of strings with length > 0.
def purify(strings):
    return [x for x in strings if x]


# Get the time data

process = subprocess.Popen('last', shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
for line in process.stdout.readlines():
    if re.search('^reboot', line):
        # Get the date
        date = re.split('Mon|Tue|Wed|Thu|Fri|Sat|Sun', line)[1]
        date = purify(re.split('\s', date))
        # 2, 4
        ranges.append([date[2], date[4]])
# pprint(ranges)


for range in ranges:
    diff = datetime.strptime(range[1], FMT) - datetime.strptime(range[0],
                                                                FMT)
    data.append(diff.seconds)



# Plot

fig = plt.figure()
ax = fig.add_subplot(111)

pprint(data)  # DEBUG

# ax.hist(data, normed=1, facecolor='red', alpha=.75)

for i, data_point in enumerate(data):
    ax.bar(i * BAR_WIDTH, data_point, width=BAR_WIDTH, alpha=.50)
    # Add text to the top of each bar
    # ax.text(i * BAR_WIDTH, data_point, str(data_point) + ' sec.',
    #         rotation='vertical')

# Set the labels
plt.xticks(np.arange(len(data)) * BAR_WIDTH, data, rotation=75,
           size='small', color='#343434')


plt.show()

