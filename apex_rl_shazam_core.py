"""
============================================================
 🚀 APEX v3 — RL + SHAZAM SIGNAL CORE (сигнал КӨБЕЙТУ)
============================================================
 Мақсат: сигнал саны ↑ + сапа ↑
 1) RL (PPO)  — тәуелсіз сигнал генераторы ( rules емес, өзі шешеді )
 2) Shazam    — multi-TF k-NN паттерн ұқсастығы (FAISS емес, numpy — қосымша жоқ)
 3) Екеуі сәйкес → SIGNAL (level=200), AI_CONFIRM босатылады
 4) Қатты қайшы болса → сигнал жоқ (сапаны сақтау)

 ҚОСУ (apex_v3_fixed.py ішінде):
   1. Файлды бот папкасына салыңыз: apex_rl_shazam_core.py
   2. Импорт қосыңыз (MT5 импорттардан кейін):
        from apex_rl_shazam_core import rl_shazam_gate, extract_features14
   3. process_symbol ішінде, "# 6. WAIT / CONFIRM" БЛОГІНАН ДҰРЫС:
        boosted = False
        boost = rl_shazam_gate(symbol, df)
        if boost and boost["signal_level"] >= LEVEL_SIGNAL:
            level = LEVEL_SIGNAL
            direction = boost["direction"]
            reasons.extend(boost["reasons"])
            boosted = True
   4. SIGNAL блокындағы AI confirm қатесін жұмсартыңыз:
        if ai_s < AI_CONFIRM_MIN and not boosted:
            log.info(f"AI reject {symbol} ({ai_s}/7)"); return
"""

import os
import time
import numpy as np
import pandas as pd
import pandas_ta as ta

# Боттың өз функцияларын қолданамыз (import тек бот папкасында жұмыс істейді)
try:
    import apex_v3_fixed as A
except ImportError:
    A = None  # тест режимінде жеке қолдануға болады

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
CONF = {
    "RL_BUY": 0.60,        # rl_p >= 0.60 → BUY
    "RL_SELL": 0.40,       # rl_p <= 0.40 → SELL
    "SH_MIN": 0.55,        # shazam минимум сенім
    "SH_STRONG": 0.65,     # shazam күшті сенім
    "AGREE_SIGNAL": 0.62,  # RL+Shazam сәйкес → SIGNAL
    "SOLO_RL_MIN": 0.74,   # жалғыз күшті RL → SIGNAL (Shazam қайшы болмағанда)
    "AGREE_CONFIRM": 0.52, # әлсіз сәйкестік → CONFIRM (180)
    "NEXT_BARS": 24,       # shazam болжам горизонты (M15)
    "K": 7,                # k-NN көршілер саны
    "LOOKBACK": 120,       # сұраныс терезесі (M15 бар)
}

SHAZAM_LIB = None
if A is not None:
    SHAZAM_LIB = os.path.join(A.RL_DIR, "shazam_lib.npz")


# ------------------------------------------------------------
# 14 FEATURE (process_symbol ішіндегідей дәл)
# ------------------------------------------------------------
def extract_features14(symbol, df, delta=None):
    """Соңғы жабылған бар бойынша 14 feature (ML/RL obs — 14, obs15 = 0)."""
    d = df.copy()
    d["atr"] = ta.atr(d["high"], d["low"], d["close"], length=14)
    d["vol_ma"] = d["tick_volume"].rolling(20, min_periods=20).mean().shift(1)
    rng = (d["high"] - d["low"]).replace(0, 1)
    d["close_loc"] = (d["close"] - d["low"]) / rng
    d["ad"] = ((d["close"] - d["low"]) - (d["high"] - d["close"])) / rng
    mfi = ta.mfi(d["high"], d["low"], d["close"], d["tick_volume"], length=14)
    d["mfi"] = mfi if mfi is not None else 50.0

    last = d.iloc[-1]
    vm = last["vol_ma"]
    vr = float(last["tick_volume"]) / float(vm) if (vm and not pd.isna(vm) and vm > 0) else 1.0
    atr_v = float(last["atr"]) if not pd.isna(last["atr"]) else 0.0
    close = float(last["close"])
    atr_pct = (atr_v / close * 100.0) if close > 0 else 0.0

    if delta is None:
        try:
            delta = A.get_delta(symbol, 60)
        except Exception:
            delta = 0.0

    try:
        adaptive, _ = A.get_adaptive(d, symbol)
    except Exception:
        adaptive = 1.0

    prices = d["close"].tail(100).values
    f_res = A.fourier_analysis(prices) if A else None
    fourier_val = f_res["cycle_strength"] if f_res else 0.5
    fd = A.fractal_dimension(prices) if A else None
    fractal_val = fd if fd else 1.5
    mstate = A.market_state_by_fractal(fd) if A else "UNKNOWN"
    mtf = A.multi_timeframe_analysis(symbol) if A else None
    mtf_score = mtf["score"] if mtf else 0.5
    wt = A.wavelet_trend(prices) if A else None
    wavelet_val = 1.0 if wt == "UP" else (-1.0 if wt == "DOWN" else 0.0)

    hour = time.gmtime().tm_hour
    market_state_val = {"STRONG_TREND": 1.0, "TREND": 0.5, "WEAK_TREND": 0.0,
                        "RANGE": -0.5, "UNKNOWN": 0.0}.get(mstate, 0.0)

    return [
        vr, abs(float(delta)), adaptive, atr_pct,
        float(last["mfi"]), float(last["ad"]),
        float(last["body"]) / atr_v if atr_v > 0 else 0.0,
        float(last["close_loc"]), float(hour),
        fourier_val, fractal_val, mtf_score, wavelet_val, market_state_val,
    ]


# ------------------------------------------------------------
# SHAZAM — numpy k-NN (FAISS қажет емес)
# ------------------------------------------------------------
def _norm_window(closes, lookback):
    """Лог-қайтару нормализациясы — масштабтан тәуелсіз."""
    w = np.asarray(closes, dtype=np.float64)[-lookback:]
    if len(w) < lookback:
        return None
    r = np.diff(np.log(np.maximum(w, 1e-9)))
    s = r.std()
    return r / s if s > 1e-12 else None


def shazam_predict_local(symbol, lookback=None):
    """
    k-NN регрессия: тарихтағы ұқсас multi-TF терезелердің
    келесі 24 барлық қайтаруын салмақтап болжайды.
    Қайтарады: dict(signal, score, k, avg_ret) немесе None
    """
    lb = lookback or CONF["LOOKBACK"]
    if SHAZAM_LIB is None or not os.path.exists(SHAZAM_LIB):
        return None
    try:
        lib = np.load(SHAZAM_LIB, allow_pickle=True)
        lib_vecs = lib["vecs"]          # (N, D) нормализованные терезелер
        lib_ret = lib["next_ret"]       # (N,)   келесі 24 бар қайтаруы
    except Exception:
        return None

    # Қазіргі терезе: M15 + H1 + H4 біріктірілген
    parts = []
    for tf, mult in [(A.mt5.TIMEFRAME_M15, 1),
                     (A.mt5.TIMEFRAME_H1, 1),
                     (A.mt5.TIMEFRAME_H4, 1)]:
        rates = A.mt5_copy_rates(symbol, tf, 0, lb)
        if rates is None or len(rates) < lb // 2:
            return None
        w = _norm_window(pd.DataFrame(rates)["close"].values, max(lb // (mult * 4), 30))
        if w is None:
            return None
        parts.append(w)
    q = np.concatenate(parts)
    if q is None or lib_vecs.shape[1] != len(q):
        return None

    qn = q / (np.linalg.norm(q) + 1e-12)
    ln = lib_vecs / (np.linalg.norm(lib_vecs, axis=1, keepdims=True) + 1e-12)
    sims = ln @ qn
    top = np.argsort(sims)[::-1][:CONF["K"]]
    mean_sim = float(np.mean(sims[top]))
    avg_ret = float(np.mean(lib_ret[top]))

    if avg_ret > 0.0012:
        sig = "BUY"
    elif avg_ret < -0.0012:
        sig = "SELL"
    else:
        sig = "WAIT"
    return {"signal": sig, "score": round(min(max(mean_sim, 0.0), 1.0), 3),
            "k": int(len(top)), "avg_ret": round(avg_ret, 5)}


def _shazam(symbol):
    """Бар болса apex_v4_shazam_core, жоқ болса — жергілікті k-NN."""
    if A is not None and A._SHAZAM_MOD is not None:
        try:
            r = A._SHAZAM_MOD.shazam_predict_symbol(symbol)
            if r:
                return r
        except Exception:
            pass
    return shazam_predict_local(symbol)


# ------------------------------------------------------------
# НЕГІЗГІ ГЕЙТ — RL + Shazam
# ------------------------------------------------------------
def rl_shazam_gate(symbol, df):
    """
    Қайтарады:
      None                        — шарт сақталмады
      {signal_level:200,...}      — SIGNAL (_rules level 200 деп қабылданады)
      {signal_level:180,...}      — CONFIRM деңгейі
    """
    if A is None:
        return None

    features = extract_features14(symbol, df)
    rl_p = A.rl_predict(features)                      # 0..1, 0.5=HOLD
    if rl_p >= CONF["RL_BUY"]:
        rl_dir, rl_strength = "BUY", (rl_p - 0.5) * 2   # 0..1
    elif rl_p <= CONF["RL_SELL"]:
        rl_dir, rl_strength = "SELL", (0.5 - rl_p) * 2
    else:
        return None                                    # RL HOLD — сигнал жоқ

    sh = _shazam(symbol)
    sh_dir = sh.get("combined_signal") or sh.get("signal") or "WAIT" \
        if isinstance(sh, dict) else "WAIT"
    sh_score = float(sh.get("combined_score", sh.get("score", 0.5))) \
        if isinstance(sh, dict) else 0.5

    reasons = [f"🤖 RL {rl_dir} {rl_p:.2f}"]
    if isinstance(sh, dict):
        reasons.append(f"🎵 Shazam {sh_dir} {sh_score*100:.0f}%")

    # 1) Қатты қайшы — сапа үшін өткізбейміз
    if sh_dir in ("BUY", "SELL") and sh_dir != rl_dir and sh_score >= CONF["SH_STRONG"]:
        A.log.info(f"RL/Shazam conflict {symbol}: rl={rl_dir} sh={sh_dir} → skip")
        return None

    # 2) Шынайы сәйкестік
    agree = False
    if sh_dir == rl_dir and sh_score >= CONF["SH_MIN"]:
        agree = True
        reasons.append("✅ RL+Shazam сәйкес")

    agree_score = 0.55 * rl_strength + 0.45 * sh_score

    if agree and agree_score >= CONF["AGREE_SIGNAL"]:
        return {"direction": rl_dir, "signal_level": 200,
                "agree": agree_score, "rl_p": rl_p, "shazam": sh, "reasons": reasons}
    if rl_strength >= CONF["SOLO_RL_MIN"] and sh_score < CONF["SH_STRONG"]:
        return {"direction": rl_dir, "signal_level": 200,
                "agree": agree_score, "rl_p": rl_p, "shazam": sh, "reasons": reasons}
    if agree and agree_score >= CONF["AGREE_CONFIRM"]:
        return {"direction": rl_dir, "signal_level": 180,
                "agree": agree_score, "rl_p": rl_p, "shazam": sh, "reasons": reasons}
    return None
