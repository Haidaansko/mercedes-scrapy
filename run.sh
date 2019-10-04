#!/bin/bash

scrapy crawl panavto -o ./scraped_data.json 2> log.txt
python3 reshape.py