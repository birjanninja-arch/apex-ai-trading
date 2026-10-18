"""
ML_AI — llm_groq
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: llm_ask, llm_analyze_filters, llm_program_strategy, llm_self_reflection, llm_brain_worker, start_llm_brain, start_strategy_programmer
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- llm_ask ---
def llm_ask(prompt, max_tokens=2000):
    """
    LLM сұрақ (JSON жауап).
    Primary: xAI Grok  |  Fallback: Groq
    """
    if not LLM_AVAILABLE or llm_client is None:
        return None
    model = LLM_MODEL
    if LLM_BACKEND == "groq" and (not model or not str(model).strip()):
        model = "openai/gpt-oss-20b"
    try:
        kwargs = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are APEX trading assistant. "
                        "Always reply with valid JSON only, no markdown."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "model": model,
            "temperature": 0.3,
            "max_tokens": max_tokens,
        }
        # response_format supported by both xAI and Groq for JSON mode
        try:
            response = llm_client.chat.completions.create(
                **kwargs, response_format={"type": "json_object"}
            )
        except Exception:
            response = llm_client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content
        if not content:
            return None
        content = content.strip()
        # Strip accidental markdown fences
        if content.startswith("```"):
            content = content.split("\n", 1)[-1]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
        return json.loads(content)
    except Exception as e:
        log.error(f"LLM ask ({LLM_BACKEND}): {str(e)[:150]}")
        return None



# --- llm_analyze_filters ---
def llm_analyze_filters(days=30):
    """
    LLM фильтрлерді талдайды:
    1. 30 күндік сигналдар
    2. Әр фильтр статистика
    3. Қай өшіру
    """
    if not LLM_ENABLED: return None
    try:
        since = time.time() - days * 86400
        conn = sqlite3.connect(JOURNAL_DB)
        c = conn.cursor()
        c.execute("""SELECT filters_passed, result FROM signals
                     WHERE timestamp > datetime(?, 'unixepoch')""",
                  (since,))
        rows = c.fetchall()
        conn.close()

        if len(rows) < LLM_MIN_SIGNALS:
            log.info(f"⏳ LLM: сигнал аз ({len(rows)}/{LLM_MIN_SIGNALS})")
            return None

        filter_names = ["ai", "news", "fg", "fred", "santiment",
                        "reddit", "corr", "div", "hft", "spoof", "rr", "level"]
        stats = {f: {"passed": 0, "tp": 0, "sl": 0, "win": 0.0} for f in filter_names}

        for fp_str, result in rows:
            try:
                passed = json.loads(fp_str) if fp_str else []
            except Exception:
                passed = []
            for f in passed:
                if f in stats:
                    stats[f]["passed"] += 1
                    if result == "TP": stats[f]["tp"] += 1
                    elif result == "SL": stats[f]["sl"] += 1

        for f in stats:
            s = stats[f]
            total = s["tp"] + s["sl"]
            s["win"] = round(s["tp"] / total, 3) if total > 0 else 0.0

        prompt = f"""Сен — APEX v3 ботының орталық интеллектісі.


# --- llm_brain_worker ---
def llm_brain_worker():
    """LLM талдау циклі (6 сағат)"""
    time.sleep(1800)
    while True:
        try:
            log.info("🧠 LLM Brain — талдау басталды...")
            decision = llm_analyze_filters(days=30)
            if decision:
                apply_filter_decision(decision)
                disable_list = decision.get("disable", [])
                keep_list = decision.get("keep", [])
                tg_send(
                    f"🧠 *LLM Brain талдау*\n\n"
                    f"🚫 Өшірілді: `{', '.join(disable_list) or '—'}`\n"
                    f"✅ Сақталды: `{', '.join(keep_list) or '—'}`\n\n"
                    f"📝 _{decision.get('reason', '')[:200]}_"
                )
            LLM_LAST_RUN[0] = time.time()
            time.sleep(LLM_INTERVAL_HOURS * 3600)
        except Exception as e:
            log.error(f"LLM worker: {e}")
            time.sleep(3600)



# --- start_llm_brain ---
def start_llm_brain():
    """LLM Brain іске қосу"""
    if not LLM_ENABLED:
        log.info("⏸ LLM өшірулі")
        return
    if not GROQ_AVAILABLE:
        log.warning("⚠️ Groq API кілт жоқ — LLM өшірулі")
        return
    threading.Thread(target=llm_brain_worker, daemon=True).start()
    log.info("✅ LLM Brain іске қосылды")


# ============================================================
# STRATEGY PROGRAMMER (Жаңа стратегия ұсыну)
# ============================================================


# --- llm_program_strategy ---
def llm_program_strategy():
    """LLM жаңа стратегия ұсынады"""
    if not LLM_ENABLED or not GROQ_AVAILABLE: return None
    try:
        conn = sqlite3.connect(JOURNAL_DB)
        c = conn.cursor()
        c.execute("""SELECT symbol, direction, result, fourier, fractal,
                            mtf_score, wavelet, delta_pct, vol_ratio
                     FROM signals WHERE result != 'PENDING'
                     ORDER BY timestamp DESC LIMIT 500""")
        rows = c.fetchall()
        conn.close()

        if len(rows) < 100: return None

        data = {
            "total": len(rows),
            "tp": sum(1 for r in rows if r[2] == "TP"),
            "sl": sum(1 for r in rows if r[2] == "SL"),
        }
        data["win_rate"] = round(data["tp"] / (data["tp"] + data["sl"]), 3) \
            if (data["tp"] + data["sl"]) > 0 else 0

        prompt = f"""Сен — трейдинг стратегінің әзірлеушісі.


# --- start_strategy_programmer ---
def start_strategy_programmer():
    """Strategy Programmer іске қосу"""
    if not LLM_ENABLED or not GROQ_AVAILABLE:
        return
    threading.Thread(target=llm_strategy_worker, daemon=True).start()
    log.info("✅ Strategy Programmer іске қосылды")


# ============================================================
# AUTO-LEARN (Self-Reflection — қателерден үйрену)
# ============================================================


# --- llm_self_reflection ---
def llm_self_reflection():
    """SL болған сигналдарды талдау"""
    if not LLM_ENABLED or not GROQ_AVAILABLE: return None
    try:
        conn = sqlite3.connect(JOURNAL_DB)
        c = conn.cursor()
        c.execute("""SELECT symbol, direction, delta_pct, vol_ratio,
                            fourier, fractal, mtf_score, wavelet, result
                     FROM signals WHERE result = 'SL'
                     ORDER BY timestamp DESC LIMIT 50""")
        rows = c.fetchall()
        conn.close()

        if len(rows) < 20: return None

        errors = []
        for r in rows:
            errors.append({
                "sym": r[0], "dir": r[1], "delta": round(r[2], 1),
                "vol": round(r[3], 2), "fourier": round(r[4], 2),
                "fractal": round(r[5], 2), "mtf": round(r[6], 2),
                "wavelet": round(r[7], 1),
            })

        prompt = f"""Сен — APEX v3 ботының өзін-өзі талдаушысы.


