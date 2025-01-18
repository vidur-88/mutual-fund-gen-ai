import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()
IS_GROQ_ENABLED = False


class MFDataAnalysis(object):
    def __init__(self):
        if IS_GROQ_ENABLED:
            self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")
        else:
            self.llm = Ollama(model="deepseek-coder")  # "phi3:latest")  # "llama3.2:1b")

    def mf_data_analysis(self, data):
        prompt_extract = PromptTemplate.from_template(
            """
            ### ANALYSE MUTUAL FUND DATA
            {mutual_fund_data}
            ### INSTRUCTION:
            The data is for mutual fund schemes.
            Your job is to extract the mutual fund with best to invest with diff diff categories and 
            return them in JSON format containing the following keys: 
            `mf type`, `scheme name`, `category name`, `crisil rating`, `aum`, `turnover`,
            `rank in category`, `standard deviation`, `sharpe ratio`, `treynor ratio`, `jenslon alpha`, 
            `1yr-return`, `2yr-return`, `3yr-return`, `5yr-return`, `sip returns`, `monthly return`, `quarterly return`, 
            `equity distribution`, `debt distribution`,  `stock allocation`, `govt bond allocation`, `corporate bond allocation`, 
            `cash allocation`, `stock holding`, `govt bond holding`, `corporate bond holding`, `cash holding`,
            `nav`, `nav data`, `52W high`, `52WH as on`, `52W low`, `52WL as on`
            Map all data based on unique scheme name, not mapped randomly.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"mutual_fund_data": data})
        if IS_GROQ_ENABLED:
            try:
                json_parser = JsonOutputParser()
                res = json_parser.parse(res.content)
                print(res)
            except OutputParserException:
                raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def mf_query_result(self, data):
        prompt_query = PromptTemplate.from_template(
            """
            ### Mutual Fund Recommendation:
            {mutual_fund_recommendation}

            ### INSTRUCTION:
            You are XYZ, a investor to invest money for mixture of short term, mid term and long term.
            Need good mutual funds recommendation with full scheme name based on its historical returns i.e 1yr, 2yr, 3yr, 5yr, sip return
            crisil rating, rank in category, risk ratio with lower standard deviation, higher sharpe ratio, higher treynor ratio 
            and for long term consider higher jenslon alpha ratio, stock allocation, debt allocation overall, cash allocation,
            annual return, quarterly return, monthly return, aum value and nav, nav date, nav 52W high, nav 52WH as on, nav 52W low, 52WL as on. 
            It has mixed of equity distribution of large cap, small cap, mid cap
            and debt distribution of private bond, government bond, aum more than 10000 cr, historical higher return
            I need at least 5 mutual funds to invest for long term, 3 mutual funds to invest mid term,
            and 2 mutual funds to invest short term
            Only, recommend which have given return more than 10% for 1-yr
            ### RECOMMENDATION VALID JSON (NO PREAMBLE):

            """
        )
        chain_recom = prompt_query | self.llm
        res = chain_recom.invoke({"mutual_fund_recommendation": data})
        if IS_GROQ_ENABLED:
            return res.content
        return res


if __name__ == "__main__":
    import sys
    print(os.getenv("GROQ_API_KEY"))