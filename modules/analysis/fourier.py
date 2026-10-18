"""
ANALYSIS — fourier
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: fourier_analysis
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- fourier_analysis ---
def fourier_analysis(prices, harmonics=FOURIER_HARMONICS):
    """Фурье талдау — баға циклдерін табу"""
    try:
        if len(prices) < 50: return None
        prices_arr = np.array(prices, dtype=float)
        prices_detrended = prices_arr - np.mean(prices_arr)
        fft_vals = np.fft.fft(prices_detrended)
        fft_freq = np.fft.fftfreq(len(prices_detrended))
        amplitude = np.abs(fft_vals)
        top_idx = np.argsort(amplitude[1:len(amplitude)//2])[::-1][:harmonics] + 1

        if len(top_idx) > 0:
            dominant_idx = top_idx[0]
            dominant_freq = abs(fft_freq[dominant_idx])
            dominant_period = int(1 / dominant_freq) if dominant_freq > 0 else 0
        else:
            dominant_period = 0

        cycle_strength = float(np.sum(amplitude[top_idx]) / np.sum(amplitude))

        if dominant_period > 0:
            recent = prices_arr[-min(dominant_period, len(prices_arr)):]
            if len(recent) > 2:
                direction = "UP" if recent[-1] > recent[0] else "DOWN"
            else:
                direction = "NEUTRAL"
        else:
            direction = "NEUTRAL"

        return {
            "trend": "UP" if prices_arr[-1] > prices_arr[0] else "DOWN",
            "cycle_strength": round(cycle_strength, 3),
            "dominant_period": dominant_period,
            "direction": direction,
        }
    except Exception as e:
        log.error(f"Fourier: {e}")
        return None


# ============================================================
# FRACTAL DIMENSION (Higuchi)
# ============================================================


