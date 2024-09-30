# -*- coding utf-8 -*-
"""
Created on november 2023
Copyright © 2023 - CryptOMaMa
"""

__author__ = "Enzo COGNEVILLE"
__copyright__ = "Copyright 2023, CryptOMaMa"
__license__ = "All rights reserved - LICENSE file is at the root of the project"

import json
import os
import numpy as np
import datetime as dt
from itertools import chain


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
    for limit in lob["bids"]:
        if float(price) == float(limit[0]) and float(limit[1]) != 0:
            found = True
            break
    for limit in lob["asks"]:
        if float(price) == float(limit[0]) and float(limit[1]) != 0: 
            found = True
            break
    return found

def get_midprice(lob : dict):
    
    if len(lob["asks"]) == 0 or len(lob["bids"]) == 0 : 
        return None #No midprice
    
    best_ask_price = None
    best_bid_price = None

    # Possible to have a volume set to 0 in the LOB
    for limit in lob["asks"]:
        if float(limit[1]) != 0 :
            best_ask_price = float(limit[0])
            break
    for limit in lob["bids"]:
        if float(limit[1]) != 0 :
            best_bid_price = float(limit[0])
            break

    if best_ask_price and best_bid_price :
        return (best_ask_price + best_bid_price)/2
    else : 
        return None

def transaction_intensity(history_dir: str):
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

    with open(os.path.join(history_dir,"depth.txt"), 'r') as depth_file:
        # Create dict of pair : "update_id":"Event_time"
        links = {json.loads(row)["u"]: json.loads(row)["E"] for row in depth_file}

    depth_arr = []
    with open(os.path.join(history_dir,"depth20.txt"), 'r') as depth20_file:
        # Create np array : [Event_time, bid_price1, bid_volume1, ..., bid_price20, bid_volume20, ask_price1, ask_volume1, ... ask_price20, ask_volume20]
        for row in depth20_file : 
            curr_row = json.loads(row)
            if len(curr_row["bids"]) != 20 or len(curr_row["asks"]) != 20:
                raise ValueError("Not a full order book")
            depth_arr.append([links[curr_row["lastUpdateId"]], *list(chain(*curr_row["bids"])), *list(chain(*curr_row["asks"]))])
    depth_arr = np.array(depth_arr, dtype = float)
    depth_arr = depth_arr[np.argsort(depth_arr[:, 0])]

    with open(os.path.join(history_dir,"aggTrade.txt"), 'r') as agg_trade_file:
        # Create np array : [Event_time, p, q]
        trades = np.array([[json.loads(row)["E"], json.loads(row)["a"], json.loads(row)["p"], json.loads(row)["q"]] for row in agg_trade_file], dtype = float)
    trades = trades[np.argsort(trades[:, 1])]
    trades = np.delete(trades, 1, 1)

    for trade in trades :  

        print(trade[0])     
        #On parcours tous les trades 
        #On récupère les LOB antérieurs à la date du trade
        for idx, sub_depth_arr in enumerate(depth_arr[depth_arr[:,0] < trade[0]][::-1]) : 
            #On parcours les LOB en sens inverse en cherchant si le prix du trade existe dans le current LOB

            stop = False
            if trade[1] in sub_depth_arr[1::2] and idx > 0 : 
                if depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][2::2][np.where(depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][1::2] == trade[1])] < sub_depth_arr[2::2][np.where(sub_depth_arr[1::2] == trade[1])]:
                    stop = True

            if not trade[1] in sub_depth_arr[1::2] and idx < 2: 
                # L'ordre est introuvable, on passe au suivant
                print("Unfoundable due to update rate of 100ms")
                break
            elif not trade[1] in sub_depth_arr[1::2] or stop :
                #On vient de trouver le LOB contenant l'ajout du LO qui vient d'être éxéctué
                lim_indexes = []
                for lob in depth_arr[depth_arr[:,0] < trade[0]][::-1][:idx] :

                    lim_indexes.append(np.where(lob[1::2] == trade[1])[0][0])

                if lim_indexes[-1] > 19 : 
                    opposite_idx = 0
                else : 
                    opposite_idx = 20
                    
                if not np.isnan(depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][1::2][opposite_idx]):
                    times_to_execute.append(dt.datetime.fromtimestamp(int(trade[0])/1000) - dt.datetime.fromtimestamp(int(depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][0])/1000))            
                    distances.append(abs(depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][1::2][lim_indexes[-1]] - depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][1::2][opposite_idx]))
                    volumes.append(min(depth_arr[depth_arr[:,0] < trade[0]][::-1][idx-1][2::2][lim_indexes[-1]], trade[2]))
                    
                    depth_arr_slice = depth_arr[depth_arr[:, 0] < trade[0]]

                    for lob_idx, lob in enumerate(depth_arr[depth_arr[:,0] < trade[0]][::-1][:idx][::-1]):
                        # On vient mettre à jour toutes les volumes disponibles entre la création de la limite et le MO
                        
                        depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]] -= trade[2]

                        if depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]] < 0 :
                            # Si négatif alors le trade va consomer d'autres LO 
                            # Reparcourir la liste dans l'autre sens

                            if lob_idx == 0 : 
                                #Initialisation du volume restant
                                last_vol_remain = depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]]
                            elif depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]] != last_vol_remain and not np.isnan(depth_arr_slice[::-1][:idx][::-1][lob_idx][1::2][opposite_idx]) :
                                # Le volume restant à être executé vient de changer,
                                # le LO de l'index a donc aussi été executé 
                                if depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]] < last_vol_remain:
                                    raise ValueError("Le volume qu'il reste a traiter est plus grand que ")
                                else : 
                                    times_to_execute.append(dt.datetime.fromtimestamp(int(trade[0])/1000) - dt.datetime.fromtimestamp(int(depth_arr_slice[::-1][:idx][::-1][lob_idx][0])/1000))            
                                    distances.append(abs(depth_arr_slice[::-1][:idx][::-1][lob_idx][1::2][lim_indexes[::-1][lob_idx]] - depth_arr_slice[::-1][:idx][::-1][lob_idx][1::2][opposite_idx]))
                                    volumes.append(abs(last_vol_remain - depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]]))
                                last_vol_remain = depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]]
                                depth_arr_slice[::-1][:idx][::-1][lob_idx][1::2][lim_indexes[lob_idx]] = np.nan

                        elif depth_arr_slice[::-1][:idx][::-1][lob_idx][2::2][lim_indexes[::-1][lob_idx]] == 0 :
                            depth_arr_slice[::-1][:idx][::-1][lob_idx][1::2][lim_indexes[::-1][lob_idx]] = np.nan

                            
                    depth_arr[depth_arr[:, 0] < trade[0]] = depth_arr_slice

                        

                break
    
    import matplotlib.pyplot as plt
    from scipy import stats
    from scipy.optimize import curve_fit

    def func(x, a, c, d):
        return a*np.exp(c*x)+d

    distances = np.array(distances)
    times_to_execute = np.array([t.total_seconds() for t in times_to_execute])
    res = stats.linregress(distances, times_to_execute)
    popt, pcov = curve_fit(func, distances, times_to_execute, bounds=((0, 0, 0), (np.inf, np.inf, np.inf)))
    plt.scatter(distances, times_to_execute)
    plt.scatter(distances, res.intercept + res.slope*distances)
    plt.scatter(distances, func(distances, *popt))
    plt.grid()
    plt.show()


    #sort by date
    rows = sorted(rows, key=lambda x: x['data'].get('E', float('inf')))

    depth20_data = []
    depth_data = []
    trade_data = []

    for item in rows:
        if "depth20" in item['stream']:
            depth20_data.append(item)
        elif "depth" in item['stream']:
            depth_data.append(item)
        elif "trade" in item["stream"]:
            trade_data.append(item)

    # Associer les valeurs de "E" dans "depth20@100ms" pour le "lastUpdateId" correspondant
    for depth20 in depth20_data:
        last_update_id = depth20["data"]["lastUpdateId"]
        
        for depth in depth_data:
            if depth["data"]["u"] == last_update_id:
                # Ajouter la clé "E" à l'entrée correspondante dans "depth20@100ms"
                depth20["data"]["E"] = depth["data"]["E"]
    
    rows = depth20_data + trade_data
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
                        
                        mid_price = get_midprice(last_depth_row)
                        
                        if not mid_price :
                            break
                        
                        for limit in last_depth_row["bids"]:
                            if price == float(limit[0]) and float(limit[1]):
                                distances.append(mid_price - price)
                                volumes.append(float(limit[1]))
                                times_to_execute.append(end_time - begin_time)
                                #update the volume to process
                                volume -= float(limit[1])
                                break
                        for limit in last_depth_row["asks"]:
                            if price == float(limit[0]) and float(limit[1]): 
                                distances.append(price - mid_price)
                                volumes.append(float(limit[1]))
                                times_to_execute.append(end_time - begin_time)
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
                                    mid_price = get_midprice(next_lob)
                                    
                                    if not mid_price :
                                        break
                                    
                                    for limit in next_lob["bids"]:
                                        if price == float(limit[0]) and float(limit[1]):
                                            distances.append(mid_price - price)
                                            volumes.append(float(limit[1]))
                                            times_to_execute.append(end_time - begin_time)
                                            #update the volume to process
                                            volume -= float(limit[1])
                                            break
                                    for limit in next_lob["asks"]:
                                        if price == float(limit[0]) and float(limit[1]): 
                                            distances.append(price - mid_price)
                                            volumes.append(float(limit[1]))
                                            times_to_execute.append(end_time - begin_time)
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
