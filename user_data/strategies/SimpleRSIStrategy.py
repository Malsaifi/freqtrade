# Import necessary libraries
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta

# Define the strategy class, inheriting from IStrategy
class SimpleRSIStrategy(IStrategy):
    """
    This is a simple trading strategy using the Relative Strength Index (RSI).
    It buys when RSI indicates an oversold condition and sells when it indicates an overbought condition.
    """

    # --- Strategy parameters ---
    # Timeframe for the candles (e.g., '5m', '15m', '1h', '4h', '1d')
    timeframe = '1h'

    # Minimal ROI (Return on Investment) for the strategy.
    # This defines the target profit percentage at which the bot will consider selling.
    # "0": 0.02 means sell if profit reaches 2% at any time.
    minimal_roi = {"0": 0.02}

    # Stoploss: percentage loss at which the trade will be closed to limit losses.
    # -0.1 means close trade if loss reaches 10%.
    stoploss = -0.1

    # Trailing Stoploss: enables a stoploss that moves up with the price.
    trailing_stop = True
    # The percentage of profit at which the trailing stop becomes active.
    trailing_stop_positive = 0.01 # Trailing stop active when profit is 1%
    # Offset from the highest point reached, at which the trailing stop triggers a sell.
    trailing_stop_positive_offset = 0.02 # If profit reaches 2%, trailing stop moves up.
    # If True, trailing stop only activates after `trailing_stop_positive_offset` profit is reached.
    trailing_only_offset_is_reached = True

    # Optimal timeframe to get the data for hyperopt (can be different from strategy timeframe)
    # This is often used when optimizing. For now, we'll keep it commented out.
    # optimal_timeframe = '5m'

    # Run "populate_indicators" only for new candle.
    # This is the default and generally recommended for performance.
    process_only_new_candles = True

    # These values can be optimized through Hyperopt later
    # Example for optimization:
    # rsi_buy_value = IntParameter(20, 35, default=30, space='buy')
    # rsi_sell_value = IntParameter(65, 80, default=70, space='sell')


    # --- Indicator calculation ---
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculates all necessary indicators for the strategy.
        This function is called once per candle for each pair.
        """
        # Calculate Relative Strength Index (RSI) with a period of 14
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    # --- Buy signal logic ---
    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Defines the conditions for opening a long position (buy signal).
        A 'buy' column is added to the dataframe, with 1 indicating a buy signal.
        """
        # Buy when RSI is below 30 (oversold condition)
        dataframe.loc[
            (
                dataframe['rsi'] < 30  # RSI is less than 30
            ),
            'buy'
        ] = 1

        return dataframe

    # --- Sell signal logic ---
    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Defines the conditions for closing a long position (sell signal).
        A 'sell' column is added to the dataframe, with 1 indicating a sell signal.
        """
        # Sell when RSI is above 70 (overbought condition)
        dataframe.loc[
            (
                dataframe['rsi'] > 70  # RSI is greater than 70
            ),
            'sell'
        ] = 1

        return dataframe
