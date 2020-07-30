# Description
Extract and download images from websites by input keywords

# Available website
- unsplash_com

# Requirements
- python >= 3.7
- Ubuntu >= 18.04

# How to setup system
## Install python
1. Start by updating the packages list and installing the prerequisites
- sudo apt update
- sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev
- sudo apt install software-properties-common

2. Add the deadsnakes PPA to your sources list (used to install python3.8 or later)
- sudo add-apt-repository ppa:deadsnakes/ppa
- When prompted press Enter to continue: Press [ENTER] to continue or Ctrl-c to cancel adding it.

3. Once the repository is enabled, install python 3.8
- sudo apt install python3.8

## Set up enviroment
1. Install python virtualenv
- sudo apt install python3.8-dev python3.8-env

2. Create new virtualenv
- python3.8 -m venv *your_folder_name*

3. Active enviroment
- source *your_folder_name*/bin/active

4. Deactive enviroment (if need)
- deactivate

## Install necessary python package
- pip install -U pip wheel setuptools
- pip install -r requirements/dev.txt

# Run Code
1. Move to workdir
- cd ./spider_app

2. Setup settings.py for scrapy
- cp 

2. Show available spiders
- crapy list

3. choose and run spider
- scrapy crawl -a tags=*your_keywords_are_seperated_by_comma* *your_selected_spider*
- Ex: scrapy crawl -a tags=*flower,friend,babay* *unsplash_spider*

# Default Config
- Watch log file: tail -f -n 100 ./spider_app/logs
- Download folder: ls ./spider_app/spider_app/download/
- Total downloaded images: find ./spider_app/download -type f | wc -l
