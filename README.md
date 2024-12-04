# Query Ease

**Query Ease** is an AI-powered tool designed to convert user input into SQL queries for extracting insights from a PostgreSQL database. The system validates queries based on schema rules and ensures only read queries are executed, improving the efficiency of data extraction for users.

## Table of Contents
- [Introduction](#introduction)
- [Application Url](#application-url)
- [Pre-requisites](#pre-requisites)
- [Setup and Installation](#setup-and-installation)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
  - [Running the Application Locally](#running-the-application-locally)

## Introduction

Query Ease is designed to help users easily interact with databases using natural language inputs. The application processes these inputs, converts them into SQL queries, validates their correctness against a PostgreSQL schema, and then executes valid queries to retrieve the desired information. This project ensures that only safe, read-only queries are executed, protecting your data while providing a seamless experience for users.

## Application URL 
[QueryEase](https://query-ease.onrender.com/)

## Pre-requisites

Before setting up the application locally, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (version 3.11.4 or higher)
- [PostgreSQL](https://www.postgresql.org/download/) (for running the database)

Additionally, you will need a PostgreSQL database and the necessary credentials (host, port, username, password, database name).

## Setup and Installation

### Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/Nitin4323/query-ease.git
cd query-ease
python -m venv venv
venv/Script/activate
pip install requirements.txt
streamlit run app.py
```
