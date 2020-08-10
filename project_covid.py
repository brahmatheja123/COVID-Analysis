# -*- coding: utf-8 -*-
"""Project_Covid.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rX3xvCI_ZWNdtr7gqW4zmi8_BFv65Dly
"""

from google.colab import files
uploaded = files.upload()

"""# Data Pre-processing"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import io
data1 = pd.read_csv(io.BytesIO(uploaded["nation_level_daily.csv - Sheet2.csv"]))
data1["Daily Confirmed Smooth"] = data1["Daily Confirmed"].rolling(window = 7).mean()
variable = data1["Daily Confirmed Smooth"]
dates = data1["Date"]
date_format = [pd.to_datetime(d) for d in dates]
figure, axis = plt.subplots(figsize = (12,5))
axis.grid()
axis.scatter(date_format, variable)
axis.set(xlabel = "Date", ylabel = "Daily Confirmed", title = "Daily Positive Cases")
dateform = DateFormatter("%d-%m")
axis.xaxis.set_major_formatter(dateform)
axis.xaxis.set_major_locator(mdates.DayLocator(interval = 7))
plt.show()
data1["Daily Deceased Smooth"] = data1["Daily Deceased"].rolling(window = 7).mean()
variable1 = data1["Daily Deceased Smooth"]
figure, axis1 = plt.subplots(figsize = (12,5))
axis1.grid()
axis1.scatter(date_format, variable1)
axis1.set(xlabel = "Date", ylabel = "Daily Deceased", title = "Daily Deceased Cases")
axis1.xaxis.set_major_formatter(dateform)
axis1.xaxis.set_major_locator(mdates.DayLocator(interval = 7))
plt.show()
data1["Daily Recovered Smooth"] = data1["Daily Recovered"].rolling(window = 7).mean()
variable2 = data1["Daily Recovered Smooth"]
figure, axis2 = plt.subplots(figsize = (12,5))
axis2.grid()
axis2.scatter(date_format, variable2)
axis2.set(xlabel = "Date", ylabel = "Daily Recovered", title = "Daily Recovered Cases")
axis2.xaxis.set_major_formatter(dateform)
axis2.xaxis.set_major_locator(mdates.DayLocator(interval = 7))
plt.show()

"""# Regression Daily Cases during Lockdown"""

from sklearn import linear_model
X = date_format
y = data1["Daily Confirmed Smooth"].tolist()[1:]
starting_date = 93
ending_date = 126
day_numbers = []
for i in range(1, len(X)):
  day_numbers.append([i])
X = day_numbers
X = X[starting_date : ending_date]
y = y[starting_date : ending_date]
linear_regression1 = linear_model.LinearRegression()
linear_regression1.fit(X,y)
from sklearn.metrics import max_error
import math
y_pred = linear_regression1.predict(X)
error = max_error(y, y_pred)
X_test = []
future_days = 134
for i in range(starting_date, starting_date + future_days):
    X_test.append([i])
y_pred_linear = linear_regression1.predict(X_test)
y_pred_max = []
y_pred_min = []
for i in range(0, len(y_pred_linear)):
    y_pred_max.append(y_pred_linear[i] + error)
    y_pred_min.append(y_pred_linear[i] - error)
from datetime import datetime, timedelta
date_zero = datetime.strptime(data1['Date'][starting_date], '%Y-%m-%d')
date_prev = []
x_ticks = []
step = 7
data_curr = date_zero
x_current = starting_date
n = int(future_days / step)
for i in range(0, n):
    date_prev.append(str(data_curr.day) + "/" + str(data_curr.month))
    x_ticks.append(x_current)
    data_curr = data_curr + timedelta(days=step)
    x_current = x_current + step
plt.grid()
plt.scatter(X, y)
plt.plot(X_test, y_pred_linear, color='green', linewidth=2)
plt.plot(X_test, y_pred_max, color='red', linewidth=1, linestyle='dashed')
plt.plot(X_test, y_pred_min, color='red', linewidth=1, linestyle='dashed')
plt.xlabel("Date")
plt.xlim(starting_date, starting_date + future_days)
plt.xticks(x_ticks, date_prev)
plt.title("Lockdown Continued Trend")
plt.ylabel("Daily Confirmed")
plt.yscale("log")
plt.savefig("prediction.png")
plt.show()

"""# Regression Daily Cases after Lockdown"""

X = date_format
y = data1["Daily Confirmed Smooth"].tolist()[1:]
starting_date = 127
day_numbers = []
for i in range(1, len(X)):
  day_numbers.append([i])
X = day_numbers
X = X[starting_date :]
y = y[starting_date :]
linear_regression1 = linear_model.LinearRegression()
linear_regression1.fit(X,y)
from sklearn.metrics import max_error
import math
y_pred = linear_regression1.predict(X)
error = max_error(y, y_pred)
X_test = []
future_days = 100
for i in range(starting_date, starting_date + future_days):
    X_test.append([i])
y_pred_linear = linear_regression1.predict(X_test)
y_pred_max = []
y_pred_min = []
for i in range(0, len(y_pred_linear)):
    y_pred_max.append(y_pred_linear[i] + error)
    y_pred_min.append(y_pred_linear[i] - error)
from datetime import datetime, timedelta
date_zero = datetime.strptime(data1['Date'][starting_date], '%Y-%m-%d')
date_prev = []
x_ticks = []
step = 7
data_curr = date_zero
x_current = starting_date
n = int(future_days / step)
for i in range(0, n):
    date_prev.append(str(data_curr.day) + "/" + str(data_curr.month))
    x_ticks.append(x_current)
    data_curr = data_curr + timedelta(days=step)
    x_current = x_current + step
plt.grid()
plt.scatter(X, y)
plt.plot(X_test, y_pred_linear, color='green', linewidth=2)
plt.plot(X_test, y_pred_max, color='red', linewidth=1, linestyle='dashed')
plt.plot(X_test, y_pred_min, color='red', linewidth=1, linestyle='dashed')
plt.xlabel("Date")
plt.xlim(starting_date, starting_date + future_days)
plt.xticks(x_ticks, date_prev)
plt.title("Post Lockdown Trend")
plt.ylabel("Daily Confirmed")
plt.yscale("log")
plt.savefig("prediction.png")
plt.show()