import pandas as pd
import requests

currency_array = ["BYR", "USD", "EUR",
                  "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]


def fetch_date(date):
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={
        date.strftime('%d/%m/%Y')}"

    response = requests.get(url)
    response.encoding = 'windows-1251'
    data = pd.read_xml(response.text, parser='etree')
    currencies = (
        data
        .reindex(columns=['CharCode', 'VunitRate'])
        .assign(VunitRate=lambda _c: _c.VunitRate.str.replace(',', '.').astype(float))
        .pivot_table(index=None, columns='CharCode', values='VunitRate', aggfunc='first')
        .reindex(columns=currency_array)
    )
    currencies.insert(0, 'date', date.strftime('%Y-%m'))

    return currencies


start_date = pd.to_datetime('2003-01-01')
end_date = pd.to_datetime('2025-01-15')
dates = pd.date_range(start_date, end_date, freq='MS')

results = map(fetch_date, dates)

df = pd.concat(results, ignore_index=True)
df.to_csv('./currency.csv', index=False)
