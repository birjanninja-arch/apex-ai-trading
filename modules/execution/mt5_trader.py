"""
EXECUTION — mt5_trader
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: mt5_safe, mt5_copy_rates, mt5_account_info, mt5_positions_get, mt5_symbol_info, mt5_symbol_info_tick, mt5_order_send, mt5_terminal_info, get_filling_mode, mt5_connect
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- mt5_safe ---
def mt5_safe(fn, *args, **kwargs):
    """Execute any MT5 call under exclusive lock. Prevents crashes & corrupted data."""
    with _mt5_lock:
        return fn(*args, **kwargs)



# --- mt5_copy_rates ---
def mt5_copy_rates(symbol, timeframe, start_pos, count):
    return mt5_safe(mt5.copy_rates_from_pos, symbol, timeframe, start_pos, count)



# --- mt5_account_info ---
def mt5_account_info():
    return mt5_safe(mt5.account_info)



# --- mt5_positions_get ---
def mt5_positions_get(**kwargs):
    return mt5_safe(mt5.positions_get, **kwargs)



# --- mt5_symbol_info ---
def mt5_symbol_info(symbol):
    return mt5_safe(mt5.symbol_info, symbol)



# --- mt5_symbol_info_tick ---
def mt5_symbol_info_tick(symbol):
    return mt5_safe(mt5.symbol_info_tick, symbol)



# --- mt5_order_send ---
def mt5_order_send(request):
    return mt5_safe(mt5.order_send, request)



# --- mt5_terminal_info ---
def mt5_terminal_info():
    return mt5_safe(mt5.terminal_info)



# --- get_filling_mode ---
def get_filling_mode(symbol_info):
    """
    Dynamically choose ORDER_FILLING_* supported by the broker/symbol.
    Priority: FOK → IOC → RETURN. Prevents TRADE_RETCODE_INVALID_FILL.
    """
    if symbol_info is None:
        return mt5.ORDER_FILLING_IOC
    fm = symbol_info.filling_mode
    # filling_mode is a bitmask: 1=FOK, 2=IOC, 4=RETURN
    if fm & 1:   # SYMBOL_FILLING_FOK
        return mt5.ORDER_FILLING_FOK
    if fm & 2:   # SYMBOL_FILLING_IOC
        return mt5.ORDER_FILLING_IOC
    return mt5.ORDER_FILLING_RETURN


# ============================================================
# LOGGING
# ============================================================


# --- mt5_connect ---
def mt5_connect():
    """MT5-ке қосылу"""
    if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        log.error(f"MT5: {mt5.last_error()}"); return False
    acc = mt5_account_info()
    if acc is None: return False
    log.info(f"MT5 OK | {acc.login} | ${acc.equity}")
    _stats["equity"] = acc.equity
    METRICS["peak_equity"] = acc.equity
    return True


# ============================================================
# STATE (JSON + DB)
# ============================================================


