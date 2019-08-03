# -*- encoding: utf-8 -*-
import json
import re

import pandas as pd


class TIPatterns(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TIPatterns, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.data_json = self.load_patterns()
        self.df = self.to_pandas()

    def load_patterns(self):
        with open('patterns.json', 'r') as f:
            return json.loads(f.read())

    def to_pandas(self):
        result = pd.DataFrame(data=self.data_json)
        result.data = result.data.apply(lambda x: x.encode('utf-8'))
        result.value = result.value.apply(lambda x: x.encode('utf-8'))
        return result

    def find_owntype(self, value):
        type_df = self.df[self.df.type == 'owntype']
        return self._find_by_dict(value, type_df)

    def find_realestatetype(self, value):
        type_df = self.df[self.df.type == 'realestatetype']
        return self._find_by_dict(value, type_df)

    def _find_by_dict(self, value, filtered_df):
        for index, row in filtered_df.iterrows():
            if row.is_regex:
                if row.is_case:
                    pattern = re.compile(row.data, re.IGNORECASE)
                else:
                    pattern = re.compile(row.data)
                result = re.findall(pattern, value)
                if result:
                    return row.value.lower()
            else:
                if row.data.lower() == value.lower():
                    return row.value.lower()
        return value

if __name__ == '__main__':
    ti_patterns = TIPatterns()
    ti_patterns.find_owntype(u'в собственности')
    # df = ti_patterns.to_pandas()
    t = 0