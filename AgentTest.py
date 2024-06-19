# 导入所需库和模块
# 1. 从langchain_anthropic导入ChatAnthropic类，用于与Anthropic的模型交互
from langchain_anthropic import ChatAnthropic
# 2. 导入TavilySearchResults类，这是来自社区工具的一个搜索功能，用于获取搜索结果
from langchain_community.tools.tavily_search import TavilySearchResults
# 3. 引入HumanMessage类，用于构造人类消息，作为输入给AI模型
from langchain_core.messages import HumanMessage
# 4. 引入SqliteSaver类，用于创建基于SQLite的内存数据库，保存代理的状态或记忆
from langgraph.checkpoint.sqlite import SqliteSaver
# 5. 引入create_react_agent函数，用于快速创建具有特定功能的代理
from langgraph.prebuilt import create_react_agent

# 创建代理组件
# 初始化内存中的SQLite数据库作为代理的记忆存储
memory = SqliteSaver.from_conn_string(":memory:")

# 选择Anthropic的Claude模型，此处使用的是"claude-3-sonnet-20240229"版本
model = ChatAnthropic(model_name="claude-3-sonnet-20240229")

# 配置搜索工具，允许每次搜索返回最多两个结果
search = TavilySearchResults(max_results=2)

# 定义代理将使用的工具列表，当前只包含搜索工具
tools = [search]

# 创建反应式代理实例，该代理结合了模型、工具和记忆存储
# 这里使用create_react_agent函数完成代理的快速搭建
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# 使用代理进行交互
# 第一次互动：用户介绍自己
# 构造消息并使用代理的stream方法进行交互，同时传递配置信息
for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="hi im bob! and i live in sf")]},
        config={"configurable": {"thread_id": "abc123"}}
):
    # 打印代理处理的每一块响应内容
    print(chunk)
    # 使用"----"分隔每次输出，便于阅读
    print("----")

# 第二次互动：询问天气
# 用户询问他们所在地的天气情况
for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="whats the weather where I live?")]},
        config={"configurable": {"thread_id": "abc123"}}
):
    # 同样，打印每次从代理接收到的响应块
    print(chunk)
    # 分割符保持输出清晰
    print("----")