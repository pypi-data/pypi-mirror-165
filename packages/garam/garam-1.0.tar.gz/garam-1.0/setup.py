from distutils.core import setup

setup(
  name = 'garam',         # How you named your package folder (MyLib)
  packages = ['garam'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Garam, for arrays too big for memory. A dictionary / list that is stored on the disk for ram intensive operations.',   # Give a short description about your library
  author = 'Jun Ru Chen',                   # Type in your name
  author_email = 'junru.chen.2007@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Shrimp33/garam',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Shrimp33/garam/archive/refs/tags/v1.0.tar.gz',    # I explain this later on
  keywords = ['disk', 'dictionaries', 'lists'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pickle',
          'shutil',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Database',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)