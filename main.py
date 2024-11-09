from services.db_connect import connect_to_postgres
from services.query_validator import validate_query
from services.query_executor import execute_query
from services.error_handler import ValidationError

def main():
    
    sql_query = "select * from student where student_name='abc';"
    
    connection = connect_to_postgres()
    
    try:
        validate_query(sql_query, connection)
        
        result = execute_query(sql_query, connection)
        print("Query executed successfully:", result)
    
    except ValidationError as e:
        print(f"Validation Error: {e.message}")
    
    finally:
        connection.close()

if __name__ == "__main__":
    main()
