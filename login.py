import yaml

try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f) or {}
except FileNotFoundError:
    config = {}

required_keys = ['appid', 'secret', 'kimi_key', 'xunfei_appid', 'xunfei_key', 'xunfei_secret', '360_key']

for key in required_keys:
    config[key] = input(f"请输入{key}：")

with open('config.yaml', 'w') as f:
    yaml.dump(config, f)

print("保存成功！")
