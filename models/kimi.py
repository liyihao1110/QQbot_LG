from openai import OpenAI
import yaml
# 读取配置文件
with open(r'config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    
client = OpenAI(
    api_key = config['kimi_key'],
    base_url = "https://api.moonshot.cn/v1",
)
 
history = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
]
 
def chat1(query, history):
    history.append({
        "role": "user", 
        "content": query
    })
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    history.append({
        "role": "assistant",
        "content": result
    })
    return result

def chat(input):
    return chat1(input, history)