import io
from pprint import pprint

from IndeedSearch import IndeedSearch
from LinkedinSearch import LinkedinSearch
from utils import cleanup, create_project
from pandas import pandas as pd


def main():
    cleanup()
    create_project()

    indeed_searches = [
        # IndeedSearch(
        #     what="react javascript python developer",
        #     where="Los Angeles",
        #     age=IndeedSearch.Filters.Age.FOURTEEN,
        #     radius=IndeedSearch.Filters.Radius.EXACT,
        #     experience=IndeedSearch.Filters.Experience.ENTRY
        # ),
        IndeedSearch(
            what="react frontend developer",
            where="Los Angeles",
            age=IndeedSearch.Filters.Age.ONE,
            radius=IndeedSearch.Filters.Radius.EXACT,
            experience=IndeedSearch.Filters.Experience.ENTRY
        )
    ]
    # python_searches = [
    #     IndeedSearch(
    #         what="python developer",
    #         where="Los Angeles",
    #         age=IndeedSearch.Filters.Age.FOURTEEN,
    #         radius=IndeedSearch.Filters.Radius.EXACT,
    #         experience=IndeedSearch.Filters.Experience.ENTRY
    #     ), IndeedSearch(
    #         what="python developer",
    #         where="Los Angeles",
    #         age=IndeedSearch.Filters.Age.FOURTEEN,
    #         radius=IndeedSearch.Filters.Radius.EXACT,
    #         experience=IndeedSearch.Filters.Experience.MID
    #     )
    # ]

    linkedin_searches = [
        LinkedinSearch(
            what="""react AND (python OR node) AND NOT (ruby OR ".NET") developer AND NOT (citizen OR Citizen OR "green card" OR "Green Card") and NOT (senior OR Senior OR lead OR Lead) AND NOT ("CyberCoders" OR "Jobot")""",
            where="Los Angeles, California, United States",
            age=LinkedinSearch.Filters.Age.PAST_24H,
            radius=LinkedinSearch.Filters.Radius.EXACT,
            experience=[LinkedinSearch.Filters.Experience.INTERNSHIP]
        )
    ]

    # TODO make them run in parallel
    mySearches = [
        # *linkedin_searches,
        *indeed_searches,
    ]
    job_list = []
    for one_search in mySearches:
        for page in one_search.pages:
            for beacon in page.beacons:
                job_list.append(beacon.dict)
    df = pd.DataFrame(job_list)
    # TODO uncomment this
    # df.sort_values(['description_text', 'url'], ascending=[True, True], inplace=True)
    # n_rows_before = len(df.index)
    # df.drop_duplicates(subset=['title', 'company_name', 'description_text'], keep='first', inplace=True)
    # n_rows_after = len(df.index)
    # print(f'Dropped {n_rows_before-n_rows_after} duplicate rows')
    # df.fillna('', inplace=True)  # fill None with ''
    # # reorder the view
    # df = df[
    #     ['company_rating', 'company_name', 'multiple_candidates', 'date_posted', 'title', 'company_location', 'salary',
    #      'estimated_salary', 'job_type', 'qualifications', 'description_text', 'benefits', 'hiring_insights',
    #      'company_indeed_profile_url', 'url']]
    # df.sort_values(['company_rating', 'company_name', 'title'], ascending=[False, True, True], inplace=True)
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
