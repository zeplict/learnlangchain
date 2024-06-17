from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key='sk-c18dc9b32dd34b50bbe80c99a9cb9ca1',
    openai_api_base='https://api.deepseek.com',
    max_tokens=1024
)

from langchain_core.messages import HumanMessage

print("测试无上下文的方式")
print(model.invoke([HumanMessage(content="Hi! I'm Bob")]))
print(model.invoke([HumanMessage(content="What's my name?")]))
# content="Hello Bob! It's nice to meet you. How can I assist you today?" response_metadata={'token_usage': {'completion_tokens': 18, 'prompt_tokens': 13, 'total_tokens': 31}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_a49d71b8a1', 'finish_reason': 'stop', 'logprobs': None} id='run-3d133751-0660-4be9-967b-f91302c9c8b2-0' usage_metadata={'input_tokens': 13, 'output_tokens': 18, 'total_tokens': 31}
# content='I\'m sorry, but I don\'t have access to personal information unless it has been shared with me in the course of our conversation. If you tell me your name, I can address you by it. Otherwise, I can use a generic term like "you" or "user."' response_metadata={'token_usage': {'completion_tokens': 59, 'prompt_tokens': 13, 'total_tokens': 72}, 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_a49d71b8a1', 'finish_reason': 'stop', 'logprobs': None} id='run-f267781e-c79f-48d2-9406-5586064d087f-0' usage_metadata={'input_tokens': 13, 'output_tokens': 59, 'total_tokens': 72}
# 这表明它并没有上下文记忆能力

from langchain_core.messages import AIMessage

print("测试传入上下文")
#传入了上下文，这种方式有点意思
print(model.invoke(
    [
        HumanMessage(content="Hi! I'm Bob"),
        AIMessage(content="Hello Bob! How can I assist you today?"),
        HumanMessage(content="What's my name?"),
    ]
))

##Message History实例，可以跟踪输入输出上下文
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

# 通过session_id拿记录。这里关键在于，这里配了with_message
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

#这是关键，通过一个RunnableWithMessageHistory得到能够记录History的runnable。
with_message_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

response = with_message_history.invoke(
    [HumanMessage(content="Hi! I'm Bob")],
    config=config,
)

print("测试通过通过一个RunnableWithMessageHistory得到能够记录History的runnable")
print(response.content)

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print(response.content)

# 换了session_id，就记不住了，因为是
config = {"configurable": {"session_id": "abc3"}}

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)
print("测试换了session_id结果")
print(response.content)

config = {"configurable": {"session_id": "abc2"}}

response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print("测试回到原来的session")
print(response.content)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

response = chain.invoke({"messages": [HumanMessage(content="hi! I'm bob")]})

print("测试ChatPromptTemplate+MessagesPlaceholder，chain = prompt | model")
print(response.content)

with_message_history = RunnableWithMessageHistory(chain, get_session_history)

config = {"configurable": {"session_id": "abc5"}}

response = with_message_history.invoke(
    [HumanMessage(content="Hi! I'm Jim")],
    config=config,
)

print("RunnableWithMessageHistory(chain, get_session_history)")
print(response.content)


response = with_message_history.invoke(
    [HumanMessage(content="What's my name?")],
    config=config,
)

print("测试这回记不记得住上下文")
print(response.content)





print("测试更复杂的prompt，这里注意是先注册模板后传入变量")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = prompt | model

response = chain.invoke(
    {"messages": [HumanMessage(content="hi! I'm bob")], "language": "Spanish"}
)

print(response.content)


print("测试 wrap this more complicated chain in a Message History class")
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

config = {"configurable": {"session_id": "abc11"}}

response = with_message_history.invoke(
    {"messages": [HumanMessage(content="whats my name?")], "language": "Spanish"},
    config=config,
)

print(response.content)

print("限制存储的上下文大小")

from langchain_core.runnables import RunnablePassthrough

def filter_messages(messages, k=10):
    return messages[-k:]

chain = (
    RunnablePassthrough.assign(messages=lambda x: filter_messages(x["messages"]))
    | prompt
    | model
)

messages = [
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]


response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="what's my name?")],
        "language": "English",
    }
)

print("测试超过阈值的记录不会被查到")
print(response.content)

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

config = {"configurable": {"session_id": "abc20"}}

response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="what's my fav ice cream")],
        "language": "English",
    }
)

print("测试没超过的")
print(response.content)

print("包在Message History里")

with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)

config = {"configurable": {"session_id": "abc20"}}

response = with_message_history.invoke(
    {
        "messages": messages + [HumanMessage(content="whats my name?")],
        "language": "English",
    },
    config=config,
)

print(response.content)

response = with_message_history.invoke(
    {
        "messages": [HumanMessage(content="whats my favorite ice cream?")],
        "language": "English",
    },
    config=config,
)
print("这回记录变多了，关于冰淇淋的上下文他也记不住了")
print(response.content)


print("为了提高交互和用户体验，引入流式返回")

config = {"configurable": {"session_id": "abc15"}}
for r in with_message_history.stream(
    {
        "messages": [HumanMessage(content="hi! I'm todd. tell me a joke")],
        "language": "English",
    },
    config=config,
):
    print(r.content, end="|")