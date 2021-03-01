import csv, pprint, datetime
gross_income = 0
income_tax = 0
marginal_tax = 0.60
obtained = {}
obtained_btc = {}
obtained_btc_cumulative = {}
price = {}
bitcoin = 0
with open('report_ALL-BTC-GBP-NONE_20210101-20210228.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    data= list(reader)
    for row in data[1:]:
        transaction = dict(zip(data[0], row))
        pprint.pprint(transaction)
        if transaction['Purpose'] == 'Hashpower mining' and transaction['Date time']:
            value = float(transaction['Amount (GBP)'])
            bitcoin_today = float(transaction['Amount (BTC)'])
            bitcoin += bitcoin_today
            when = transaction['Date time']
            dt = datetime.datetime.strptime(when[:-4], '%Y-%m-%d %H:%M:%S')
            day = (dt.year, dt.month, dt.day)
            gross_income += value
            obtained.setdefault(day, 0)
            obtained[day] += value
            obtained_btc.setdefault(day, 0)
            obtained_btc[day] += bitcoin_today
            obtained_btc_cumulative[day] = bitcoin
            price[day] = float(transaction['Exchange rate'])
            income_tax += marginal_tax * value
            print(f'value={value:.2f} gross income={gross_income:.2f} income tax={income_tax:.2f} bitcoin={bitcoin}')

for day in sorted(obtained):
    print()
    print('capital gain on', day)
    bitcoin = obtained_btc_cumulative[day]
    bitcoin_today = obtained_btc[day]
    potential_sale_price = bitcoin * price[day]
    print(f'cumulative bitcoin on that day {bitcoin} value {potential_sale_price:.2f}')
    same_day_sale_paid = bitcoin_today * price[day]
    bed_and_breakfast_paid = 0
    bed_and_breakfast_btc = 0
    other_price_series = []
    dt = datetime.datetime(day[0], day[1], day[2], 12, 0,0)
    bitcoin_remaining = max(bitcoin - bitcoin_today, 0)
    for altd in sorted(obtained_btc):
        # was the sale after the gain and within 30 days?
        age = dt - datetime.datetime(altd[0], altd[1], altd[2], 12,0,0)
        print(age.days)
        if age.days  > -31 and age.days < 0:
            bb_allocated = max(0, min(bitcoin_remaining, obtained_btc[altd]))
            bb_allocated_fiat = bb_allocated * price[altd]
            bed_and_breakfast_paid += bb_allocated_fiat
            bed_and_breakfast_btc += bb_allocated
            print(f'bed and breakfast {altd} bitcoing to allocate {bitcoin_remaining} paid {bb_allocated_fiat} (=btc {bb_allocated} at {price[altd]})' )
            bitcoin_remaining -= bb_allocated
        else:
            other_price_series.append(price[altd])
    print('other price series', other_price_series)
    mean_other_price_series = sum(other_price_series)/len(other_price_series) if other_price_series else 0
    other_btc = max(bitcoin - bitcoin_today - bed_and_breakfast_btc, 0)
    other_btc_price = other_btc * mean_other_price_series
    base_price = same_day_sale_paid + bed_and_breakfast_paid + other_btc_price
    print(f'same day sale element=£{same_day_sale_paid:.2f}, bed and breakfast element=£{bed_and_breakfast_paid:.2f} remaining pool=£{other_btc_price:.2f}')
    gain = potential_sale_price - base_price
    print(f'value for capital gains if selling all=£{base_price:.2f}, capital gain=£{gain:.2f}')
            
print(f'gross income=£{gross_income:.2f} income tax due=£{income_tax:.2f}')
pprint.pprint(price)
pprint.pprint(obtained)
