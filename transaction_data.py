"""
This file turns the dataset into a dictionary to be pickled containing the necessary figures for the transaction visualization. Takes a few minutes to run.
"""
import pandas as pd
from business_coords import coords
import math
from business_view import show_info
import time
import datetime
import pickle

#get the cc and loyalty data
cc_data = pd.read_csv(r'./Data/cc_data.csv')
loyalty_data = pd.read_csv(r'./Data/loyalty_data.csv')

#list of datetimes
dates = ["all_time", datetime.datetime(2014,1,6,0,0), datetime.datetime(2014,1,7,0,0), datetime.datetime(2014,1,8,0,0), datetime.datetime(2014,1,9,0,0), datetime.datetime(2014,1,10,0,0), datetime.datetime(2014,1,11,0,0), datetime.datetime(2014,1,12,0,0), datetime.datetime(2014,1,13,0,0), datetime.datetime(2014,1,14,0,0), datetime.datetime(2014,1,15,0,0), datetime.datetime(2014,1,16,0,0), datetime.datetime(2014,1,17,0,0), datetime.datetime(2014,1,18,0,0), datetime.datetime(2014,1,19,0,0), datetime.datetime(2014,1,20,0,0)]

#make a dictionary containing the necessary data so the program doesn't have to do this on the fly
data = dict(coords)

#iterate thru locations
for location in coords.keys():

    data[location] = {}
    print(location)

    #iterate thru dates
    for i in range(15):

        date = dates[i]

        if str(date) == "all_time":
            
            df_location_cc = cc_data[cc_data['location'] == location]
            total_transactions_cc = df_location_cc.shape[0]
            total_spent_cc = df_location_cc['price'].sum()

            df_location_loyalty = loyalty_data[loyalty_data['location'] == location]
            total_transactions_loyalty = df_location_loyalty.shape[0]
            total_spent_loyalty = df_location_loyalty['price'].sum()

            data[location][str(date)] = {"cc":{"total_transactions":total_transactions_cc, "total_spent":total_spent_cc}, "loyalty":{"total_transactions":total_transactions_loyalty, "total_spent":total_spent_loyalty}}

        if str(date) != "4/20" and str(date) != "all_time":

            df_new_cc = cc_data[(pd.to_datetime(cc_data['timestamp']) > str(date)) & (pd.to_datetime(cc_data['timestamp']) < str(dates[i+1]))]
            df_location_cc = df_new_cc[df_new_cc['location'] == location]
            total_transactions_cc = df_location_cc.shape[0]
            total_spent_cc = df_location_cc['price'].sum()

            df_new_loyalty = loyalty_data[(pd.to_datetime(loyalty_data['timestamp']) > str(date)) & (pd.to_datetime(loyalty_data['timestamp']) < str(dates[i+1]))]
            df_location_loyalty = df_new_loyalty[df_new_loyalty['location'] == location]
            total_transactions_loyalty = df_location_loyalty.shape[0]
            total_spent_loyalty = df_location_loyalty['price'].sum()

            data[location][str(date)] = {"cc":{"total_transactions":total_transactions_cc, "total_spent":total_spent_cc}, "loyalty":{"total_transactions":total_transactions_loyalty, "total_spent":total_spent_loyalty}}

print(data)

pickle.dump(data, open("transaction_data_dict.pkl", "wb"))
