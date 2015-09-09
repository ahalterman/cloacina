import cloacina
import json
import glob
import csv
import datetime

#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("username", help="username")
#parser.add_argument("password", help="password")
#
#args = parser.parse_args()
#USERNAME = args.username
#PASSWORD = args.password

logger = None

ln_user, ln_password, db_collection, whitelist_file, pool_size, log_dir, log_level, auth_db, auth_user, auth_pass, db_host = cloacina.parse_config()

source_dict = {
    "New York Times":"6742",
    "BBC Monitoring":"10962",
    "AFP":"10903",
    "AllAfrica":"361826",
    "Australian Associated Press":"160586",
}

authToken = cloacina.authenticate(ln_user, ln_password)
print authToken

big_stories = []
big_junk = []

# All this junk will be by source (i.e. by row) for now, which is actually useful for pooling later.
# But for now it'll only run on the first line of the source list csv.

try:
    sourcelist = open(whitelist_file, 'r').readlines()
    sourcelist = [line.replace('\n', '').split('\t') for line in
                     sourcelist if line]
    # Filtering based on list of sources from the config file
    # to_scrape = {listing[0]: [listing[1], listing[2]] for listing in sourcelist} <-- leave as list for now.
except IOError:
    print 'There was an error. Check the log file for more information.'
    logger.warning('Could not open URL whitelist file.')
    raise


def make_datelist(date1, date2):
    start = datetime.datetime.strptime(date1, '%Y-%m-%d')
    end = datetime.datetime.strptime(date2, '%Y-%m-%d')
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    date_list = [i.strftime("%Y-%m-%d") for i in date_generated]
    return date_list

#date_list = ["2015-08-01", "2015-08-02", "2015-08-03"]
#
for source in sourcelist:
    date_list = make_datelist(source[1], source[2])
    print type(source[0])
    print type(source[2])
    print "Scraping source {0} from {1} to {2}".format(source[0], source[1], source[2])
    for d in date_list:
        total = cloacina.get_source_day_total(source[0], d, authToken)
        if total:
            total = total[0]
            output = cloacina.download_day_source(source[0], d, total, authToken)
            big_stories.extend(output['stories'])
            big_junk.extend(output['junk'])
#
#for d in date_list:
#    total = cloacina.get_source_day_total("AFP", d, authToken)
#    total = total[0]
#    output = cloacina.download_day_source("AFP", d, total, authToken)
#    big_stories.extend(output['stories'])
#    big_junk.extend(output['junk'])
#



print "Number of stories: ",
print len(big_stories)
print "Number of stories with padding errors: ",
print len(big_junk)
print big_stories[12]
with open('bbc_stories.json', 'w') as outfile:
    json.dump(big_stories, outfile)
