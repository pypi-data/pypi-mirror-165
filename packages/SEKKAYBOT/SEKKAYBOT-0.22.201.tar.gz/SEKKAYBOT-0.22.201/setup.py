import setuptools
    
setuptools.setup(
    name="SEKKAYBOT",
    version="0.22.201",
    author="Sekkay",
    description="Lobby bot.",
    url="https://www.youtube.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'fortnitepy==3.6.5',
        'BenBotAsync',
        'FortniteAPIAsync',
        'uvloop',
        'sanic==21.6.2',
        'colorama',
        'aiohttp'
    ],
)
