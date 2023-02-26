from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
from colorama import init, Fore, Back
from talib.abstract import *
import time, json, logging, configparser
import time
import pandas as pd
import numpy as np
import talib

my_user = "laissilva6363@gmail.com"
my_pass = "wali1234"

#CONFIGURAÇÃO SE ESTÁ LOGADO OU NÃO
Iq=IQ_Option(my_user,my_pass)
iqch1,iqch2=Iq.connect()
if iqch1==True:
    print("logado ( ͡ ° ͜ʖ ͡ °)")
else:
    print("login failed ┌( ಠ_ಠ)-💣")

print("Aguarde...")
total = []
tempo = time.time()

for i in range(44):
    X = Iq.get_candles("EURUSD", 60, 1000, tempo)
    total = X+total
    tempo = int(X[0]['from'])-1

inputs = {
    'close': np.array([]),
    'high': np.array([]),
    'low': np.array([]),
    'volume': np.array([])
}

for candle in total:
    inputs["close"] = np.append(inputs["close"], candle["close"])
    inputs["high"] = np.append(inputs["high"], candle["max"])
    inputs["low"] = np.append(inputs["low"], candle["min"])
    inputs["volume"] = np.append(inputs["volume"], candle["volume"])
    
    
total_wins = 0
total_losses = 0


rsi_periods = 6
mfi_periods = 6
cci_periods = 17

# Testar todas as combinações possíveis
rsi = talib.RSI(inputs['close'], timeperiod=rsi_periods)
mfi = talib.MFI(inputs['high'], inputs['low'], inputs['close'], inputs['volume'], timeperiod=mfi_periods)
cci = talib.CCI(inputs['high'], inputs['low'], inputs['close'], timeperiod=cci_periods)

win_count = 0
loss_count = 0            
for i in range(max(rsi_periods, mfi_periods, cci_periods), len(total)):
    if rsi[i-1] > 65 and mfi[i-1] > 66 and cci[i] < 84:
        # Sell
        if total[i]['close'] < total[i-1]['close']:
            win_count += 1
        else:
            loss_count += 1
    elif rsi[i-1] < 30 and mfi[i-1] < 30 and cci[i] > -81:
        # Buy
        if total[i]['close'] > total[i-1]['close']:
            win_count += 1
        else:
            loss_count += 1
        
total_wins += win_count
total_losses += loss_count
winrate = win_count / (win_count + loss_count)



#with open("resultado.txt", "a") as f:
    #f.write(f"RSI periodo: {rsi_sobrecompra} | MFI sobrecompra: {mfi_sobrecompra} | cci sobrecompra: {cci_sobrecompra} | Wins: {win_count} | Loses: {loss_count} | Winrate: {winrate * 100:.2f}%\n")
print(f"Wins: {win_count} | Loses: {loss_count} | Winrate: {winrate * 100:.2f}%")


total_trades = total_wins + total_losses
winrate = total_wins / total_trades
lossrate = total_losses / total_trades

profit_per_trade = 2 * winrate - 2 * lossrate
total_profit = profit_per_trade * total_trades
banca_atual = 40 + total_profit

#print(f"Total trades: {total_trades}")
#print(f"Total wins: {winrate * 100:.2f}%")
#print(f"Total loss: {lossrate * 100:.2f}%")
#print(f"Total profit trades: {profit_per_trade * 100:.2f}%")
#print(f"Total total de ganho: {total_profit}")
#print(f"Total banca atual: {banca_atual}")

#1666 - 102