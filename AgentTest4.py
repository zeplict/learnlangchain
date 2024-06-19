import getpass
import os

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

model = ChatOpenAI(openai_api_key='sk-mS76xCwq11FuBZdLw0CIbvQIezBqjrHPamw4oDOamTZD2XQx',base_url="https://api.chatanywhere.tech/v1")

from langchain_core.messages import HumanMessage
# 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
os.environ["TAVILY_API_KEY"] = getpass.getpass()
tavily_tool = TavilySearchResults()
tools = [tavily_tool]

# response = model.invoke([HumanMessage(content="hi!")])
# print(response.content)
model_with_tools = model.bind_tools(tools)
#
# response = model_with_tools.invoke([HumanMessage(content="Hi!")])
# print(response)
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

# response = model_with_tools.invoke([HumanMessage(content="Hi,what's the capital of America?")])
#
# print(response)
# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")
from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(model, tools)

response = agent_executor.invoke({"messages": [HumanMessage(content="hi!")]})

print(response["messages"])

response = agent_executor.invoke(
    {"messages": [HumanMessage(content="whats the weather in sf?")]}
)
print(response["messages"])

for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="whats the weather in sf?")]}
):
    print(chunk)
    print("----")


async for event in agent_executor.astream_events(
        {"messages": [HumanMessage(content="whats the weather in sf?")]}, version="v1"
):
    kind = event["event"]
    if kind == "on_chain_start":
        if (
                event["name"] == "Agent"
        ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
            print(
                f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
            )
    elif kind == "on_chain_end":
        if (
                event["name"] == "Agent"
        ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
            print()
            print("--")
            print(
                f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
            )
    if kind == "on_chat_model_stream":
        content = event["data"]["chunk"].content
        if content:
            # Empty content in the context of OpenAI means
            # that the model is asking for a tool to be invoked.
            # So we only print non-empty content
            print(content, end="|")
    elif kind == "on_tool_start":
        print("--")
        print(
            f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
        )
    elif kind == "on_tool_end":
        print(f"Done tool: {event['name']}")
        print(f"Tool output was: {event['data'].get('output')}")
        print("--")