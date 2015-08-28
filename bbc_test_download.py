import lexikon

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("username", help="username")
parser.add_argument("password", help="password")

args = parser.parse_args()
USERNAME = args.username
PASSWORD = args.password

source_dict = {
    "New York Times":"6742",
    "BBC Monitoring":"10962",
    "AFP":"10903",
    "AllAfrica":"361826",
    "Australian Associated Press":"160586",
}

authToken = lexikon.authenticate(USERNAME, PASSWORD)
print authToken

big_stories = []
big_junk = []


date_list = ["2015-08-01", "2015-08-02", "2015-08-03", "2015-08-04", "2015-08-05", "2015-08-06", "2015-08-07", "2015-08-08", "2015-08-09", "2015-08-10"]
for d in date_list:
    total = lexikon.get_source_day_total("BBC Monitoring", d, authToken)
    total = total[0]
    output = lexikon.download_day_source("BBC Monitoring", d, total, authToken)
    big_stories.extend(output['stories'])
    big_junk.extend(output['junk'])

print "Number of stories: ",
print len(big_stories)
print "Number of stories with padding errors: ",
print len(big_junk)
print big_stories[12]
