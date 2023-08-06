from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
]

setup(
    name = 'wilwil',
    version = '0.0.1',
    description = 'Who am i?',
    long_description = open('README.txt').read() + '\n\n' +  open('CHANGELOG.txt').read(),
    author = 'WilWil',
    author_email = 'wildan8376@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    url = 'https://github.com/IkuzoMyDream/',
    download_url = 'https://github.com/IkuzoMyDream/',
    keywords = ['WilWil', 'Wil Wil'],
    packages = find_packages(),
    install_requires = ['']
)