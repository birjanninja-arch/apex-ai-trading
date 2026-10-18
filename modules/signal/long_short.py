"""
SIGNAL — long_short
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: calculate_level, build_signal_object, format_signal_text, process_symbol
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- calculate_level ---
def calculate_level(df, structure, phase, delta, seq, adaptive):
    """
    5 деңгей есептеу:
    100 NORMAL → 120 PREPARE → 150 READY → 180 CONFIRM → 200 SIGNAL
    """
    if len(df) < 50 or not structure: return LEVEL_NORMAL, [], None
    last = df.iloc[-2]
    vm = df["vol_ma"].iloc[-2]
    if vm <= 0: return LEVEL_NORMAL, [], None
    vr = last["tick_volume"] / vm
    atr = last["atr"]
    if pd.isna(atr) or atr <= 0: return LEVEL_NORMAL, [], None
    rng = last["range"]
    if rng <= 0: return LEVEL_NORMAL, [], None
    ad = last["ad"]
    sup = structure["support"]; res = structure["resistance"]
    is_bull = last["close"] > last["open"]
    is_bear = last["close"] < last["open"]
    d = None
    if last["low"] < sup and last["close"] > sup: d = "BUY"
    elif last["high"] > res and last["close"] < res: d = "SELL"
    elif ad > 0 and is_bull: d = "BUY"
    elif ad < 0 and is_bear: d = "SELL"
    if d is None: return LEVEL_NORMAL, [], None

    dyn_p = VOL_PREPARE_BASE * adaptive
    dyn_r = VOL_READY_BASE * adaptive
    dyn_s = VOL_SIGNAL_BASE * adaptive

    reasons = []; lvl = LEVEL_NORMAL
    if vr >= dyn_p:
        lvl = LEVEL_PREPARE
        reasons.append(f"📊 Көлем {vr:.2f}× (≥{dyn_p:.2f})")
    if lvl >= LEVEL_PREPARE:
        broke = ((d == "BUY" and last["low"] < sup and last["close"] > sup) or
                 (d == "SELL" and last["high"] > res and last["close"] < res))
        if broke and vr >= dyn_r:
            lvl = LEVEL_READY
            reasons.append("📈 Structure")
        er, _ = calculate_effort_result(df)
        if er == "EFFORT_EQ_RESULT":
            lvl = LEVEL_READY
            reasons.append("⚖️ Effort=Result")
    if lvl >= LEVEL_READY and phase:
        ph = phase["phase"]
        if (d == "BUY" and ph in ["accumulation", "markup"]) or \
           (d == "SELL" and ph in ["distribution", "markdown"]):
            lvl = LEVEL_CONFIRM
            reasons.append(f"🌍 4H {ph}")
        sd, _ = analyze_supply_demand(df)
        if (d == "BUY" and sd == "DEMAND_WINS") or (d == "SELL" and sd == "SUPPLY_WINS"):
            lvl = LEVEL_CONFIRM
            reasons.append(f"📊 {sd}")
        if seq and seq.get("next_expected") in ["sos", "lps", "hft"]:
            lvl = LEVEL_CONFIRM
            reasons.append("🔗 Seq")
    if lvl >= LEVEL_CONFIRM:
        if abs(delta) >= HFT_DELTA_MIN:
            dd = "BUY" if delta > 0 else "SELL"
            if dd == d:
                lvl = LEVEL_SIGNAL
                reasons.append(f"🐋 Delta {delta:+.1f}%")
        if vr >= dyn_s:
            lvl = LEVEL_SIGNAL
            reasons.append(f"🔥 Көлем {vr:.2f}× (≥{dyn_s:.2f})")
    return lvl, reasons, d


# ============================================================
# 🆕 WAIT ENGINE (LONG / SHORT / WAIT)
# ============================================================


# --- build_signal_object ---
def build_signal_object(symbol, direction, level, plan, phase, seq,
                        reasons, ensemble, ens_breakdown, mstate,
                        fourier_val, fractal_val, mtf_score, wavelet_val,
                        er, sd, ell_str, gann_str, dow_str, delta, vr_now,
                        filters_passed, source="MT5"):
    """
    🆕 Signal объектісін жасау (LONG/SHORT/WAIT)
    Қайтарады: dict
    """
    try:
        # Action анықтау
        if level >= LEVEL_SIGNAL and direction:
            action = "LONG" if direction == "BUY" else "SHORT"
        elif level >= LEVEL_PREPARE and direction:
            action = "WAIT"
        else:
            action = "NONE"

        # Сенімділік (confidence)
        confidence = ensemble

        # Себептері
        all_reasons = list(reasons)
        if er and er != "NORMAL":
            all_reasons.append(f"⚖️ {er}")
        if sd and sd != "BALANCED":
            all_reasons.append(f"📊 {sd}")
        if ell_str and ell_str != "—":
            all_reasons.append(f"🌊 {ell_str}")
        if gann_str and gann_str != "—":
            all_reasons.append(f"📐 Gann {gann_str}")
        if dow_str and dow_str != "—":
            all_reasons.append(f"📊 {dow_str}")

        return {
            "symbol": symbol,
            "action": action,
            "direction": direction,
            "level": level,
            "confidence": round(confidence, 3),
            "entry": plan.get("entry") if plan else 0,
            "sl": plan.get("sl") if plan else 0,
            "tp": plan.get("tp") if plan else 0,
            "rr": plan.get("rr") if plan else 0,
            "risk_usd": plan.get("risk_usd") if plan else 0,
            "qty": plan.get("risk_usd") if plan else 0,  # legacy field; real lot in open_position
            "phase": phase["phase"] if phase else "?",
            "sequence": seq["phase"] if seq else "—",
            "state": mstate,
            "delta": delta,
            "vol_ratio": vr_now,
            "fourier": fourier_val,
            "fractal": fractal_val,
            "mtf": mtf_score,
            "wavelet": wavelet_val,
            "rl": ens_breakdown.get("rl", 0.5),
            "ml": ens_breakdown.get("ml", 0.5),
            "ensemble": ensemble,
            "filters_passed": filters_passed,
            "reasons": all_reasons,
            "source": source,
            "ts": time.time(),
        }
    except Exception as e:
        log.error(f"Build signal: {e}")
        return None



# --- format_signal_text ---
def format_signal_text(sig, auto_result=None, mode="MANUAL"):
    """
    Signal объектісін Telegram мәтініне айналдыру
    """
    try:
        action = sig.get("action", "NONE")
        if action == "LONG":
            emoji = "🟢🟢🟢"
            title = "СИГНАЛ — BUY"
        elif action == "SHORT":
            emoji = "🔴🔴🔴"
            title = "СИГНАЛ — SELL"
        elif action == "WAIT":
            emoji = "🟡"
            title = "WAIT"
        else:
            emoji = "⚪"
            title = "NONE"

        symbol = sig.get("symbol", "?")
        level = sig.get("level", 0)
        confidence = sig.get("confidence", 0)
        reasons = sig.get("reasons", [])
        filters = sig.get("filters_passed", [])

        # Filters строку
        filters_str = ", ".join(filters) if filters else "—"

        # Auto
        auto_str = ""
        if action in ["LONG", "SHORT"]:
            if auto_result and auto_result.get("ok"):
                auto_str = (f"\n\n🤖 *AUTO:* ✅ Lot `{auto_result['lot']}` "
                            f"Ticket `{auto_result['ticket']}` "
                            f"Slip `{auto_result.get('slippage', 0):.5f}` "
                            f"Lat `{auto_result.get('latency', 0):.0f}ms`")
            elif mode != "MANUAL":
                auto_str = f"\n\n🤖 *AUTO:* ❌ {auto_result.get('reason', '?') if auto_result else 'OFF'}"
            else:
                auto_str = f"\n\n🤖 *AUTO:* 🖐 MANUAL"

        # Signal text
        if action in ["LONG", "SHORT"]:
            text = (
                f"{emoji} *{title}*\n\n"
                f"📌 {symbol} | M15\n"
                f"📊 Деңгей: {level}%\n"
                f"🌍 4H: {sig.get('phase', '?')}\n"
                f"🐋 Delta: {sig.get('delta', 0):+.1f}%\n"
                f"⚖️ {sig.get('reasons', [''])[0] if reasons else '—'}\n"
                f"🔬 Adv: F={sig.get('fourier', 0):.2f} | "
                f"Fr={sig.get('fractal', 0):.2f} | "
                f"MTF={sig.get('mtf', 0):.2f} | "
                f"W={sig.get('wavelet', 0):+.1f}\n"
                f"🧠 ML: {sig.get('ml', 0.5):.2f}\n"
                f"🤖 RL: {sig.get('rl', 0.5):.2f}\n"
                f"🎯 Ensemble: *{confidence:.2f}*\n"
                f"🔍 Filters: `{filters_str}`\n\n"
                f"💵 Entry: `{sig.get('entry', 0)}`\n"
                f"🛑 SL: `{sig.get('sl', 0)}`\n"
                f"🎯 TP: `{sig.get('tp', 0)}`\n"
                f"📊 R:R = {sig.get('rr', 0)}:1\n"
                f"💰 Risk: ${sig.get('risk_usd', 0)}\n\n"
                + "\n".join(f"  • {r}" for r in reasons)
                + auto_str
            )
        elif action == "WAIT":
            text = (
                f"{emoji} *WAIT — {symbol}*\n\n"
                f"📊 Деңгей: {level}%\n"
                f"🌍 4H: {sig.get('phase', '?')}\n"
                f"🧭 Бағыт: *{sig.get('direction', '?')}*\n\n"
                f"⏳ Күтеміз:\n"
                + "\n".join(f"  • {r}" for r in reasons)
            )
        else:
            text = f"{emoji} *{symbol}* — сигнал жоқ"

        return text
    except Exception as e:
        log.error(f"Format signal: {e}")
        return f"⚠️ Signal format error: {e}"


# ============================================================
# RISK MANAGER
# ============================================================


# --- process_symbol ---
def process_symbol(symbol):
    """
    Бір символды толық талдау:
    1. Деректер + индикаторлар
    2. Structure + Phase
    3. Delta + Adaptive
    4. Sequence
    5. 🆕 Wyckoff v2 (10+ шарт)
    6. Level (5 деңгей)
    7. WAIT / SIGNAL
    8. AI Confirm
    9. Filters chain
    10. Trade plan
    11. Advanced features
    12. Ensemble (Rules+ML+Adv+RL)
    13. Auto Trader
    14. Voice
    15. Chart + Journal + Telegram
    """
    try:
        # ==========================================
        # 1. ДЕРЕКТЕР + ИНДИКАТОРЛАР (look-ahead bias жоқ)
        # ==========================================
        rates = mt5_copy_rates(symbol, TIMEFRAME, 0, 120)
        if rates is None or len(rates) < 60:
            return
        df = pd.DataFrame(rates)
        # Drop currently forming candle (repaint / incomplete bar)
        if len(df) > 1:
            df = df.iloc[:-1].copy()
        if len(df) < 50:
            return

        df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=ATR_PERIOD)
        # volume_ma shifted so current bar is NOT in its own baseline
        df["vol_ma"] = (
            df["tick_volume"].rolling(VOL_MA_WINDOW, min_periods=VOL_MA_WINDOW).mean().shift(1)
        )
        df["range"] = df["high"] - df["low"]
        df["body"] = (df["close"] - df["open"]).abs()
        df["close_loc"] = (df["close"] - df["low"]) / df["range"].replace(0, 1)
        mfi = ta.mfi(df["high"], df["low"], df["close"], df["tick_volume"], length=14)
        df["mfi"] = mfi if mfi is not None else 50.0
        rng = (df["high"] - df["low"]).replace(0, 1)
        df["ad"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng

        # ==========================================
        # 2. STRUCTURE + PHASE
        # ==========================================
        structure = analyze_structure(df)
        if not structure:
            return
        phase = analyze_4h_phase(symbol)
        if not phase:
            return
        with _state_lock:
            MEM["phases"][symbol] = phase
        mem_save()

        # ==========================================
        # 3. DELTA + ADAPTIVE
        # ==========================================
        delta = get_delta(symbol, 60)
        seq = get_sequence(symbol)
        adaptive, atr_pct = get_adaptive(df, symbol)

        # ==========================================
        # 4. SEQUENCE
        # (df already excludes forming candle → last closed = iloc[-1])
        # ==========================================
        if seq is None:
            last = df.iloc[-1]
            vm = df["vol_ma"].iloc[-1]
            if vm is not None and not pd.isna(vm) and float(vm) > 0:
                vr = float(last["tick_volume"]) / float(vm)
                sup = structure["support"]; res = structure["resistance"]
                dyn_p = VOL_PREPARE_BASE * adaptive

                # Spring/Shakeout (Wyckoff v2 — 12 шарт)
                if last["low"] < sup and last["close"] > sup and vr >= dyn_p:
                    event = "shakeout" if vr >= dyn_p * 1.5 else "spring"
                    init_sequence(symbol, event, "BUY", float(last["close"]),
                                  sup, res, float(last["atr"]), vr)
                    tg_send(f"📋 *{symbol} — {event.upper()}*\n"
                            f"🌍 4H: {phase['phase']}\n"
                            f"📊 Көлем: {vr:.2f}×\n🔗 ST күтеміз")
                    log.info(f"SEQ: {symbol} — {event} (BUY)")
                    return

                # UTAD/UT
                if last["high"] > res and last["close"] < res and vr >= dyn_p:
                    event = "utad" if vr >= dyn_p * 1.2 else "ut"
                    init_sequence(symbol, event, "SELL", float(last["close"]),
                                  sup, res, float(last["atr"]), vr)
                    tg_send(f"📋 *{symbol} — {event.upper()}*\n🔗 ST күтеміз")
                    log.info(f"SEQ: {symbol} — {event} (SELL)")
                    return
        else:
            evt = check_sequence_events(symbol, df, structure)
            if evt:
                tg_send(f"🔗 *{symbol} — {evt['event'].upper()}*\n"
                        f"Seq: {seq['phase']} → {evt['event']}")
                log.info(f"SEQ: {symbol} — {evt['event']}")
                return

        # ==========================================
        # 5. LEVEL (5 деңгей)
        # ==========================================
        level, reasons, direction = calculate_level(
            df, structure, phase, delta, seq, adaptive)
        prev = MEM["levels"].get(symbol, {}).get("level", 0)
        MEM["levels"][symbol] = {
            "level": level, "direction": direction,
            "reasons": reasons, "created_at": time.time()
        }
        mem_save()

        # ==========================================
        # 6. WAIT / CONFIRM (120% PREPARE Telegram-ға жіберілмейді)
        # Тек LEVEL_CONFIRM (180%+) → WAIT хабарлама
        # ==========================================
        if level >= LEVEL_CONFIRM and level < LEVEL_SIGNAL and direction:
            # CONFIRM хабарлама (бұрынғы PREPARE спам орнына)
            if prev < LEVEL_CONFIRM:
                tg_send(
                    f"📋 *{symbol} — CONFIRM ({level}%)*\n"
                    f"🌍 4H: {phase['phase']}\n"
                    f"🐋 Delta: {delta:+.1f}%\n"
                    f"📐 Adaptive: {adaptive:.2f}\n"
                    f"🧭 {direction}\n"
                    + "\n".join(f"  • {r}" for r in reasons)
                )
                log.info(f"CONFIRM: {symbol} — {level}% ({direction})")

            wait_data = calculate_wait_signal(
                symbol, df, structure, phase, level, direction, reasons)
            if wait_data:
                send_wait_signal(symbol, wait_data, phase)

                if VOICE_ON_SIGNAL and VOICE_ENABLED:
                    voice_text = voice_wait_message(
                        symbol, direction, level, wait_data.get("reasons", []))
                    tg_send_voice(voice_text)
            return

        # ==========================================
        # 7. SIGNAL (200%) — барлық тексеру
        # ==========================================
        if level >= LEVEL_SIGNAL and direction:
            # Duplicate detection
            last_sent = MEM["sent_signals"].get(symbol, 0)
            if time.time() - last_sent < DUPLICATE_WINDOW_SEC:
                log.info(f"⏭️ Duplicate skip: {symbol}")
                return

            # ==========================================
            # 8. AI CONFIRM (Elliott + Gann + Dow)
            # ==========================================
            filters_passed = []
            ai_s, ai_reasons = ai_confirm(df, direction)
            if ai_s < AI_CONFIRM_MIN:
                log.info(f"AI reject {symbol} ({ai_s}/7)")
                return
            reasons.extend(ai_reasons)
            filters_passed.append("ai")

            # ==========================================
            # 8b. WYCKOFF ENGINE CONFIRM (sequence-based)
            # Standalone engine: SPRING→TEST/SOS/LPS or UT→SOW/LPSY
            # ==========================================
            if WYCKOFF_ENGINE_OK and is_filter_enabled("wyckoff_engine"):
                try:
                    we_cfg = WyckoffConfig(
                        lookback=40,
                        drop_forming_candle=False,  # already dropped above
                        min_bars=50,
                        target_r_multiple=max(RISK_REWARD_MIN, 2.0),
                        min_r_multiple=RISK_REWARD_MIN,
                    )
                    we = analyze_wyckoff(df, we_cfg)
                    we_sig = we.get("signal", "WAIT")
                    want = "LONG" if direction == "BUY" else "SHORT"
                    if we_sig == "WAIT":
                        log.info(f"WyckoffEngine WAIT {symbol}: {we.get('reasons', [])[:1]}")
                        return
                    if we_sig != want:
                        log.info(f"WyckoffEngine reject {symbol}: engine={we_sig} want={want}")
                        return
                    # Optional: tighten SL/TP from engine risk_plan if R:R better
                    rp = we.get("risk_plan")
                    if rp:
                        reasons.append(
                            f"📐 WE {we_sig} R:R={rp.get('reward_risk', 0):.2f}"
                        )
                    filters_passed.append("wyckoff_engine")
                except Exception as e:
                    log.warning(f"WyckoffEngine error {symbol}: {e}")
                    # Soft-fail: do not block signal if engine crashes

            # ==========================================
            # 9. FILTER CHAIN (12 фильтр)
            # ==========================================
            # News PAUSE
            if is_filter_enabled("news"):
                news_ok, news_r = check_mt5_calendar(2)
                if not news_ok:
                    log.info(f"News PAUSE {symbol}")
                    return
                news_s = get_news_sentiment()
                if news_s < -0.3 and direction == "BUY": return
                if news_s > 0.3 and direction == "SELL": return
                filters_passed.append("news")

            # Fear & Greed
            if is_filter_enabled("fg"):
                fg_dir = get_fear_greed_dir()
                if fg_dir and fg_dir != direction:
                    log.info(f"FG reject {symbol}")
                    return
                filters_passed.append("fg")

            # FRED Macro
            if is_filter_enabled("fred"):
                macro_dir, macro_r = macro_direction()
                if macro_dir and macro_dir != direction:
                    log.info(f"Macro reject {symbol}")
                    return
                if macro_r: reasons.append(macro_r)
                filters_passed.append("fred")

            # Santiment
            if is_filter_enabled("santiment"):
                san = get_santiment()
                if san:
                    btc_social = san.get("BTC_social", 0)
                    if btc_social > 50000:
                        reasons.append(f"🔗 BTC social {int(btc_social)}")
                filters_passed.append("santiment")

            # Reddit
            if is_filter_enabled("reddit"):
                reddit_s = get_reddit_sentiment()
                if reddit_s < -0.3 and direction == "BUY": return
                if reddit_s > 0.3 and direction == "SELL": return
                if reddit_s != 0: reasons.append(f"💬 Reddit {reddit_s:+.2f}")
                filters_passed.append("reddit")

            # Correlation
            if is_filter_enabled("corr"):
                corr_ok, corr_r = check_correlation(symbol)
                if not corr_ok:
                    log.info(f"Corr reject {symbol}")
                    return
                filters_passed.append("corr")

            # Divergence (tick CVD preferred)
            if is_filter_enabled("div"):
                div = detect_divergence(df, symbol=symbol)
                if div and div["direction"] != direction:
                    log.info(f"Div reject {symbol}: {div.get('type')}")
                    return
                if div:
                    reasons.append(f"📊 {div['type']}")
                filters_passed.append("div")

            # Order Flow: Delta + Footprint + VP + Absorption + CVD
            if is_filter_enabled("hft"):
                of_ok, of_reasons, of_metrics = order_flow_signal(symbol, direction)
                if not of_ok:
                    log.info(f"OF reject {symbol}: {of_reasons[:2]}")
                    return
                reasons.extend(of_reasons[:4])
                if of_metrics.get("poc") is not None:
                    reasons.append(f"POC {of_metrics['poc']}")
                spoofing = detect_spoofing(symbol)
                if spoofing:
                    log.info(f"Spoof reject {symbol}")
                    return
                filters_passed.append("hft")
                filters_passed.append("orderflow")

            # ==========================================
            # 10. TRADE PLAN (R:R check)
            # df excludes forming candle → last closed = iloc[-1]
            # ==========================================
            last = df.iloc[-1]
            entry = float(last["close"])
            # S/R for stop from prior bars only (exclude signal bar)
            lb = df.iloc[-(CANDLES_LOOKBACK + 1):-1] if len(df) > CANDLES_LOOKBACK else df.iloc[:-1]
            l_ev = float(lb["low"].min())
            h_ev = float(lb["high"].max())
            atr_v = float(last["atr"]) if not pd.isna(last["atr"]) else 0.0
            if atr_v <= 0:
                log.info(f"ATR reject {symbol}")
                return

            plan = build_trade_plan(
                direction, entry, atr_v,
                structure["support"], structure["resistance"],
                l_ev, h_ev, seq["phase"] if seq else "spring")
            if not plan:
                log.info(f"R:R reject {symbol}")
                return
            if not validate_risk():
                log.info(f"Risk reject {symbol}")
                return
            filters_passed.append("rr")
            filters_passed.append("level")

            # ==========================================
            # 11. ADVANCED FEATURES (14 features)
            # ==========================================
            er, _ = calculate_effort_result(df)
            sd, _ = analyze_supply_demand(df)
            ell = detect_elliott(df); ell_str = ell["wave"] if ell else "—"
            gann = detect_gann(df); gann_str = gann["level"] if gann else "—"
            dow = detect_dow(df); dow_str = dow["name"] if dow else "—"
            hour = datetime.now(timezone.utc).hour

            _vm = df["vol_ma"].iloc[-1]
            vr_now = float(last["tick_volume"]) / float(_vm) if (_vm is not None and not pd.isna(_vm) and float(_vm) > 0) else 1.0

            prices = df["close"].tail(100).values

            # Fourier
            f_res = fourier_analysis(prices)
            fourier_val = f_res["cycle_strength"] if f_res else 0.5

            # Fractal
            fd = fractal_dimension(prices)
            fractal_val = fd if fd else 1.5
            mstate = market_state_by_fractal(fd)

            # MTF
            mtf = multi_timeframe_analysis(symbol)
            mtf_score = mtf["score"] if mtf else 0.5

            # Wavelet
            wt = wavelet_trend(prices)
            wavelet_val = 1.0 if wt == "UP" else (-1.0 if wt == "DOWN" else 0.0)

            # 14 features
            features = [
                vr_now, abs(delta), adaptive, atr_pct,
                float(last["mfi"]), float(last["ad"]),
                float(last["body"]) / atr_v if atr_v > 0 else 0,
                float(last["close_loc"]), hour,
                fourier_val, fractal_val, mtf_score, wavelet_val,
                {"STRONG_TREND": 1.0, "TREND": 0.5, "WEAK_TREND": 0.0,
                 "RANGE": -0.5, "UNKNOWN": 0.0}.get(mstate, 0.0)
            ]

            # ==========================================
            # 12. ENSEMBLE (Rules + ML + Adv + RL + Shazam v4)
            # ==========================================
            shazam_result = None
            if SHAZAM_ENABLED and SHAZAM_STATUS.get("ready"):
                try:
                    if _SHAZAM_MOD is not None:
                        shazam_result = _SHAZAM_MOD.shazam_predict_symbol(symbol)
                except Exception as _se:
                    log.debug(f"Shazam predict {symbol}: {_se}")

            ensemble, ens_breakdown = ensemble_predict(
                level, delta, er, sd, adaptive, features, shazam_result=shazam_result)

            # Shazam қатты қайшы: combined SELL vs direction BUY (немесе керісінше)
            if shazam_result and shazam_result.get("combined_signal") in ("BUY", "SELL"):
                sh_sig = shazam_result["combined_signal"]
                want = "BUY" if direction == "BUY" else "SELL"
                if sh_sig != want and float(shazam_result.get("combined_score", 0)) >= SHAZAM_MIN_CONF:
                    log.info(f"Shazam conflict {symbol}: sh={sh_sig} want={want} → skip")
                    return
                reasons.append(
                    f"🎵 Shazam {sh_sig} "
                    f"{float(shazam_result.get('combined_score', 0))*100:.0f}% "
                    f"k={shazam_result.get('shazam', {}).get('k', 0)}"
                )

            # Features сақтау (ML үшін)
            features_save(symbol, {
                "vol_ratio": vr_now, "delta_pct": delta,
                "adaptive": adaptive, "atr_pct": atr_pct,
                "mfi": float(last["mfi"]), "ad": float(last["ad"]),
                "body_atr": float(last["body"]) / atr_v if atr_v > 0 else 0,
                "close_loc": float(last["close_loc"]), "hour": hour,
                "direction": direction, "entry": plan["entry"],
                "sl": plan["sl"], "tp": plan["tp"],
                "fourier": fourier_val, "fractal": fractal_val,
                "mtf_score": mtf_score, "wavelet": wavelet_val,
                "market_state": mstate})

            # ==========================================
            # 13. AUTO TRADER
            # ==========================================
            auto_ok, auto_r = can_trade()
            auto_result = None
            if auto_ok:
                auto_result = open_position(
                    symbol, direction,
                    plan["entry"], plan["sl"], plan["tp"],
                    plan["risk_usd"], source="MT5", magic=20261013)

            # ==========================================
            # 14. SIGNAL ОБЪЕКТІСІ
            # ==========================================
            sig = build_signal_object(
                symbol, direction, level, plan, phase, seq, reasons,
                ensemble, ens_breakdown, mstate,
                fourier_val, fractal_val, mtf_score, wavelet_val,
                er, sd, ell_str, gann_str, dow_str, delta, vr_now,
                filters_passed, "MT5")

            # ==========================================
            # 15. SIGNAL МӘТІНІ
            # ==========================================
            signal_text = format_signal_text(sig, auto_result, get_mode())

            # ==========================================
            # 16. CHART + TELEGRAM
            # ==========================================
            chart_data = {
                "support": structure["support"],
                "resistance": structure["resistance"],
                "entry": plan["entry"], "sl": plan["sl"], "tp": plan["tp"],
                "rr": plan["rr"],
                "event": seq["phase"] if seq else "—",
                "phase": phase["phase"],
                "signal": direction,
                "adaptive": adaptive,
                "delta_pct": delta,
                "fourier": fourier_val,
                "fractal": fractal_val,
                "mtf": mtf_score,
                "wavelet": wavelet_val,
                "rl": ens_breakdown.get("rl", 0.5),
                "ensemble": ensemble,
            }
            chart_buf = build_chart(symbol, chart_data)

            if chart_buf:
                tg_photo(chart_buf, signal_text)
            else:
                tg_send(signal_text)

            # ==========================================
            # 17. VOICE (қазақша)
            # ==========================================
            if VOICE_ON_SIGNAL and VOICE_ENABLED:
                voice_text = voice_signal_message(
                    symbol, direction, level,
                    plan['entry'], plan['sl'], plan['tp'], ensemble)
                tg_send_voice(voice_text)

            # ==========================================
            # 18. БАТЫРМАЛАР
            # ==========================================
            tg_buttons(
                f"⚡ *{symbol}* — {direction}\n_Батырманы басыңыз:_",
                signal_buttons(symbol, direction)
            )

            # ==========================================
            # 19. ЖУРНАЛ
            # ==========================================
            journal_log(
                symbol, direction, level, phase["phase"],
                seq["phase"] if seq else "—",
                plan["entry"], plan["sl"], plan["tp"],
                plan["rr"], plan.get("risk_usd", 0), delta, vr_now,
                adaptive, er, sd, ell_str, gann_str, dow_str,
                ensemble, get_mode(),
                fourier_val, fractal_val, mtf_score, wavelet_val,
                filters_passed, "MT5", ens_breakdown.get("rl", 0.5))

            register_signal(symbol)
            with _state_lock:
                MEM["sent_signals"][symbol] = time.time()
                _stats["signals"] = _stats.get("signals", 0) + 1
                _stats["daily_trades"] = _stats.get("daily_trades", 0) + 1
            mem_save()

            log.info(f"✅ SIGNAL: {symbol} ({direction}) "
                     f"L={level}% ens={ensemble:.2f}")

            # Sequence тазалау
            if seq:
                del MEM["sequences"][symbol]
                mem_save()

    except Exception as e:
        _stats["errors"] += 1
        log.error(f"Err {symbol}: {e}")


# ============================================================
# TRAILING WORKER
# ============================================================


