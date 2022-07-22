from pandas import pandas as pd
import sys

df: pd.DataFrame = pd.read_pickle('out/dataframe.pickle')
print(df.info())

df.sort_values(['description_text', 'url'], ascending=[True, True], inplace=True)

n_rows_before = len(df.index)
df.drop_duplicates(subset=['title', 'company_name', 'description_text'], keep='first', inplace=True)
n_rows_after = len(df.index)

# reorder the view
df = df[['company_rating', 'company_name', 'multiple_candidates', 'date_posted', 'title', 'company_location', 'salary',
         'estimated_salary', 'job_type', 'qualifications', 'description_text', 'benefits', 'hiring_insights',
         'company_indeed_profile_url', 'url']]
df.sort_values(['company_rating', 'company_name', 'title'], ascending=[False, True, True], inplace=True)
df.to_csv('out/search-mod.csv')
print(f'Dropped {n_rows_before - n_rows_after} duplicate rows')
