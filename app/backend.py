from service import Metadata
from service import RAG
from service import Features
from utility import Database
import pandas as pd

def initialize_app_session(host, port, database, username, password):
    """
    Main method to initialize a query ease application session
        1) resets the database details
        2) generate database metadata file
        3) reset AI engine session
        4) execute base prompts
    """
    Database.reset(host, port, database, username, password)
    filename = create_database_metadata_file()
    get_vector_store(filename=filename)
    reset_ai_engine()
    execute_base_prompts()  

def execute_prompt(prompt, retries=3):
    """
    Main method to send prompt to AI engine and get the select query and execute
        1) Send prompt to AI engine and to generate the select query
        2) Run validate, execute loop for a maximum of given retries
    """
    status, message, result = False, 'AI failed to generate valid query', list()
    sql_chat = False

    response  = RAG.get_llm_response(user_query=prompt)
    if response['is_sql']:
        status , error_msg = Database.validate_query(response['SQL'])
        if status:
            # _,result,_ = Database.execute_query(response['SQL'])
            df  = pd.read_sql(response['SQL'],Database.get_connection())
            sql_chat = True
            return sql_chat,df
        else:
            return sql_chat,result     
    else :
        return sql_chat,response['normal_response']

def create_database_metadata_file():
    """
    Method to create database metadata file
    """
    filename = 'data/metadata/database.txt'
    Metadata.export_database_metadata(filename)
    return filename

def get_vector_store(filename):
    """
    Method to create the chunks from meta data file
    """
    RAG.get_vector_store(filename)

def reset_ai_engine():
    pass

def execute_base_prompts():
    pass

def get_excel_from_df(df):
    return Features.convert_df_to_excel(df)
