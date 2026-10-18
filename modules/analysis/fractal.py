"""
ANALYSIS — fractal
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: fractal_dimension, market_state_by_fractal
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- fractal_dimension ---
def fractal_dimension(prices, window=FRACTAL_WINDOW):
    """
    Higuchi әдісі — фракталдық өлшем.
    Қайтарады: float (1.0 - 2.0)
    1.0 = түзу сызық (тренд)
    1.5 = Brownian
    2.0 = шуыл (флэт)
    """
    try:
        if len(prices) < window: return None
        prices_arr = np.array(prices[-window:], dtype=float)
        L = []
        k_values = [2, 4, 8, 16, 32]

        for k in k_values:
            Lk = []
            for m in range(k):
                idx = np.arange(m, len(prices_arr), k)
                if len(idx) < 2: continue
                Lmk = np.sum(np.abs(np.diff(prices_arr[idx])))
                Lmk = Lmk * (len(prices_arr) - 1) / (k * len(idx))
                Lk.append(Lmk)
            if Lk:
                L.append(np.mean(Lk))

        if len(L) < 2: return None

        x = np.log(1.0 / np.array(k_values[:len(L)]))
        y = np.log(np.array(L))
        coeffs = np.polyfit(x, y, 1)
        fd = coeffs[0]
        return round(float(fd), 3)
    except Exception as e:
        log.error(f"Fractal: {e}")
        return None



# --- market_state_by_fractal ---
def market_state_by_fractal(fd):
    """Fractal dimension → нарық күйі"""
    if fd is None: return "UNKNOWN"
    if fd < 1.3:    return "STRONG_TREND"
    elif fd < 1.5:  return "TREND"
    elif fd < 1.7:  return "WEAK_TREND"
    else:           return "RANGE"


# ============================================================
# WAVELET TRANSFORM
# ============================================================


