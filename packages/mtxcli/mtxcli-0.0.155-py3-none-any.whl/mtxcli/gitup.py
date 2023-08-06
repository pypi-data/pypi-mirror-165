#!/usr/bin/env python3
import sys
import os
from mtlibs.docker_helper import isInContainer
from mtlibs import process_helper
from pathlib import Path
import logging
from dotenv import load_dotenv, find_dotenv
from mtlibs.github import gitup

import argparse  

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("urls") 
    args = parser.parse_args()
    logger.info(f"urls: {args.urls}")
    gitup_urls = args.urls or os.environ.get("MTX_GITUP")
    if not gitup_urls:
        logger.info(f"need urls")
        exit()
    items = gitup_urls.split("|")
    for item in items:
        gitup(item)

if __name__ == "__main__":
    main()