"""
RISK — sl_tp
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: load_sltp_config, get_sltp_for, build_trade_plan
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- load_sltp_config ---
def load_sltp_config():
    if os.path.exists(SLTP_FILE):
        try:
            with open(SLTP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception: pass
    return {"global": {}}



# --- get_sltp_for ---
def get_sltp_for(event, symbol=None):
    cfg = load_sltp_config()
    g = cfg.get("global", {})
    if event in g:
        return g[event]["sl_mult"], g[event]["tp_r"]
    return 0.7, 3.5



# --- build_trade_plan ---
def build_trade_plan(direction, entry, atr, sup, res, l_ev, h_ev, event):
    """
    Trade plan — SL/TP/R:R + risk_usd.
    Lot есептеу open_position ішінде (calc_lot) жасалады — мұнда qty жоқ.
    """
    sl_m, tp_r = get_sltp_for(event)
    if direction == "BUY":
        sl = l_ev - sl_m * atr
        risk = entry - sl
        if risk <= 0:
            return None
        tp = entry + tp_r * risk
    else:
        sl = h_ev + sl_m * atr
        risk = sl - entry
        if risk <= 0:
            return None
        tp = entry - tp_r * risk
    rr = abs(tp - entry) / risk if risk > 0 else 0
    if rr < RISK_REWARD_MIN:
        return None
    with _state_lock:
        eq = _stats.get("equity", 10000.0)
    risk_usd = eq * (RISK_PER_TRADE / 100.0)
    return {
        "entry": round(entry, 5),
        "sl": round(sl, 5),
        "tp": round(tp, 5),
        "rr": round(rr, 2),
        "risk_usd": round(risk_usd, 2),
        "sl_dist": round(risk, 5),
    }



