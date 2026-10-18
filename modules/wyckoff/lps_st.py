"""
WYCKOFF — lps_st
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: detect_lps_v2, detect_st_v2, detect_shakeout_v2
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- detect_lps_v2 ---
def detect_lps_v2(df, i):
    """
    🆕 WYCKOFF LPS (Last Point of Support) v2 — 6 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend: UP
        if ctx["trend"] != "UP": return None

        # 2. Range: support > close > resistance
        if not (ctx["sup"] < last["close"] < ctx["res"]): return None

        # 3. Close жоғары (кері түзету)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.5: return None

        # 4. Volume dry-up
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr > 1.0: return None

        # 5. Supportтан алыс
        if abs(last["low"] - ctx["sup"]) > ctx["range"] * 0.15: return None

        # 6. R:R
        atr = ctx["atr"]
        sl = ctx["sup"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0: return None
        tp = last["close"] + risk * 3.0

        return {
            "event": "lps",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": 0.7,
            "context": ctx,
            "conditions": 6,
        }
    except Exception:
        return None



# --- detect_st_v2 ---
def detect_st_v2(df, i):
    """
    🆕 WYCKOFF ST (Secondary Test) v2 — 5 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Support-қа жақын
        if abs(last["low"] - ctx["sup"]) > ctx["range"] * 0.1: return None

        # 2. Volume dry-up
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr > 0.9: return None

        # 3. Кіші body
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.5: return None

        # 4. Close support-тан жоғары
        if last["close"] < ctx["sup"]: return None

        # 5. Direction: BUY (accumulation context)
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        return {
            "event": "st",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": 0.6,
            "context": ctx,
            "conditions": 5,
        }
    except Exception:
        return None



# --- detect_shakeout_v2 ---
def detect_shakeout_v2(df, i):
    """
    🆕 WYCKOFF SHAKEOUT v2 — 8 ШАРТ (Spring-нің күшті нұсқасы)
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend DOWN
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        # 2. Support break
        if not (last["low"] < ctx["sup"]): return None

        # 3. Close recovery
        if not (last["close"] > ctx["sup"]): return None

        # 4. Volume climax (жоғары)
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 2.0: return None

        # 5. Close location
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.5: return None

        # 6. Body size
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.8: return None

        # 7. Lower wick
        lower_wick = min(last["open"], last["close"]) - last["low"]
        if lower_wick < body * 1.5: return None

        # 8. R:R
        sl = last["low"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0: return None
        tp = last["close"] + risk * 3.5

        return {
            "event": "shakeout",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 3.0, 1.0),
            "context": ctx,
            "conditions": 8,
        }
    except Exception:
        return None



