from langchain_core.output_parsers import JsonOutputParser
import json
from langchain_community.document_loaders import WebBaseLoader


def load_url_content(url):
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content
    return page_data

def parse_listing(res):
    json_parser = JsonOutputParser()
    json_res = json_parser.parse(res.content)
    listing = json_res
    return listing


