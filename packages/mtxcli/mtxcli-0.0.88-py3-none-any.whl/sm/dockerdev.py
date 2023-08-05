import sys
import os
from mtlibs.docker_helper import isInContainer
from mtlibs import process_helper
from pathlib import Path
import logging
from os import path
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
from mtlibs.github import gitup,gitParseOwnerRepo,gitclone
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def console_script_entry():
    logger.info("git clone 并启动开发容器")

    if isInContainer():
        logger.error("not in container")
        return
    giturl = os.environ.get("MTX_DEV_GIT")
    if not giturl:
        logger.info("没有指定giturl，跳过clone")
    else:
        logger.info(f"gitup 环境变量:{giturl}")
        items = giturl.split("|")
        for item in items:
            logger.info(f"处理{item}")
            parsed = urlparse(giturl)
            owner,repo,file = gitParseOwnerRepo(giturl)
            clone_to = path.join(os.getcwd(),repo)
            logger.info(f"clone 到 {clone_to}")
            if Path(clone_to).exists():
                logger.info("文件已经存在,跳过clone")
            else:
                gitclone(owner,repo,parsed.username,clone_to)
                logger.info("clone 完成")
   
    process_helper.exec("service ssh start")
    logger.info("就绪")
    process_helper.exec("sleep infinity")
        
    