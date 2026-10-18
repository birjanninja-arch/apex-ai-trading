"""
RISK — limits
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: set_mode, get_mode, can_trade, validate_risk
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- validate_risk ---
def validate_risk():
    """Тәуекел лимиттерін тексеру (thread-safe)"""
    with _state_lock:
        now = time.time()
        if now - _stats.get("day_start", 0) > 86400:
            _stats["day_start"] = now
            _stats["daily_trades"] = 0
            _stats["daily_loss"] = 0.0
        if _stats.get("daily_trades", 0) >= DAILY_TRADES_LIMIT:
            return False
        if _stats.get("daily_loss", 0.0) >= DAILY_LOSS_LIMIT:
            return False
        return True


# ============================================================
# AUTO TRADER
# ============================================================


# --- set_mode ---
def set_mode(mode):
    """Режим ауыстыру"""
    AUTO_STATE["mode"] = mode
    AUTO_STATE["enabled"] = mode != "MANUAL"
    auto_save()
    log.info(f"🤖 Mode: {mode}")
    return mode



# --- get_mode ---
def get_mode():
    """Ағымдағы режим"""
    return AUTO_STATE.get("mode", "MANUAL")



# --- can_trade ---
def can_trade():
    """Auto Trader рұқсаты (thread-safe)"""
    with _state_lock:
        now = time.time()
        if now - AUTO_STATE.get("day_start", 0) > 86400:
            AUTO_STATE["day_start"] = now
            AUTO_STATE["daily_trades"] = 0
            AUTO_STATE["daily_loss"] = 0.0
            # auto_save outside lock to avoid deadlock
            need_save = True
        else:
            need_save = False
        enabled = AUTO_STATE.get("enabled", False)
        daily_trades = AUTO_STATE.get("daily_trades", 0)
        daily_loss = AUTO_STATE.get("daily_loss", 0.0)
    if need_save:
        auto_save()
    if not enabled:
        return False, "Auto OFF"
    if daily_trades >= DAILY_TRADES_LIMIT:
        return False, "Daily trades"
    if daily_loss >= DAILY_LOSS_LIMIT:
        return False, "Daily loss"
    return True, "OK"



