"""
RISK — position_size
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: calc_lot, open_position
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- calc_lot ---
def calc_lot(symbol, risk_usd, sl_dist):
    """
    Lot есептеу — thread-safe, volume_step/min/max құрметтейді.
    """
    if sl_dist <= 0:
        return 0.01
    info = mt5_symbol_info(symbol)
    if not info:
        return 0.01
    tv = info.trade_tick_value
    ts = info.trade_tick_size
    if ts <= 0 or tv <= 0:
        return 0.01
    # risk_usd = lot * (sl_dist / tick_size) * tick_value
    lot = risk_usd / (sl_dist / ts * tv)
    step = info.volume_step or 0.01
    lot = max(info.volume_min, min(round(lot / step) * step, info.volume_max))
    return round(lot, 3)



# --- open_position ---
def open_position(symbol, direction, entry, sl, tp, risk_usd,
                  source="MT5", magic=20261013):
    """
    Позиция ашу (MT5) — thread-safe + dynamic filling mode.
    source: MT5 / TV_Bridge / Hedge
    magic: 20261013 (MT5) / 888388 (TV) / 777777 (Hedge)
    """
    with _state_lock:
        enabled = AUTO_STATE.get("enabled", False)
    if not enabled and source == "MT5":
        return {"ok": False, "reason": "Auto OFF"}

    info = mt5_symbol_info(symbol)
    if not info:
        return {"ok": False, "reason": "No symbol"}

    sl_dist = abs(entry - sl)
    lot = calc_lot(symbol, risk_usd, sl_dist)
    if lot < info.volume_min:
        return {"ok": False, "reason": f"Lot too small ({lot})"}

    tick = mt5_symbol_info_tick(symbol)
    if not tick:
        return {"ok": False, "reason": "No tick"}

    ot = mt5.ORDER_TYPE_BUY if direction == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if direction == "BUY" else tick.bid
    filling = get_filling_mode(info)

    t0 = time.time()
    req = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": ot,
        "price": price,
        "sl": round(sl, info.digits) if sl > 0 else 0.0,
        "tp": round(tp, info.digits) if tp > 0 else 0.0,
        "deviation": 20,
        "magic": magic,
        "comment": f"APEX v3 {source}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling,
    }

    try:
        r = mt5_order_send(req)
        latency = (time.time() - t0) * 1000

        with _state_lock:
            LATENCY_LOG.append(latency)
            if len(LATENCY_LOG) > 100:
                LATENCY_LOG.pop(0)

        if r is None:
            return {"ok": False, "reason": "No response"}
        if r.retcode != mt5.TRADE_RETCODE_DONE:
            return {"ok": False, "reason": f"Err {r.retcode}"}

        slippage = abs(r.price - price)

        with _state_lock:
            AUTO_STATE["daily_trades"] = AUTO_STATE.get("daily_trades", 0) + 1
            AUTO_STATE.setdefault("positions", []).append({
                "ticket": r.order,
                "symbol": symbol,
                "direction": direction,
                "lot": lot,
                "entry": r.price,
                "slippage": slippage,
                "source": source,
                "ts": time.time(),
            })
        auto_save()

        log.info(f"✅ Position: {symbol} {direction} lot={lot} | {source} fill={filling}")

        return {
            "ok": True,
            "ticket": r.order,
            "lot": lot,
            "price": r.price,
            "slippage": slippage,
            "latency": latency,
        }
    except Exception as e:
        log.error(f"Open position: {e}")
        return {"ok": False, "reason": str(e)[:80]}


# ============================================================
# CHART (mplfinance)
# ============================================================


