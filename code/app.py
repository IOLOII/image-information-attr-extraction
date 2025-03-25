# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import os
import requests
import re
import json
import logging
import oss2
from auth import auth_login, require_login

app = Flask(__name__)

endpoint = os.environ['OSS_ENDPOINT']
auth = oss2.StsAuth(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'],
                    os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'])
bucket = oss2.Bucket(auth, endpoint, os.environ['OSS_BUCKET'])


app.config['UPLOAD_FOLDER'] = './'
app.config['ALLOWED_EXTENSIONS'] = {'jpeg', 'png', 'jpg'}


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/login', methods=['POST', 'GET'])
def login():
    return auth_login()


@app.route('/', methods=['GET'])
@require_login
def index():
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
@require_login
def handle_upload():
    try:
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        result = bucket.put_object(file.filename, file.stream)
        if result.status == 200:
            oss_sign_url = bucket.sign_url('GET', file.filename, 3600)
            data = {'url': oss_sign_url}
            return jsonify({'code': 200, 'data': data})
        else:
            return jsonify({'code': 200, 'data': {}})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/completions', methods=['POST'])
@require_login
def handle_completions():
    try:
        data = request.json
        oss_url = data.get('url')
        prompt = data.get('prompt', '')
        response = curl_request(oss_url, prompt)
        data = None
        if response.status_code == 200:
            logging.info("Response: %s", response.json())
            resp_content = response.json()['choices'][0]['message']['content']
            logging.info("resp_content: %s", resp_content)
            data = extract_code_blocks(resp_content)
            logging.info("extract_code_blocks resp_content: %s", data)
            data = json.loads(data)
        if data is None:
            return jsonify({'code': 400, 'data': {}})
        return jsonify({'code': 200, 'data': data, 'src': oss_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def curl_request(oss_url, prompt):
    logger = logging.getLogger()
    api_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer ' + os.environ['DASHSCOPE_API_KEY'],
        'Content-Type': 'application/json; charset=utf-8'
    }
    data = {
        'model': 'qwen-vl-max',
        'messages': [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': '回答用JSON返回结果，key必须使用中文，JSON数据格式必须正确,百分数用字符串返回。例如："0.1%"。'
                    },
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': oss_url
                        }
                    },
                    {
                        'type': 'text',
                        'text': "请提取信息"
                    },
                    {
                        'type': 'text',
                        'text': prompt
                    }
                ]
            }
        ]
    }
    logger.info(f"data: {data}")
    post_data = json.dumps(data, ensure_ascii=False, indent=4)
    return requests.post(api_url, data=post_data.encode('utf-8'), headers=headers)


def extract_code_blocks(text):
    pattern = r'```json\n(.*?)```'
    code_blocks = re.findall(pattern, text, re.DOTALL)
    return code_blocks[0] if code_blocks else ''


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
