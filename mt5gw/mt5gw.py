import os
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import pywt
import ta
import talib
import pandas_ta
import tulipy
from . import mtds_ni
from warnings import simplefilter

# Ignore warnings
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action="ignore", category=FutureWarning)
simplefilter(action="ignore", category=RuntimeWarning)


class MetaTraderManager:
    def __init__(self):
        self.mt5 = mt5
        try:
            self.mt5.initialize()
            self.tfs = {'1min': mt5.TIMEFRAME_M1,
                        '2min': mt5.TIMEFRAME_M2,
                        '3min': mt5.TIMEFRAME_M3,
                        '4min': mt5.TIMEFRAME_M4,
                        '5min': mt5.TIMEFRAME_M5,
                        '10min': mt5.TIMEFRAME_M10,
                        '12min': mt5.TIMEFRAME_M12,
                        '15min': mt5.TIMEFRAME_M15,
                        '20min': mt5.TIMEFRAME_M20,
                        '30min': mt5.TIMEFRAME_M30,
                        '1h': mt5.TIMEFRAME_H1,
                        '2h': mt5.TIMEFRAME_H2,
                        '3h': mt5.TIMEFRAME_H3,
                        '4h': mt5.TIMEFRAME_H4,
                        '6h': mt5.TIMEFRAME_H6,
                        '8h': mt5.TIMEFRAME_H8,
                        '12h': mt5.TIMEFRAME_H12,
                        '1d': mt5.TIMEFRAME_D1,
                        '1w': mt5.TIMEFRAME_W1,
                        '1m': mt5.TIMEFRAME_MN1}

        except Exception as e:
            print(e)
            print("initialize() failed, error code =", self.mt5.last_error())
            quit()

    def get_all_symbols(self):
        self.mt5.initialize()
        return self.mt5.symbols_get()

    def get_supported_timeframes(self):
        return list(self.tfs.keys())

    def get_market_book(self, symbol):
        self.mt5.initialize()
        return self.mt5.market_book_get(symbol)

    def get_mt5_timeframe(self, tf):
        return self.tfs.get(tf, None)

    def get_orders(self, instrument):
        self.mt5.initialize()
        return self.mt5.orders_get(symbol=instrument)

    def get_positions(self, instrument=None):
        self.mt5.initialize()
        if instrument:
            return self.mt5.positions_get(symbol=instrument)
        return self.mt5.positions_get()

    def get_symbol_info(self, symbol):
        self.mt5.initialize()
        return self.mt5.symbol_info(symbol)

    def get_last_tick(self, symbol):
        self.mt5.initialize()
        return self.mt5.symbol_info_tick(symbol)

    def place_order(self, order):
        self.mt5.initialize()

        order_dict = {"buy_market": self.mt5.ORDER_TYPE_BUY,
                      "sell_market": self.mt5.ORDER_TYPE_SELL,
                      "buy_limit": self.mt5.ORDER_TYPE_BUY_LIMIT,
                      "sell_limit": self.mt5.ORDER_TYPE_SELL_LIMIT,
                      "buy_stop": self.mt5.ORDER_TYPE_BUY_STOP,
                      "sell_stop": self.mt5.ORDER_TYPE_SELL_STOP}

        request = {
            "action": self.mt5.TRADE_ACTION_DEAL if order['order_type'] in ["buy_market", "sell_market"] else self.mt5.TRADE_ACTION_PENDING,
            "symbol": order['instrument'],
            "volume": float(order['lot_size']),
            "type": order_dict[order['order_type']],
            "price": float(order['entry_level']) if "entry_level" in order else None,
            "sl": float(order['stop_loss']) if "stop_loss" in order else None,
            "tp": float(order['take_profit']) if "take_profit" in order else None,
            "magic": int(order.get('magic', 2121)),
            "type_time": self.mt5.ORDER_TIME_SPECIFIED if "expiration" in order else None,
            "type_filling": self.mt5.ORDER_FILLING_IOC,
            "comment": order["comment"] if "comment" in order else None,
            "expiration": self.mt5.symbol_info_tick(order['instrument']).time + order['expiration'] * 60 if "expiration" in order else None
        }

        # Drop all None values
        request = {k: v for k, v in request.items() if v is not None}

        self.mt5.initialize()
        try:
            result = self.mt5.order_send(request)
        except Exception as e:
            print("Order send failed, error code =", self.mt5.last_error())
            print(e)
            quit()
        if result.retcode != self.mt5.TRADE_RETCODE_DONE:
            print("Order send failed, retcode={}".format(result.retcode))
            print(result)

        return result

       

    def close_position(self, ticket):
        self.mt5.initialize()

        pos = self.mt5.positions_get(ticket=ticket)
        print (pos)
        if pos is None or len(pos) < 1:
            print("Position not found!")
            return None

        pos = pos[0]
        # Prepare the closing order
        close_request = {
            "action": self.mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": self.mt5.ORDER_TYPE_SELL if pos.type == self.mt5.ORDER_TYPE_BUY else self.mt5.ORDER_TYPE_BUY,
            "position": pos.ticket,
            "type_filling": self.mt5.ORDER_FILLING_IOC
        }

        return self.mt5.order_send(close_request)

    def add_pivot_levels(self, df, num_candles=14, num_levels=5, keep_distance_only=True):
        """
        Calculate pivot levels using different methods (Standard, Fibonacci, Camarilla, Woodie, Demark).

        Parameters:
        df (pd.DataFrame): DataFrame containing OHLC data with columns 'open', 'high', 'low', 'close', 'volume'.
        num_candles (int): Number of past candles to use in pivot calculation.
        num_levels (int): Number of support and resistance levels to calculate.
        keep_distance_only (bool): If True, drop the levels and keep only distances to the close price.

        Returns:
        pd.DataFrame: DataFrame with added pivot levels and/or distances.
        """
        df = df.sort_index().copy()

        # Calculate the rolling max, min, and the previous close
        rolling_high = df['high'].rolling(window=num_candles, min_periods=num_candles).max()
        rolling_low = df['low'].rolling(window=num_candles, min_periods=num_candles).min()
        previous_close = df['close'].shift(1)

        # List to track all created columns
        created_columns = []

        # Standard Pivot Points
        P = (rolling_high + rolling_low + previous_close) / 3
        df['standard_P'] = P
        created_columns.append('standard_P')

        for j in range(1, num_levels + 1):
            df[f'standard_R{j}'] = P + j * (rolling_high - rolling_low)
            df[f'standard_S{j}'] = P - j * (rolling_high - rolling_low)
            created_columns.extend([f'standard_R{j}', f'standard_S{j}'])

        # Fibonacci Pivot Points
        fib_levels = np.array([0.236, 0.382, 0.5, 0.618, 0.786, 1.000, 1.272, 1.618])
        for j in range(1, min(num_levels, len(fib_levels)) + 1):
            df[f'fibonacci_R{j}'] = P + fib_levels[j-1] * (rolling_high - rolling_low)
            df[f'fibonacci_S{j}'] = P - fib_levels[j-1] * (rolling_high - rolling_low)
            created_columns.extend([f'fibonacci_R{j}', f'fibonacci_S{j}'])

        # Camarilla Pivot Points
        for j in range(1, min(num_levels, 4) + 1):
            factor = 1.1 / (12 / j)
            df[f'camarilla_R{j}'] = previous_close + (rolling_high - rolling_low) * factor
            df[f'camarilla_S{j}'] = previous_close - (rolling_high - rolling_low) * factor
            created_columns.extend([f'camarilla_R{j}', f'camarilla_S{j}'])

        # Woodie's Pivot Points
        woodies_P = (rolling_high + rolling_low + 2 * df['open'].shift(1)) / 4
        df['woodie_P'] = woodies_P
        created_columns.append('woodie_P')

        for j in range(1, num_levels + 1):
            df[f'woodie_R{j}'] = woodies_P + j * (rolling_high - rolling_low)
            df[f'woodie_S{j}'] = woodies_P - j * (rolling_high - rolling_low)
            created_columns.extend([f'woodie_R{j}', f'woodie_S{j}'])

        # Demark Pivot Points
        demark_X = np.where(previous_close < df['open'].shift(1),
                            rolling_high + 2 * rolling_low + previous_close,
                            np.where(previous_close > df['open'].shift(1),
                                    2 * rolling_high + rolling_low + previous_close,
                                    rolling_high + rolling_low + 2 * previous_close))
        demark_P = demark_X / 4
        df['demark_P'] = demark_P
        created_columns.append('demark_P')

        df['demark_R1'] = demark_X / 2 - rolling_low
        df['demark_S1'] = demark_X / 2 - rolling_high
        created_columns.extend(['demark_R1', 'demark_S1'])

        # Calculate distances to pivot levels
        distance_columns = []
        for col in created_columns:
            method_prefix = col.split('_')[0]
            for j in range(1, num_levels + 1):
                if f'{method_prefix}_R{j}' in df.columns:
                    distance_col = f'distance_to_{method_prefix}_R{j}'
                    df[distance_col] = df['close'] - df[f'{method_prefix}_R{j}']
                    distance_columns.append(distance_col)
                if f'{method_prefix}_S{j}' in df.columns:
                    distance_col = f'distance_to_{method_prefix}_S{j}'
                    df[distance_col] = df['close'] - df[f'{method_prefix}_S{j}']
                    distance_columns.append(distance_col)

        # Optionally drop all the created pivot levels and keep only distance to the reference field
        if keep_distance_only:
            df.drop(columns=created_columns, inplace=True)

        return df

    def wavelet_denoising(self, data, wavelet, level):
        coeff = pywt.wavedec(data.values, wavelet, level=level)
        coeff[1:] = [np.zeros_like(c) for c in coeff[1:]]
        reconstructed = pywt.waverec(coeff, wavelet)[:len(data)]
        return pd.Series(reconstructed, index=data.index)

    def ssa_denoising(self, data, window_length, n_components):
        try:
            from pyssa import SSA
        except ImportError:
            raise ImportError("pyssa package is required for SSA denoising")
        
        """
        Apply Singular Spectrum Analysis (SSA) denoising to the input time series.

        Parameters:
        - data (pd.Series): Input time series data to denoise.
        - window_length (int): The window length for SSA decomposition.
        - n_components (int): Number of SSA components to retain for reconstruction.

        Returns:
        - pd.Series: Denoised time series with the same index as the input.
        """
        ssa = SSA(data.values, window_length)
        ssa.fit()
        reconstructed = ssa.reconstruct(n_components)
        return pd.Series(reconstructed, index=data.index)

    def emd_denoising(self, data, n_imfs_to_remove):
        try:
            from PyEMD import EMD
        except ImportError:
            raise ImportError("PyEMD package is required for EMD denoising")
        
        """
        Apply Empirical Mode Decomposition (EMD) denoising to the input time series.

        Parameters:
        - data (pd.Series): Input time series data to denoise.
        - n_imfs_to_remove (int): Number of high-frequency IMFs to remove.

        Returns:
        - pd.Series: Denoised time series with the same index as the input.
        """
        emd = EMD()
        imfs = emd(data.values)
        reconstructed = imfs[n_imfs_to_remove:].sum(axis=0)
        return pd.Series(reconstructed, index=data.index)


    def kalman_denoising(self, data, transition_matrices=1, observation_matrices=1, 
                            transition_covariance=1e-4, observation_covariance=1, 
                            initial_state_mean=0, initial_state_covariance=1):
            
            try:
                from pykalman import KalmanFilter
            except ImportError:
                raise ImportError("pykalman package is required for Kalman filter denoising")
            
            """
            Apply Kalman filter denoising to the input time series data.

            Parameters:
            - data (pd.Series): Input time series data to denoise.
            - transition_matrices (float): Transition matrix for the state equation (default: 1 for local level model).
            - observation_matrices (float): Observation matrix (default: 1 for direct observation).
            - transition_covariance (float): Covariance of process noise (default: 1e-4).
            - observation_covariance (float): Covariance of observation noise (default: 1).
            - initial_state_mean (float): Initial state mean (default: 0).
            - initial_state_covariance (float): Initial state covariance (default: 1).

            Returns:
            - pd.Series: Denoised time series with the same index as the input.
            """
            kf = KalmanFilter(
                transition_matrices=transition_matrices,
                observation_matrices=observation_matrices,
                transition_covariance=transition_covariance,
                observation_covariance=observation_covariance,
                initial_state_mean=initial_state_mean,
                initial_state_covariance=initial_state_covariance
            )
            state_means, _ = kf.filter(data.values)
            return pd.Series(state_means.flatten(), index=data.index)

    def denoise_dataframe(self, df, denoise_func=None, method='wavelet', wavelet='rbio2.8', 
                          level=2, kalman_params={}, ssa_params={}, emd_params={}, 
                          apply_columns=[], preserve_col_names=False):
        """
        Apply denoising to specified columns of the DataFrame using the selected method.

        Parameters:
        - df (pd.DataFrame): Input DataFrame to denoise.
        - denoise_func (callable, optional): Custom denoising function (takes pd.Series, returns pd.Series).
        - method (str): Denoising method ('wavelet', 'kalman', 'ssa', 'emd'; default: 'wavelet').
        - wavelet (str): Wavelet type for wavelet denoising (default: 'rbio2.8').
        - level (int): Decomposition level for wavelet denoising (default: 2).
        - kalman_params (dict): Parameters for Kalman filter denoising.
        - ssa_params (dict): Parameters for SSA denoising (e.g., {'window_length': 20, 'n_components': 5}).
        - emd_params (dict): Parameters for EMD denoising (e.g., {'n_imfs_to_remove': 1}).
        - apply_columns (list): Columns to denoise; if empty, applies to all numeric columns.
        - preserve_col_names (bool): If False, adds 'denoised_' prefix; if True, overwrites original columns.

        Returns:
        - pd.DataFrame: DataFrame with denoised columns.
        """
        if not apply_columns:
            apply_columns = df.columns
        
        for column in apply_columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                new_column_name = f"denoised_{column}" if not preserve_col_names else column
                data = df[column].dropna()
                
                if denoise_func is not None:
                    df[new_column_name] = denoise_func(data)
                elif method == 'wavelet':
                    df[new_column_name] = self.wavelet_denoising(data, wavelet, level)
                elif method == 'kalman':
                    df[new_column_name] = self.kalman_denoising(data, **kalman_params)
                elif method == 'ssa':
                    window_length = ssa_params.get('window_length', 20)
                    n_components = ssa_params.get('n_components', 5)
                    df[new_column_name] = self.ssa_denoising(data, window_length, n_components)
                elif method == 'emd':
                    n_imfs_to_remove = emd_params.get('n_imfs_to_remove', 1)
                    df[new_column_name] = self.emd_denoising(data, n_imfs_to_remove)
                else:
                    raise ValueError(f"Unsupported denoising method: {method}")
        
        return df
   
    def add_indicators(self, library, indicators, rf, silent=False):
        suffix_counter = {}
        now = datetime.datetime.now()

        for ti in indicators:
            if hasattr(library, ti["method"]) and callable(getattr(library, ti["method"])):
                method = getattr(library, ti["method"])
                pos_args = []
                key_map = {
                    "o": "open",
                    "h": "high",
                    "l": "low",
                    "c": "close",
                    "v": "volume"
                }
                for i in ti["args"]:
                    key = key_map.get(i, None)
                    if key is not None:
                        if library == tulipy:
                            pos_args.append(rf[key].astype(float).values)
                        else:
                            pos_args.append(rf[key].astype(float))
                    else:
                        print("[WARNING]: Ignoring unknown positional argument '%s' for method '%s'" % (
                            i, ti["method"]))

                retval = method(*pos_args, **ti.get("kwargs", {}))

                if isinstance(retval, tuple):
                    for i, r in enumerate(retval):
                        column_name = "%s%s_%s" % (
                            ti.get("prefix", ""), ti.get("name", ti["method"]).lower(), i)
                        suffix_counter[column_name] = suffix_counter.get(
                            column_name, 0) + 1
                        final_column_name = column_name + "_" + \
                            str(suffix_counter[column_name]
                                ) if suffix_counter[column_name] > 1 else column_name
                        if len(rf) > len(r):
                            r = np.append(np.full(len(rf) - len(r), np.nan), r)
                        rf[final_column_name] = r
                elif isinstance(retval, pd.DataFrame):
                    for c in retval.columns:
                        column_name = "%s%s" % (
                            ti.get("prefix", ""), c.replace("_", "|"))
                        suffix_counter[column_name] = suffix_counter.get(
                            column_name, 0) + 1
                        final_column_name = column_name + "_" + \
                            str(suffix_counter[column_name]
                                ) if suffix_counter[column_name] > 1 else column_name
                        rf[final_column_name] = retval[c]
                else:
                    column_name = "%s%s" % (
                        ti.get("prefix", ""), ti.get("name", ti["method"]).lower())
                    suffix_counter[column_name] = suffix_counter.get(
                        column_name, 0) + 1
                    final_column_name = column_name + "_" + \
                        str(suffix_counter[column_name]
                            ) if suffix_counter[column_name] > 1 else column_name
                    if retval is not None:
                        if len(rf) > len(retval):
                            retval = np.append(
                                np.full(len(rf) - len(retval), np.nan), retval)
                    rf[final_column_name] = retval
            else:
                print("Method %s is not supported!" % ti["method"])
        if not silent:
            print(" %s -- %s indicators added in %s seconds" % (library.__name__,
                  len(indicators), (datetime.datetime.now() - now).total_seconds()))
        return rf

    def fetch(self, instrument, timeframe, bars=None,
              date_from=None, date_to=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              mas=[], lookbacks=[], native_indicators=[], ta_indicators=[],
              pandasta_indicators=[], talib_indicators=[], talib_candle_patterns=False,
              ta_all=False, taf_all=False, tulip_indicators=[], denoise_data=None,
              add_meta_dates=False, add_year=False, add_price_summaries=True,
              add_gap=False, sr_levels=[], sr_fields=["close"], pivot_levels=0,
              fill_empty_ranges=False, provide_open_bar=True, drop_na=True,
              drop_columns=[], silent=False):

        if isinstance(instrument, list):
            dataframes = []
            max_df_len = 0

            for i in instrument:
                tmpdf = self.fetch(i, timeframe, bars=bars, mas=mas, lookbacks=lookbacks,
                                   native_indicators=native_indicators, ta_indicators=ta_indicators,
                                   pandasta_indicators=pandasta_indicators, talib_indicators=talib_indicators,
                                   talib_candle_patterns=talib_candle_patterns, ta_all=ta_all, taf_all=taf_all,
                                   tulip_indicators=tulip_indicators, add_meta_dates=False, add_year=False, add_price_summaries=add_price_summaries, add_gap=add_gap,
                                   sr_levels=sr_levels, sr_fields=sr_fields, pivot_levels=pivot_levels,
                                   fill_empty_ranges=True, provide_open_bar=provide_open_bar,
                                   drop_na=True, drop_columns=drop_columns, date_from=date_from, date_to=date_to, silent=silent, denoise_data=denoise_data)

                tmpdf.columns = ["%s-%s" % (i, col)
                                 for col in tmpdf.columns.values]
                dataframes.append(tmpdf)
                if len(tmpdf) > max_df_len:
                    max_df_len = len(tmpdf)

            min_date = min(df.index.min() for df in dataframes)
            max_date = max(df.index.max() for df in dataframes)
            data = pd.DataFrame(index=pd.date_range(
                start=min_date, end=max_date, freq=timeframe))

            for df in dataframes:
                data = data.merge(df, left_index=True,
                                  right_index=True, how='left')

            for col in data.columns:
                if col.endswith("-volume"):
                    data[col].fillna(value=0, inplace=True)

            data.fillna(method='bfill', inplace=True)

            if add_meta_dates:
                d = data.index.to_series()
                if "min" in timeframe:
                    data['minute'] = d.dt.minute
                if timeframe not in ["1d"]:
                    data['hour'] = d.dt.hour
                data['day'] = d.dt.day
                data['month'] = d.dt.month
                data['weekday'] = d.dt.dayofweek
                if add_year:
                    data["year"] = d.dt.year

            data.replace([np.inf, -np.inf], np.nan, inplace=True)
            data.dropna(inplace=True)

            if not silent:
                print("Multi-Instrument Dataframe - [%s/%s] - Providing %s bars" % (
                    instrument, timeframe, len(data)))
                print(" -- Dataset begins at: %s" % data.index.min())
                print(" -- Dataset ends at: %s" % data.index.max())

            return data

        if not mt5.initialize():
            raise Exception(
                "MT5 initialize() failed, error code =", mt5.last_error())

        mt_timeframe = self.get_mt5_timeframe(timeframe)
        if mt_timeframe is None:
            raise Exception("Timeframe not supported!")

        rates = None
        if bars is not None:
            rates = mt5.copy_rates_from_pos(
                instrument, mt_timeframe, 0 if provide_open_bar else 1, bars)
        elif date_from is not None:
            if not isinstance(date_from, datetime.datetime):
                date_from = parse(date_from)
            if not isinstance(date_to, datetime.datetime):
                date_to = parse(date_to)
            print("Fetching data from %s to %s" % (date_from, date_to))
            rates = mt5.copy_rates_range(
                instrument, mt_timeframe, date_from, date_to)

        if rates is None or len(rates) < 1:
            print(rates)
            print(mt5.last_error())
            raise Exception("Instrument %s has no data!" % instrument)

        rf = pd.DataFrame(rates).drop(['spread', 'real_volume'], axis=1)
        rf = rf.rename(columns={'tick_volume': 'volume'})
        rf['Date'] = pd.to_datetime(rf['time'], unit='s')
        rf = rf.drop(columns='time')
        rf = rf.set_index(["Date"], drop=True)

        if add_gap:
            rf['gap'] = rf['open'] - rf['close'].shift(1)
            rf['gap'] = rf['gap'].fillna(value=0)
      
        if fill_empty_ranges:
            idx = pd.period_range(
                rf.index.min(), rf.index.max(), freq=timeframe).to_timestamp()
            rf = rf.reindex(idx)
            rf['volume'] = rf['volume'].fillna(value=0)
            rf.fillna(method='ffill', inplace=True)

        if pivot_levels > 0:
            rf = self.add_pivot_levels(df=rf, num_levels=pivot_levels)

        if denoise_data is not None:
            denoise_func = denoise_data.get('func', None)
            method = denoise_data.get('method', 'wavelet')
            wavelet = denoise_data.get('wavelet', 'rbio2.8')
            level = denoise_data.get('level', 2)
            kalman_params = denoise_data.get('kalman_params', {})
            ssa_params = denoise_data.get('ssa_params', {})
            emd_params = denoise_data.get('emd_params', {})
            rf = self.denoise_dataframe(
                rf,
                denoise_func=denoise_func,
                method=method,
                wavelet=wavelet,
                level=level,
                kalman_params=kalman_params,
                ssa_params=ssa_params,
                emd_params=emd_params
            )

        if add_price_summaries:
            rf['avgPrice'] = rf[['low', 'high']].mean(axis=1)
            rf['ohlcPrice'] = rf[['open', 'high', 'low', 'close']].mean(axis=1)
            rf['range'] = rf['high'] - rf['low']
            rf['momentum'] = rf['open'] - rf['close']

        for field in sr_fields:
            if field in rf.columns and pd.api.types.is_numeric_dtype(rf[field]):
                for level in sr_levels:
                    rf["support_%s_%s" % (str(level), field)] = rf[field].shift(
                        1).rolling(int(level)).min()
                    rf["resistance_%s_%s" % (str(level), field)] = rf[field].shift(
                        1).rolling(int(level)).max()
            else:
                print("Field %s does not exist or is not numeric!" % field)

        if add_meta_dates:
            d = rf.index.to_series()
            if mt_timeframe < mt5.TIMEFRAME_H1:
                rf['minute'] = d.dt.minute
            if mt_timeframe < mt5.TIMEFRAME_D1:
                rf['hour'] = d.dt.hour
            rf['day'] = d.dt.day
            rf['month'] = d.dt.month
            rf['weekday'] = d.dt.dayofweek
            if add_year:
                rf['year'] = d.dt.year

        if taf_all:
            rf = TA_Features.get_all_indicators(rf)

        rf = self.add_indicators(talib, talib_indicators, rf, silent=silent)
        rf = self.add_indicators(ta, ta_indicators, rf, silent=silent)
        rf = self.add_indicators(mtds_ni, native_indicators, rf, silent=silent)
        rf = self.add_indicators(
            pandas_ta, pandasta_indicators, rf, silent=silent)

        if ta_all:
            rf = ta.add_all_ta_features(
                rf, open="open", high="high", low="low", close="close", volume="volume", fillna=True)

        if talib_candle_patterns:
            for p in talib.get_function_groups()['Pattern Recognition']:
                rf[p] = (getattr(talib, p)(rf['open'].astype(float), rf['high'].astype(
                    float), rf['low'].astype(float), rf['close'].astype(float)) / 100).astype('int')

        for m in mas:
            fields = m.get("fields", None)
            if fields is None:
                fields = [m["field"]]
            for field in fields:
                if field in rf.columns and pd.api.types.is_numeric_dtype(rf[field]):
                    if m["method"].lower() in ["sma", "ema", "wma", "dema", "tema", "trima", "kama", "mama", "t3"]:
                        for period in m.get("periods", [14]):
                            ma = getattr(talib, m["method"].upper())(
                                rf[field].astype(float), timeperiod=int(period))
                            percentage = (ma / rf[field]) * 100
                            rf["%s-%s-%s-pct" %
                                (m["method"].lower(), str(period), field)] = percentage
                    else:
                        print("Method %s is not supported!" % m["method"])
                else:
                    print("Field %s does not exist or is not numeric!" % field)

        for lb in lookbacks:
            if lb["field"] in rf.columns:
                for period in lb.get("periods", [1, 2]):
                    period = int(period)
                    if lb.get("ratio", False):
                        rf[f"lb_{period}_{lb['field']}"] = rf[lb["field"]
                                                              ] / rf[lb["field"]].shift(period)
                    else:
                        rf[f"lb_{period}_{lb['field']}"] = rf[lb["field"]].shift(
                            period)

        if drop_na:
            rf.replace([np.inf, -np.inf], np.nan, inplace=True)
            rf.dropna(inplace=True)

        if not silent:
            print("Metatrader 5 - [%s/%s] - Providing %s bars" %
                  (instrument, timeframe, len(rf)))
            print("""Market Stats (%s/%s):
                    Period Analysis:
                    %s to
                    %s (last %s bar)""" % (instrument, timeframe, rf.index.min(), rf.index.max(), "OPEN" if provide_open_bar else "CLOSED"))

        if len(drop_columns) > 0:
            rf.drop(columns=drop_columns, inplace=True)

        self.mt5.shutdown()

        return rf.copy()
