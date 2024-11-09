import sqlparse
from services.error_handler import ValidationError

def validate_query(sql_query, connection):
    
    parsed_query = sqlparse.parse(sql_query)
    # print("parsed_query : ",parsed_query)
    statement = parsed_query[0]
    # print("statement : ",statement)
    command_type = statement.get_type()
    # print("command_type : ",command_type)
    
    if command_type != 'SELECT':
        raise ValidationError("Only SELECT queries are allowed.")
    
    cursor = connection.cursor()
    try:
        cursor.execute(f"EXPLAIN {sql_query}")
    except Exception as e:
        raise ValidationError(f"SQL Syntax Error: {e}")
    finally:
        cursor.close()
    
    return True
