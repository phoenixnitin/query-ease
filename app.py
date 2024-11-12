import streamlit as st

import app


def sidebar():
    st.sidebar.title("DB Details")
    with st.sidebar.form(key='db_details'):
        host = st.text_input('Host', key="db_host")
        username = st.text_input('Username', key="db_user")
        password = st.text_input('Password', key="db_password", type='password')
        port = st.text_input('Port', key="db_port")
        database = st.text_input('Database', key="db_name")
        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            app.initialize_app_session(host, port, database, username, password)
            st.success("Database details updated!")

# Main chat interface
def chat_interface():
    st.title("QueryEase : Business Insights at Fingertips")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    with st.form(key='user_input_form', clear_on_submit=True):
        user_input = st.text_input("Ask a question:")
        submit = st.form_submit_button(label="Send")

    if submit and user_input:
        response = app.execute_prompt(user_input)
        st.session_state['history'].append((user_input, response))

    # Display the chat history
    for question, answer in st.session_state['history']:
        st.write(f"**You**: {question}")
        st.write(f"**Bot**: {answer}")

    # Scroll to the bottom automatically
    st.write("<div id='bottom'></div>", unsafe_allow_html=True)
    st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

def main():
    sidebar()
    chat_interface()

if __name__ == "__main__":
    main()
