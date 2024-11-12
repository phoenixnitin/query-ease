from service import Metadata
from utility import Database


def initialize_app_session(host, port, database, username, password):
    """
    Main method to initialize a query ease application session
        1) resets the database details
        2) generate database metadata file
        3) reset AI engine session
        4) execute base prompts
    """
    Database.reset(host, port, database, username, password)
    create_database_metadata_file()
    reset_ai_engine()
    execute_base_prompts()

def execute_prompt(prompt, retries=3):
    """
    Main method to send prompt to AI engine and get the select query and execute
        1) Send prompt to AI engine and to generate the select query
        2) Run validate, execute loop for a maximum of given retries
    """
    status, message, result = False, 'AI failed to generate valid query', list()
    return status, message, result

def create_database_metadata_file():
    """
    Method to create database metadata file
    """
    filename = 'data/metadata/database.txt'
    Metadata.export_database_metadata(filename)

def reset_ai_engine():
    pass

def execute_base_prompts():
    pass
