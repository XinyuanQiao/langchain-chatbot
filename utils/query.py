from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
import pinecone
from templates.qa_prompt import QA_PROMPT
from templates.condense_prompt import CONDENSE_PROMPT

def query(openai_api_key, pinecone_api_key, pinecone_environment, pinecone_index, pinecone_namespace):
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)

    pinecone.init(api_key=pinecone_api_key,environment=pinecone_environment)
    vectorstore = Pinecone.from_existing_index(index_name=pinecone_index, embedding=embeddings, text_key='text', namespace=pinecone_namespace)

    model = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0, openai_api_key=openai_api_key)
    retriever = vectorstore.as_retriever(qa_template=QA_PROMPT, question_generator_template=CONDENSE_PROMPT)
    qa = ConversationalRetrievalChain.from_llm(llm=model, retriever=retriever, return_source_documents=True)

    return qa