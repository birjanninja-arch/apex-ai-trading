"""
ANALYSIS — wavelet_mtf
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: wavelet_denoise, wavelet_trend, multi_timeframe_analysis
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- wavelet_denoise ---
def wavelet_denoise(prices, wavelet=WAVELET_TYPE, levels=WAVELET_LEVELS):
    """Wavelet — шуылдан тазалау"""
    try:
        import pywt
        if len(prices) < 50: return None
        prices_arr = np.array(prices, dtype=float)
        coeffs = pywt.wavedec(prices_arr, wavelet, level=levels)

        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        threshold = sigma * np.sqrt(2 * np.log(len(prices_arr)))

        coeffs_thresh = [coeffs[0]]
        for c in coeffs[1:]:
            c_thresh = pywt.threshold(c, threshold, mode="soft")
            coeffs_thresh.append(c_thresh)

        denoised = pywt.waverec(coeffs_thresh, wavelet)
        return denoised[:len(prices_arr)]
    except Exception as e:
        log.error(f"Wavelet: {e}")
        return None



# --- wavelet_trend ---
def wavelet_trend(prices):
    """Wavelet бойынша тренд бағыты"""
    try:
        denoised = wavelet_denoise(prices)
        if denoised is None or len(denoised) < 10: return None
        recent = denoised[-10:]
        slope = (recent[-1] - recent[0]) / max(abs(recent[0]), 1e-9)
        if slope > 0.001: return "UP"
        elif slope < -0.001: return "DOWN"
        else: return "SIDE"
    except Exception:
        return None


# ============================================================
# MULTI-TIMEFRAME
# ============================================================


# --- multi_timeframe_analysis ---
def multi_timeframe_analysis(symbol):
    """
    M15 + H1 + H4 + D1 талдау.
    Қайтарады: dict {alignment, score, trend_m15, trend_h1, trend_h4, trend_d1}
    """
    try:
        timeframes = {
            "M15": mt5.TIMEFRAME_M15,
            "H1":  mt5.TIMEFRAME_H1,
            "H4":  mt5.TIMEFRAME_H4,
            "D1":  mt5.TIMEFRAME_D1,
        }
        trends = {}
        for tf_name, tf_val in timeframes.items():
            rates = mt5_copy_rates(symbol, tf_val, 0, 60)
            if rates is None or len(rates) < 50: continue
            df = pd.DataFrame(rates)
            df = df.iloc[:-1]
            if len(df) < 50: continue
            e20 = df["close"].ewm(span=20).mean().iloc[-1]
            e50 = df["close"].ewm(span=50).mean().iloc[-1]
            cur = df["close"].iloc[-1]
            if cur > e20 > e50:
                trends[tf_name] = "UP"
            elif cur < e20 < e50:
                trends[tf_name] = "DOWN"
            else:
                trends[tf_name] = "SIDE"

        if not trends: return None

        up_count = sum(1 for v in trends.values() if v == "UP")
        down_count = sum(1 for v in trends.values() if v == "DOWN")
        total = len(trends)

        if up_count == total:
            alignment = "STRONG_UP"; score = 1.0
        elif down_count == total:
            alignment = "STRONG_DOWN"; score = 1.0
        elif up_count >= total * 0.75:
            alignment = "UP"; score = 0.75
        elif down_count >= total * 0.75:
            alignment = "DOWN"; score = 0.75
        else:
            alignment = "MIXED"; score = 0.4

        return {
            "alignment": alignment,
            "score": score,
            "trend_m15": trends.get("M15", "?"),
            "trend_h1": trends.get("H1", "?"),
            "trend_h4": trends.get("H4", "?"),
            "trend_d1": trends.get("D1", "?"),
        }
    except Exception as e:
        log.error(f"MultiTF: {e}")
        return None
        
        # ============================================================
# ML TRAINER (XGBoost + LogReg)
# ============================================================

# Full ML feature set (14) — matches process_symbol / features_save / RL obs

