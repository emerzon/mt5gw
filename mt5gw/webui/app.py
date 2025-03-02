from flask import Flask, render_template, request, jsonify
from mt5gw import MetaTraderManager  # Your class file
import pandas as pd

app = Flask(__name__)
manager = MetaTraderManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/symbols')
def get_symbols():
    symbols = manager.get_all_symbols_list()
    return jsonify(symbols)

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    # Extract parameters from the request
    data = request.get_json()
    instrument = data['instrument']
    timeframe = data['timeframe']
    bars = data.get('bars')
    denoise_methods = data.get('denoise_methods', [])
    denoise_settings = data.get('denoise_settings', {})

    # Prepare parameters for fetch
    fetch_params = {
        'instrument': instrument,
        'timeframe': timeframe,
        'bars': bars
    }

    # Process each denoising method separately
    denoised_data = {}

    # Apply denoising methods
    if denoise_methods:
        print(f"Processing denoising methods: {denoise_methods}")
        for method in denoise_methods:
            try:
                print(f"Applying denoising method: {method}")
                
                # Get method-specific settings if available
                method_settings = denoise_settings.get(method, {})
                
                # Create denoise_data dictionary with method and settings
                denoise_data = {
                    'method': method,
                    'apply_columns': ['close']
                }
                
                # Add method-specific settings to denoise_data
                if method == 'wavelet' and method_settings:
                    denoise_data['level'] = int(method_settings.get('level', 2))
                    denoise_data['wavelet_type'] = method_settings.get('type', 'db4')
                elif method == 'kalman' and method_settings:
                    denoise_data['q'] = float(method_settings.get('q', 0.01))
                    denoise_data['r'] = float(method_settings.get('r', 1.0))
                elif method == 'ssa' and method_settings:
                    denoise_data['window_length'] = int(method_settings.get('window', 20))
                    denoise_data['groups'] = int(method_settings.get('groups', 2))
                elif method == 'emd' and method_settings:
                    imfs_value = method_settings.get('imfs', '2')
                    n_imfs_to_remove = int(imfs_value)

                    denoise_data['emd_params'] = {'n_imfs_to_remove': n_imfs_to_remove}

                method_params = {
                    'instrument': instrument,
                    'timeframe': timeframe,
                    'bars': bars,
                    'denoise_data': denoise_data
                }

                print(f"Method params: {method_params}")
                df_denoised = manager.fetch(**method_params)

                # Store the denoised column with method name for identification
                for col in df_denoised.columns:
                    if col.startswith('denoised_close'):
                        print(f"Found and processing denoised_close column for method: {method}")
                        # Use consistent naming: method_denoised_close
                        denoised_data[f"{method}_denoised_close"] = df_denoised[col].tolist()
                        # Also return a time array
                        denoised_data[f"{method}_denoised_time"] = df_denoised.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
            except Exception as e:
                print(f"Error applying {method} denoising: {str(e)}")

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
        
        return jsonify(data_dict)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
