
from distutils.core import setup
setup(
    name='test-memphis-py',
    packages=['memphis'],
    version='0.0.5',
    license='GPL',
    description='A powerful message broker for developers',
    readme="README.md",
    author='Memphis.dev',
    author_email='shoham@memphis.dev',
    url='https://github.com/shohamroditimemphis/test-memphis.py',
    download_url='https://github.com/shohamroditimemphis/test-memphis.py/releases/tag/v0.0.5.tar.gz',
    keywords=['message broker', 'devtool', 'streaming', 'data'],
    install_requires=[
        'asyncio',
        'nats-py'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)