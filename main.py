# pip3 install langchain_openai
# python3 deepseek_v2_langchain.py
from langchain_openai import ChatOpenAI


def generate_pet_name():  # 定义一个函数generate_pet_name
    llm = ChatOpenAI(
        model='deepseek-chat',
        openai_api_key='sk-f533270f68b1475e9c33f6141808de76',
        openai_api_base='https://api.deepseek.com',
        max_tokens=1024
    )

    # 使用OpenAI模型生成宠物名字。这里的字符串是向模型提供的提示，模型会基于此生成宠物名字。
    name = llm.invoke("I have a dog pet and I want a cool name for it. Suggest me five cool names for my pet.").content

    return name  # 返回生成的名字


# 当该脚本作为主程序运行时，执行以下代码
if __name__ == "__main__":
    print(generate_pet_name())  # 调用generate_pet_name函数，并打印返回的结果
