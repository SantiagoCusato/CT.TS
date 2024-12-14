import backtrader as bt
import datetime
from strategies import GoldenCross
import pandas as pd


# Listado de símbolos de Yahoo Finance
symbols = ['TSLA', 'GOOGL', 'MSFT', 'AAPL']
start_date = '2021-01-01'
end_date = '2021-12-31'
cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000)

for symbol in symbols:
    try:
        csv_path = f"data/{symbol}.csv"
        df = pd.read_csv(csv_path)
        df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest']
        df.to_csv(csv_path, index=False) 
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error al modificar csv para cerebro de {symbol}: {e}")


# Añadir datos al "Cerebro" para cada símbolo
for symbol in symbols:
    try:
        # Cargar los datos desde Yahoo Finance usando YahooFinanceData
        data = bt.feeds.YahooFinanceCSVData(
              dataname=(f'data/{symbol}.csv'),
              fromdate=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
              todate=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
              reverse=False
              
                   )
        
        # Añadir los datos al cerebro
        cerebro.adddata(data, name=symbol)
        print(f"Datos cargados para {symbol}. Total de barras de datos: {len(data)}")
        print(f"Datos cargados para {symbol}")
    except Exception as e:
        print(f"Error al cargar datos de {symbol}: {e}")


# Añadir estrategia al "Cerebro"
cerebro.addstrategy(GoldenCross)

# Correr la estrategia
cerebro.run()

# Plotear los resultados
cerebro.plot()