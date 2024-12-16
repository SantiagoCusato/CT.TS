import yfinance as yf
import pandas as pd
import os
import time

# Lista de símbolos
symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']

# Fechas
start_date = "2021-01-01"
end_date = "2021-12-31"

# Carpeta de salida
output_folder = "data"

# Crear carpeta de salida si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Descarga, almacenamiento y depuración de datos en velas diarias
for symbol in symbols:
    try:
        print(f"🔄 Descargando datos diarios para {symbol}...")

        # Descargar los datos en velas diarias usando yfinance
        data = yf.download(
            tickers=symbol,
            start=start_date,
            end=end_date,
            interval='1d',  # Velas diarias
        )

        # Definir la ruta del archivo CSV
        output_path = os.path.join(output_folder, f"{symbol}.csv")

        # Guardar los datos en el archivo CSV
        print(f"💾 Guardando datos en {output_path}...")
        data.to_csv(output_path)
        print(f"✅ Archivo creado: {output_path}")
        time.sleep(0.1)  # Evitar sobrecarga de peticiones

        # Leer y modificar el archivo CSV
        csv_path = f"data/{symbol}.csv"
        df = pd.read_csv(csv_path)

        # Cambiar los nombres de las columnas
        df.columns = [
            'datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest'
        ]
        df.to_csv(csv_path, index=False)
        print(f"✅ CSV modificado correctamente para {symbol}")

        # Eliminar valores no deseados
        valores_a_quitar = ['Date', 'Ticker', symbol]
        df = df[~df.applymap(lambda x: str(x).strip()).isin(valores_a_quitar).any(axis=1)]
        df.to_csv(csv_path, index=False)
        print(f"✅ Filas no deseadas eliminadas para {symbol}")

    except Exception as e:
        print(f"❌ Error al descargar datos de {symbol}: {e}")
