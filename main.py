from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import pprint
import collections


def get_year_form(years):
    last_digit = years % 10
    last_two_digits = years % 100
    
    if 11 <= last_two_digits <= 14:
        return 'лет'
    elif last_digit == 1:
        return 'год'
    elif 2 <= last_digit <= 4:
        return 'года'
    else:
        return 'лет' 
  
      
def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']))

    template = env.get_template('template.html')

    company_foundation = datetime.date(year=1920, month=1, day=1)
    todays_date = datetime.date.today()

    years = todays_date.year - company_foundation.year

    excel_wines_df = pandas.read_excel(
        'wine.xlsx', 
        sheet_name='Лист1',
        na_values=' ', 
        keep_default_na=False)
    
    wines = excel_wines_df.to_dict(orient='records')

    wines_by_category = collections.defaultdict(list)
    for wine in wines:
        wines_by_category[wine['Категория']].append(wine)
        
    pprint.pprint(wines_by_category)

    rendered_page = template.render(
        wines_by_category=wines_by_category,
        company_age=years,
        year_form = get_year_form(years))

    with open('index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()