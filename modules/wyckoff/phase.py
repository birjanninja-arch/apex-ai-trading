"""
WYCKOFF — phase
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: find_wyckoff_patterns_v2, analyze_structure, analyze_4h_phase
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- find_wyckoff_patterns_v2 ---
def find_wyckoff_patterns_v2(df):
    """
    🆕 WYCKOFF v2 — Барлық паттерндерді іздеу (10+ шарт)
    Қайтарады: list of dict (әр паттерн 5+ шарт)
    """
    patterns = []
    for i in range(48, len(df) - 3):
        # Spring (12 шарт)
        p = detect_spring_v2(df, i)
        if p: patterns.append(p)

        # Shakeout (8 шарт)
        p = detect_shakeout_v2(df, i)
        if p: patterns.append(p)

        # UTAD (10 шарт)
        p = detect_utad_v2(df, i)
        if p: patterns.append(p)

        # SOS (7 шарт)
        p = detect_sos_v2(df, i)
        if p: patterns.append(p)

        # SOW (7 шарт)
        p = detect_sow_v2(df, i)
        if p: patterns.append(p)

        # LPS (6 шарт)
        p = detect_lps_v2(df, i)
        if p: patterns.append(p)

        # ST (5 шарт)
        p = detect_st_v2(df, i)
        if p: patterns.append(p)

    # Ең соңғы 20 паттернді ғана қайтару
    patterns.sort(key=lambda x: x["idx"], reverse=True)
    return patterns[:20]



# --- analyze_structure ---
def analyze_structure(df):
    """
    Structure талдау (21 свеча).
    Look-ahead bias жоқ: support/resistance соңғы ЖАБЫЛҒАН бардан БҰРЫНғы lookback.
    df already should exclude the forming candle (iloc[:-1] applied upstream).
    """
    if len(df) < CANDLES_LOOKBACK + 1:
        return None
    # Use bars before the latest closed bar for S/R (shift logic)
    hist = df.iloc[-(CANDLES_LOOKBACK + 1):-1]
    if len(hist) < CANDLES_LOOKBACK:
        return None
    sup = float(hist["low"].min())
    res = float(hist["high"].max())
    cur = float(df.iloc[-1]["close"])
    rng = res - sup
    if rng <= 0:
        return None
    return {
        "support": sup,
        "resistance": res,
        "current": cur,
        "position_pct": ((cur - sup) / rng * 100),
        "range": rng,
    }



# --- analyze_4h_phase ---
def analyze_4h_phase(symbol):
    """4H фаза (тек жабылған свечалар — repaint fix)"""
    try:
        rates = mt5_copy_rates(symbol, mt5.TIMEFRAME_H4, 0, 250)
        if rates is None or len(rates) < 200: return None
        df = pd.DataFrame(rates)
        df = df.iloc[:-1]  # Аяқталмаған свечаны алып тастаймыз
        if len(df) < 200: return None

        rng = (df["high"] - df["low"]).replace(0, 1)
        ad = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng
        ad_n = ad.iloc[-1]; ad_m = ad.rolling(20).mean().iloc[-1]
        e50 = df["close"].ewm(span=50).mean().iloc[-1]
        e200 = df["close"].ewm(span=200).mean().iloc[-1]
        tr = "UP" if e50 > e200 * 1.001 else "DOWN" if e50 < e200 * 0.999 else "SIDE"
        if ad_n > ad_m and tr == "UP": ph = "markup"
        elif ad_n > ad_m and tr in ["SIDE", "DOWN"]: ph = "accumulation"
        elif ad_n < ad_m and tr == "DOWN": ph = "markdown"
        elif ad_n < ad_m and tr in ["SIDE", "UP"]: ph = "distribution"
        else: ph = "unknown"
        prev = MEM["phases"].get(symbol, {})
        prev_ph = prev.get("phase")
        trans = None
        if prev_ph == "markdown" and ph in ["accumulation", "markup"]: trans = "BULL_TRANS"
        elif prev_ph == "markup" and ph in ["distribution", "markdown"]: trans = "BEAR_TRANS"
        return {"phase": ph, "ad": float(ad_n), "trend": tr,
                "transition": trans, "created_at": time.time()}
    except Exception: return None


# ============================================================
# SEQUENCE (Spring → ST → SOS → LPS → HFT)
# ============================================================


