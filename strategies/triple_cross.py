import math
import backtrader as bt


class TripleCross(bt.Strategy):
    params = (
        ('fast', 10),       # Período de la media rápida
        ('mid', 30),        # Período de la media intermedia
        ('slow', 60),       # Período de la media lenta
        ('order_pct', 0.10),  # 10% del valor de la cartera
    )

    def __init__(self):
        # Inicialización de indicadores y registros
        self.indicators = {}
        self.transactions = []  # Registro de todas las transacciones
        self.portfolio_values = []  # Registro del valor del portfolio en el tiempo
        self.purchase_history = {}  # Registro de compras por ticker
        

        for data in self.datas:
            self.indicators[data._name] = {
                'sma_fast': bt.indicators.SimpleMovingAverage(
                    data.close, period=self.p.fast
                ),
                'sma_mid': bt.indicators.SimpleMovingAverage(
                    data.close, period=self.p.mid
                ),
                'sma_slow': bt.indicators.SimpleMovingAverage(
                    data.close, period=self.p.slow
                ),
            }

    def next(self):
        # Lógica de trading para cada paso temporal
        portfolio_value = self.broker.getvalue()
        self.portfolio_values.append({
            'date': self.datas[0].datetime.date(0),
            'value': portfolio_value,
        })

        for data in self.datas:
            current_cash = self.broker.cash
            amount_to_invest = self.params.order_pct * portfolio_value
            price = data.close[0]
            position = self.getposition(data)

            # Obtener los valores actuales de las medias
            sma_fast = self.indicators[data._name]['sma_fast'][0]
            sma_mid = self.indicators[data._name]['sma_mid'][0]
            sma_slow = self.indicators[data._name]['sma_slow'][0]

            # Señal de compra: rápida > intermedia > lenta
            if not position and sma_fast > sma_mid > sma_slow:
                if current_cash >= amount_to_invest:
                    size = math.floor(amount_to_invest / price)
                    self.buy(data=data, size=size)

                    if data._name not in self.purchase_history:
                        self.purchase_history[data._name] = []

                    self.purchase_history[data._name].append({
                        'date': self.datas[0].datetime.date(0),
                        'size': size,
                        'price': price,
                        'total': size * price,
                    })
                    self.transactions.append({
                        'date': self.datas[0].datetime.date(0),
                        'ticker': data._name,
                        'action': 'BUY',
                        'size': size,
                        'price': price,
                        'total': size * price,
                    })
                    print(f"**Comprando {size} acciones de {data._name} a ${price:.2f}**")
                else:
                    print(f"**Fondos insuficientes para comprar {data._name}**")

            # Señal de venta: rápida < intermedia < lenta
            elif position and sma_fast < sma_mid < sma_slow:
                size = position.size
                if size > 0:
                    self.close(data=data)
                    self.transactions.append({
                        'date': self.datas[0].datetime.date(0),
                        'ticker': data._name,
                        'action': 'SELL',
                        'size': size,
                        'price': price,
                        'total': size * price,
                    })
                    print(f"**Vendiendo {size} acciones de {data._name} a ${price:.2f}**")
                else:
                    print(f"**No tienes acciones de {data._name} para vender**")

    def stop(self):
       # Generar el reporte final de mi estrategia al finalizar la simulacion
        print("\n _____ HISTORIAL DE COMPRAS POR TICKER ____ ")
        for ticker, purchases in self.purchase_history.items():
            print(f"\n{ticker}:")
            for purchase in purchases:
                print(f"  {purchase['date']} | Size: {purchase['size']} | "
                      f"Precio: ${purchase['price']:.2f} | Total: ${purchase['total']:.2f}")

        print("\n _____ RESUMEN DE TRANSACCIONES ____")
        for t in self.transactions:
            print(f"{t['date']} | {t['action']} | {t['ticker']} | "
                  f"Size: {t['size']} | Precio: ${t['price']:.2f} | Total: ${t['total']:.2f}")

        print("\n____ VARIACIÓN DEL PORTFOLIO _____ ")
        for v in self.portfolio_values:
            print(f"{v['date']} | Cartera TripleCross: ${v['value']:.2f}")

  