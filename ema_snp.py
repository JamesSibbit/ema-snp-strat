from pandas_datareader import data
import pandas as pd
import pandas_datareader.data as web
import datetime
import numpy as np
import smtplib as sm
from time import sleep
import os
from getpass import getpass

sent_from = user.input("Enter gmail account to send from: ")
to = user.input("Enter email to send to: ")
password = getpass("Enter your API password for gmail: ")

while True:
    today = datetime.date.today() - datetime.timedelta(days=1)
    last_month = today - datetime.timedelta(days=31)

    try:
        panel_data = web.DataReader("^GSPC", 'yahoo', last_month, today)
        print("Pulled SNP data")
    except Exception as e:
        raise e

    close = panel_data['Close']

    weekdays = pd.date_range(start = last_month, end = today, freq = 'B')

    close = close.reindex(weekdays)

    close = close.fillna(method = 'bfill')

    ema_five = close.ewm(span = 5, adjust=False).mean()
    ema_twenty = close.ewm(span = 10, adjust=False).mean()

    raw = close - ema_five
    rawtwen = close - ema_twenty
    position = raw.apply(np.sign).shift(1)
    positiontwen = rawtwen.apply(np.sign).shift(1)

    try:
        smtp_object = sm.SMTP('smtp.gmail.com', 587)
        smtp_object.ehlo
        smtp_object.starttls()
        smtp_object.login(sent_from, password=password)
        print("Login successful")
    except Exception as e:
        print("Login failed")
        raise e

    if (position[-1] != position[-2]) and (position[-1] > position[-2]):
        msg = "\r\n".join([
          "From: "+sent_from,
          "To: "+to,
          "Subject: Go long",
          "",
          "Buy!"
          ])

        try:
            smtp_object.sendmail(sent_from, to, msg)
            print("Email sent")
        except Exception as e:
            print("Email failed to send")
    elif (position[-1] != position[-2]) and (position[-1] < position[-2]):
        msg = "\r\n".join([
          "From: "+sent_from,
          "To: "+to,
          "Subject: Go short",
          "",
          "Sell!"
          ])

        try:
            smtp_object.sendmail(sent_from, to, msg)
            print("Email sent")
        except Exception as e:
            print("Email failed to send")
    else:
        msg = "\r\n".join([
          "From: "+sent_from,
          "To: "+to,
          "Subject: No move",
          "",
          "No change - stick"
          ])

        try:
            smtp_object.sendmail(sent_from, to, msg)
            print("Email sent")
        except Exception as e:
            print("Email failed to send")

    smtp_object.close()
    sleep(86400)
    print("Refreshing")
    continue
