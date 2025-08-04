import asyncio

from dotenv import load_dotenv
load_dotenv()

# from langchain_groq.chat_models import ChatGroq
from langchain_openai.chat_models import ChatOpenAI


from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

client = MultiServerMCPClient(
    {
        "mcp_financas": {
            "url": "http://localhost:4200/mcp",
            "transport": "streamable_http",
        },
        # "mcp_financas": {
        #     "command": "python",
        #     "args": ["D:/AulasYoutube/tutorial_mcp_langgraph/server_mcp.py"],
        #     "transport": "stdio",
        # },
    }
)


async def create_graph():
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    # llm = ChatGroq(model="escolher_modelo_aqui", temperature=0)

    financas_tools = await client.get_tools()

    graph = create_react_agent(model=llm, tools=financas_tools, checkpointer=MemorySaver())

    return graph

async def main():
    config = {"configurable": {"thread_id": "conversa_1"}}
    agent = await create_graph()
    while True:
        message = input("User: ")
        response = await agent.ainvoke({"messages": [HumanMessage(content=message)]}, config=config)
        print("AI: " + response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
