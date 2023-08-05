import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name = "ghsu",
    version = "0.1.0",
    author = "Karime Maamari",
    author_email = "maamari@usc.edu",
    description = ("An automated Github account setup tool."),
    license = "MIT",
    keywords = "github account setup",
    url = "http://packages.python.org/ghsu",
    packages=['ghsu'],
    #long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',              
    install_requires=["selenium>=4.3.0",
                      "webdriver_manager>=3.8.2"],                    
     entry_points={
         'console_scripts': ['ghsu = ghsu.ghsu:main', 'ghsussh = ghsu.ghsu:set_ssh', 'ghsurepo = ghsu.ghsu:create_repo'],
     }
    )
