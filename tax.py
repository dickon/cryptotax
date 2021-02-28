import csv, pprint, datetime
gross_income = 0
income_tax = 0
marginal_tax = 0.60
obtained = {}
obtained_btc = {}
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
            price[day] = float(transaction['Exchange rate'])
            income_tax += marginal_tax * value
            print(f'value={value:.2f} gross income={gross_income:.2f} income tax={income_tax:.2f} bitcoin={bitcoin}')
            potential_sale_price = bitcoin * price[day]
            print(f'potential sale price={potential_sale_price:.2f}')
            same_day_sale_paid = bitcoin_today * price[day]
            bed_and_breakfast_paid = 0
            bed_and_breakfast_btc = 0
            other_price_series = []
            for altd in obtained_btc:
                # was the sale in the last 30 days?
                age = dt - datetime.datetime(altd[0], altd[1], altd[2], 12,0,0)
                print(age)
                if age.days  < 31:
                    bb_today = obtained_btc[altd] * price[altd]
                    bed_and_breakfast_paid += bb_today
                    bed_and_breakfast_btc += obtained_btc[altd]
                    print(f'bed and breakfast {altd} paid {bb_today} (=btc {obtained_btc[altd]} at {price[altd]})' )
                else:
                    other_price_series.append(price[altd])
            print('other price series', other_price_series)
            mean_other_price_series = sum(other_price_series)/len(other_price_series) if other_price_series else 0
            other_btc = bitcoin - bitcoin_today - bed_and_breakfast_btc
            other_btc_price = other_btc * mean_other_price_series
            base_price = same_day_sale_paid + bed_and_breakfast_paid + other_btc_price
            print(f'same day sale element=£{same_day_sale_paid:.2f}, bed and breakfast element=£{bed_and_breakfast_paid:.2f} remaining pool=£{other_btc_price:.2f}')
            gain = potential_sale_price - base_price
            print(f'value for capital gains if selling all=£{base_price}, capital gain=£{gain:.2f}')
            
print(f'gross income=£{gross_income:.2f} income tax due=£{income_tax:.2f} capital gain if all sold now=£{gain:.2f}')
pprint.pprint(price)
pprint.pprint(obtained)
