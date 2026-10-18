"""
WYCKOFF — sos_sow
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: detect_sos_v2, detect_sow_v2
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- detect_sos_v2 ---
def detect_sos_v2(df, i):
    """
    🆕 WYCKOFF SOS (Sign of Strength) v2 — 7 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend: UP/Accumulation
        if ctx["trend"] not in ["UP", "SIDE"]: return None

        # 2. Bull candle
        is_bull = last["close"] > last["open"]
        if not is_bull: return None

        # 3. Resistance break
        if not (last["close"] > ctx["res"]): return None

        # 4. Body size (үлкен)
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body < atr * 0.7: return None

        # 5. Volume
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.5: return None

        # 6. Close location (жоғары)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.7: return None

        # 7. R:R
        sl = last["low"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0: return None
        tp = last["close"] + risk * 3.0

        return {
            "event": "sos",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 7,
        }
    except Exception:
        return None



# --- detect_sow_v2 ---
def detect_sow_v2(df, i):
    """
    🆕 WYCKOFF SOW (Sign of Weakness) v2 — 7 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend: DOWN/Distribution
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        # 2. Bear candle
        is_bear = last["close"] < last["open"]
        if not is_bear: return None

        # 3. Support break
        if not (last["close"] < ctx["sup"]): return None

        # 4. Body size
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body < atr * 0.7: return None

        # 5. Volume
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.5: return None

        # 6. Close location (төмен)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc > 0.3: return None

        # 7. R:R
        sl = last["high"] + atr * 0.3
        risk = sl - last["close"]
        if risk <= 0: return None
        tp = last["close"] - risk * 3.0

        return {
            "event": "sow",
            "direction": "SELL",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 7,
        }
    except Exception:
        return None



