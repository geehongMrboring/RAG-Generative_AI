md5_path = "./md5.txt"
collection_name = "rag"
persist_directory = "./chroma_db"

# splitter
chunk_size = 1000
chunk_overlap = 100
# More scientific separator priority order
separator = [
    "\n\n",    # 1. Prefer to split by double newline (large paragraphs)
    "\n",      # 2. Split by single newline (lines)
    "。",      # 3. Chinese period
    "！",      # 4. Chinese exclamation mark
    "？",      # 5. Chinese question mark
    "!",       # 6. English exclamation mark
    "?",       # 7. English question mark
    "；",      # 8. Chinese semicolon
    ";",       # 9. English semicolon
    "……",      # 10. Ellipsis
    ".",       # 11. English period (placed later to avoid splitting abbreviations)
    " ",       # 12. Space
    ""         # 13. Last resort, split by character
]
max_split_char_number = 1000

similarity_threshold = 2

embedding_model_name = "nomic-embed-text"
chat_model_name = "qwen2.5:1.5b"

session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }