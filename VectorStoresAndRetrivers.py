# pip install langchain langchain-chroma langchain-openai
# sk-proj-GzD2dqcO3bwNzIXCJswaT3BlbkFJIuNrml5IP7mfCj4eIBkr

# export LANGCHAIN_TRACING_V2="true"
# export LANGCHAIN_API_KEY="sk-proj-GzD2dqcO3bwNzIXCJswaT3BlbkFJIuNrml5IP7mfCj4eIBkr"
# 一堆文档
# import getpass
# import os
#
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
import asyncio
from langchain_core.documents import Document
import nest_asyncio
nest_asyncio.apply()

# 导入 asyncio
import asyncio
documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

# 向量数据库
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(openai_api_key='sk-mS76xCwq11FuBZdLw0CIbvQIezBqjrHPamw4oDOamTZD2XQx',base_url="https://api.chatanywhere.tech/v1"),
)

print(vectorstore.similarity_search("cat"))


# print("异步调用")
import asyncio

# 假设 vectorstore 是某个库的对象，先导入该库
# import vectorstore_library

# async def search_cat():
#     # 初始化 vectorstore 对象
#     # vectorstore = vectorstore_library.VectorStore()
#
#     # 异步调用 asimilarity_search 方法
#     results = await vectorstore.asimilarity_search("cat")
#
#     # 处理搜索结果
#     for result in results:
#         print(result)

# 运行异步函数
# asyncio.run(search_cat())

# print("运行打分")
# print(vectorstore.similarity_search_with_score("cat"))

print("Return documents based on similarity to a embedded query:")
embedding = OpenAIEmbeddings(openai_api_key='sk-mS76xCwq11FuBZdLw0CIbvQIezBqjrHPamw4oDOamTZD2XQx',base_url="https://api.chatanywhere.tech/v1").embed_query("cat")
# print(vectorstore.similarity_search("cat"))
print(vectorstore.similarity_search_by_vector(embedding))


from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # 选择最优结果

print(retriever.batch(["cat", "shark"]))
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(openai_api_key='sk-mS76xCwq11FuBZdLw0CIbvQIezBqjrHPamw4oDOamTZD2XQx',base_url="https://api.chatanywhere.tech/v1",model="gpt-3.5-turbo-0125")


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

response = rag_chain.invoke("tell me about cats")

print(response.content)