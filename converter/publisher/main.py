import argparse
import logging

from config.getconfig import getConfig
from pagesController import deletePages, searchPages
from pagesPublisher import publishFolder

logging.basicConfig(level=logging.INFO)

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--login', help='Login with "" is mandatory', required=True)
parser.add_argument('--password', help='Password with "" is mandatory', required=True)
parser.add_argument('--folder', help='Folder containing markdown files', required=True)
parser.add_argument('--confluence_space', help='Confluence space key', required=True)
parser.add_argument('--parent_page_id', help='Confluence parent page ID', required=True)
args = parser.parse_args()
inputArguments = vars(args)

overrides = {
    "github_folder_with_md_files": inputArguments['folder'],
    "confluence_space": inputArguments['confluence_space'],
    "counfluence_parent_page_id": inputArguments['parent_page_id']
}

CONFIG = getConfig(overrides=overrides)

logging.debug(CONFIG)

pages = searchPages(login=inputArguments['login'], password=inputArguments['password'])
deletePages(pagesIDList=pages, login=inputArguments['login'], password=inputArguments['password'])

publishFolder(folder=CONFIG["github_folder_with_md_files"], 
              login=inputArguments['login'], 
              password=inputArguments['password'])
