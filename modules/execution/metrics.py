"""
EXECUTION — metrics
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: metrics_update, metrics_load, get_metrics_summary
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- metrics_update ---
def metrics_update(pnl, result):
    """Метрика жаңарту (6 көрсеткіш)"""
    global METRICS
    try:
        if result == "TP":
            METRICS["wins"] += 1
            METRICS["gross_profit"] += abs(pnl)
        elif result == "SL":
            METRICS["losses"] += 1
            METRICS["gross_loss"] += abs(pnl)

        METRICS["net_profit"] = METRICS["gross_profit"] - METRICS["gross_loss"]

        # Peak equity update
        acc = mt5_account_info()
        if acc:
            if acc.equity > METRICS["peak_equity"]:
                METRICS["peak_equity"] = acc.equity
            dd = (METRICS["peak_equity"] - acc.equity) / METRICS["peak_equity"] * 100
            if dd > METRICS["max_dd"]:
                METRICS["max_dd"] = dd

        # Expectancy
        total = METRICS["wins"] + METRICS["losses"]
        if total > 0:
            avg_win = METRICS["gross_profit"] / max(METRICS["wins"], 1)
            avg_loss = METRICS["gross_loss"] / max(METRICS["losses"], 1)
            wr = METRICS["wins"] / total
            METRICS["expectancy"] = (wr * avg_win) - ((1 - wr) * avg_loss)

        # Profit Factor
        if METRICS["gross_loss"] > 0:
            METRICS["profit_factor"] = METRICS["gross_profit"] / METRICS["gross_loss"]

        # Recovery Factor
        if METRICS["max_dd"] > 0:
            METRICS["recovery"] = METRICS["net_profit"] / METRICS["max_dd"]

        # Metrics DB
        _save_json(os.path.join(DATA_DIR, "metrics.json"), METRICS)
    except Exception as e:
        log.error(f"Metrics: {e}")



# --- metrics_load ---
def metrics_load():
    """Метрика жүктеу"""
    global METRICS
    d = _load_json(os.path.join(DATA_DIR, "metrics.json"), {})
    if d: METRICS.update(d)
    log.info(f"📈 Metrics: {METRICS['wins']}W / {METRICS['losses']}L")



# --- get_metrics_summary ---
def get_metrics_summary():
    """Метрика қорытындысы"""
    m = METRICS
    total = m["wins"] + m["losses"]
    wr = (m["wins"] / total * 100) if total > 0 else 0
    return {
        "wins": m["wins"],
        "losses": m["losses"],
        "win_rate": round(wr, 2),
        "net_profit": round(m["net_profit"], 2),
        "expectancy": round(m["expectancy"], 4),
        "profit_factor": round(m["profit_factor"], 2),
        "max_dd": round(m["max_dd"], 2),
        "recovery": round(m["recovery"], 2),
    }
    # ============================================================
# 🆕 WYCKOFF v2 — 10+ ШАРТ (Сіздің сыныңыз бойынша)
# ============================================================


