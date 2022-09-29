import json

import pandas as pd
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL

from ... import db
from ...models import Company, CompanyUserNote, Search

def get_filtered_companies(user_id):
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
        Search.user_id == user_id,
        CompanyUserNote.is_filtered == True
    ).set_label_style(LABEL_STYLE_TABLENAME_PLUS_COL).distinct()
    df = pd.read_sql(stmt, db.session.bind)
    table_json = json.loads(df.to_json(orient='records'))
    return table_json