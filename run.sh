#!/bin/bash

scrapy crawl panavto -o $SCRAPY_FILE 2> $LOG_FILE
python reshape.py