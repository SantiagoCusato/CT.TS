import datetime

import backtrader as bt

from strategies.golden_cross import GoldenCross
from strategies.death_cross import DeathCross

# Listado de símbolos de Yahoo Finance
symbols = ['GOOGL', 'MSFT', 'AAPL','TSLA']
start_date = '2021-01-01'
end_date = '2021-12-31'

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

# Añadir datos al "Cerebro" para cada simbolo
for symbol in symbols:
    try:
        data = bt.feeds.YahooFinanceCSVData(
            dataname=f'data/{symbol}.csv',
            fromdate=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
            todate=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
            reverse=False
        )

        cerebro.adddata(data, name=symbol)
        
    except Exception as e:
        print(f"Error al cargar datos de {symbol}: {e}")


# Añadir estrategia al "Cerebro"
cerebro.addstrategy(GoldenCross)
cerebro.addstrategy(DeathCross)


# Correr la estrategia
print(f"____ | | Valor inicial del portafolio {cerebro._broker.get_cash()}| | ____ ")
cerebro.run()
print(f"____ | | Valor Final del portafolio {cerebro._broker.get_cash()}| | ____")
# Plotear los resultados
cerebro.plot(
    volume=True,
    grid=True,
    legend=True,
    ylabel='Precio',
    ylabel_lower='Volumen'
)
