from setuptools import setup, find_packages
from os.path import join, dirname
import jreq

setup(
    name='jreq',
    version=jreq.__version__,
    packages=find_packages(),
    description='JSON Requests',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author=jreq.__author__,
    author_email='ya360@uh.net.ru',
    maintainer=jreq.__author__,
    maintainer_email='ya360@uh.net.ru',
    download_url='https://github.com/imercury13/jreq',
    #url='https://ya360.uh.net.ru',
    license='MIT',
    project_urls={
        "Documentation": "https://jreq.readthedocs.io/ru/1.1.0",
        "Bug Tracker": "https://github.com/imercury13/jreq/issues"
    },
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python'
    ],
    install_requires=[
		'requests',
    ],
    include_package_data=True,
)
