import autogen

config_list = autogen.config_list_from_json("./config.json")

# User Agent: Oversees the task and approves the plan
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin overseeing code execution tasks. You approve plans and monitor execution.",
    code_execution_config={
        "work_dir": "code",
        "use_docker": False  
    },
    human_input_mode="TERMINATE",  # Close session after task completion
)

# Code Generator Agent (Developer): Generates and executes code
developer = autogen.AssistantAgent(
    name="Developer",
    llm_config={"config_list": config_list},
    system_message="""Developer. You write Python/Shell code to solve tasks. It should include ways to handle edge cases and also proper error management. It should also include a way to check input and validate it. Save the code to disk, and ensure it is 
    wrapped in a code block specifying the script type and file name. And use normal tests and show inputs and the outputs explicity""",
)

# Planner Agent: Plans the task
describe = autogen.AssistantAgent(
    name="Planner",
    system_message="""Describer. Describe the code written by the developer. Explain the code in detail, including the logic and the expected output. Provide a detailed explanation of the code, including the logic and the expected output.""",
    llm_config={"config_list": config_list},
)



            
user_task = input("Please enter the task you want to be done: ")

# Create the initial message for the planner
message = f"{user_task}. The Developer should write the code, execute it, and return the result. Then Describe agent should describe the code in detail."

# Group Chat: Facilitates communication between agents
group_chat = autogen.GroupChat(
    agents=[user_proxy, developer, describe],
    messages=[], 
    max_round=3# Maximum number of rounds for the task
)


manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": config_list},
)

# Initiate the chat
user_proxy.initiate_chat(
    manager,
    message= message
)
