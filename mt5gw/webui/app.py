from flask import Flask, render_template, request, jsonify
from mt5gw import MetaTraderManager  # Your class file
import pandas as pd

app = Flask(__name__)
manager = MetaTraderManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    # Extract parameters from the request
    data = request.get_json()
    instrument = data['instrument']
    timeframe = data['timeframe']
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    indicators = data.get('indicators', [])
    denoise_methods = data.get('denoise_methods', [])

    # Prepare parameters for fetch
    fetch_params = {
        'instrument': instrument,
        'timeframe': timeframe,
        'date_from': date_from,
        'date_to': date_to
    }

    # Process each denoising method separately
    denoised_data = {}

    # Apply denoising methods
    if denoise_methods:
        print(f"Processing denoising methods: {denoise_methods}")
        for method in denoise_methods:
            try:
                print(f"Applying denoising method: {method}")
                method_params = {
                    'instrument': instrument,
                    'timeframe': timeframe,
                    'date_from': date_from,
                    'date_to': date_to,
                    'denoise_data': {'method': method, 'apply_columns': ['close']}
                }
                df_denoised = manager.fetch(**method_params)
                # Store the denoised column with method name for identification
                for col in df_denoised.columns:
                    if col.startswith('denoised_close'):
                        print(f"Found and processing denoised_close column for method: {method}")
                        # Use consistent naming: method_denoised_close
                        denoised_data[f"{method}_denoised_close"] = df_denoised[col].tolist()
                        #Also return a time array
                        denoised_data[f"{method}_denoised_time"] = df_denoised.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
            except Exception as e:
                print(f"Error applying {method} denoising: {str(e)}")

    # Add technical indicators if selected
    talib_indicators = []
    for ind in indicators:
        if ind == 'sma':
            talib_indicators.append({'method': 'SMA', 'args': ['c'], 'kwargs': {'timeperiod': 14}})
        elif ind == 'rsi':
            talib_indicators.append({'method': 'RSI', 'args': ['c'], 'kwargs': {'timeperiod': 14}})
    if talib_indicators:
        fetch_params['talib_indicators'] = talib_indicators

    # Fetch data from MetaTraderManager (without denoising)
    try:
        print("Fetching base data (without denoising)...")
        df = manager.fetch(**fetch_params)
        print("Columns in dataframe:", df.columns.tolist())

        # Convert DataFrame to JSON-compatible format
        data_dict = {
            'time': df.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            'open': df['open'].tolist(),
            'high': df['high'].tolist(),
            'low': df['low'].tolist(),
            'close': df['close'].tolist(),
            'volume': df['volume'].tolist()
        }
        print(f"data_dict after base data: {data_dict.keys()}")

        # Add all separately denoised data
        for key, values in denoised_data.items():
            print(f"Adding separately denoised data: {key}, values: {values[:10]}...")  # Print first 10 values
            data_dict[key] = values
        print(f"data_dict after denoised data: {data_dict.keys()}")

        # Add indicator columns
        for ind in indicators:
            for col in df.columns:
                if ind == 'sma' and col.startswith('sma_'):
                    data_dict['sma'] = df[col].tolist()
                if ind == 'rsi' and col.startswith('rsi_'):
                    data_dict['rsi'] = df[col].tolist()
        print(f"data_dict after indicators: {data_dict.keys()}")
        
        return jsonify(data_dict)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
