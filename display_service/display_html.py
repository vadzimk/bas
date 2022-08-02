import os
import pandas as pd
import numpy as np
import jinja2

from jinja2 import Environment, FileSystemLoader

template_env = Environment(loader=FileSystemLoader('templates/'))

# Project specific global variables: paths, URIs, etc.
file_abspath = os.path.abspath(__file__)
file_basename = os.path.basename(file_abspath)
file_dirname = os.path.dirname(file_abspath)


def main():
    """The main function."""
    os.chdir(file_dirname)

    df: pd.DataFrame = pd.read_pickle('../out/dataframe.pickle')

    df = df.reset_index(drop=True)
    df.index.name = 'id'
    df.reset_index(inplace=True)
    print(df.index)
    print(df)

    # Generate HTML from template.

    # template = template_env.get_template('simple-template.html')
    # template = template_env.get_template('bootstrap-template.html')
    # output_html = template.render(dataframe=df.to_html(table_id="table", border=0))
    template = template_env.get_template('tabulator-template.html')
    output_html = template.render(dataframe=df.to_json(orient='records'), fields=df.columns.values)

    # Write generated HTML to file.
    with open("demo.html", "w", encoding="utf-8") as file_obj:
        file_obj.write(output_html)


if __name__ == "__main__":
    main()

#  TODO

# make filter work on all columns when no column is selected    https://github.com/olifolkerd/tabulator/issues/505
# auto column layout   http://tabulator.info/docs/5.3/columns#autocolumns
# if not database then make it upload data from file
# cell menu is obeying the header menu classes thus it sticks to the top of the screen as well, need to change this
# employ a strategy to filter all unfit jobs first. and apply to all that are fit and then track the application progress
# the app could query the jobs every day and add them to the bottom of the unprocessed list
# the date of job posting is in days ago, but it will become stale tomorrow, need to store the actual date and then convert it back