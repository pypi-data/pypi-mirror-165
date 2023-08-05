import pandas as pd
from .request_utilities import Request
from .multithreading_utilities import MultiThread


class ESPN:
    def __init__(self, data_type='batting', match_type='Test', view_type=''):
        self.req_util = Request.Request()
        self.match_types = {'Test': '1', 'ODI': '2', 'T20': '3', 'All': '11',
                            'Test_Women': '8', 'ODI_Women': '9', 'T20_Women': '10',
                            'Test_Youth': '20', 'ODI_Youth': '21', 'T20_Youth': '22'}
        self.match_type = self.match_types[match_type]
        self.data_type = data_type
        self.view_type = view_type
        self.template = 'results'
        self.result_set = pd.DataFrame()
        self.list_of_dataframes = []

    def __raise_exception(self, e):
        print("An error occurred. Please report bug at https://github.com/SanketPatole/ESPN-Statsguru-Scraper/issues")
        print("Alternatively, you can report bug at snkt.pat2@gmail.com.")
        print(e)
        print("An error occurred. Please report bug at https://github.com/SanketPatole/ESPN-Statsguru-Scraper/issues")
        print("Alternatively, you can report the bug at snkt.pat2@gmail.com.")

    def __get_number_of_pages(self, trial_count=0):
        try:
            url = self.req_util.build_url(self.data_type, self.match_type, self.view_type, self.template, page_num=1)
            url_object = self.req_util.get_url_object_with_agent(url)
            data = pd.read_html(url_object)
            return int(str(data[1][0]).split("\n")[0].split(" ")[7])
        except Exception as e:
            if trial_count < 10:
                return self.__get_number_of_pages(trial_count=trial_count + 1)
            else:
                self.__raise_exception(e)
                exit(1)

    def __fetch_data(self, page_num, trial_count=0):
        try:
            url = self.req_util.build_url(self.data_type, self.match_type, self.view_type, self.template,
                                          page_num=page_num)
            url_object = self.req_util.get_url_object_with_agent(url)
            data = pd.read_html(url_object)[2]
            if self.view_type in ['series', 'ground', 'host', 'opposition']:
                new_column_names = list(data.columns) + [self.view_type]
                data = pd.concat([data.iloc[::2].reset_index(drop=True),
                                  data.iloc[1::2].iloc[:, 0].reset_index(drop=True)], axis=1)
                data.columns = new_column_names
            self.list_of_dataframes[page_num - 1] = data
        except Exception as e:
            if trial_count < 10:
                self.__fetch_data(page_num, trial_count=trial_count + 1)
            else:
                self.__raise_exception(e)
                exit(1)

    def get_score(self, number_of_pages=99999):
        try:
            self.result_set = pd.DataFrame()
            number_of_pages = min(self.__get_number_of_pages(), number_of_pages)
            self.list_of_dataframes = [pd.DataFrame() for _ in range(number_of_pages)]
            function_arguments = [page_num + 1 for page_num in range(number_of_pages)]
            MultiThread.MultiThread(function=self.__fetch_data, arguments=function_arguments).run()
            result = pd.concat(self.list_of_dataframes, axis=0, ignore_index=True)
            return result[[col for col in result.columns if 'Unnamed' not in col]]
        except Exception as e:
            self.__raise_exception(e)
            exit(1)
