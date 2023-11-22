#!/bin/bash
coverage run --source='./task_tracker' manage.py test task_tracker
coverage report > coverageReport.txt
