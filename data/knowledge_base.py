import os
import config_data as config # 导入你的配置文件（存放路径、分段大小等）
import hashlib 
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

# --- 工具函数：指纹识别（查重） ---

def check_md5(md5_str:str):
    """检查这个文件的指纹是否已经存在记录中"""
    if not os.path.exists(config.md5_path):
        # 如果文件不存在，创建一个空的
        open(config.md5_path, 'w', encoding='utf-8').close()
        return False
    else:
        # 读取每一行指纹，对比现在这个
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            if line.strip() == md5_str:
                return True # 找到了，说明重复了
        return False

def save_md5(md5_str:str):
    """把新文件的指纹存进登记簿"""
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')
    
def get_string_md5(input_str:str, encoding='utf-8'):
    """给字符串生成一个唯一的身份证号（MD5）"""
    str_bytes = input_str.encode(encoding=encoding)
    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    return md5_obj.hexdigest()

# --- 核心服务类 ---

class KnowledgeBaseService(object):
    def __init__(self):
        # 确保存放数据库的文件夹存在
        os.makedirs(config.persist_directory, exist_ok=True) 
    
        # 初始化 Chroma 数据库
        self.chroma = Chroma(
            collection_name=config.collection_name,
            # 使用你刚才安装的 Ollama 里的 nomic 模型
            embedding_function = OllamaEmbeddings(model="nomic-embed-text"),
            persist_directory=config.persist_directory
        )
        
        # 初始化“碎纸机”
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,        # 每一块多长（比如500字）
            chunk_overlap=config.chunk_overlap,  # 块与块之间重叠多少（防止切断上下文）
            separators=config.separator,         # 按什么切（换行、句号等）
            length_function=len 
        )

    def upload_by_string(self, data: str, filename):
        """核心业务：把一段文字存入数据库"""
        # 1. 先查重
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "【跳过】内容已经存在知识库中了"
        
        # 2. 如果太长，就切碎；不长就直接用
        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        # 3. 准备“元数据”（就像图书卡片上的备注：作者、时间）
        metadata= {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "ONG",        
        }

        # 4. 存入数据库（最耗显卡的一步，因为要转向量）
        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
            ids=[filename] * len(knowledge_chunks)
        )
        
        # 5. 存入 MD5 记录，防止下次重复
        save_md5(md5_hex)
        return "【成功】内容上传成功"

# 测试代码
if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_string("hello world", "test.txt")
    print(r)