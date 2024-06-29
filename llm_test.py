import os

from langchain_community.llms import Tongyi
os.environ["DASHSCOPE_API_KEY"] = "sk-7fe065bd9c5f487f8a36373b864c6e06"
llm = Tongyi(model_name="qwen-plus")
print(llm.invoke("你好"))
