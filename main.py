from TheSearch import TheSearch, Filters
from utils import cleanup, create_project
from pandas import pandas as pd
import pickle


def main():
    cleanup()
    create_project()

    reactSearches = [
        TheSearch(
            what="react frontend developer",
            where="Los Angeles",
            age=Filters.Age.FOURTEEN,
            radius=Filters.Radius.EXACT,
            experience=Filters.Experience.ENTRY
        ), TheSearch(
            what="react frontend developer",
            where="Los Angeles",
            age=Filters.Age.FOURTEEN,
            radius=Filters.Radius.EXACT,
            experience=Filters.Experience.MID
        )
    ]
    # pythonSearches = [
    #     TheSearch(
    #         what="python developer",
    #         where="Los Angeles",
    #         age=Filters.Age.FOURTEEN,
    #         radius=Filters.Radius.EXACT,
    #         experience=Filters.Experience.ENTRY
    #     ), TheSearch(
    #         what="python developer",
    #         where="Los Angeles",
    #         age=Filters.Age.FOURTEEN,
    #         radius=Filters.Radius.EXACT,
    #         experience=Filters.Experience.MID
    #     )
    # ]

    mySearches = [
        *reactSearches,
        # *pythonSearches // TODO this is commented to reduce the scope of the query for testing the bootstrap-table
    ]
    job_list = []
    for one_search in mySearches:
        for page in one_search.pages:
            for beacon in page.beacons:
                job_list.append(beacon.dict)
    df = pd.DataFrame(job_list)
    df.sort_values(['description_text', 'url'], ascending=[True, True], inplace=True)
    n_rows_before = len(df.index)
    df.drop_duplicates(subset=['title', 'company_name', 'description_text'], keep='first', inplace=True)
    n_rows_after = len(df.index)
    print(f'Dropped {n_rows_before-n_rows_after} duplicate rows')
    df.fillna('', inplace=True)  # fill None with ''
    # reorder the view
    df = df[
        ['company_rating', 'company_name', 'multiple_candidates', 'date_posted', 'title', 'company_location', 'salary',
         'estimated_salary', 'job_type', 'qualifications', 'description_text', 'benefits', 'hiring_insights',
         'company_indeed_profile_url', 'url']]
    df.sort_values(['company_rating', 'company_name', 'title'], ascending=[False, True, True], inplace=True)
    df.to_csv('out/search.csv')
    df.to_pickle('out/dataframe.pickle')


if __name__ == '__main__':
    main()


#  get first page
#  get number of pages div id=searchCountPages
#  get links to the jobs
#  parse each link
#  get job attributes
# >  break apart full job description
#  find red flags
#  find good flags
