from openai import OpenAI

# config has OPENAI_API_KEY=''
from config import *

import pandas as pd

def chat_response(user_input):
  client = OpenAI(api_key=OPENAI_API_KEY)

  prompt = f'''convert the text query into the corresponding sql query and only give the sql query as result. Dont put any explaination not a single word or heading like sql.
  text query : {user_input} 
  Database schema : {schema}
  check table and there columns fields correctly sql which has column name not present in above table schema
  self evaluate the sql before writing it.
  crossverify the column you write in sql and the database schema they must match with corresponding table
  NOte : join maximum tables to achieve the result'''

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
      {"role": "user", "content": prompt}
    ]
  )

  sql_query = completion.choices[0].message.content

  return sql_query

# def execute_sql(sql_query):
#   try:
#     cursor=connection.cursor()
#     cursor.execute(sql_query)
#     result = cursor.fetchall()
#     column_names = [description[0] for description in cursor.description]
#     cursor.close()
#     connection.close()
#     return column_names,result
#   except Exception as e:
#     return None, str(e)

def chat_interface(user_input):

  sql_query = chat_response(user_input)

  print("***************** START ********************************")
  print("corresponding SQl : \n",sql_query)

# testing purpose
#   sql_query = '''
#   SELECT sorder.order_id, sorder.order_date, od.product_id, od.quantity, od.unit_price, oe.execution_status
# FROM sorder
# JOIN order_detail od ON sorder.order_id = od.order_id
# LEFT JOIN order_exec oe ON sorder.order_id = oe.order_id;
  # '''

  print("*******************************************************")
  # column_names, result = execute_sql(sql_query)
  # try:
  #   df = pd.DataFrame(result,columns=column_names)
  #   print("Result : \n",df )
  # except Exception as e:
  #   print("error : ",result)
  # print("********************* END ****************************")


if __name__ == "__main__":
  
  # while(True):
  #   user_input = input("Chat : ")

  #   if(user_input=='q'):
  #     break
  #   chat_interface(user_input)
  #   print("if want to exit enter 'q' as input to Chat")

  user_input = '''Give me Cancelled orders of ENX market for the date 20240418 '''
  chat_interface(user_input)
  
