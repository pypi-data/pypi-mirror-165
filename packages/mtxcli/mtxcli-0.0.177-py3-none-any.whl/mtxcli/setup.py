from setuptools import setup
import setuptools
import os
import shutil
from pathlib import Path

version_file = Path(__file__).parent.joinpath("version.txt")
print(f"version file : {version_file}")
f = open(version_file,"r")
version = f.read()
f.close()

with open("README.md", "r") as fh:
    long_description = fh.read()

def gen_data_files(*dirs):
    print("gen_data_files =========================================================", dirs)
    results = []
    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            results.append((root, map(lambda f: root + "/" + f, files)))
    print("gen_data_files result ===============", results)
    return results

# 上一个构建的残留会影响打包文件，所以这里先清除。
print("清理目录")
build_dir = os.path.join(os.getcwd(),"build")
if Path(build_dir).exists():        
    shutil.rmtree(build_dir)

packages = setuptools.find_packages(
    exclude=("test", "mtxcms*", "mtx_cloud.*", "mtxauth*", "gallery*"))


if os.path.exists("requirements.txt"):
    install_requires = open("requirements.txt").read().split("\n")
    install_requires = [item for item in install_requires if not item.startswith("-r ")]
else:
    install_requires = []
    

setup(name='mtxcli',
    version=version,
    description='The funniest joke in the world',
    long_description='long_description',  # readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='funniest joke comedy flying circus',
    url='http://github.com/storborg/funniest',
    author='Flying Circus',
    author_email='flyingcircus@example.com',
    license='MIT',
    packages=[
        "mtxcli"
    ],
    package_dir={
        'mtxcli': 'mtxcli'
    },
    #   package_data={'demo': ['data/*.txt']},
    # install_requires=[
    # 'markdown',
    # 'flask',
    # 'pyyaml',
    # 'python-dotenv',
    # 'requests>=2.26.0',
    # 'monotonic>=1.5',
    # 'docker',
    # 'wheel',  
    # 'packaging>=21.0',
    # 'celery',
    # ],    
    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    include_package_data=True,
    package_data={
    #   'demo': ['data/*.txt'],
        'mtxcli': ['data/*.conf'],
    },
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'dockerdev=mtxcli.dockerdev:main',
            'gitup=mtxcli.gitup:main',
            'dc=mtxcli.dc:main',
            'dc2=mtxcli.dc:main',
            'mtgp=mtxcli.mtgp_init:main',
            'mtdp=mtxcli.mtdp:main',
            'mtpub=mtxcli.mtpublish:main',
        ]
    },
    scripts=['mtxcli/dc.py'],
)