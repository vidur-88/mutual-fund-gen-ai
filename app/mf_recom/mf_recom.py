import time

from app.mf_recom.mf_data_analysis import MFDataAnalysis
from app.utils.clean_text import clean_text
from app.utils.read_mf_data import ReadMFData


class MFRecom(object):
    def __init__(self):
        self.input_data = self.get_mf_data()
        self.llm_data = []
        self.recom_data = []

    def get_mf_data(self):
        read_mf_data = ReadMFData()
        read_mf_data.get_all_files("../../resource")
        read_mf_data.read_mf_data()
        return read_mf_data.get_mf_data()

    def mf_recom(self):
        mf_data_analysis = MFDataAnalysis()
        start_index = 0
        size_of_data = 2
        while len(self.input_data) > start_index:
            break
            try:
                self.llm_data += mf_data_analysis.mf_data_analysis(self.input_data[start_index:start_index+size_of_data])
                start_index += size_of_data
                time.sleep(70)
            except Exception as e:
                print(e.args)
            if start_index > 10:
                break
        print(start_index)
        self.recom_data = mf_data_analysis.mf_query_result(self.input_data)


if __name__ == "__main__":
    mf_recom = MFRecom()
    mf_recom.mf_recom()
    print(mf_recom.recom_data)


# def create_streamlit_app(llm, portfolio, clean_text):
#     st.title("📧 Cold Mail Generator")
#     url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
#     submit_button = st.button("Submit")
#
#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             data = clean_text(loader.load().pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(data)
#             for job in jobs:
#                 skills = job.get('skills', [])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job, links)
#                 st.code(email, language='markdown')
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")
#
#
# if __name__ == "__main__":
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     create_streamlit_app(chain, portfolio, clean_text)