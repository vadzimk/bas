# Job board scrapper

## Overview

This is an Indeed job board scrapper that actually works.

## Usage

poetry install  
poetry run python3 main.py  
poetry run display-html.py

## Output

A csv file and html table with the following fields:

``` ['company_rating', 'company_name', 'multiple_candidates', 'date_posted', 'title', 'company_location', 'salary',
         'estimated_salary', 'job_type', 'qualifications', 'description_text', 'benefits', 'hiring_insights',
         'company_indeed_profile_url', 'url']```