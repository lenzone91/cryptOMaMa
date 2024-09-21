# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import json
import datetime as dt


def is_limit_in_LOB(lob : dict, price : float):
    """
    Look if the trade price is present in the LOB.

    Parameters
    ----------
    lob : dict
        LOB to looking in
    
    Returns
    -------
    found : bool
        Is the trade price is present in the LOB
    """
    found = False #is the trade price is found in the last LOB limits
    for limit in lob["b"]:
        if float(price) == float(limit[0]) and float(limit[1]) != 0:
            found = True
            break
    for limit in lob["a"]:
        if float(price) == float(limit[0]) and float(limit[1]) != 0: 
            found = True
            break
    return found

def get_midprice(lob : dict):
    
    if len(lob["a"]) == 0 or len(lob["b"]) == 0 : 
        return None #No midprice
    
    best_ask_price = None
    best_bid_price = None

    # Possible to have a volume set to 0 in the LOB
    for limit in lob["a"]:
        if float(limit[1]) != 0 :
            best_ask_price = float(limit[0])
            break
    for limit in lob["b"]:
        if float(limit[1]) != 0 :
            best_bid_price = float(limit[0])
            break

    if best_ask_price and best_bid_price :
        return (best_ask_price + best_bid_price)/2
    else : 
        return None

def transaction_intensity(history_file: str):
    """
    Calibrate parameters of the intensity function of sell and buy depending 
    on the spread between a quote and the midprice. 
    The intensity function is :
        $\lambda^b(\delta^b) = Ae^{-k(s-s^b)}$ and $\lambda^a(\delta^a) = Ae^{-k(s-s^a)}$
    With $\delta^b = S - S^b $ and $\delta^a = S - S^a $, $S$ the midprice, $S^b$ and $S^a$
    respectively the quote at bid and ask.

    Parameters
    ----------
    history_file : str
        Path to the broker historic 
    
    Returns
    -------
    A : positive float
    k : positive float
    """

    distances = []
    volumes = []
    times_to_execute = []

    with open(history_file, 'r') as file:
        # Get all distances between midprice and trade price + volume
        rows = [json.loads(row.rstrip()) for row in file]

    #sort by date
    rows = sorted(rows, key=lambda x: x['data'].get('E', float('inf')))

    for row_idx, row in enumerate(rows):
        
        if "trade" in row["stream"]:

            done = False
            end_time = dt.datetime.fromtimestamp(int(row["data"]["E"])/1000)
            price = float(row["data"]["p"])
            volume = float(row["data"]["q"])
            last_depth_row = None

            for backward_idx, backward_row in enumerate(rows[:row_idx][::-1]):
                if "depth" in backward_row["stream"]:
                    is_limit = is_limit_in_LOB(backward_row["data"], price)
                    if is_limit :
                        last_depth_row = backward_row["data"]
                        last_depth_row_idx = backward_idx
                    elif last_depth_row :
                        begin_time = dt.datetime.fromtimestamp(int(last_depth_row["E"])/1000)
                        times_to_execute.append(end_time - begin_time)
                        
                        mid_price = get_midprice(last_depth_row)
                        
                        if not mid_price :
                            break
                        
                        for limit in last_depth_row["b"]:
                            if price == float(limit[0]) and float(limit[1]):
                                distances.append(mid_price - price)
                                volumes.append(float(limit[1]))
                                #update the volume to process
                                volume -= float(limit[1])
                                break
                        for limit in last_depth_row["a"]:
                            if price == float(limit[0]) and float(limit[1]): 
                                distances.append(price - mid_price)
                                volumes.append(float(limit[1]))
                                #update the volume to process
                                volume -= float(limit[1])
                                break
                        
                        #Process the remaining volume with forward loop
                        while volume > 0 and last_depth_row_idx < row_idx-1:
                            last_depth_row_idx += 1 
                            next_row = rows[last_depth_row_idx]

                            if "depth" in next_row["stream"]:
                                
                                next_lob = next_row["data"]

                                is_limit = is_limit_in_LOB(next_lob, price)

                                if is_limit :
                                    begin_time = dt.datetime.fromtimestamp(int(next_lob["E"])/1000)
                                    times_to_execute.append(end_time - begin_time)
                                    
                                    mid_price = get_midprice(next_lob)
                                    
                                    if not mid_price :
                                        break
                                    
                                    for limit in next_lob["b"]:
                                        if price == float(limit[0]) and float(limit[1]):
                                            distances.append(mid_price - price)
                                            volumes.append(float(limit[1]))
                                            #update the volume to process
                                            volume -= float(limit[1])
                                            break
                                    for limit in next_lob["a"]:
                                        if price == float(limit[0]) and float(limit[1]): 
                                            distances.append(price - mid_price)
                                            volumes.append(float(limit[1]))
                                            #update the volume to process
                                            volume -= float(limit[1])
                                            break
                        if volume > 0 : 
                            print("Warning, it remains volume for trade : "+ str(row_idx) + " and LOB : " + str(last_depth_row_idx))
                        else : 
                            done = True
                        break
                    else :
                        break
        
            if not done :
                print("Not done")
    print("")

    return A, k
