import requests
from fake_useragent import UserAgent


class Request:
    def __init__(self):
        pass

    def build_url(self, data_type, match_type, view_type, template, page_num):
        return f"https://stats.espncricinfo.com/ci/engine/stats/index.html?" \
               f"type={data_type};" \
               f"class={match_type};" \
               f"view={view_type};" \
               f"template={template};" \
               f"page={page_num}"

    def get_url_object_with_agent(self, url):
        ua = UserAgent()
        header = {"User-Agent": str(ua.random)}
        return requests.get(url, headers=header).text
