from langchain_community.document_loaders import WebBaseLoader
from app.utils.clean_text import clean_text


class WebParser(object):
    def __init__(self, url_input):
        self.url_input = url_input

    def get_web_data(self):
        try:
            web_loader = WebBaseLoader([self.url_input])
            return clean_text(web_loader.load().pop().page_content)
        except Exception as e:
            print("Error while parsing web page, error: {}".format(e.args))
