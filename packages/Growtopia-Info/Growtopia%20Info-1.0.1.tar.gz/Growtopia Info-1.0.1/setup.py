from setuptools import setup, find_packages

def readme() -> str:
    with open(r'README.txt') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
 
setup(
    name="Growtopia Info",
    version="1.0.1",
    description="This code can search any information in Growtopia, including Sprite, Description, Player Online, and more!",
    long_description=readme(),
    long_description_content_type="",
    url="https://github.com/Gabrielbjb/growtopia-info",
    author="Gabrielbjb",
    author_email="gabrielbjb@protonmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords=['Growtopia','Growtopia Wiki', 'Growtopia Fandom'],
    packages=find_packages(),
    install_requires=['']
)