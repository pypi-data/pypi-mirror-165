#!/usr/bin/env python3
import sys
import os
from mtlibs.docker_helper import isInContainer
from mtlibs import process_helper
from pathlib import Path
import logging
from dotenv import load_dotenv, find_dotenv
from mtlibs.github import gitup

import base64
import json
import logging
import shlex
import subprocess
import time
from os.path import relpath
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import re
from os import path
import argparse
from mtlibs import gitclone,gitParseOwnerRepo

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def gitpod_clone_private_repo(giturl:str):
    """
        给定git 网址，下载到指定路径并根据规则运行相关代码。
    """
    parsed = urlparse(giturl)
    owner,repo,file = gitParseOwnerRepo(giturl)

    clone_to = path.join("/workspace",repo)
    gitclone(owner,repo,parsed.username,clone_to)
    if not file:
        logger.info("no entry script,skip launch")
    if file:
        file = file.lstrip("/")
        scriptFile = path.join(clone_to,file)
        if not Path(scriptFile).exists():
            logger.warn(f"入口文件不存在{scriptFile}")

        Path(scriptFile).chmod(0o700)
        logger.info(f"[TODO]开始执行入口文件 {scriptFile}") 
        # logfile = open(path.join(clone_to,GITUP_LOGFILE),'w')
        # subprocess.Popen([scriptFile],
        #     stdout=logfile, #输出重定向到文件。
        #     stderr=logfile,
        #     # stdout=subprocess.PIPE, 
        #     # stderr=subprocess.PIPE,
        #     cwd=clone_to,
        #     shell=False,
        # )

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