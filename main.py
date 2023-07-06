import os

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
# from langchain.schema import (
#     AIMessage,
#     HumanMessage,
#     SystemMessage
# )


from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

import models

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

llm = OpenAI(model_name=models.models['gpt3'], openai_api_key=OPENAI_API_KEY, temperature=0.9)

prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")

search = GoogleSearchAPIWrapper()
searchTool = Tool(
    name="Google Search",
    description="Search Google for recent results.",
    func=search.run,
)

tools = [*load_tools(["llm-math"], llm=llm), searchTool]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

x = agent.run(
    "What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?")
print(x)
