"""
SIGNAL — wait_engine
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: calculate_wait_signal
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- calculate_wait_signal ---
def calculate_wait_signal(symbol, df, structure, phase, level, direction, reasons):
    """
    WAIT сигналы — тек CONFIRM (180%+) деңгейінде.
    """
    if not WAIT_ENABLED:
        return None

    if level < WAIT_LEVEL_MIN:
        return None
    if level >= LEVEL_SIGNAL:
        return None

    # Соңғы WAIT-тан 30 мин өткен бе?
    last_wait = MEM["wait_signals"].get(symbol, 0)
    if time.time() - last_wait < 1800: return None

    wait_reasons = []
    next_check = []

    # Volume
    last = df.iloc[-2]
    vm = df["vol_ma"].iloc[-2]
    if vm > 0:
        vr = last["tick_volume"] / vm
        if vr < VOL_PREPARE_BASE:
            wait_reasons.append(f"📊 Көлем {vr:.2f}× — 1.5× күтеміз")
            next_check.append("volume")

    # Delta
    delta = get_delta(symbol, 60)
    if abs(delta) < HFT_DELTA_MIN:
        wait_reasons.append(f"🐋 Delta {delta:+.1f}% — 25%+ күтеміз")
        next_check.append("delta")

    # 4H phase
    if phase and phase["phase"] not in ["accumulation", "markup", "distribution", "markdown"]:
        wait_reasons.append(f"🌍 4H phase: {phase['phase']}")
        next_check.append("phase")

    # Structure бұзылу
    if direction == "BUY":
        if last["low"] >= structure["support"]:
            wait_reasons.append(f"📈 Support {structure['support']:.2f} күтеміз")
            next_check.append("structure")
    elif direction == "SELL":
        if last["high"] <= structure["resistance"]:
            wait_reasons.append(f"📉 Resistance {structure['resistance']:.2f} күтеміз")
            next_check.append("structure")

    # Егер 2+ себеп болса — WAIT
    if len(wait_reasons) >= 2:
        MEM["wait_signals"][symbol] = time.time()
        mem_save()
        return {
            "action": "WAIT",
            "direction": direction,
            "level": level,
            "reasons": wait_reasons,
            "next_check": next_check,
            "ts": time.time(),
        }

    return None



