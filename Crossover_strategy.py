import pandas as pd
import datetime as dt
import mplfinance as mpf
import numpy as np
import sys, os


def swing_finder(df,long_index,long_short,long_index_row):
    try:
        df = df.rename(columns={'high':'High','open':'Open',
                                'low':'Low','close':'Close'})
        date_column='dateTime'
        swing_high_index=0
        swing_low_index=0
        swing_formed=False
        swing_first=False
        swing_formed2=False
        swing_first2=False
        low_formed=False
        high_formed=False
        flag_first_high, flag_first_low = '', ''
        first = dt.datetime(1900, 1, 1, 9, 15)
        second = dt.datetime(1900, 1, 1, 9, 20)
        for i in range(long_index_row,len(df)):
            time_of_day = str((df['Date_Time'])[i])[11:]
            time = df.index[i]
            if long_short == 'short':
                if time==df.index[long_index_row]:
                    anchorbar=i
                    df.iloc[i,anchors_swing_id] = 'anchor'
                    flag_first_high=True

                        
                if swing_formed==False:
                    if flag_first_high==True:
                        if df['High'][i]>df['High'][anchorbar]:
                            anchorbar=i
                            df.iloc[i,anchors_swing_id] = 'anchor'
                            swing_first=False
                        elif df['High'][i]<df['High'][anchorbar] and df['Low'][i]<df['Low'][anchorbar] and df['Close'][i]<df['Close'][anchorbar] and  swing_first==False:
                            swing_first=True
                            swing_first_candle=i
                            df.iloc[i,anchors_swing_id] = 'first_candle'

                        if swing_first==True and swing_formed==False and long_index<df.index[i] and swing_first_candle != i:
                            if df['High'][i]<df['High'][anchorbar] and df['Low'][i]<df['Low'][anchorbar] and df['Close'][i]<df['Close'][anchorbar]:
                                swing_formed=True
                                high_formed=True
                                swing_high_index=anchorbar
                                df.iloc[i,anchors_swing_id] = 'second_candle'
                                if long_short =='short':
                                    break
                            

            #####ENTER SWING LOW(long side exit)
            if long_short=='long':
                if time==df.index[long_index_row]:
                    anchorbar2=i
                    df.iloc[i,anchors_swing_id] = 'anchor low'

                    flag_first_low=True
                        
                if swing_formed2==False:
                    if flag_first_low==True:
                        if df['Low'][i]<df['Low'][anchorbar2]:
                            anchorbar2=i
                            df.iloc[i,anchors_swing_id] = 'anchor low'

                            swing_first2=False

                        elif df['High'][i]>df['High'][anchorbar2] and df['Low'][i]>df['Low'][anchorbar2] and df['Close'][i]>df['Close'][anchorbar2] and swing_first2==False:
                            swing_first2=True
                            df.iloc[i,anchors_swing_id] = 'first candle'

                            swing_first_candle2=i

                        if swing_first2==True and swing_formed2==False and swing_first_candle2 != i:
                            if df['High'][i]>df['High'][anchorbar2] and df['Low'][i]>df['Low'][anchorbar2] and df['Close'][i]>df['Close'][anchorbar2] and long_index<df.index[i]:
                                swing_formed2=True
                                low_formed=True
                                df.iloc[i,anchors_swing_id] = 'second candle'

                                swing_low_index=anchorbar2
                                if long_short =='long':
                                    break

            if time_of_day ==  '3:10:00':
                flag_first_high= False
                flag_first_low = False
                
        return low_formed,high_formed,swing_high_index,swing_low_index
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
            
file_name = input('enter the file name without .csv\n:')
sl_type = input('sl type?\n1.Exit at 3:10 close or\n2.TSL(swing exit)\nEnter:')
df=pd.read_csv(file_name +'.csv')

#df changes
df['action']=''
action_id = df.columns.get_loc('action')
df['start']=float()
start_id = df.columns.get_loc('start')
df['result']=''
result_id = df.columns.get_loc('result')
df['points']=float()
points_id = df.columns.get_loc('points')
df['crossover']=''
first ='09:15:00'
crossover_id = df.columns.get_loc('crossover')
df['crossunder']=''
crossunder_id = df.columns.get_loc('crossunder')
df['formation']=''
formation_id = df.columns.get_loc('formation')
df['formation2']=''
formation_id2 = df.columns.get_loc('formation2')
df['formation3']=''
formation_id3 = df.columns.get_loc('formation3')
df['formation4']=''
formation_id4 = df.columns.get_loc('formation4')
df['anch']=''
anch_id = df.columns.get_loc('anch')
df['anch2']=''
anch_id2 = df.columns.get_loc('anch2')

df['entry_price']=float()
entry_price_id = df.columns.get_loc('entry_price')
df['sl_price']=float()
sl_price_id = df.columns.get_loc('sl_price')

df['exit_price']=float()
exit_price_id = df.columns.get_loc('exit_price')

df['first_candle']=float()
first_candle_id = df.columns.get_loc('first_candle')

df['anchors_swing']=''
anchors_swing_id = df.columns.get_loc('anchors_swing')


df['Reason']=''
Reason_id = df.columns.get_loc('Reason')
df['ema'] = df['Close'].ewm(span=20, adjust=False).mean()

df['Date_Time']=pd.to_datetime(df['Date_Time'],dayfirst=True)
df = df.set_index('Date_Time',drop=False)


position_status='close'
last = '15:10:00'
final = '15:25:00'
first ='09:15:00'
begin_trade = False

first_candle_long_sl = False
first_candle_short_sl = False

prev_day_high, day_high = 0, 0
prev_day_low, day_low = 10000000, 100000000

exit_when_swing_long,exit_when_swing_short =False, False
canexit,can_exit = False, False
position_status = 'close'
for i in range(1,len(df)):
    df.iloc[i,points_id]=df.iloc[i-1,points_id]
    date=str(df.index[i])[11:19]
    if date==first and begin_trade == True:
        if df['Low'][i]>prev_day_high:
            first_value = 'gap-up'
        elif df['High'][i]<prev_day_low:
            first_value = 'gap-down'

        elif df['Low'][i] < prev_day_high and df['High'][i] > prev_day_high:
            first_value = 'break-up'


        elif df['High'][i] > prev_day_low and df['Low'][i] < prev_day_low:
            first_value = 'break-down'

        else:
            first_value= 'within Prev day Range'

    if begin_trade == True:
        try:
            df.iloc[i,first_candle_id] = first_value
        except:
            hl=1
            
            
    ###Exit######
    #TAKE PROFIT/STOPLOSS buy-side
    if position_status == 'open_buy':
        if sl_type == '1':
            if date == last:
                df.iloc[i,result_id] ='Exit'
                position_status = 'close'
                df.iloc[i,exit_price_id]  =  df['Close'][i]
                df.iloc[i,points_id]=df.iloc[i,points_id]-(entryprice-df['Close'][i])
                df.iloc[i,Reason_id]='Exit @ 03:15'
                exit_when_swing_long = False
                begin_trade = False
                canexit = False
                
            if df['Low'][i] < slprice and position_status == 'open_buy':
                df.iloc[i,result_id]='SL'
                position_status='close'
                df.iloc[i,exit_price_id]=slprice
                df.iloc[i,points_id]=df.iloc[i,points_id]-(entryprice-slprice)
                df.iloc[i,Reason_id]='SL HIT'
                exit_when_swing_long = False
                begin_trade = False
                canexit = False
        else:
            if exit_when_swing_long == False and canexit == False:
                if df['Close'][i]<df['ema'][i]:
                    exit_when_swing_long = True
                    long_index = df.index[i]
                    long_index_row = i
                    
            if exit_when_swing_long == True: 
                low_formed,high_formed,swing_high_index,swing_low_index = swing_finder(df,long_index,'long',long_index_row)
                if low_formed == True:
                    triggerprice = df['Low'][swing_low_index]
                    df.iloc[swing_low_index,sl_price_id] = triggerprice
                    i = swing_low_index - 1
                    exit_when_swing_long = False
                    canexit = True
                
            if canexit == True:
                if df['Low'][i]<triggerprice and position_status == 'open_buy':
                    canexit = False
                    df.iloc[i,result_id] ='Exit'
                    position_status = 'close'
                    df.iloc[i,exit_price_id] = triggerprice
                    df.iloc[i,points_id] = df.iloc[i,points_id]-(entryprice-triggerprice)
                    df.iloc[i,Reason_id] = 'TSL'
                    df.iloc[i,sl_price_id] = triggerprice
                    exit_when_swing_long = False
                    begin_trade = False
                    canexit = False

            if date == last and position_status == 'open_buy':
                df.iloc[i,result_id] ='Exit'
                position_status = 'close'
                df.iloc[i,exit_price_id]  =  df['Close'][i]
                df.iloc[i,points_id]=df.iloc[i,points_id]-(entryprice-df['Close'][i])
                df.iloc[i,Reason_id]='Exit @ 03:15'
                exit_when_swing_long = False
                begin_trade = False
                canexit = False
                
            if df['Low'][i] < slprice and position_status == 'open_buy':
                df.iloc[i,result_id]='SL'
                position_status='close'
                df.iloc[i,exit_price_id]=slprice
                df.iloc[i,points_id]=df.iloc[i,points_id]-(entryprice-slprice)
                df.iloc[i,Reason_id]='SL HIT'
                exit_when_swing_long = False
                begin_trade = False
                canexit = False
                    
    ##########SHORT POSITION EXIT
    if position_status == 'open_sell':
        if sl_type == '1':
            if date == last:
                df.iloc[i,result_id]='Exit'
                position_status='close'
                df.iloc[i,exit_price_id]=df['Close'][i]
                df.iloc[i,points_id]=df.iloc[i,points_id]+(entry_price-df['Close'][i])
                df.iloc[i,Reason_id]='Exit @ 03:15'
                exit_when_swing_short = False
                begin_trade = False
                can_exit = False
            
            if df['High'][i] > sl_price and position_status == 'open_sell':
                df.iloc[i,result_id]='SL'
                position_status='close'
                df.iloc[i,exit_price_id]=sl_price
                df.iloc[i,points_id]=df.iloc[i,points_id]+(entry_price-sl_price)
                df.iloc[i,Reason_id]='SL HIT'
                exit_when_swing_short = False
                begin_trade = False
                can_exit = False
                
        else:
            df.iloc[i,sl_price_id] = sl_price
            
            if exit_when_swing_short == False and can_exit == False:
                if df['Close'][i]>df['ema'][i]:
                    exit_when_swing_short = True
                    long_index = df.index[i]
                    long_index_row = i
                
            if exit_when_swing_short == True: 
                low_formed,high_formed,swing_high_index,swing_low_index = swing_finder(df,long_index,'short',long_index_row)
                if high_formed == True:
                    trigger_price = df['High'][swing_high_index]
                    df.iloc[swing_high_index,sl_price_id] = trigger_price
                    i = swing_high_index - 1
                    exit_when_swing_short = False
                    can_exit = True
                    
            if can_exit == True:
                if df['High'][i] > trigger_price and position_status == 'open_sell':
                    can_exit = False
                    df.iloc[i,result_id] = 'Exit'
                    position_status = 'close'
                    df.iloc[i,exit_price_id] = trigger_price
                    df.iloc[i,points_id] = df.iloc[i,points_id]+(entry_price-trigger_price)
                    df.iloc[i,Reason_id] = 'TSL'
                    df.iloc[i,sl_price_id] = trigger_price
                    exit_when_swing_short = False
                    begin_trade = False
                    can_exit = False
                    
            if date == last and position_status == 'open_sell':
                df.iloc[i,result_id]='Exit'
                position_status='close'
                df.iloc[i,exit_price_id]=df['Close'][i]
                df.iloc[i,points_id]=df.iloc[i,points_id]+(entry_price-df['Close'][i])
                df.iloc[i,Reason_id]='Exit @ 03:15'
                exit_when_swing_short = False
                begin_trade = False
                can_exit = False

            if df['High'][i] > sl_price and position_status == 'open_sell':
                df.iloc[i,result_id]='SL'
                position_status='close'
                df.iloc[i,exit_price_id]=sl_price
                df.iloc[i,points_id]=df.iloc[i,points_id]+(entry_price-sl_price)
                df.iloc[i,Reason_id]='SL HIT'
                exit_when_swing_short = False
                begin_trade = False
                can_exit = False
            
    #LONG (Entering trade)
    if date == first:
        day_high = df['High'][i]
        day_low = df['Low'][i]
        if df['High'][i]> prev_day_high:
            prev_day_high = df['High'][i]
            first_candle_long_sl = True
            firstslprice = df['Low'][i]
            
        if df['Low'][i]< prev_day_low:
            prev_day_low = df['Low'][i]
            first_candle_short_sl = True
            firstsl_price = df['High'][i]
    else:
        if df['High'][i]>day_high:
            day_high = df['High'][i]
        if df['Low'][i]<day_low:
            day_low = df['Low'][i]
            
        if (position_status=='close') and begin_trade == True and date<last:   
            if df['High'][i]> prev_day_high:
                df.iloc[i,action_id] = 'long'
                y = i
                position_status = 'open_buy'
                entryprice = prev_day_high
                df.iloc[i,entry_price_id] = entryprice
                if first_candle_long_sl == False:
                    slprice = df['Low'][i-1]
                else:
                    slprice = firstslprice
                df.iloc[i,sl_price_id] = slprice
                    
            elif df['Low'][i]< prev_day_low:
                df.iloc[i,action_id] = 'short'
                y = i
                position_status ='open_sell'
                entry_price=prev_day_low
                df.iloc[i,entry_price_id]=prev_day_low
                if first_candle_short_sl == False:
                    sl_price=df['High'][i-1]
                else:
                    sl_price=firstsl_price
                df.iloc[i,sl_price_id]=sl_price
                
    if date == final:
        prev_day_high = day_high
        prev_day_low = day_low
        begin_trade = True
        first_candle_short_sl = False
        first_candle_long_sl = False
        
####PLOTTIN
profits=[]
actions=[]
trade=0
Tp=0
Sl=0
#RESULT#####
for i in range(len(df)):
    if df['result'][i]=='Exit':
        profits.append(df['High'][i])
    else:
        profits.append(np.nan)

for i in range(len(df)):        
    if df['action'][i]=='long' or df['action'][i]=='short':
        actions.append(df['Close'][i])
        trade=trade+1
    else:
        actions.append(np.nan)
   

print('no. of trades:{}'.format(trade))  

kwargs = dict(type='candle',volume=False,figratio=(15,8),figscale=1)
apd = [mpf.make_addplot(actions,type='scatter',color='yellow',marker='^',markersize=100),
       mpf.make_addplot(profits,type='scatter',color='red',marker='v',markersize=100),
       mpf.make_addplot(df['ema'],type='line',color='red'),]
mpf.plot(df,addplot=apd,**kwargs,style='yahoo')
    
date_column='Date_Time'
column_names = ["Entry Date", "Exit Date","Entry Time",
                "stock_name",'Reason', "Trade","Entry Price",
                "Exit Time", "Exit Price", "Points made",
                "SL","points till here","SL price","ema",'first candle']

result=pd.DataFrame(column_names)

df.to_csv('wholedata.csv')



####RESULTS WITH A TRADESHEET:
df2=df[0:0]
for i in range(len(df)):
    if df['action'][i]=='long' or df['action'][i]=='short'or df['result'][i]=='SL'or df['result'][i]=='TP' or df['result'][i]=='Exit':
            df2=df2.append(df.iloc[i],ignore_index=True)

for i in range(1,len(df2)):       
    if df2['result'][i]=='Exit' or df2['result'][i]=='SL':
        slprice = df2['sl_price'][i-1]
##        else:
##            slprice = df2['sl_price'][i]
        if (df2['points'][i]-df2['points'][i-1])>=0:

            result=result.append([{'Entry Date':str(df2[date_column][i-1])[:10],
                                   'Entry Time':str(df2[date_column][i-1])[10:19],
                                   'Trade':df2['action'][i-1],
                                   'Entry Price':df2['entry_price'][i-1],
                                   'Exit Date':str(df2[date_column][i])[:10],
                                   'Exit Time':str(df2[date_column][i])[10:19],
                                   'Exit Price':df2['exit_price'][i],
                                   'Points Made':round(df2['points'][i]-df2['points'][i-1],1),
                                   'SL':'SL',
                                   'points till here':round((df2['points'][i]),2),
                                   'SL price': slprice,
                                   "stock_name":'test',
                                   'Reason':df2['Reason'][i],
                                   "ema":df2['ema'][i],
                                   "first candle": df2['first_candle'][i-1]}],
                                  ignore_index=True)
            
        elif (df2['points'][i]-df2['points'][i-1])<0:
            result=result.append([{'Entry Date':str(df2[date_column][i-1])[:10],
                                   'Entry Time':str(df2[date_column][i-1])[10:19],
                                   'Trade':df2['action'][i-1],
                                   'Entry Price':df2['entry_price'][i-1],
                                   'Exit Date':str(df2[date_column][i])[:10],
                                   'Exit Time':str(df2[date_column][i])[10:19],
                                   'Exit Price':df2['exit_price'][i],
                                   'Points Made':round(df2['points'][i]-df2['points'][i-1],2),
                                   'SL':'SL',
                                   'points till here':round((df2['points'][i]),2),
                                   'SL price':slprice,
                                   "stock_name":'test',
                                   'Reason':df2['Reason'][i],
                                   "ema":df2['ema'][i],
                                   "first candle": df2['first_candle'][i-1]}],
                                  ignore_index=True)
result=result.round(2)
result=result[11:]

for i in range(len(result)):
    
#SLIPPAGE and points
    if result['Trade'].iloc[i]=='short':
        result['Entry Price'].iloc[i]=float(result['Entry Price'].iloc[i])-2
        if result['SL'].iloc[i]=='SL':
            result['Exit Price'].iloc[i]=float(result['Exit Price'].iloc[i])+2
        result['Points Made'].iloc[i]=float(result['Entry Price'].iloc[i])-float(result['Exit Price'].iloc[i])
        
    elif result['Trade'].iloc[i]=='long':
        result['Entry Price'].iloc[i]=float(result['Entry Price'].iloc[i])+2
        if result['SL'].iloc[i]=='SL':
            result['Exit Price'].iloc[i]=float(result['Exit Price'].iloc[i])-2
        result['Points Made'].iloc[i]=float(result['Exit Price'].iloc[i])-float(result['Entry Price'].iloc[i])

            
for i in range(1,len(result)):
    if i==1:
        result['points till here'].iloc[i]=result['Points Made'].iloc[i]
    if result['stock_name'].iloc[i]!=result['stock_name'].iloc[i-1]:
        result['points till here'].iloc[i]=result['Points Made'].iloc[i]
    if result['stock_name'].iloc[i]==result['stock_name'].iloc[i-1]:
        result['points till here'].iloc[i]=result['points till here'].iloc[i-1]+result['Points Made'].iloc[i]


a=' 15:10:00'

for i in range(len(result)):
    if result['Exit Time'].iloc[i]==a and result['Points Made'].iloc[i]>0:
            result['SL'].iloc[i]='Exit/TP'
    elif result['Exit Time'].iloc[i]==a and result['Points Made'].iloc[i]<0:
            result['SL'].iloc[i]='Exit/SL'
            
result.to_csv(file_name+'tradesheet_ver4.csv')

