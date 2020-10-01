import pandas as pd

read_file = pd.read_excel(r'test.xlsx')
read_file.to_csv(r'name.csv', index=None, header=True)