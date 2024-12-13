import math
import backtrader as bt

class GoldenCross(bt.Strategy):
    params = (('fast', 10),
              ('slow', 30),
              ('order_pct', 0.10),
              ('ticker', ['AAPL', 'GOOGL', 'MSFT', 'TSLA']))

    def __init__(self):
        # Indicadores
        self.sma_10 = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.fast,
            plotname='10-day SMA'
        )
        self.sma_30 = bt.indicators.SimpleMovingAverage(
            self.data.close,
            period=self.p.slow,
            plotname='30-day SMA'
        )
        self.crossover = bt.indicators.CrossOver(self.sma_10, self.sma_30)
        self.purchase_log = []  # Registro de compras

    def next(self):
        current_cash = self.broker.cash
        portfolio_value = self.broker.getvalue()
        amount_to_invest = self.params.order_pct * portfolio_value
        price = self.data.close[0]

        # Validar si hay cruce al alza
        if not self.position:  # No hay posición abierta
            if self.crossover > 0:
                if current_cash >= amount_to_invest:
                    size = math.floor(amount_to_invest / price)
                    self.buy(size)
                    self.purchase_log.append({'ticker': self.data._name, 'size': size, 'price': price})
                    print(f"Comprando {size} acciones de {self.data._name} a ${price:.2f}")
                else:
                    print("Fondos insuficientes para comprar")
        
        # Validar si hay cruce a la baja
        elif self.crossover < 0:
            print(f"Vendiendo {self.position.size} acciones de {self.data._name} a ${price:.2f}")
            self.close()