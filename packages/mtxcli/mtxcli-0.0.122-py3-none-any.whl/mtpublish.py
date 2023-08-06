#!/usr/bin/env python3

import os
import sys
import re
from version_parser import Version
from pathlib import Path
import shutil
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")

import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




def publish_pypi():
    """
        用于二进制包发布到可自由下载的公网地址。
        目前仅支持python setuptools 的方式，
        打算后续支持npm , docker hub 等方式。
    """    
    def credential():
        pypi_username = os.environ.get("PYPI_USERNAME")
        pypi_password = os.environ.get("PYPI_PASSWORD")
        content = f"""[pypi]
username:{pypi_username}
password:{pypi_password}"""
        path = os.path.join(os.path.expanduser("~"),".pypirc")
        with open(path,"w") as fd:
            fd.write(content)
            
    def version_patch():        
        init_py_path = "__init__.py"
        version = ""
        with open(init_py_path, 'r') as fd:
            version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                                fd.read(), re.MULTILINE).group(1)  

        v1 = Version(version)
        build_version = int(v1.get_build_version()) +1
        newVersion = f"{v1.get_major_version()}.{v1.get_minor_version()}.{build_version}"
        print(f"new version: {newVersion}")
        with open(init_py_path, 'w') as fd:
            fd.write(f"""__version__="{newVersion}" """)
    
    def clear_dist():
        print("清理目录")
        dist_dir = os.path.join(os.getcwd(),"dist")
        print(f"dist_dir: {dist_dir}")
        if Path(dist_dir).exists():        
            shutil.rmtree(dist_dir)
            
    def clear_build():
        print("清理目录")
        build_dir = os.path.join(os.getcwd(),"build")
        print(f"build_dir: {build_dir}")
        if Path(build_dir).exists():        
            shutil.rmtree(build_dir)
            
    credential()
    version_patch()
    clear_dist()
    clear_build()
    os.system(f"""python3 setup.py bdist_wheel""")
    os.system(f"""twine upload dist/*""")
    
def main():
    publish_pypi()
    
if __name__ == "__main__":
    main()