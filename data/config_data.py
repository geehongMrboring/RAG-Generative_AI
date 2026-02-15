md5_path = "./md5.txt"
collection_name = "rag"
persist_directory = "./chroma_db"

# splitter 
chunk_size = 1000
chunk_overlap = 100
separator = ["\n\n", "\n", " ", ".", ",", "。", "、", ":", ";", "【", "】", "(", ")", "《", "》", "“", "”", "【", "】", "《", "》", "(", ")", ":", ":", "。", "、", ":", ";", ":", "。", "、", ":", ";", "!", "!", "?", "?", "!", "?", "!", "?"]
max_split_char_number = 1000