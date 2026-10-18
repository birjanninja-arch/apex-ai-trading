"""
WYCKOFF — utad
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: detect_utad_v2
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- detect_utad_v2 ---
def detect_utad_v2(df, i):
    """
    🆕 WYCKOFF UTAD v2 — 10 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]
        next_candle = df.iloc[i+1] if i+1 < len(df) else None

        # 1. Trend: UP немесе SIDE (тарату)
        if ctx["trend"] not in ["UP", "SIDE"]: return None

        # 2. Range context
        if not (0.5 < ctx["range_pct"] < 8.0): return None

        # 3. Resistance break
        if not (last["high"] > ctx["res"]): return None

        # 4. Close reversal
        if not (last["close"] < ctx["res"]): return None

        # 5. Close location (төмен жабу)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc > 0.4: return None

        # 6. Volume climax
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.3: return None

        # 7. Volume dry-up
        if next_candle is not None:
            next_vr = next_candle["tick_volume"] / vm if vm > 0 else 1.0
            if next_vr > 1.2: return None

        # 8. Body size
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.7: return None

        # 9. Upper wick (ұзын)
        upper_wick = last["high"] - max(last["open"], last["close"])
        if upper_wick < body * 1.3: return None

        # 10. R:R check
        sl = last["high"] + atr * 0.3
        risk = sl - last["close"]
        if risk <= 0: return None
        tp = last["close"] - risk * 3.0

        return {
            "event": "utad",
            "direction": "SELL",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 10,
        }
    except Exception:
        return None



