import requests
import json
import yaml

# 读取配置文件
with open(r'config.yaml', 'r') as file:
    config = yaml.safe_load(file)

url = "https://api.360.cn/v1/chat/completions"

def chat1(input):
    payload = {
        "model": "360gpt-pro",
        "messages": [
            {
                "role": "user",
                "content": input
            }
        ],
        "stream": False,
        "temperature": 0.9,
        "max_tokens": 2048,
        "top_p": 0.5,
        "top_k": 0,
        "repetition_penalty": 1.05,
        "num_beams": 1,
        "user": "andy"
    }
    headers = {
        'Authorization': f'Bearer {config["360_key"]}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 检查请求是否成功
        answer = response.json()
        return answer['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"解析响应错误: {e}")
        return None
