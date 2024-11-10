import streamlit as st
import psycopg2
from datetime import date
from dotenv import load_dotenv
import os

# Function to connect to the PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        host=os.getenv("host"),
        database=os.getenv("database"),
        user=os.getenv("user"), 
        password=os.getenv("password"),
        port = os.getenv("port")
    )

# Create a table for conversation history (if not exists)
def setup_db():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversation_history
                (id SERIAL PRIMARY KEY, username VARCHAR(100), question TEXT, answer TEXT, date DATE)''')
    conn.commit()
    c.close()
    conn.close()

# Sidebar for admin input and displaying chat history
def sidebar(role):
    
    if role == 'Admin':
        with st.sidebar.form(key='db_details'):
            st.text_input('Host', key="db_host")
            st.text_input('Username', key="db_user")
            st.text_input('Password', key="db_password", type='password')
            st.text_input('Port', key="db_port")
            st.text_input('Database', key="db_name")
            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                st.success("Database details updated!")
    
    st.sidebar.title("Conversation History")
    chat_days = fetch_conversations_dates()
    for chat_date in chat_days:
        formatted_chat_date = chat_date.strftime("%Y-%m-%d")
        click = st.sidebar.button(f"{formatted_chat_date}")
        if click :
            chats = fetch_conversations_of_date(formatted_chat_date)
            st.header(f"chat history of date : {formatted_chat_date}")
            for question, answer in chats :
                st.write(f"**You**: {question}")
                st.write(f"**Bot**: {answer}")

def fetch_conversations_of_date(target_date):
    conn = connect_to_db()
    c = conn.cursor()
    query = "SELECT question, answer FROM conversation_history where date = %s"
    c.execute(query,(target_date,))
    conversations = c.fetchall()
    print("conversion  : ",conversations)
    conn.close()
    return conversations

# Fetching conversation history from PostgreSQL DB
def fetch_conversations_dates():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("SELECT distinct date FROM conversation_history ORDER BY date DESC")
    conversations = c.fetchall()
    conn.close()
    return conversations

# Main chat interface
def chat_interface(username):
    st.title("QueryEase : Business Insights at Fingertips")

    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    with st.form(key='user_input_form', clear_on_submit=True):
        user_input = st.text_input("Ask a question:")
        submit = st.form_submit_button(label="Send")

    if submit and user_input:
        response = generate_response(user_input)
        st.session_state['history'].append((user_input, response))

        # Save conversation to PostgreSQL
        today = date.today()
        print("todays date : ",today)
        save_conversation(username, user_input, response, today)

    # Display the chat history
    for question, answer in st.session_state['history']:
        st.write(f"**You**: {question}")
        st.write(f"**Bot**: {answer}")
    
    # Scroll to the bottom automatically
    st.write("<div id='bottom'></div>", unsafe_allow_html=True)
    st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

# Save conversation to PostgreSQL DB
def save_conversation(username, question, answer, date):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("INSERT INTO conversation_history (username, question, answer, date) VALUES (%s, %s, %s, %s)",
              (username, question, answer, date))
    conn.commit()
    conn.close()

# Placeholder function for generating bot responses
def generate_response(question):
    return "Hello Bro, How its going?."

# Main function
def main():
    load_dotenv()
    setup_db()  # Ensure DB and table are set up

    # Sidebar and user role selection
    # role = st.sidebar.radio("Role", ['Admin', 'User'])
    st.sidebar.title("Input Panel")
    username = st.sidebar.text_input("Enter your username:", value="User1")
    sidebar('Admin')

    chat_interface(username)

if __name__ == "__main__":
    main()
