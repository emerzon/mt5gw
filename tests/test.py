from mt5gw import MetaTraderManager  # Your class file

mt = MetaTraderManager()

test_df = mt.fetch(instrument='EURUSD', timeframe='1min', bars=10, denoise_data={'method': 'wavelet', 'apply_columns': ['close']})
print(test_df)
