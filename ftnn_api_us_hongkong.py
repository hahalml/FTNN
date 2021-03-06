#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
'''
Created on 2015年8月26日
@author: futu
'''

#时区采用的是汉城时区

#如果这个分钟内没有一笔成交，这个是

import socket
import json
import string
import sys
from time import sleep
import time
import os
import pandas as pd
import math
import numpy as np

import winsound

def Example_Analysis():
    global file_souji_fengzhong
    global local_date_4_file

    global stock_number
    global market_name

    wav_file_up="C:\\Windows\\Media\\StarWar_force.wav"
    wav_file_down="C:\\Windows\\Media\\StarWar_nuclear.wav"
    file_result_example="C:\\IBM-9\\FTNN_HK\\Analysis_out_example"+"_"+market_name+"_"+stock_number+"_"+local_date_4_file+".csv"

    if os.path.exists(file_result_example)==False:
        f=open(file_result_example,"w")
        print >>f,"MA Up/Down,Time,MA5,MA10,MA20,MA30,MA60"
        f.close()

    df_tmp=pd.read_csv(file_souji_fengzhong)
    last_line_data=df_tmp.tail(1)
    #if len(df_tmp)>0 and math.isnan(last_line_data.ix[:,8])==False:

    if len(df_tmp)>20:
        if (last_line_data.ix[:,4] > last_line_data.ix[:,5]).bool() and \
            (last_line_data.ix[:,5] > last_line_data.ix[:,6]).bool():
            #last_line_data.ix[0,6] > last_line_data.ix[0,7] and \
            #last_line_data.ix[0,7] > last_line_data.ix[0,8] :
            winsound.PlaySound(wav_file_up, winsound.SND_NODEFAULT)
            f=open(file_result_example,"a")
            print >>f,"Up,"+str(list(last_line_data.ix[:,0]).pop())+","\
                        +str(list(last_line_data.ix[:,4]).pop())+","\
                        +str(list(last_line_data.ix[:,5]).pop())+","\
                        +str(list(last_line_data.ix[:,6]).pop())+","\
                        +str(list(last_line_data.ix[:,7]).pop())+","\
                        +str(list(last_line_data.ix[:,8]).pop())
            f.close()

        elif (last_line_data.ix[:,4] < last_line_data.ix[:,5]).bool() and \
              (last_line_data.ix[:,5] < last_line_data.ix[:,6]).bool():
            #last_line_data.ix[0,6] < last_line_data.ix[0,7] and \
            #last_line_data.ix[0,7] < last_line_data.ix[0,8] :
            winsound.PlaySound(wav_file_down, winsound.SND_NODEFAULT)
            f=open(file_result_example,"a")
            print >>f,"Down,"+str(list(last_line_data.ix[:,0]).pop())+","\
                       +str(list(last_line_data.ix[:,4]).pop())+","\
                       +str(list(last_line_data.ix[:,5]).pop())+","\
                       +str(list(last_line_data.ix[:,6]).pop())+","\
                       +str(list(last_line_data.ix[:,7]).pop())+","\
                       +str(list(last_line_data.ix[:,8]).pop())
            f.close()

def MA_xielv(XieLv_Num,MA5,MA10,MA20,MA30,MA60,MA120):
    global df_5
    df_tmp=df_5.tail(XieLv_Num-1).head(1)
    lenth_df_tmp=len(df_5)
    if lenth_df_tmp>5 and math.isnan(df_tmp.ix[:,4])==False:
        MA5_xielv=(MA5-list(df_tmp.ix[:,4]).pop())/list(df_tmp.ix[:,4]).pop()
    else:
        MA5_xielv=np.nan

    if lenth_df_tmp>10 and math.isnan(df_tmp.ix[:,5])==False:
        MA10_xielv=(MA10-list(df_tmp.ix[:,5]).pop())/list(df_tmp.ix[:,5]).pop()
    else:
        MA10_xielv=np.nan

    if lenth_df_tmp>20 and math.isnan(df_tmp.ix[:,6])==False:
        MA20_xielv=(MA20-list(df_tmp.ix[:,6]).pop())/list(df_tmp.ix[:,6]).pop()
    else:
        MA20_xielv=np.nan

    if lenth_df_tmp>30 and math.isnan(df_tmp.ix[:,7])==False:
        MA30_xielv=(MA30-list(df_tmp.ix[:,7]).pop())/list(df_tmp.ix[:,7]).pop()
    else:
        MA30_xielv=np.nan

    if lenth_df_tmp>60 and math.isnan(df_tmp.ix[:,8])==False:
        MA60_xielv=(MA60-list(df_tmp.ix[:,8]).pop())/list(df_tmp.ix[:,8]).pop()
    else:
        MA60_xielv=np.nan

    if lenth_df_tmp>120 and math.isnan(df_tmp.ix[:,9])==False:
        MA120_xielv=(MA120-list(df_tmp.ix[:,9]).pop())/list(df_tmp.ix[:,9]).pop()
    else:
        MA120_xielv=np.nan

    return MA5_xielv,MA10_xielv,MA20_xielv,MA30_xielv,MA60_xielv,MA120_xielv


def MA(MA_x,Latest_Value):
    global file_souji_fengzhong
    df_tmp=pd.read_csv(file_souji_fengzhong,index_col=0)
    value_tmp=(df_tmp.ix[:,3].tail(MA_x-1).sum()+Latest_Value)/MA_x
    return value_tmp

def MACD(Latest_Value):
    #使用通达信的MACD计算方法：
    #第一天：EMA_12=收盘价；EMA_26=收盘价；DIF=0；DEA=0;MACD=0(不套用公式）
    #第二天-第N天:套用公式
    #EMA（12）= 前一日EMA（12）×11/13＋今日收盘价×2/13
    #EMA（26）= 前一日EMA（26）×25/27＋今日收盘价×2/27
    #DIFF=今日EMA（12）- 今日EMA（26）
    #DEA（MACD）= 前一日DEA×8/10＋今日DIF×2/10
    #BAR=2×(DIFF－DEA)
    #参考http://blog.sina.com.cn/s/blog_5938eb510100fz89.html

    global file_souji_fengzhong

    short = 12
    long = 26
    mid = 9
    df_tmp=pd.read_csv(file_souji_fengzhong,index_col=0)
    MACD_EMA_SHORT_POSITION=df_tmp.columns.searchsorted('MACD_EMA_12')

    if len(df_tmp)==0:
        MACD_EMA_short=Latest_Value
        MACD_EMA_long =Latest_Value
        MACD_DIF = 0
        MACD_DEA = 0
        MACD_MACD = 0

    else:
        Last_Trade_4_MACD=df_tmp.tail(1)
        MACD_EMA_short=Last_Trade_4_MACD.ix[0,MACD_EMA_SHORT_POSITION]*(short-1)/(short+1)+\
                       Latest_Value*2/(short+1)

        MACD_EMA_long=Last_Trade_4_MACD.ix[0,MACD_EMA_SHORT_POSITION+1]*(long-1)/(long+1)+\
                       Latest_Value*2/(long+1)

        MACD_DIF = MACD_EMA_short - MACD_EMA_long

        MACD_DEA =Last_Trade_4_MACD.ix[0,MACD_EMA_SHORT_POSITION+3]*(mid-1)/(mid+1)+\
                  MACD_DIF*2/(mid+1)

        MACD_MACD = (MACD_DIF - MACD_DEA) * 2

    return MACD_EMA_short,MACD_EMA_long,MACD_DIF,MACD_DEA,MACD_MACD

which_market='2'
stock_number='BABA'
if which_market=="1":
    market_name="hk"
elif which_market=="2":
    market_name="us"
else:
    market_name="XX"

# 上一分钟信息
LastMinute=None
LastTradeOrderTime=None

#local_date_4_file=time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()-24*60*60))
local_date_4_file=time.strftime('%Y%m%d',time.localtime(time.time()-24*60*60))

file_souji_tmp="C:\\IBM-9\\FTNN_HK\\ftnn_souji_"+market_name+"_"+stock_number+"_"+local_date_4_file+".csv"
file_souji_all="C:\IBM-9\FTNN_HK\\ftnn_souji_all_"+market_name+"_"+stock_number+"_"+local_date_4_file+".csv"
file_souji_fengzhong="C:\IBM-9\FTNN_HK\\ftnn_souji_fengzhong_"+market_name+"_"+stock_number+"_"+local_date_4_file+".csv"

df_4=pd.DataFrame()
df_5=pd.DataFrame()
df_6=pd.DataFrame()

#futnn plubin会开启本地监听服务端
# 请求及发送数据都是jason格式, 具体详见插件的协议文档
host="localhost"
port=11111


local_date=time.strftime('%Y-%m-%d',time.localtime(time.time()-24*60*60))

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

#需要确认电脑时区是香港时区
now_time=time.localtime(time.time()-24*60*60)
if which_market=='1':
    if (now_time>time.strptime(local_date+" "+"9:30:00", "%Y-%m-%d %H:%M:%S") and \
        now_time<time.strptime(local_date+" "+"12:00:01", "%Y-%m-%d %H:%M:%S")) or \
        (now_time>time.strptime(local_date+" "+"13:00:00", "%Y-%m-%d %H:%M:%S") and \
        now_time<time.strptime(local_date+" "+"16:00:01", "%Y-%m-%d %H:%M:%S")):
        in_time_range=1
    else:
        in_time_range=0
elif which_market=='2':
    if now_time>time.strptime(local_date+" "+"9:30:00", "%Y-%m-%d %H:%M:%S") and \
        now_time<time.strptime(local_date+" "+"16:00:01", "%Y-%m-%d %H:%M:%S"):
        in_time_range=2
    else:
        in_time_range=0
else:
    in_time_range=0

while in_time_range>0:
    actual_second=time.strftime("%S",now_time)
    if int(actual_second)%2!=0:
        #发送报价请求，Market为2表示是美股
        #req = {'Protocol':'1001', 'ReqParam':{'Market':'1','StockCode':'00700'},'Version':'1'}
        req = {'Protocol':'1001', 'ReqParam':{'Market':which_market,'StockCode':stock_number},'Version':'1'}
        #req = {'Protocol':'1001', 'ReqParam':{'Market':'1','StockCode':'00700'},'Version':'1'}
        #req = {'Protocol':'1001', 'ReqParam':{'Market':'1','StockCode':'01585'},'Version':'1'}
        str_1 = json.dumps(req) + "\n"
        print str_1
        s.send(str_1)
        rsp = ""
        while True:
            buf = s.recv(1024)
            rsp = rsp + buf
            #找到"\n"就认为结束了
            try:
                rsp.index('\n')
                break;
            except Exception, e:
                print "recving..."
        print rsp

        rsp_current_price_str=rsp.split(',')[4]
        current_price=rsp_current_price_str.split('"')[3]

        #输出的时间是按秒计算的，现在距离0点0分0秒多长时间
        rsp_current_time_str=rsp.split(',')[11]
        current_time=rsp_current_time_str.split('"')[3]
        trade_order_time=current_time
        current_hour=int(current_time)/3600
        current_minute=(int(current_time)-current_hour*3600)/60
        current_second=int(current_time)-current_hour*3600-current_minute*60

        actual_minute=time.strftime("%M",now_time)
        actual_hour=time.strftime("%H",now_time)

        print current_hour
        print current_minute
        print current_second
        print current_price
        print "------"
        print actual_hour
        print actual_minute
        print actual_second


        print "LastMinute:",LastMinute
        print "actual_minute:",actual_minute
        print "current_minute:",current_minute

        if LastMinute!=None:
            if ( (int(actual_minute)<=int(LastMinute) and int(actual_hour)==int(LastHour)) or int(actual_hour)<int(LastHour)  ):
                print "(int(actual_minute)<=int(LastMinute) and int(actual_hour)==int(LastHour)) or int(actual_hour)<int(LastHour)"
            else:
                print "(int(actual_minute)<=int(LastMinute) and int(actual_hour)==int(LastHour)) or int(actual_hour)<int(LastHour) NOT OK"

            if ( (int(current_minute)<=int(LastMinute) and int(current_hour)==int(LastHour))  or int(current_hour)<int(LastHour)  ):
                print "(int(current_minute)<=int(LastMinute) and int(current_hour)==int(LastHour))  or int(current_hour)<int(LastHour)"
            else:
                print "(int(current_minute)<=int(LastMinute) and int(current_hour)==int(LastHour))  or int(current_hour)<int(LastHour) NOT OK"

        if LastMinute==None or \
            (   (   (int(actual_minute)<=int(LastMinute) and int(actual_hour)==int(LastHour)) or int(actual_hour)<int(LastHour) )and \
                (   (int(current_minute)<=int(LastMinute) and int(current_hour)==int(LastHour))  or int(current_hour)<int(LastHour) ) ):
            if os.path.exists(file_souji_tmp)==False:
                f=open(file_souji_tmp,"w")
                print>>f,"Date,Price"
                f.close()

            if os.path.exists(file_souji_all)==False:
                f=open(file_souji_all,"w")
                print>>f,"Date,Price"
                f.close()

            if os.path.exists(file_souji_fengzhong)==False:
                f=open(file_souji_fengzhong,"w")
                print>>f," ,open,high,low,close,MA5,MA10,MA20,MA30,MA60,MA120,MA5_XieLv_0,MA10_XieLv_0,MA20_XieLv_0,MA30_XieLv_0,MA60_XieLv_0,MA120_XieLv_0,MACD_EMA_12,MACD_EMA_26,MACD_DIF,MACD_DEA,MACD_MACD"
                f.close()

            f=open(file_souji_tmp,"a")
            print>>f,local_date+" "+str(current_hour)+":"+str(current_minute)+":"+str(current_second)+","+str(current_price)
            f.close()

        else:
            df_1=pd.read_csv(file_souji_tmp)
            df_4=pd.read_csv(file_souji_all)
            df_4=df_4.append(df_1,ignore_index=True)
            df_4.to_csv(file_souji_all,index=False)

            df_1.index=pd.tseries.index.DatetimeIndex(df_1.ix[:,0])
            df_2=df_1.ix[:,1]
            df_3=df_2.resample('1min',how='ohlc')

            df_5=pd.read_csv(file_souji_fengzhong,index_col=0)
            #df_tmp=df_3.ix[0]


            if len(df_5)==0:
                df_tmp=df_3.tail(1)
            elif df_3.head(1).index>pd.tseries.index.DatetimeIndex(df_5.tail(1).index):
                df_tmp=df_3.head(1)
            elif df_3.tail(1).index>pd.tseries.index.DatetimeIndex(df_5.tail(1).index):
                df_tmp=df_3.tail(1)
            else:
                #就是为了更换一个index,需要这么麻烦吗
                if int(actual_minute)==0:
                    #针对整点，分钟为0的场景，减1分钟应该是59分，而不是-1
                    str_tmp=time.strftime("%Y-%m-%d ",now_time)+str(int(actual_hour)-1)+':59'
                else:
                    str_tmp=time.strftime("%Y-%m-%d %H:",now_time)+str(int(actual_minute)-1) #就是为了更换一个index,需要这么麻烦吗
                df_7 = pd.DataFrame(df_tmp.ix[0].open, index=[str_tmp],columns=['open'])
                df_7['high']=df_tmp['high'].ix[0]
                df_7['low'] =df_tmp['low'].ix[0]
                df_7['close'] =df_tmp['close'].ix[0]
                df_tmp=df_7

            print df_tmp
            print "------"
            print df_3
            print "*****"
            print actual_minute

            #trade_order_time!=LastTradeOrderTime

            #df_tmp=df_3.tail(1)

            MA5_tmp=MA(5,df_tmp.ix[0,3])
            MA10_tmp=MA(10,df_tmp.ix[0,3])
            MA20_tmp=MA(20,df_tmp.ix[0,3])
            MA30_tmp=MA(30,df_tmp.ix[0,3])
            MA60_tmp=MA(60,df_tmp.ix[0,3])
            MA120_tmp=MA(120,df_tmp.ix[0,3])

            df_tmp['MA5']=MA5_tmp
            df_tmp['MA10']=MA10_tmp
            df_tmp['MA20']=MA20_tmp
            df_tmp['MA30']=MA30_tmp
            df_tmp['MA60']=MA60_tmp
            df_tmp['MA120']=MA120_tmp

            #计算各个MA斜率
            XieLv_Num=3
            MA5_xielv,MA10_xielv,MA20_xielv,MA30_xielv,MA60_xielv,MA120_xielv=MA_xielv(XieLv_Num,MA5_tmp,MA10_tmp,MA20_tmp,MA30_tmp,MA60_tmp,MA120_tmp)

            df_tmp['MA5_XieLv_0']= MA5_xielv
            df_tmp['MA10_XieLv_0']= MA10_xielv
            df_tmp['MA20_XieLv_0']= MA20_xielv
            df_tmp['MA30_XieLv_0']= MA30_xielv
            df_tmp['MA60_XieLv_0']= MA60_xielv
            df_tmp['MA120_XieLv_0']= MA120_xielv


            #增加MACD
            MACD_EMA_short,MACD_EMA_long,MACD_DIF,MACD_DEA,MACD_MACD=MACD(df_tmp.ix[0,3])

            df_tmp['MACD_EMA_12']=MACD_EMA_short
            df_tmp['MACD_EMA_26']=MACD_EMA_long
            df_tmp['MACD_DIF']=MACD_DIF
            df_tmp['MACD_DEA']=MACD_DEA
            df_tmp['MACD_MACD']=MACD_MACD

            df_5=df_5.append(df_tmp)

            df_5.to_csv(file_souji_fengzhong)

            os.remove(file_souji_tmp)
            #写入新分钟的成交数据
            f=open(file_souji_tmp,"w")
            print>>f,"Date,Price"
            print>>f,local_date+" "+str(current_hour)+":"+str(current_minute)+":"+str(current_second)+","+str(current_price)
            f.close()

            # Example:To Analysis Data
            Example_Analysis()

            #似乎还要往前
            LastTradeOrderTime=trade_order_time
            #caculate_zhibiao(df_3.ix[0,0],)
            #caculate_MACD(df_3)

        if int(actual_hour)> int(current_hour):
            LastHour=actual_hour
            LastMinute=actual_minute
        elif int(actual_hour)== int(current_hour):
            LastHour=current_hour
            LastMinute=max(int(actual_minute),int(current_minute))
        elif int(actual_hour)< int(current_hour):
            LastHour=current_hour
            LastMinute=current_minute

    # noinspection PyUnboundLocalVariable,PyUnboundLocalVariable
    sleep(1)

    now_time=time.localtime(time.time()-24*60*60)
    if which_market=='1':
        if (now_time>time.strptime(local_date+" "+"9:30:00", "%Y-%m-%d %H:%M:%S") and \
            now_time<time.strptime(local_date+" "+"12:00:01", "%Y-%m-%d %H:%M:%S")) or \
            (now_time>time.strptime(local_date+" "+"13:00:00", "%Y-%m-%d %H:%M:%S") and \
            now_time<time.strptime(local_date+" "+"16:00:01", "%Y-%m-%d %H:%M:%S")):
            in_time_range=1
        else:
            in_time_range=0
    elif which_market=='2':
        if now_time>time.strptime(local_date+" "+"9:30:00", "%Y-%m-%d %H:%M:%S") and \
            now_time<time.strptime(local_date+" "+"16:00:01", "%Y-%m-%d %H:%M:%S"):
            in_time_range=2
        else:
            in_time_range=0
    else:
        in_time_range=0
