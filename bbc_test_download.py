import cloacina
import json
import glob
import csv
import datetime
from multiprocessing import Pool

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
    sourcefile = open(whitelist_file, 'r').read().splitlines()
    sourcelist = [line.split('\t') for line in sourcefile]
    print sourcelist
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

print sourcelist
print type(sourcelist)

pool = Pool(pool_size)

def download_source(source):
    if len(source) != 3:
        logger.warning("Source doesn't have three columns: ({0})".format(source))
        pass
    date_list = make_datelist(source[1], source[2])
    try:
        source_dict[source[0]]
    except KeyError:
        logger.warning("Source name ({0}) not in source dictionary.".format(source[0]))
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

for source in sourcelist:
   download_source(source)

#results = [pool.apply_async(download_source, (source)) for source in
#        sourcelist]

# This is diagnostic stuff and will be switched out with the Mongo connector
# for production.
print "Number of stories: ",
print len(big_stories)
print "Number of stories with padding errors: ",
print len(big_junk)
print big_stories[12]
with open('bbc_stories.json', 'w') as outfile:
    json.dump(big_stories, outfile)
