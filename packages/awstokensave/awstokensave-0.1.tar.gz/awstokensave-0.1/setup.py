from setuptools import setup, find_packages

setup(
    name='awstokensave',
    version='0.1',
    url='https://github.com/h4rithd/awsTokenEx',
    license='MIT',
    author='h4rithd',
    author_email='h4rithd@pm.me',
    description='This script is for read the env file and then search for the aws temporary credentials after that set it on ~/.aws/credentials file with profile name',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    keywords='awstokenex aws aws-token aws-secret AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'textwrap',
        'argparse',
        'flask_httpauth',
        'pathlib',
        'colorama'
    ],
)
