# importing csv module
import pandas
import datetime as dt

filename = f"BillPayment_Log-{dt.datetime.now():%Y%m%d}" + ".LOG"
df = pandas.read_csv(filename, index_col='ReceiptNumber')
print(df)