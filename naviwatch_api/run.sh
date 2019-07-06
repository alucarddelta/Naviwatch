#!/bin/bash


gunicorn --bind 0.0.0.0:5155 run:app --workers 8
