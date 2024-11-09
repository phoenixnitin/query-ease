def execute_query(sql_query, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()