from enum import Enum


class LinkedinSearch():
    class Filters:
        class Radius(str, Enum):
            EXACT = 'distance=0'
            FIVE = 'distance=5'
            TEN = 'distance=10'
            TWENTY_FIVE = 'distance=25'
            FIFTY = 'distance=50'
            HUNDRED = 'distance=100'
            ALL = ''

        class Experience(str, Enum):
            INTERNSHIP = '1'
            ENTRY_LEVEL = '2'
            ASSOCIATE = '3'
            MID_SENIOR = '4'
            DIRECTOR = '5'
            EXECUTIVE = '6'
            ALL = ''

        class Age(str, Enum):
            PAST_MONTH = '&f_TPR=r2592000'
            PAST_WEEK = '&f_TPR=r604800'
            PAST_24H = '&f_TPR=r86400'
            ALL = ''


class IndeedSearch():
    class Filters:
        class Radius(str, Enum):
            EXACT = '&radius=0'
            FIVE = '&radius=5'
            TEN = '&radius=10'
            FIFTEEN = '&radius=15'
            TWENTY_FIVE = '&radius=25'
            HUNDRED = '&radius=100'
            ALL = ''

        class Experience(str, Enum):
            ENTRY = 'explvl(ENTRY_LEVEL)'
            MID = 'explvl(MID_LEVEL)'
            SENIOR = 'explvl(SENIOR_LEVEL)'
            ALL = ''

        class Education(str, Enum):
            SCHOOL = 'attr(FCGTU%7CQJZM9%252COR)',
            ASSOCIATES = 'attr(FCGTU%7CQJZM9%7CUTPWG%252COR)',
            BACHELORS = 'attr(FCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)',
            MASTERS = 'attr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)',
            ALL = ''

        class Age(str, Enum):
            LAST = 'last'
            ONE = '1'
            TREE = '3'
            SEVEN = '7'
            FOURTEEN = '14'
            ALL = ''


def convert_search_fields(input_fields: dict, job_board: str):
    """ converts search field values to the enum values that a particular search can accept
     including the experience filed that is either an array or a single value
    examples can be found in the test_tasks.py file
     """
    reference = {
        'linkedin': {
            'radius': {
                '': LinkedinSearch.Filters.Radius.ALL,
                'exact': LinkedinSearch.Filters.Radius.EXACT,
                '5mi': LinkedinSearch.Filters.Radius.FIVE,
                '10mi': LinkedinSearch.Filters.Radius.TEN,
                '25mi': LinkedinSearch.Filters.Radius.TWENTY_FIVE,
                '50': LinkedinSearch.Filters.Radius.FIFTY
            },
            'experience': {
                '': LinkedinSearch.Filters.Experience.ALL,
                'internship': LinkedinSearch.Filters.Experience.INTERNSHIP,
                'entry level': LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
                'associate': LinkedinSearch.Filters.Experience.ASSOCIATE,
                'mid-senior': LinkedinSearch.Filters.Experience.MID_SENIOR,
                'director': LinkedinSearch.Filters.Experience.DIRECTOR,
                'executive': LinkedinSearch.Filters.Experience.EXECUTIVE
            },
            'age': {
                '': LinkedinSearch.Filters.Age.ALL,
                'month': LinkedinSearch.Filters.Age.PAST_MONTH,
                'week': LinkedinSearch.Filters.Age.PAST_WEEK,
                'day': LinkedinSearch.Filters.Age.PAST_24H
            }
        },
        'indeed': {
            'radius': {
                '': IndeedSearch.Filters.Radius.ALL,
                'exact': IndeedSearch.Filters.Radius.EXACT,
                '5mi': IndeedSearch.Filters.Radius.FIVE,
                '10mi': IndeedSearch.Filters.Radius.TEN,
                '15mi': IndeedSearch.Filters.Radius.FIFTEEN,
                '25mi': IndeedSearch.Filters.Radius.TWENTY_FIVE,
                '100mi': IndeedSearch.Filters.Radius.HUNDRED,
            },
            'experience': {
                '': IndeedSearch.Filters.Experience.ALL,
                'entry level': IndeedSearch.Filters.Experience.ENTRY,
                'mid': IndeedSearch.Filters.Experience.MID,
                'senior': IndeedSearch.Filters.Experience.SENIOR,
            },
            'age': {
                '': IndeedSearch.Filters.Age.ALL,
                '1 day': IndeedSearch.Filters.Age.ONE,
                '3 days': IndeedSearch.Filters.Age.TREE,
                '7 days': IndeedSearch.Filters.Age.SEVEN,
                '14 days': IndeedSearch.Filters.Age.FOURTEEN,
            },
            'education': {
                'school': IndeedSearch.Filters.Education.SCHOOL,
                'associates': IndeedSearch.Filters.Education.ASSOCIATES,
                'bachelors': IndeedSearch.Filters.Education.BACHELORS,
                'masters': IndeedSearch.Filters.Education.MASTERS,
            }
        }
    }
    result = {}
    for k, v in input_fields.items():
        if k in reference[job_board].keys():
            if k == 'experience' and job_board == 'linkedin':
                experience = [reference[job_board][k][exp] for exp in input_fields[k]]
                result[k] = experience
            else:
                result[k] = reference[job_board][k][v]

        else:
            result[k] = v
    return result
