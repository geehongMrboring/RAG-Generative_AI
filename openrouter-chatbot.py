import os
from openai import OpenAI
from dotenv import load_dotenv

def start_chat():
    # 1. 自动定位并加载 .env 文件（解决找不到路径的问题）
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))
    
    API_KEY = os.getenv("OPENROUTER_API_KEY")

    if not API_KEY:
        print("❌ 错误: 未读取到 API_KEY。请确保 .env 文件在脚本同级目录，且内容为: OPENROUTER_API_KEY=你的Key")
        return

    # 2. 初始化 OpenAI 客户端 (适配 OpenRouter)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )

    # 3. 初始化对话历史 (上下文记忆)
    messages = [
        {"role": "system", "content": "你是一个乐于助人的 AI 助手。"}
    ]

    print(f"✅ 机器人已上线 (当前模型: DeepSeek R1 Free)")
    print("👉 输入 '退出' 结束对话")
    print("-" * 40)

    while True:
        user_input = input("\n👤 你: ").strip()
        
        if user_input.lower() in ['exit', 'quit', '退出']:
            print("🤖 机器人: 下次见！")
            break
        
        if not user_input:
            continue

        # 加入用户消息
        messages.append({"role": "user", "content": user_input})

        print("🤖 AI: ", end="", flush=True)

        try:
            # 4. 调用 API (开启流式传输)
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=messages,
                stream=True
            )
            
            full_reply = ""
            
            # 5. 逐个字打印回复内容
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_reply += content
            
            print() # 换行

            # 将 AI 的回答存入记忆
            messages.append({"role": "assistant", "content": full_reply})
                
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    start_chat()