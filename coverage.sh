#!/bin/bash
coverage run --source='.' manage.py test task_tracker
coverage report > coverageReport.txt
