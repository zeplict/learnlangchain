from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key='sk-f533270f68b1475e9c33f6141808de76',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

print(model.invoke(messages))

## 不用chain的方法,model处理messages,parser处理result
from langchain_core.output_parsers import StrOutputParser

result = model.invoke(messages)

parser = StrOutputParser()

print(parser.invoke(result))

## 处理结果像链一样连接在一起
chain = model | parser

print(chain.invoke(messages))

## 使用prompt模板,prompt被分为若干组成部分： # template = ChatPromptTemplate.from_messages([ ("system", "You are a helpful AI bot.
# Your name is {name}."), ("human", "Hello, how are you doing?"), ("ai", "I'm doing well, thanks!"), ("human",
# "{user_input}"), ])
from langchain_core.prompts import ChatPromptTemplate

#模板的使用
system_template = "Translate the following into {language}:"

# prompt_template = ChatPromptTemplate.from_messages(
#     [("system",  "Translate the following into {language}:"), ("user", "{text}")]
# )
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

result = prompt_template.invoke({"language": "italian", "text": "hi"})

print(result)

print(result.to_messages())


# 结合三个组件，prompt模板处理，
chain = prompt_template | model | parser
print(chain.invoke({"language": "cantonese", "text": "晚上吃什么"}))

