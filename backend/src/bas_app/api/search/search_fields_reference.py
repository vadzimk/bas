from bas_app.scraper.IndeedSearch import IndeedSearch
from bas_app.scraper.LinkedinSearch import LinkedinSearch

reference = {
        'linkedin': {
            'radius': {
                'all': LinkedinSearch.Filters.Radius.ALL,
                'exact': LinkedinSearch.Filters.Radius.EXACT,
                '5mi': LinkedinSearch.Filters.Radius.FIVE,
                '10mi': LinkedinSearch.Filters.Radius.TEN,
                '25mi': LinkedinSearch.Filters.Radius.TWENTY_FIVE,
                '50': LinkedinSearch.Filters.Radius.FIFTY
            },
            'experience': {
                'all': LinkedinSearch.Filters.Experience.ALL,
                'internship': LinkedinSearch.Filters.Experience.INTERNSHIP,
                'entry level': LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
                'associate': LinkedinSearch.Filters.Experience.ASSOCIATE,
                'mid-senior': LinkedinSearch.Filters.Experience.MID_SENIOR,
                'director': LinkedinSearch.Filters.Experience.DIRECTOR,
                'executive': LinkedinSearch.Filters.Experience.EXECUTIVE
            },
            'age': {
                'all': LinkedinSearch.Filters.Age.ALL,
                'month': LinkedinSearch.Filters.Age.PAST_MONTH,
                'week': LinkedinSearch.Filters.Age.PAST_WEEK,
                'day': LinkedinSearch.Filters.Age.PAST_24H
            }
        },
        'indeed': {
            'radius': {
                'all': IndeedSearch.Filters.Radius.ALL,
                'exact': IndeedSearch.Filters.Radius.EXACT,
                '5mi': IndeedSearch.Filters.Radius.FIVE,
                '10mi': IndeedSearch.Filters.Radius.TEN,
                '15mi': IndeedSearch.Filters.Radius.FIFTEEN,
                '25mi': IndeedSearch.Filters.Radius.TWENTY_FIVE,
                '100mi': IndeedSearch.Filters.Radius.HUNDRED,
            },
            'experience': {
                'all': IndeedSearch.Filters.Experience.ALL,
                'entry level': IndeedSearch.Filters.Experience.ENTRY,
                'mid': IndeedSearch.Filters.Experience.MID,
                'senior': IndeedSearch.Filters.Experience.SENIOR,
            },
            'age': {
                'all': IndeedSearch.Filters.Age.ALL,
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