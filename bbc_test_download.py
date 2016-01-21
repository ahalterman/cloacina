import cloacina
from cloacina import mongo_connection
import json
import glob
import csv
import datetime
from multiprocessing import Pool
from pymongo import MongoClient
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler("cloacina_run.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Writing logs to {0}".format("cloacina_run.log"))

ln_user, ln_password, db_collection, whitelist_file, pool_size, log_dir, log_level, auth_db, auth_user, auth_pass, db_host = cloacina.parse_config()

if db_host:
    connection = MongoClient(host=db_host)
else:
    connection = MongoClient()

db = connection.lexisnexis
collection = db[db_collection]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--user", help="LexisNexis username")
parser.add_argument("--password", help="Password for LexisNexis username")
parser.add_argument("--source", help="sourcename;start_yyyy-mm-dd;end_yyyy-mm-dd")

args = parser.parse_args()
ln_user = args.user
ln_password = args.password
source = [args.source]

print source

authToken = cloacina.authenticate(ln_user, ln_password)
if not authToken:
    logger.error("No auth token generated")
print authToken

#big_stories = []
#big_junk = []



#try:
#    sourcefile = open(whitelist_file, 'r').read().splitlines()
#    sourcelist = [line.split(';') for line in sourcefile]
#    print sourcelist
#    # Filtering based on list of sources from the config file
#    # to_scrape = {listing[0]: [listing[1], listing[2]] for listing in sourcelist} <-- leave as list for now.
#except IOError:
#    print 'There was an error. Check the log file for more information.'
#    logger.warning('Could not open URL whitelist file.')
#    raise

sourcelist = [line.split(';') for line in source] 

with open('source_name_id.json') as source_file:                                                                                                                                     
        source_dict = json.load(source_file)     

print "Sourcelist:",
print sourcelist
print "Scraping from source number {0}".format(source_dict[sourcelist[0][0]])


def make_date_source_list(source):
    if len(source) != 3:
        logger.warning("Source is not of length 3. Formatting problem? {0}".format(source))
    start = datetime.datetime.strptime(source[1], '%Y-%m-%d')
    end = datetime.datetime.strptime(source[2], '%Y-%m-%d')
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    date_list = [i.strftime("%Y-%m-%d") for i in date_generated]
    source_list = [[source[0], date] for date in date_list]
    return source_list

print "Un-nesting source list."
sourcelist = [make_date_source_list(source) for source in sourcelist] # apply to each source
sourcelist = [item for sublist in sourcelist for item in sublist] # flatten list of lists. there has to be a neater way.

if len(sourcelist) < 30:
    print sourcelist
if len(sourcelist) > 30:
    print sourcelist[0:30]
#logger.info(sourcelist)

def download_wrapper(source):
    # there's some global ugliness going on here. specifically, authToken
    try:
        output = cloacina.download_day_source(source[0], source[1], source[2], authToken)
        lang = 'english'
       
        mongo_error = []
        for result in output['stories']:
            try:
                entry_id = mongo_connection.add_entry(collection, result['news_source'],
                    result['article_title'], result['publication_date_raw'],
                    result['article_body'], lang, result['doc_id'])
            except Exception as e:
                mongo_error.append(e)
        if mongo_error:
            logger.warning("There were error(s) in the Mongo loading {0}".format(mongo_error))
    except Exception as e:
        logger.warning("Error downloading {0}: {1}".format(source, e))

pool = Pool(pool_size)
logger.info("Using {0} workers to get source-day totals.".format(pool_size))

totals = [pool.apply_async(cloacina.get_source_day_total, (source[0], source[1], authToken)) for source in sourcelist]
totals = [r.get(9999999) for r in totals]

logger.info("Here are the totals:\n{0}".format(totals))
print totals

try:
    print sum(totals)
except Exception:
    print "Error printing sum of totals."

# add the totals in a third "column" to the sourcelist
# maybe a better way to do this is to have the totals function take in a list
# and add the totals in the same function.
for i, source in enumerate(sourcelist):
    source.append(totals[i])

# logger.info(sourcelist)

print "Sending the source list to the pool of workers for downloading"
pool.map(download_wrapper, sourcelist)

logger.info("Process complete")

