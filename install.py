import pip

def install(package):
    pip.main(['install', package])

packages = ['selenium', 'tweepy', 'pyspeedtest']
for package in packages:
    install(package)