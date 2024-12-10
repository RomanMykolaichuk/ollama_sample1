
from crewai import Agent, Task, Crew, Process
import os

from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "llama3",
    base_url = "http://localhost:11434/v1")





email = "You are invited on the conference to learn more about LLM. Please confirm your participation asap"
is_verbose = True

classifier = Agent(
    role = "email_classifier",
    maxiter = 2,
    llm=llm,
    goal = f"accuratelly classify '{email}' based on their body into classes: important, common, spam. return only one word - class name",
    backstory = "You are an AI assistant that will classify emails into classes: important, common, spam. You will receive only email body. Your mission is to help user manage their email inbox and prioritize their emails.",
    )

responder = Agent(
    role = "responder",
    maxiter = 2,
    llm=llm,
    goal = "respond to user's emails based on its importance, respond to important emails first theb to common emails and ignore spam emails. Write simple text response",
    backstory = "You are an AI assistant that will respond to user's emails. Your mission is only respond to email accuratelly and honestly.",    
    )

classify_email = Task(
    description = "classify_email",
    agent = classifier,       
    expected_output="important or common or spam"
    )

respond_to_email = Task(
    description = "respond_to_email based on importantce returning by 'classifier' agent.",
    agent = responder,
    context = [classify_email],
    expected_output="email response, only body text"   
    )   

crew = Crew(
    agents=[classifier, responder],
    maxprm = 20,
    tasks = [classify_email, respond_to_email],
    verbose=2,
    process=Process.sequential
    )   

output = crew.kickoff()

print(output, classify_email.output)