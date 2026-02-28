import config_data as config
from langchain_chroma import Chroma

class VectorStoreService(object):
    def __init__(self, embedding):
        """"
        param embedding: The embedding model to be passed in
        """
        self.embedding = embedding
        # Initialize the vector store
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        """Get the retriever for the vector store"""
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})
        

if __name__ == "__main__":
    from langchain_ollama import OllamaEmbeddings
    retriever = VectorStoreService(OllamaEmbeddings(model="nomic-embed-text")).get_retriever()

    res = retriever.invoke("What is Python?")
    print(res)
