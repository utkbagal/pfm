from typing import Dict
import pandas as pd


class BuyPlanGenerator:
    """
    Generates structured trade plan.
    """

    def generate(self, context: Dict) -> Dict:

        df: pd.DataFrame = context["indicator_df"]
        setups = context["setups"]

        latest = df.iloc[-1]

        price = latest["close"]
        atr = latest.get("atr_14", 0)

        primary_setup = setups[0]  # take strongest setup
        setup_type = primary_setup["setup_type"]

        entry_range = self._calculate_entry(df, setup_type)
        stop_loss = self._calculate_stop_loss(df, entry_range, atr)
        target_primary, target_extended = self._calculate_targets(
            entry_range, atr
        )

        rr = self._risk_reward(entry_range, stop_loss, target_primary)

        validity_days = self._validity_window(setup_type)

        return {
            "entry_range": entry_range,
            "stop_loss": round(stop_loss, 2),
            "target_primary": round(target_primary, 2),
            "target_extended": round(target_extended, 2),
            "risk_reward_ratio": round(rr, 2),
            "validity_days": validity_days
        }

    # -----------------------------------
    # Entry logic
    # -----------------------------------

    def _calculate_entry(self, df, setup_type):

        latest = df.iloc[-1]

        if setup_type == "BREAKOUT":
            high = latest["high"]
            return (round(high * 1.001, 2), round(high * 1.005, 2))

        if setup_type == "PULLBACK":
            ema_20 = latest["ema_20"]
            return (round(ema_20 * 0.995, 2), round(ema_20 * 1.005, 2))

        if setup_type == "RSI_REVERSAL":
            close = latest["close"]
            return (round(close * 1.001, 2), round(close * 1.004, 2))

        return (latest["close"], latest["close"])

    # -----------------------------------
    # Stop-loss logic
    # -----------------------------------

    def _calculate_stop_loss(self, df, entry_range, atr):

        recent_low = df["low"].tail(5).min()
        entry_price = entry_range[0]

        atr_buffer = entry_price - atr

        return min(recent_low, atr_buffer)

    # -----------------------------------
    # Target logic
    # -----------------------------------

    def _calculate_targets(self, entry_range, atr):

        entry_price = entry_range[0]

        target_2pct = entry_price * 1.02
        target_atr = entry_price + (1.2 * atr)

        primary = max(target_2pct, target_atr)
        extended = entry_price + (2 * atr)

        return primary, extended

    # -----------------------------------
    # Risk Reward
    # -----------------------------------

    def _risk_reward(self, entry_range, stop, target):

        entry = entry_range[0]
        risk = entry - stop
        reward = target - entry

        if risk <= 0:
            return 0

        return reward / risk

    # -----------------------------------
    # Validity
    # -----------------------------------

    def _validity_window(self, setup_type):

        if setup_type == "BREAKOUT":
            return 3
        if setup_type == "PULLBACK":
            return 5
        if setup_type == "RSI_REVERSAL":
            return 2

        return 3
