import json

import pandas as pd
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL

from ... import db
from ...models import Company, CompanyUserNote, Search, SearchModel


def get_filtered_companies(user_id):
    print('get_filtered_companies')
    stmt = db.select(Company.id,
                     Company.name,
                     Company.industry,
                     Company.size,
                     Company.location,
                     Company.profile_url,
                     Company.homepage_url,
                     CompanyUserNote.note
                     ) \
        .join(CompanyUserNote.company) \
        .filter(
        CompanyUserNote.user_id == user_id,
        CompanyUserNote.is_filtered == True
    ).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
    df = pd.read_sql(stmt, db.session.bind)
    table_json = json.loads(df.to_json(orient='records'))
    print(table_json)
    return table_json
