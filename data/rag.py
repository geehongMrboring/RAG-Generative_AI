from langchain_ollama import OllamaEmbeddings
from vector_stores import VectorStoreService
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history
from langchain_core.runnables.history import RunnableWithMessageHistory

class RagService(object):
    
    def __init__(self):
    
        self.vector_service = VectorStoreService(
            embedding=OllamaEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "Primarily use the provided reference materials. "
                 "Answer user questions concisely and professionally. Reference materials: {context}"),
                ("system", "The user's conversation history is also provided as follows:"), 
                MessagesPlaceholder("history"),
                ("user", "Please answer the user's question: {input}")
            ]
        )
        
        self.chat_model = ChatOllama(model=config.chat_model_name, 
                                     temperature=0)
        self.chain = self.__get_chain()

    def __get_chain(self):
        """Get the final execution chain."""
        retriever = self.vector_service.get_retriever()

        def format_documents(docs: list[Document]):
            if not docs:
                return "No relevant documents found."
            formatted_str = ""
            for doc in docs:
                formatted_str += f"Document snippet: {doc.page_content}\nDocument metadata: {doc.metadata}\n\n"
            return formatted_str
        
        def format_for_retriever(value):
            return value["input"]
        
        def format_for_prompt_template(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriever | format_documents 
            } | RunnableLambda(format_for_prompt_template)
              | self.prompt_template
              | self.chat_model
              | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain, 
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        return conversation_chain
    
if __name__ == "__main__":
    session_config = {
        "configurable": {
            "session_id" : "user_001"
        }
    }
    service = RagService().chain.invoke({"input": "What is Python?"}, session_config)
    
    print(service)