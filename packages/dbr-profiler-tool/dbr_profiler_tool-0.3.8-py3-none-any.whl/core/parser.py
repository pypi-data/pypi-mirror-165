
import configparser
from distutils.log import Log
from core import wmconstants
from core.logging_utils import LoggingUtils
import logging
from os import path
import json,re

loggr=None

if loggr == None:
    loggr = LoggingUtils.get_logger()

def set_defaults(args):
    if 'profile' not in args.keys():
        args.update({'profile':''})
    if 'url' not in args.keys():
        args.update({'url':''})        
    if 'verbosity' not in args.keys():
        args.update({'verbosity':'false'})
    if 'verify_ssl' not in args.keys():
        args.update({'verify_ssl':'false'})
    if 'export_db' not in args.keys():
        args.update({'export_db':'logs'})


def url_validation(url):
    if '/?o=' in url:
        # if the workspace_id exists, lets remove it from the URL
        url = re.sub("\/\?o=.*", '', url)
    elif 'net/' == url[-4:]:
        url = url[:-1]
    elif 'com/' == url[-4:]:
        url = url[:-1]
    return url.rstrip("/")



#DEBUG < INFO < WARNING < ERROR < CRITICAL
def getLogLevel(s):
    s=s.upper()
    if s == "DEBUG": return logging.DEBUG
    elif s == "INFO": return logging.INFO
    elif s == "WARNING": return logging.WARNING
    elif s == "ERROR": return logging.ERROR
    elif s == "CRITICAL": return logging.CRITICAL

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


def parse_dbcfg(creds_path='~/.databrickscfg', profile='DEFAULT'):
    config = configparser.ConfigParser()
    abs_creds_path = path.expanduser(creds_path)
    config.read(abs_creds_path)
    try:
        current_profile = dict(config[profile])
        return current_profile
    except KeyError:
        raise ValueError(
            'Unable to find credentials to load for profile. Profile only supports tokens.')

#parse args from json string
#'''{"profile": "", "url":"", "account_id":"dcdbb945-e659-4e8c-b108-db6b3ac3d0eb", "export_db": "logs", "verify_ssl": "False", "verbosity":"info", 
#   "clusterid":clusterid,"master_name_scope":"swat_masterscp", 
#   "master_name_key":"user", "master_pwd_scope":"swat_masterscp", "master_pwd_key":"pass",
#       "workspace_pat_scope":"swat_masterscp",  "workspace_pat_token":"sat_token" }'''

def parse_input_jsonargs(jsonargs):
    args =json.loads(jsonargs)
    set_defaults(args)
    url = url_validation(args['url']
    args.update({'url':url})
    args.update({'verbosity':getLogLevel(args['verbosity'])})
    LoggingUtils.loglevel=args['verbosity'] #update class variable
    args.update({'verify_ssl':str2bool(args['verify_ssl'])})
    return args




