from crewai import LLM, Agent, Task
import os

llm = LLM(
    model="qwen-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

prompt = "What is the capital of France?"
response = llm.call([{"role": "user", "content": prompt}])
print(response)

agent = Agent(
    role="Assistant",
    goal="Answer the question",
    backstory="You are a helpful assistant that can answer questions.",
    llm=llm,
    verbose=True,
)

task = Task(
    description="Answer the question",
    expected_output="The capital of France is Paris.",
    agent=agent,
)

result = agent.execute_task(task)
print(result)