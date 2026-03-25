import os
import config_data as config  # Import your configuration file (paths, chunk sizes, etc.)
import hashlib
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

# --- Utility functions: fingerprint (duplicate check) ---

def check_md5(md5_str: str):
    """Check if the file's fingerprint already exists in the record."""
    if not os.path.exists(config.md5_path):
        # If the file does not exist, create an empty one
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        # Read each line of fingerprints and compare with the current one
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line.strip() == md5_str:
                return True  # Found it, indicating duplication
        return False

def save_md5(md5_str: str):
    """Save the fingerprint of the new file into the registry."""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding='utf-8'):
    """Generate a unique ID (MD5) for a string."""
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()

# --- Core service class ---

class KnowledgeBaseService(object):
    def __init__(self):
        # Ensure the database storage directory exists
        os.makedirs(config.persist_directory, exist_ok=True)

        # Initialize Chroma database
        self.chroma = Chroma(
            collection_name=config.collection_name,
            # Use the nomic model from Ollama you just installed
            embedding_function=OllamaEmbeddings(model=config.embedding_model_name),
            persist_directory=config.persist_directory
        )

        # Initialize the text splitter
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,        # Size of each chunk (e.g., 500 characters)
            chunk_overlap=config.chunk_overlap,  # Overlap between chunks (to prevent cutting off context)
            separators=config.separator,         # Separators for splitting (newlines, periods, etc.)
            length_function=len
        )

    def upload_by_string(self, data: str, filename):
        """Core business: store a piece of text into the database."""
        # 1. First check for duplicates
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[Skipped] Content already exists in the knowledge base"

        # 2. If too long, split; otherwise use directly
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        # 3. Prepare metadata (like notes on a library card: author, time)
        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "ONG",
        }

        # 4. Store into database (most GPU-intensive step, because of vectorization)
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        # 5. Save MD5 record to prevent future duplicates
        save_md5(md5_hex)
        return "[Success] Content uploaded successfully"

# Test code
if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_string("hello world", "test.txt")
    print(r)