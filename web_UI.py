# app.py
from flask import Flask, render_template, Response, request, jsonify
import subprocess
import threading
import time
import re
import webbrowser
import yaml

# 读取配置文件
with open(r'config.yaml', 'r') as file:
    config = yaml.safe_load(file)
app = Flask(__name__)

# 用于标记命令行输出
output_stream = []
output_stream_lock = threading.Lock()

def strip_ansi_escape(line):
    """
    去除ANSI转义序列。
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', line)

def run_group_py(output_callback):
    """
    运行 group.py 并实时输出命令行日志。
    """
    try:
        process = subprocess.Popen(
            ["python", "group.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # 行缓冲，实时输出
        )

        # 实时读取输出并发送到回调函数
        for line in iter(process.stdout.readline, ''):
            cleaned_line = strip_ansi_escape(line.rstrip())
            output_callback(cleaned_line)  # 确保每行日志正确显示

        process.stdout.close()
        process.wait()

    except Exception as e:
        output_callback(f"Error running bot: {str(e)}")
    finally:
        if process.poll() is None:  # 确保子进程在异常情况下也被关闭
            process.terminate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_bot():
    # 启动 group.py 文件
    threading.Thread(target=run_group_py, args=(stream_output,)).start()
    return "Bot started!", 200

def stream_output(line):
    """
    通过 SSE 将输出发送到客户端。
    """
    with output_stream_lock:
        output_stream.append(line)  # 将输出添加到全局输出流列表

@app.route('/logs')
def logs():
    """
    将命令行日志实时发送到网页。
    """
    def generate():
        previous_output = 0
        while True:
            with output_stream_lock:
                current_output = len(output_stream)
                if current_output > previous_output:
                    data = output_stream[previous_output:current_output]
                    yield 'data: ' + '\n'.join(data) + '\n\n'  # 发送每行日志并换行
                    previous_output = current_output
            time.sleep(0.1)

    return Response(generate(), mimetype='text/event-stream')

@app.route('/login', methods=['POST'])
def xunfei_login():
    data = request.json
    appid = data.get('appid')
    appsercet = data.get('appsercet')
    appkey = data.get('appkey')
    config['xunfei_appid'] = appid
    config['xunfei_secret'] = appsercet
    config['xunfei_key'] = appkey
    save_config()
    return jsonify({'status': 'success'}), 200

@app.route('/kimi-login', methods=['POST'])
def kimi_login():
    data = request.json
    config['kimi_key'] = data.get('appid')
    save_config()
    return jsonify({'status': 'success'}), 200

@app.route('/ai360-login', methods=['POST'])
def ai360Login():
    data = request.json
    config['360_key'] = data.get('appid')
    save_config()
    return jsonify({'status': 'success'}), 200

@app.route('/qq-login', methods=['POST'])
def qqLogin():
    data = request.json
    config['appid'] = data.get('account')
    config['secret'] = data.get('password')
    save_config()
    return jsonify({'status': 'success'}), 200

def save_config():
    with open(r'config.yaml', 'w') as file:
        yaml.dump(config, file)

if __name__ == '__main__':
    port = 5000
    url = f'http://127.0.0.1:{port}/'

    threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, port=port)).start()

    time.sleep(1)
    webbrowser.open(url)
