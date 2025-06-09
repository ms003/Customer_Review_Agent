from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.output_parsers import PydanticOutputParser
import pandas as pd
from langchain_openai import ChatOpenAI
from src.prompts.templates import *
import json


def analyse_pdf(responses_dict:dict):
    df = pd.DataFrame(responses_dict)
    # Set up the parser
    parser = PydanticOutputParser(pydantic_object=ReviewDf)
    prompt_txt = """
    Analyze the given dataframe and generate the response based on the instructions
    mentioned below in the format instructions.
    
    Format Instructions:
    {format_instructions}
    
    Dataframe:
    {df}
    """
    prompt = PromptTemplate(
        template=prompt_txt,
        input_variables=["df"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chatgpt = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)
    agent_executor = create_pandas_dataframe_agent(
        llm=chatgpt,
        df=df,
        agent_type="tool-calling",
        allow_dangerous_code=True,
        verbose=False,
    )

    # Format the prompt with the DataFrame
    formatted_prompt = prompt.format(df=df)

    # Invoke the agent executor
    response = agent_executor.invoke(formatted_prompt)

    # Print the output
    print(response["output"])
    return response



def format_output(response):
    json_string = response['output'].strip('```json').strip('```').strip()
    analysis_dict = json.loads(json_string)
    return pd.DataFrame([analysis_dict])


