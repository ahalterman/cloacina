import cloacina
import json
import glob
import csv
import datetime
from multiprocessing import Pool

logger = None

ln_user, ln_password, db_collection, whitelist_file, pool_size, log_dir, log_level, auth_db, auth_user, auth_pass, db_host = cloacina.parse_config()

# maybe read this in from a JSON?
source_dict = {
    "New York Times":"6742",
    "BBC Monitoring":"10962",
    "AFP":"10903",
    "AllAfrica":"361826",
    "Australian Associated Press":"160586",
}

authToken = cloacina.authenticate(ln_user, ln_password)

big_stories = []
big_junk = []

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


def make_date_source_list(source):
    start = datetime.datetime.strptime(source[1], '%Y-%m-%d')
    end = datetime.datetime.strptime(source[2], '%Y-%m-%d')
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    date_list = [i.strftime("%Y-%m-%d") for i in date_generated]
    source_list = [[source[0], date] for date in date_list]
    return source_list

sourcelist = [make_date_source_list(source) for source in sourcelist] # apply to each source
sourcelist = [item for sublist in sourcelist for item in sublist] # flatten list of lists. there has to be a neater way.
logger.info("Source list: {0},".format(sourcelist))
 

def download_wrapper(source):
    # there's some global ugliness going on here. specifically, authToken
    output = cloacina.download_day_source(source[0], source[1], source[2], authToken)
    # We can't add this to the same global list because that doesn't work with
    # multiprocessing
    #print output

pool = Pool(pool_size)

totals = [pool.apply_async(cloacina.get_source_day_total, (source[0], source[1], authToken)) for source in sourcelist]
totals = [r.get(9999999) for r in totals]
totals = [int(item) for sublist in totals for item in sublist] # again with the crappy de-nesting
print totals

# add the totals in a third "column" to the sourcelist
# maybe a better way to do this is to have the totals function take in a list
# and add the totals in the same function.
for i, source in enumerate(sourcelist):
    source.append(totals[i])

# This doesn't actually do anything yet--handle the output in the
# download_wrapper funtion.
pool.map(download_wrapper, sourcelist)

# This is diagnostic stuff and will be switched out with the Mongo connector
# for production.
print "Number of stories: ",
print len(big_stories)
print "Number of stories with padding errors: ",
print len(big_junk)
print big_stories[12]
with open('bbc_stories.json', 'w') as outfile:
    json.dump(big_stories, outfile)
