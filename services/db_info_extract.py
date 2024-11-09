import psycopg2
from psycopg2 import sql
import db_connect


def get_table_details(cursor, schema, table):
    cursor.execute(
        sql.SQL("""
            SELECT 
                column_name, 
                data_type,
                character_maximum_length
            FROM information_schema.columns 
            WHERE table_schema = %s AND table_name = %s;
        """),
        [schema, table]
    )
    return cursor.fetchall()


def get_table_relations(cursor, schema, table):
    cursor.execute(
        sql.SQL("""
            SELECT
                tc.table_name AS foreign_table,
                kcu.column_name AS foreign_column,
                ccu.table_name AS referenced_table,
                ccu.column_name AS referenced_column
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
              AND tc.table_schema = %s 
              AND tc.table_name = %s;
        """),
        [schema, table]
    )
    return cursor.fetchall()


def extract_db_metadata():
    connection = db_connect.connect_to_postgres()
    if not connection:
        return
    
    cursor = connection.cursor()

    cursor.execute("""
        SELECT schema_name 
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema','pg_toast');
    """)
    schemas = cursor.fetchall()

    with open("db_metadata.txt", "w") as file:
        for schema in schemas:
            schema_name = schema[0]
            file.write(f"Schema: {schema_name}\n")
            
            cursor.execute(
                sql.SQL("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = %s;
                """),
                [schema_name]
            )
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                file.write(f"  Table: {table_name}\n")
                
                columns = get_table_details(cursor, schema_name, table_name)
                file.write(f"    Columns:\n")
                for column in columns:
                    column_name, data_type , character_maximum_length = column
                    # To avoid the NOne value at end of each line in case iof integer
                    if(data_type == 'integer'):
                        file.write(f"      {column_name}: {data_type}\n")
                    else:
                        file.write(f"      {column_name}: {data_type} {character_maximum_length}\n")
                
                
                relations = get_table_relations(cursor, schema_name, table_name)
                if relations:
                    file.write(f"    Relations:\n")
                    for relation in relations:
                        foreign_table, foreign_column, ref_table, ref_column = relation
                        file.write(f"      {foreign_column} in {table_name} references {ref_column} in {ref_table}\n")
                else:
                    file.write(f"    No relations found.\n")
    
    cursor.close()
    connection.close()
    print("Database metadata written to db_metadata.txt")


if __name__ == "__main__":
    extract_db_metadata()
