from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import ChatOpenAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.config import QDRANT_API_KEY, QDRANT_API_URL


class RAGProcessor:
    def __init__(self):
        rag_system_prompt = """You are an intelligent assistant trained to analyze and summarize content from uploaded documents or video transcripts. Every time I upload a document or video, I expect you to pull insights and present the content in a structured, actionable way.
        The response should follow this format:
        1. Start with a Clear Overview
        2. Begin by summarizing the main idea or strategy from the content, focusing on the core objectives or challenges being addressed.
        3. Highlight Key Insights from Experts
        4. Identify and explain key insights or expert opinions from the content. Attribute these insights to the relevant thought leaders mentioned in the content, and mention their areas of expertise or influence.
        5. Provide Time-stamped or Sectioned References
        6. Include a timestamp (if it’s a video) or page/section reference (if it’s a document) for each key insight to allow for easy navigation to the specific point in the content.
        7. Present Actionable Steps or Recommendations
        8. Summarize the key takeaways or practical steps that can be applied based on the content.
        9. Include Links to the Full Content
        10. Always include the link to the video or document so that I can access the full resource.

        If you don't know the answer, just say that "I apologize for the inconvenience. Unfortunately, I don't have access to specific information on your query at the moment.

        {context}
        """
        system_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", rag_system_prompt),
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

        llm_model_name = "gpt-4o-mini"
        chatbot_llm = ChatOpenAI(model=llm_model_name, temperature=0, verbose=True)
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3}
        )

        history_aware_retriever = create_history_aware_retriever(
            llm=chatbot_llm, retriever=retriever, prompt=rephrase_prompt
        )
        document_chain = create_stuff_documents_chain(llm=chatbot_llm, prompt=system_prompt)
        self.conversational_retrieval_chain = create_retrieval_chain(history_aware_retriever, document_chain)

    def chat(self, user_input, chat_history: List[BaseMessage] = []):
        result = self.conversational_retrieval_chain.invoke({"input": user_input, "chat_history": chat_history})
        return result["answer"]
