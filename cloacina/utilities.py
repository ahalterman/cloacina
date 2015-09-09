from ConfigParser import ConfigParser
import glob
import os

# thanks, OEDA! https://github.com/openeventdata/scraper/blob/master/scraper.py

def _parse_config(parser):
    try:
        if 'Auth' in parser.sections():
            auth_db = parser.get('Auth', 'auth_db')
            auth_user = parser.get('Auth', 'auth_user')
            auth_pass = parser.get('Auth', 'auth_pass')
            db_host = parser.get('Auth', 'db_host')
        else:
            # Try env vars too
            auth_db = os.getenv('MONGO_AUTH_DB') or ''
            auth_user = os.getenv('MONGO_AUTH_USER') or ''
            auth_pass = os.getenv('MONGO_AUTH_PASS') or ''
            db_host = os.getenv('MONGO_HOST') or ''

        ln_user = parser.get('LexisNexis', 'user')
        ln_password = parser.get('LexisNexis', 'password')
        log_dir = parser.get('Logging', 'log_file')
        log_level = parser.get('Logging', 'level')
        collection = parser.get('Database', 'collection_list')
        whitelist = parser.get('URLS', 'file')
        pool_size = int(parser.get('Processes', 'pool_size'))
        return ln_user, ln_password, collection, whitelist, pool_size, log_dir, log_level, auth_db, auth_user, \
               auth_pass, db_host
    except Exception, e:
        print 'Problem parsing config file. {}'.format(e)

def parse_config():
    """Function to parse the config file."""
    config_file = glob.glob('default_config.ini')
    parser = ConfigParser()
    if config_file:
        parser.read(config_file)
    else:
        cwd = os.path.abspath(os.path.dirname(__file__))
        config_file = os.path.join(cwd, 'default_config.ini')
        parser.read(config_file)
    return _parse_config(parser)
