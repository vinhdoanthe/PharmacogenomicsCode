# Pharmacogenomics

## Introduction

## How to start
### Prerequisites
* Python 3.8++
* Virtualenv
* PostgreSQL 12++
### Installation
**Note**: This tutorial is tested on Macbook M1 with MacOS Ventura 13.3.1. It should work on Ubuntu or other Linux distributions.
* Clone this repository
* Go to project folder
* Create virtual environment with command `python -m venv venv`
* Activate virtual environment with command `source venv/bin/activate`
* Install libraries with command `python -m pip install -r requirements.txt`
* Create `.env` file in project folder with content from `.env.example` file: `cp .env.example .env`. Then update values in `.env` file
* Run command `python manage.py migrate` to create database
* Run command `python manage.py runserver` to start server

### Import data
* Download data from [this Google Drive link](https://drive.google.com/file/d/1atLQWvx2kSH_iF5ueNi1ZBcoIfxHT2z-/view?usp=sharing)
* Create `data` folder then extract data to this folder
* Run command `python scripts/run_many_builds.py` to import data to database

### Develop API
All APIs are developed in `api` app.

#### Example
`GET /api/v1/gene/{gene_id}/` to get gene information
