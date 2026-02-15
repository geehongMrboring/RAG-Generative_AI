# 导入 streamlit 库，并简写为 st（这是行业惯例，方便后面调用）
import time
import streamlit as st
from knowledge_base import KnowledgeBaseService
# 在网页上显示一个大标题
st.title("知识库更新服务")

# 创建一个文件上传组件
# label: 显示在上传框上方的文字
# type: 限制只能上传文本文件 (.txt)
# accept_multiple_files: 设置为 False 表示一次只能传一个文件
uploader_file = st.file_uploader (
    "请上传TXT文件", 
    type=["txt"],
    accept_multiple_files=False
)

# 如果 session_state 中没有 service 这个键，就在里面新建一个
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

# 判断用户是否已经选择了文件
# 如果 uploader_file 不是空的（None），就执行冒号缩进里面的代码
if uploader_file is not None:
    
    # 获取文件的基本信息
    file_name = uploader_file.name  # 获取文件名
    file_type = uploader_file.type  # 获取文件类型（MIME类型）
    file_size = uploader_file.size / 1024  # 获取文件大小，原始单位是字节(B)，除以1024转成KB

    # 显示一个二级标题，展示文件名
    # f"..." 是 Python 的格式化字符串，可以把变量直接塞进大括号里显示
    st.subheader(f"文件名：{file_name}")
    
    # 在网页上显示文件格式和保留两位小数的大小
    st.write(f"格式：{file_type} | 大小：{file_size:.2f} KB")

    # 读取文件的内容
    # .getvalue() 获取的是二进制数据
    # .decode("utf-8") 将二进制数据转换成我们能读懂的中文/英文文字
    text = uploader_file.getvalue().decode("utf-8")
    
    with st.spinner("正在上传文件到知识库中..."):
        time.sleep(1)
        result = st.session_state["service"].upload_by_string(text, file_name)
        st.write(result)

    