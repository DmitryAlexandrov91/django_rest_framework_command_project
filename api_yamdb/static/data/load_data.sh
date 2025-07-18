#!/bin/bash

python manage.py get_data static/data/category.csv
python manage.py get_data static/data/genre.csv
python manage.py get_data static/data/title.csv