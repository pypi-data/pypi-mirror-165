import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
     name='trex-mail',  
     version='0.1.3',
     author="Jack Lok",
     author_email="sglok77@gmail.com",
     description="TRex Core library package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://bitbucket.org/lokjac/trex-mail",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[            
          'Flask-Mail',
          'mailjet_rest',
          'sendgrid',
      ],
 )

