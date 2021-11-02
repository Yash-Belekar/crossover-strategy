# crossover-strategy
a crossover strategy backtest on 5 min data (give any csv file with ohlc data(named: Open,High, Low, Close). The py file when ran will ask for name of csv file as data source.)
The strategy rules:-
1. There are two sl choices, first one is intraday exit and sl type 2 is carry forward of the position. 
2. Intraday exit time is @3:20 pm
3. If prev day high is broken, we enter at that price and the candle's low that broke the high is used as sl price. vice versa for shorting
4. Once entered we can exit @3:20 if no other exit rule is active. We also exit on sl price. There is a third exit rule, if close price falls below ema 20(in case of long position),we check for swing formation on the lower side, if swing formed, the lowest point is the alternate sl price we can exit on.








Hi Humans,
Yash here, I like to code strategies to trade in nse market using python. 
