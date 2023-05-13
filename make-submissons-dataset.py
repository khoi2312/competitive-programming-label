import pandas as pd
import os
import json

DATA_PATH = './codeforces-dataset/contests/'
FILE_NAMEs = [_ for _ in os.listdir(DATA_PATH) if _.endswith('.csv')]

with open('./data/tags.json') as f:
    tags_dataset = json.load(f)

cpp_langs = \
    {'GNU C++17', 'GNU C++14', 'GNU C++11', 'GNU C++', \
     'GNU C++17 (64)', 'GNU C++20 (64)'}

metadata = ['contest_id', 'submission_id', 'author', \
            'language', 'problem', 'source_code']

for f in FILE_NAMEs:
    df = pd.read_csv(open(DATA_PATH + f, 'r'), encoding='utf-8', engine='c')
    df = df[(df['verdict'] == 'Accepted') \
                & (df['language'].isin(cpp_langs))]
    df = df[metadata]
    df['problem'] = df['problem'].apply(lambda x: x.split('\n')[0])
    df = df[df['problem'].isin(tags_dataset)]

    df.to_csv('./data/submission/' + f, index=False)
    os.remove(DATA_PATH + f)
