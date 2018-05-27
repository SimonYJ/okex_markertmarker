
#encoding:utf-8


from OkcoinSpotAPI import OkcoinSpot  #导入官方库
import json
import time
import sys

Info = json.load(open(sys.argv[1])) #导入mm.json中的数据

initCounter = Info['initCounter'] #对json里面的initCounter进行赋值
baseInfo = Info['baseInfo']       #对json里面的baseInfo进行赋值
Names = [Info['currency'] for info in baseInfo] #将currency以列表的形式赋值给Names
marketLength = len[baseInfo]      #取baseInfo的长度进行赋值
Balances = [0.0 for i in range(marketLength)]
buyOrders = [[] for i in range(marketLength)]
sellOrders = [[] for i in range(marketLength)]


config = open['.config','r']
lines = config.readlines()
apikey = lines[0].strip()
secretkey = lines[1].strip()
config.close()

okcoinRESTURL = 'www.okcoin.cn' #国内修改为 www.okcoin.cn
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

flagShow = True
def checkMyOrders(index,orders,targetOrders,Type):
	temp = [order for order in targetOrders]
	uselessOrdersID = []
    for order in orders:
        seq = order[0]
        myPrice = order[1]
        myIOUAmount = order[2]
        flagUseless = True
        for target in temp:
            price = target[0]
            amount = target[1]
            if (abs(myPrice/price - 1)< 0.0001) and (abs(myIOUAmount/amount -1)< 0.1):
                temp.remove(target)
                flagUseless = False
                break
        if flagUseless:
           #
           print(u'现货取消订单')
           print(okcoinSpot.cancelOrder(Names[index]+'_'+Names[0],str(seq)))	
    for target in temp:
        price = target[0]
        amount = target[1]
        #
        print (Names[index]+'_'+Names[0],Type,str(price),str(amount))
        print (okcoinSpot.trade(Names[index]+'_'+Names[0],Type,str(price),str(amount)))

  while  True:
   	   time.sleep(5)
   	   #print(u'用户现货信息')
   	   try:
   	   	  res = json.loads(okcoinSpot.userinfo())
   	   except :
   	   	  continue
       funds = res['info']['funds']
       #print 
       for i in range(marketLength):
           Balances[i] = float(funds['free'][Names[i]])+float(funds['freezed'][Names[i]]) 
   	   #
   	   flagsuc = True
   	   for i in range(i,marketLength):
   	   	   buyOrders[i] = []
   	   	   sellOrders[i] = []
   	   	   try:
   	   	   	   res = json.loads(okcoinSpot.orderinfo(Names[i]+'_'+Names[0],'-1'))
   	   	   except:
   	   	   	   flagsuc = False
   	   	   	   break
   	   	   #print(res)
   	   	   orders = res['orders']
   	   	   for orders in orders:
   	   	   	   info = [order['order_id'],order['price'],order['amount']]
   	   	   	   if order['type'] == 'buy':
   	   	   	   	   buyOrders[i].append(info)
   	   	   	   else order['type'] == 'sell':
   	   	   	   	   sellOrders[i].append(info)
   	   	if not flagsuc:
   	   		continue
   	    #
   	    #################Analyse######################
   	    diff = 0
   	    for t in range(1,marketLength):
   	    	initPrice = baseInfo[t]['initPrice']
   	    	lowLimit = baseInfo[t]['lowLimit']
   	    	highLimit = baseInfo[t]['highLimit']
   	    	gap = baseInfo[t]['gap']
   	    	rate = baseInfo[t]['rate']
   	    	initBase = baseInfo[t]['initBase']
   	    	tradeAmount = baseInfo[t]['tradeAmount']
   	    	orderLengh = baseInfo[t]['orderLengh']



   	    	initbuy = -gap
            initsell = gap 
            balanceState = (Balance[t] - initBase)/tradeAmount

            balanceStateBuy = balanceState
            buyDecimal = balanceStateBuy - math.floor(balanceStateBuy)

            if(buyDecimal < 0.1):
            	buyDecimal = buyDecimal +1;
            	balanceStateBuy = math.floor(balanceStateBuy)
            else:
            	balanceStateBuy = math.ceil(balanceStateBuy)
            buyAounmt = buyDecimal + tradeAmount
            buyPower = initbuy + balanceStateBuy
            buyPrice = initPrice + math.pow(rate,buyPower)

            balanceStateSell = balanceState
            sellDecimal = math.ceil(balanceStateSell) - balanceStateSell
            if(sellDecimal < 0.1):
            	sellDecimal = sellDecimal + 1
            	balanceStateSell = math.ceil(balanceStateSell)
            else:
            	balanceStateSell = math.floor(balanceStateSell)
            sellAounmt = sellDecimal + tradeAmount
            sellPower = initsell + balanceStateSell
            sellPrice = initPrice + math.pow(rate,sellPower)
            diff = diff + (-balanceState)*tradeAmount*buyPrice


            #
            buyTarget = []
            sellTarget = []
            for i in range(orderLengh):
            	if i == 0:
            		buyTarget.append([round(buyPrice,2),round(buyAounmt,2)])
            		sellTarget.append([round(sellPrice,2),round(sellAounmt,3)])
            	else:
            		sellTarget.append([round(sellPrice * math.pow(rate,i),2),round(tradeAmount,3)])
            		buyTarget.append([round(buyPrice * math.pow(rate,-i),2),round(tradeAmount,3)])
            print(Names[t],'\n',buyTarget,'\n',sellTarget)

            if(Balances[t]<tradeAmount * orderLengh):
            	if flagShow:
            		print('not enough'+ Names[t]+'to create sell orders')
            else:
            	checkMyOrders(t,sellPrice[t],sellTarget,'sell')
            if(Balances[0] < tradeAmount * orderLengh*buyPrice)
                print('not enough '+ Balances[0]+'!')
            else:
               checkMyOrders(t,buyOrders[t],buyTarget,'buy')

    if flagShow:
       print('currency Balances:',Balances)
       print('you should have:',initCounter + diff.Names[0]) 
       flagShow = False             

            