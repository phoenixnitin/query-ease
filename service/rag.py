import google.generativeai as genai
import os
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import re
from logger import Logger
import json


class RAG :
    _logger = Logger.get_logger()
    load_dotenv()
    genai.configure(api_key=os.getenv('API_KEY'))

    @classmethod
    def create_chunks(cls,filename):
        """
        Method to create the chunks from meta data file
        """
        with open(filename,'r') as f:
            data = f.read()

        table_name_pattern = r'\bTable\b' 
        split_data = re.split(table_name_pattern, data)

        chunks = []
        for i, chunk in enumerate(split_data):
            if i > 0:
                chunk = f'Table{chunk}'
            chunks.append(chunk)

        return chunks

    @classmethod
    def get_vector_store(cls,filename):
        """
        Method to create the vector storage from file
        """
        text_chunks = cls.create_chunks(filename)
        embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=os.getenv('API_KEY'))
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")


    @classmethod
    def _get_prompt(cls):
        """
        Method to read base prompt from file
        """
        filename = 'data/base_prompts/01.txt'
        with open(filename,'r') as f:
            prompt = f.read()
        return prompt


    @classmethod
    def _get_conversational_chain(cls):
        """
        Method to create the conversional chain.
        """
        prompt_template = """You are the smart agent who only answer question related to database extraction and generate the postgres sql code in mention instruction format.

        instructions:
        1.answer all greetiing/welcome/hi..hello. reponses in nomral_response key value.
        2.Analysed the provided text context and use provided database meta-data to generate the sql code as output.
        3.provide output in key-value pair format: ["is_sql": True/False, "SQL": "None/converted SQL code","normal_response" :"response to query "]
        4.if user prompt ask for other information apart form sql return : ["is_sql": False, "SQL": "None","normal_response" :"response to query "]
        5.Only generate select keyword sql code if user prompt ask to update/insert/delete/other DB operation 
        return ["is_sql": False, "SQL": "update/insert/delete/other DB query not allowed","normal_response" :"response to query "]
        6.Only answer to user prompt that are related to database information. if user prompt ask other outof context return
        ["is_sql": false, "SQL": "outof context question","normal_response" :"response to query "].
        7. provide output in json format but dont write header json word to it. only return json data.
        user prompt: \n{question}\n
        Context: \n{context}?\n
    """
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro",temperature=0.3,api_key=os.getenv('API_KEY'))

        prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        return chain
    

    @classmethod
    def get_llm_response(cls, user_query):
        """
        Method to get the llm response
        """
        embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=os.getenv('API_KEY'))
    
        new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_query)
        cls._logger.info("doc : ",docs)

        chain = cls._get_conversational_chain()

        raw_response = chain({"input_documents":docs, "question": user_query}, return_only_outputs=True)

        # cls._logger.info("response : ", json.dumps(response))
        cls._logger.info("Reply: ", raw_response["output_text"])
        response : str= raw_response["output_text"]
        clean_response = json.loads(response[8:-3])
        return clean_response