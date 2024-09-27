from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from src.config import QDRANT_API_KEY, QDRANT_API_URL


system_message = """You are a helpful chatbot. Use only the following pieces of context to answer the question at the end.
Do not try to make up the answer by your own.
If user is greeting or saying thank you, respond accordingly.
Answer only from the context.
If you don't know the answer, just say that "I apologize for the inconvenience. Unfortunately, I don't have access to specific information on your query at the moment.

{context}

"""
system_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=["input"], template="{input}")),
    ]
)

rephrase_question_prompt_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}

Follow Up Input: {input}
Standalone question:"""

rephrase_prompt = PromptTemplate.from_template(template=rephrase_question_prompt_template)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

qdrant_client = QdrantClient(url=QDRANT_API_URL, api_key=QDRANT_API_KEY, timeout=60)

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="demo_collection",
    embedding=embeddings,
)

from langchain_openai import ChatOpenAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

llm_model_name = "gpt-3.5-turbo"
chatbot_llm = ChatOpenAI(model=llm_model_name, temperature=0, verbose=True)
retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3})

history_aware_retriever = create_history_aware_retriever(llm=chatbot_llm, retriever=retriever, prompt=rephrase_prompt)
document_chain = create_stuff_documents_chain(llm=chatbot_llm, prompt=system_prompt)
conversational_retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)
