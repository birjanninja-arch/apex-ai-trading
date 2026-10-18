"""
WYCKOFF — spring
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: wyckoff_context, detect_spring_v2
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- wyckoff_context ---
def wyckoff_context(df, i, lookback=48):
    """
    Wyckoff контексті есептеу.
    Қайтарады: dict (trend, range_pct, sup, res, atr, ema50, ema200)
    """
    try:
        recent = df.iloc[max(0, i-lookback):i]
        if len(recent) < 20: return None

        sup = float(recent["low"].min())
        res = float(recent["high"].max())
        rng = res - sup
        range_pct = (rng / sup * 100) if sup > 0 else 0

        # Trend context
        e50 = df["close"].iloc[max(0, i-50):i].ewm(span=50).mean().iloc[-1]
        e200 = df["close"].iloc[max(0, i-200):i].ewm(span=200).mean().iloc[-1]
        trend = "UP" if e50 > e200 * 1.001 else "DOWN" if e50 < e200 * 0.999 else "SIDE"

        # ATR
        atr_series = ta.atr(df["high"].iloc[max(0, i-30):i],
                             df["low"].iloc[max(0, i-30):i],
                             df["close"].iloc[max(0, i-30):i], length=14)
        atr = float(atr_series.iloc[-1]) if atr_series is not None and len(atr_series) > 0 else 0

        return {
            "trend": trend,
            "range_pct": range_pct,
            "sup": sup,
            "res": res,
            "range": rng,
            "atr": atr,
            "ema50": e50,
            "ema200": e200,
        }
    except Exception:
        return None



# --- detect_spring_v2 ---
def detect_spring_v2(df, i):
    """
    🆕 WYCKOFF SPRING v2 — 12 ШАРТ
    Қайтарады: dict немесе None
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]
        prev = df.iloc[i-1] if i > 0 else last
        next_candle = df.iloc[i+1] if i+1 < len(df) else None

        # 1. Trend context: DOWN (жинақтау)
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        # 2. Range context: 1-5%
        if not (0.5 < ctx["range_pct"] < 8.0): return None

        # 3. Support break
        if not (last["low"] < ctx["sup"]): return None

        # 4. Close recovery
        if not (last["close"] > ctx["sup"]): return None

        # 5. Close location (жоғары жабу)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.6: return None

        # 6. Volume climax
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.5: return None

        # 7. Volume dry-up (келесі свеча)
        if next_candle is not None:
            next_vr = next_candle["tick_volume"] / vm if vm > 0 else 1.0
            if next_vr > 1.2: return None

        # 8. Body size (кіші body)
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.6: return None

        # 9. Lower wick (ұзын)
        lower_wick = min(last["open"], last["close"]) - last["low"]
        if lower_wick < body * 1.5: return None

        # 10. R:R check
        sl = last["low"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0:
            return None

        # 11. 4H phase — accumulation / markup only (reject distribution)
        try:
            with _state_lock:
                # symbol may be attached as attr; fall back to soft pass
                ph = None
                for _sym, _ph in MEM.get("phases", {}).items():
                    ph = _ph
                    break
            if ph:
                p = str(ph.get("phase", "")).lower()
                if p in ("distribution", "markdown"):
                    return None
        except Exception:
            pass

        # 12. No spoofing — reject if any spoof mark younger than 5 min
        try:
            with _state_lock:
                spoof_map = dict(MEM.get("spoof", {}))
            now = time.time()
            for _k, ts in spoof_map.items():
                if now - float(ts) < 300:
                    return None
        except Exception:
            pass

        return {
            "event": "spring",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 12,
        }
    except Exception:
        return None



