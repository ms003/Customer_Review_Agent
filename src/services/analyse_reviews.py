from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd
from src.prompts.templates import *
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser




def analyse_df(name:str,col:str):

        chatgpt = ChatOpenAI(model='gpt-4o-mini', temperature=0.5)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(name)
        reviews_column = df[col]
        reviews = [f"""{review}""" for review in reviews_column]
        print(reviews)
        parser = PydanticOutputParser(pydantic_object=ReviewAnalysisResponse)

        prompt_txt = """
                     Analyze the given customer review below and \
                     generate the response based on the instructions
                     mentioned below in the format instructions.

                     Format Instructions:
                     {format_instructions}

                     Review:
                     {review}
                    """

        prompt = PromptTemplate(
            template=prompt_txt,
            input_variables=["review"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = (prompt
                 |
                 chatgpt
                 |
                 parser)

        reviews_formatted = [{'review': review} for review in reviews]
        reviews_formatted

        responses = chain.map().invoke(reviews_formatted)
        responses_dict = [x.dict() for x in responses]

        return responses_dict

