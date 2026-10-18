"""
ML_AI — context
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: rule_score, ensemble_predict
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- rule_score ---
def rule_score(level, delta, er, sd, adaptive):
    """Ережелер бойынша ұпай"""
    score = 0.0
    score += min(level / 200.0, 1.0) * 0.40
    score += min(abs(delta) / 50.0, 1.0) * 0.20
    if er == "EFFORT_EQ_RESULT":
        score += 0.15
    elif er == "ABSORPTION":
        score += 0.10
    if sd in ["DEMAND_WINS", "SUPPLY_WINS"]:
        score += 0.15
    return min(score, 1.0)



# --- ensemble_predict ---
def ensemble_predict(level, delta, er, sd, adaptive, features=None, shazam_result=None):
    """
    APEX v3/v4 Ensemble:
    - Rules 35%
    - ML 20%
    - Advanced (Fourier+Fractal+MTF+Wavelet) 15%
    - RL (live) 10%
    - Shazam v4 (FAISS multi-TF + 10y RL) 20%
    """
    rule_p = rule_score(level, delta, er, sd, adaptive)

    if features is not None and len(features) >= 14:
        ml_p = ml_predict(features)
        fourier_str = features[9]
        fractal_val = features[10]
        mtf_score = features[11]
        wavelet_val = features[12]

        adv_score = (
            fourier_str * 0.25 +
            (1 - abs(fractal_val - 1.5) / 0.5) * 0.25 +
            mtf_score * 0.25 +
            (1 if wavelet_val > 0 else 0.5 if wavelet_val == 0 else 0) * 0.25
        )
        adv_score = max(0, min(1, adv_score))

        rl_p = rl_predict(features) if RL_STATUS.get("ready") else 0.5

        # Shazam v4 boost
        sh_p = 0.5
        sh_sig = "WAIT"
        if shazam_result and SHAZAM_ENABLED:
            comb = shazam_result.get("combined_signal", "WAIT")
            sc = float(shazam_result.get("combined_score", 0.5))
            sh_sig = comb
            if comb == "BUY":
                sh_p = sc
            elif comb == "SELL":
                sh_p = 1.0 - sc
            else:
                sh_p = 0.5

        final = (
            rule_p * 0.35 +
            ml_p * 0.20 +
            adv_score * 0.15 +
            rl_p * 0.10 +
            sh_p * 0.20
        )
        final = max(0.0, min(1.0, float(final)))

        return final, {
            "rules": rule_p, "ml": ml_p, "advanced": adv_score,
            "rl": rl_p, "shazam": sh_p, "shazam_signal": sh_sig,
            "fourier": fourier_str, "fractal": fractal_val,
            "mtf": mtf_score, "wavelet": wavelet_val,
            "final": final,
        }

    if features is not None and ML_STATUS.get("ready"):
        ml_p = ml_predict(features)
        final = rule_p * 0.7 + ml_p * 0.3
        return final, {"rules": rule_p, "ml": ml_p, "final": final}

    return rule_p, {"rules": rule_p, "ml": 0.5, "final": rule_p}
    # ============================================================
# TELEGRAM
# ============================================================


