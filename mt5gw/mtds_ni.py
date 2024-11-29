import numpy as np
import talib

def apply_smoothing(series, method='EMA', period=14):
    """
    Applies the specified smoothing method to a NumPy array using TA-Lib.

    Parameters:
    - series: NumPy array to smooth.
    - method: Smoothing method ('EMA', 'SMA', 'WMA', 'DEMA', 'T3', 'KAMA', 'TRIMA').
    - period: Period for the smoothing.

    Returns:
    - Smoothed NumPy array.
    """
    method = method.upper()
    if method == 'EMA':
        return talib.EMA(series, timeperiod=period)
    elif method == 'SMA':
        return talib.SMA(series, timeperiod=period)
    elif method == 'WMA':
        return talib.WMA(series, timeperiod=period)
    elif method == 'DEMA':
        return talib.DEMA(series, timeperiod=period)
    elif method == 'T3':
        return talib.T3(series, timeperiod=period)
    elif method == 'KAMA':
        return talib.KAMA(series, timeperiod=period)
    elif method == 'TRIMA':
        return talib.TRIMA(series, timeperiod=period)
    else:
        raise ValueError(f"Unsupported smoothing method: {method}")

def rvi(open_series, high_series, low_series, close_series, lookback=10, smoothing_method='SMA', smoothing_period=4):
    """
    Relative Vigor Index (RVI) calculation using TA-Lib and apply_smoothing.

    Parameters:
    - open_series: NumPy array of open prices.
    - high_series: NumPy array of high prices.
    - low_series: NumPy array of low prices.
    - close_series: NumPy array of close prices.
    - lookback: Period for calculating the numerator and denominator.
    - smoothing_method: Method for smoothing the RVI signal line.
    - smoothing_period: Period for smoothing the RVI signal line.

    Returns:
    - rvi_series: The RVI values.
    - rvi_signal: The smoothed signal line for RVI.
    """
    # Calculate Numerator and Denominator for RVI
    close_open_diff = close_series - open_series
    high_low_diff = high_series - low_series

    numerator = talib.SMA(close_open_diff, timeperiod=lookback)
    denominator = talib.SMA(high_low_diff, timeperiod=lookback)

    rvi_series = numerator / denominator

    # Calculate RVI signal line using apply_smoothing
    rvi_signal = apply_smoothing(rvi_series, method=smoothing_method, period=smoothing_period)

    return rvi_series, rvi_signal

def supertrend(high_series, low_series, close_series, multiplier=3, lookback=14):
    """
    SuperTrend indicator implementation using TA-Lib functions.

    Parameters:
    - high_series: NumPy array of high prices.
    - low_series: NumPy array of low prices.
    - close_series: NumPy array of close prices.
    - multiplier: Multiplier for ATR.
    - lookback: Period for ATR calculation.

    Returns:
    - supertrend_pct_diff: Percentage difference between supertrend and close price.
    """
    # Calculate ATR using TA-Lib
    atr = talib.ATR(high_series, low_series, close_series, timeperiod=lookback)

    # Calculate basic bands
    middle_band = (high_series + low_series) / 2
    basic_upper_band = middle_band + multiplier * atr
    basic_lower_band = middle_band - multiplier * atr

    # Initialize final bands and supertrend
    final_upper_band = np.copy(basic_upper_band)
    final_lower_band = np.copy(basic_lower_band)
    supertrend_series = np.zeros_like(close_series)
    supertrend_pct_diff = np.zeros_like(close_series, dtype=float)

    for i in range(1, len(close_series)):
        if close_series[i - 1] > final_upper_band[i - 1]:
            final_upper_band[i] = basic_upper_band[i]
        else:
            final_upper_band[i] = min(basic_upper_band[i], final_upper_band[i - 1])

        if close_series[i - 1] < final_lower_band[i - 1]:
            final_lower_band[i] = basic_lower_band[i]
        else:
            final_lower_band[i] = max(basic_lower_band[i], final_lower_band[i - 1])

        # Determine SuperTrend value
        if close_series[i] <= final_upper_band[i]:
            supertrend_series[i] = final_upper_band[i]
        else:
            supertrend_series[i] = final_lower_band[i]

        # Calculate percentage difference
        supertrend_pct_diff[i] = ((supertrend_series[i] - close_series[i]) / close_series[i]) * 100

    return supertrend_pct_diff

def twap(open_series, high_series, low_series, close_series, ratio=True):
    """
    Time-Weighted Average Price (TWAP) calculation using TA-Lib.

    Parameters:
    - open_series: NumPy array of open prices.
    - high_series: NumPy array of high prices.
    - low_series: NumPy array of low prices.
    - close_series: NumPy array of close prices.
    - ratio: If True, returns the percentage difference between TWAP and close price.

    Returns:
    - twap_series or twap_pct_diff: TWAP values or percentage difference.
    """
    # Calculate average price using TA-Lib's AVGPRICE
    average_price = talib.AVGPRICE(open_series, high_series, low_series, close_series)

    # Calculate expanding mean (TWAP) using cumulative sum for efficiency
    twap_series = np.cumsum(average_price) / np.arange(1, len(average_price) + 1)

    if ratio:
        # Calculate the percentage difference from the close price
        twap_pct_diff = ((twap_series - close_series) / close_series) * 100
        return twap_pct_diff
    else:
        return twap_series

def pov(close_series, volume_series, pov_rate=0.2):
    """
    Percentage of Volume (POV) indicator calculation.

    Parameters:
    - close_series: NumPy array of close prices.
    - volume_series: NumPy array of volumes.
    - pov_rate: Percentage of volume rate.

    Returns:
    - pov_indicator: PoV as a percentage of the close price.
    """
    daily_execution_target = volume_series * pov_rate

    # Calculate the PoV as a percentage of the close price
    pov_indicator = (daily_execution_target / close_series) * 100

    return pov_indicator

def rsl(close_series, period=15, ma_method='SMA'):
    """
    Relative Strength Line (RSL) calculation using apply_smoothing.

    Parameters:
    - close_series: NumPy array of close prices.
    - period: Period for moving average.
    - ma_method: Moving average method ('SMA', 'EMA', 'WMA', 'DEMA', 'TEMA').

    Returns:
    - rsl_series: The RSL values.
    """
    # Use apply_smoothing for moving average
    ma = apply_smoothing(close_series, method=ma_method, period=period)

    # RSL calculation
    rsl_series = close_series / ma
    return rsl_series

def ehlers_rpi(high_series, low_series, volume_series, minperiod=8, maxperiod=50, hpPeriod=40, medianPeriod=10, decibelPeriod=20):
    """
    Calculates the Ehlers Restoring Pull Indicator.

    Parameters:
    - high_series: NumPy array of high prices.
    - low_series: NumPy array of low prices.
    - volume_series: NumPy array of volumes.
    - minperiod: Minimum period for cycle detection.
    - maxperiod: Maximum period for cycle detection.
    - hpPeriod: Period for high-pass filter.
    - medianPeriod: Period for the median filter.
    - decibelPeriod: Decibel threshold.

    Returns:
    - NumPy array with V1 and V2 columns.
    """
    length = len(high_series)

    # Prepare indicator output
    v1 = np.zeros(length)
    v2 = np.zeros(length)

    # High-pass filter constants
    a1 = (1 - np.sin(2 * np.pi / hpPeriod)) / np.cos(2 * np.pi / hpPeriod)
    a2 = 0.5 * (1 + a1)

    # Initialize arrays
    hp = np.zeros(length)
    smoothHp = np.zeros(length)
    dc = np.zeros(length)
    Q = np.zeros(maxperiod + 1)
    I = np.zeros(maxperiod + 1)
    Real = np.zeros(maxperiod + 1)
    Imag = np.zeros(maxperiod + 1)
    Ampl = np.zeros(maxperiod + 1)
    OldQ = np.zeros(maxperiod + 1)
    OldI = np.zeros(maxperiod + 1)
    OlderQ = np.zeros(maxperiod + 1)
    OlderI = np.zeros(maxperiod + 1)
    OldReal = np.zeros(maxperiod + 1)
    OldImag = np.zeros(maxperiod + 1)
    OlderReal = np.zeros(maxperiod + 1)
    OlderImag = np.zeros(maxperiod + 1)
    OldAmpl = np.zeros(maxperiod + 1)
    DB = np.zeros(maxperiod + 1)

    for shift in range(1, length):
        p0 = (high_series[shift] + low_series[shift]) / 2
        p1 = (high_series[shift - 1] + low_series[shift - 1]) / 2
        hp[shift] = a2 * (p0 - p1) + a1 * hp[shift - 1]

        if shift >= 5:
            smoothHp[shift] = (
                hp[shift] + 2 * hp[shift - 1] + 3 * hp[shift - 2] +
                3 * hp[shift - 3] + 2 * hp[shift - 4] + hp[shift - 5]
            ) / 12

        delta = -0.015 * shift + 0.5
        delta = max(delta, 0.15)

        num = 0.0
        denom = 0.0
        maxAmpl = 0.0
        s1 = smoothHp[shift] - smoothHp[shift - 1]

        for n in range(minperiod, maxperiod + 1):
            beta = np.cos(2 * np.pi / n)
            gamma = 1 / np.cos(4 * np.pi * delta / n)
            alpha = gamma - np.sqrt(gamma ** 2 - 1)

            Q[n] = (n / (2 * np.pi)) * s1
            I[n] = smoothHp[shift]
            Real[n] = 0.5 * (1 - alpha) * (I[n] - OlderI[n]) + \
                beta * (1 + alpha) * OldReal[n] - alpha * OlderReal[n]
            Imag[n] = 0.5 * (1 - alpha) * (Q[n] - OlderQ[n]) + \
                beta * (1 + alpha) * OldImag[n] - alpha * OlderImag[n]
            Ampl[n] = Real[n] ** 2 + Imag[n] ** 2
            maxAmpl = max(maxAmpl, Ampl[n])

            OlderI[n] = OldI[n]
            OldI[n] = I[n]
            OlderQ[n] = OldQ[n]
            OldQ[n] = Q[n]
            OlderReal[n] = OldReal[n]
            OldReal[n] = Real[n]
            OlderImag[n] = OldImag[n]
            OldImag[n] = Imag[n]
            OldAmpl[n] = Ampl[n]

        for n in range(minperiod, maxperiod + 1):
            if maxAmpl != 0:
                t = 1 - 0.99 * Ampl[n] / maxAmpl
                if t != 0:
                    DB[n] = -medianPeriod * np.log(0.01 / t) / np.log(10)
            if DB[n] > decibelPeriod:
                DB[n] = decibelPeriod
            if DB[n] <= 3:
                num += n * (decibelPeriod - DB[n])
                denom += (decibelPeriod - DB[n])

        if denom != 0:
            dc[shift] = num / denom

        domCyc = np.median(dc[max(0, shift - medianPeriod):shift + 1])
        if domCyc < minperiod:
            domCyc = decibelPeriod
        beta = np.cos(2 * np.pi / domCyc)
        gamma = 1 / np.cos(4 * np.pi * delta / domCyc)
        alpha = gamma - np.sqrt(gamma ** 2 - 1)

        v1[shift] = volume_series[shift] * (2 * np.pi / domCyc) ** 2

        # Calculate moving average of v1 over minperiod using cumulative sum for efficiency
        if shift >= minperiod:
            v2[shift] = np.sum(v1[shift - minperiod + 1:shift + 1]) / minperiod
        else:
            v2[shift] = np.mean(v1[:shift + 1])

    # Creating the final NumPy array with V1 and V2    
    return v1,v2

def ultra_wpr(high_series, low_series, close_series, WPR_Period=13, W_Method='EMA', StartLength=3, WPhase=100, Step=5, StepsTotal=10,
              SmoothMethod='EMA', SmoothLength=3, SmoothPhase=100):
    """
    Ultra WPR indicator implementation using TA-Lib and apply_smoothing.

    Parameters:
    - high_series: NumPy array of high prices.
    - low_series: NumPy array of low prices.
    - close_series: NumPy array of close prices.
    - WPR_Period: Period for WPR calculation.
    - W_Method: Smoothing method for WPR.
    - StartLength: Initial smoothing period.
    - WPhase: Smoothing parameter (not used in this implementation).
    - Step: Period change step.
    - StepsTotal: Number of period changes.
    - SmoothMethod: Smoothing method for the counts.
    - SmoothLength: Smoothing depth.
    - SmoothPhase: Smoothing parameter (not used in this implementation).

    Returns:
    - bulls: Smoothed counts of increasing smoothed WPR values.
    - bears: Smoothed counts of decreasing smoothed WPR values.
    """

    # Compute WPR using TA-Lib
    wpr = talib.WILLR(high_series, low_series, close_series, timeperiod=WPR_Period)

    # Initialize periods
    periods = [StartLength + sm * Step for sm in range(StepsTotal + 1)]

    # Initialize lists to store smoothed WPRs
    xwpr0 = []

    # Compute smoothed WPRs for each period
    for period in periods:
        smoothed_wpr = apply_smoothing(wpr, method=W_Method, period=period)
        xwpr0.append(smoothed_wpr)

    # Initialize ups and dns arrays
    ups = np.zeros_like(wpr)
    dns = np.zeros_like(wpr)

    # For each smoothed WPR, compare current value with previous value
    for smoothed_series in xwpr0:
        xwpr_current = smoothed_series
        xwpr_previous = np.roll(xwpr_current, 1)
        xwpr_previous[0] = np.nan  # Handle first element

        ups += (xwpr_current > xwpr_previous).astype(int)
        dns += (xwpr_current <= xwpr_previous).astype(int)

    # Smooth the ups and dns counts using apply_smoothing
    bulls = apply_smoothing(ups, method=SmoothMethod, period=SmoothLength)
    bears = apply_smoothing(dns, method=SmoothMethod, period=SmoothLength)

    return bulls, bears


def ultra_rsi(price_series, RSI_Period=13, W_Method='EMA', StartLength=3, WPhase=100, Step=5, StepsTotal=10,
              SmoothMethod='EMA', SmoothLength=3, SmoothPhase=100):
    """
    Ultra RSI indicator implementation using TA-Lib and apply_smoothing.

    Parameters:
    - price_series: NumPy array of prices (e.g., close prices).
    - RSI_Period: Period for RSI calculation.
    - W_Method: Smoothing method for RSI ('EMA', 'SMA', 'WMA', 'DEMA', 'T3', 'KAMA', 'TRIMA').
    - StartLength: Initial smoothing period.
    - WPhase: Smoothing parameter (not used in this implementation).
    - Step: Period change step.
    - StepsTotal: Number of period changes.
    - SmoothMethod: Smoothing method for the counts.
    - SmoothLength: Smoothing depth.
    - SmoothPhase: Smoothing parameter (not used in this implementation).

    Returns:
    - bulls: Smoothed counts of increasing smoothed RSI values.
    - bears: Smoothed counts of decreasing smoothed RSI values.
    """
    # Compute RSI using TA-Lib
    rsi = talib.RSI(price_series, timeperiod=RSI_Period)

    # Initialize periods
    periods = [StartLength + sm * Step for sm in range(StepsTotal + 1)]

    # Initialize lists to store smoothed RSIs
    xrsis = []

    # Compute smoothed RSI for each period
    for period in periods:
        smoothed_rsi = apply_smoothing(rsi, method=W_Method, period=period)
        xrsis.append(smoothed_rsi)

    # Initialize ups and dns arrays
    ups = np.zeros_like(rsi)
    dns = np.zeros_like(rsi)

    # For each smoothed RSI, compare current value with previous value
    for smoothed_series in xrsis:
        xrsi_current = smoothed_series
        xrsi_previous = np.roll(xrsi_current, 1)
        xrsi_previous[0] = np.nan  # Handle first element

        # Increment 'ups' and 'dns' counts
        ups += (xrsi_current > xrsi_previous).astype(int)
        dns += (xrsi_current <= xrsi_previous).astype(int)

    # Smooth the ups and dns counts using apply_smoothing
    bulls = apply_smoothing(ups, method=SmoothMethod, period=SmoothLength)
    bears = apply_smoothing(dns, method=SmoothMethod, period=SmoothLength)

    return bulls, bears