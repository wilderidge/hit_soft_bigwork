from pathlib import Path
from openai import OpenAI

client = OpenAI(
    api_key="sk-efa4612fff8c4f188745929f9553e1c8",  # 替换成真实DashScope的API_KEY
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务endpoint
)


def qw_chat(context, question):
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                'role': 'system',
                'content': 'You are a helpful assistant.'
            },
            {
                'role': 'system',
                'content': context
            },
            {
                'role': 'user',
                'content': question
            }
        ],
        stream=True
    )
    print("正在生成对话...")
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    print("对话生成完毕,结果如下:")
    print(response)
    return response
