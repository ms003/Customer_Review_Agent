from dotenv import load_dotenv
from pathlib import Path
from config.settings import VM_SELENIUM_FILE
import os
from src.services.analyse_responses import analyse_pdf, format_output
from src.services.create_report import *
from src.services.analyse_reviews import analyse_df

dotenv_path = Path('../../.env')
load_dotenv(dotenv_path=dotenv_path)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")


df = pd.read_csv(VM_SELENIUM_FILE)

if __name__=='__main__':
    responses_dict = analyse_df(VM_SELENIUM_FILE, 'Content')
    second_response= analyse_pdf(responses_dict)
    analysis_dict = format_output(second_response)
    plot_sentiment(responses_dict, 'sentiment', 'Sentiment_Analysis')
    create_pdf_report(analysis_dict)











