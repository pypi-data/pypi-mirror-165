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
from mtlibs.github import gitclone, gitParseOwnerRepo
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_env():
    env_names = [
        "GIT_TOKEN",
        "DOCKER_HUB_USER",
        "DOCKER_HUB_PASSWORD",
    ]

    # print(os.environ)
    for item in env_names:
        print(f"---{item}")

        if not os.environ.get(item):
            print(f"error: need env {item}")
            return False

    return True


def open_project(projectDir:str):
    cmd = f"cd {projectDir} && code ."
    logger.info(f"cmd {cmd}")
    os.system(cmd)


def gitpod_clone_private_repo(giturl: str, force=False, open=True):
    """
        在gp中clone 并打开项目源码
    """
    logger.info(f"giturl {giturl}")
    parsed = urlparse(giturl)
    if not parsed.hostname:
        logger.error(f"url incorrect : {giturl}")
        return
    uri = parsed
    owner, repo, file = gitParseOwnerRepo(giturl)

    clone_to = path.join("/workspace", repo)
    if Path(clone_to).exists() and not force:
        logger.info(f"target dir existing, skip clone")
    else:
        gitclone(owner, repo, parsed.username, clone_to)
        if not file:
            logger.info("no entry script,skip launch")
        if file:
            file = file.lstrip("/")
            scriptFile = path.join(clone_to, file)
            if not Path(scriptFile).exists():
                logger.warn(f"入口文件不存在{scriptFile}")

            Path(scriptFile).chmod(0o700)
            logger.info(f"[TODO]开始执行入口文件 {scriptFile}")

    if open:
        open_project(clone_to)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls")
    parser.add_argument("--open", default=True, action="store_true", help="increase output verbosity")
    parser.add_argument("--force",default=False, action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    logger.info(f"args: {args}")
    gitup_urls = args.urls
    if not gitup_urls:
        logger.info(f"need urls")
        exit()
    items = gitup_urls.split("|")
    for item in items:
        gitpod_clone_private_repo(item)


if __name__ == '__main__':
    main()
