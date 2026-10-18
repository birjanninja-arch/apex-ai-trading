"""
EXECUTION — journal_db
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: db_init, journal_log, journal_stats, features_save, features_update_labels
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- db_init ---
def db_init():
    """Journal + Features DB жасау"""
    try:
        conn = sqlite3.connect(JOURNAL_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, symbol TEXT, direction TEXT,
            level INTEGER, phase TEXT, sequence TEXT,
            entry REAL, sl REAL, tp REAL, rr REAL, qty REAL,
            delta_pct REAL, vol_ratio REAL,
            adaptive REAL, effort_result TEXT, sd_state TEXT,
            elliott TEXT, gann TEXT, dow TEXT,
            ensemble REAL, auto_mode TEXT,
            fourier REAL, fractal REAL, mtf_score REAL, wavelet REAL,
            rl_score REAL,
            filters_passed TEXT, source TEXT,
            result TEXT DEFAULT 'PENDING', exit_price REAL)""")
        conn.commit(); conn.close()

        conn = sqlite3.connect(FEATURE_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER, symbol TEXT,
            vol_ratio REAL, delta_pct REAL, adaptive REAL, atr_pct REAL,
            mfi REAL, ad REAL, body_atr REAL, close_loc REAL,
            hour INTEGER, direction TEXT, entry REAL, sl REAL, tp REAL,
            fourier REAL, fractal REAL, mtf_score REAL, wavelet REAL,
            market_state TEXT, label INTEGER DEFAULT -1)""")
        conn.commit(); conn.close()

        # 🆕 Metrics DB
        conn = sqlite3.connect(METRICS_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER, symbol TEXT, direction TEXT,
            entry REAL, sl REAL, tp REAL, exit REAL,
            pnl REAL, result TEXT, source TEXT)""")
        conn.commit(); conn.close()

        log.info("✅ DB OK (Journal + Features + Metrics)")
    except Exception as e: log.error(f"DB: {e}")



# --- journal_log ---
def journal_log(symbol, direction, level, phase, sequence,
                entry, sl, tp, rr, qty, delta, vol_ratio,
                adaptive, er, sd, ell, gann, dow, ensemble, auto_mode,
                fourier=0, fractal=0, mtf_score=0, wavelet=0,
                filters_passed=None, source="MT5", rl_score=0.5):
    """Сигнал журналға жазу (thread-safe DB)"""
    try:
        with _db_lock:
            conn = sqlite3.connect(JOURNAL_DB, timeout=30)
            c = conn.cursor()
            filters_str = json.dumps(filters_passed or [])
            c.execute("""INSERT INTO signals
                (timestamp, symbol, direction, level, phase, sequence,
                 entry, sl, tp, rr, qty, delta_pct, vol_ratio,
                 adaptive, effort_result, sd_state,
                 elliott, gann, dow, ensemble, auto_mode,
                 fourier, fractal, mtf_score, wavelet, rl_score,
                 filters_passed, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (datetime.now().isoformat(), symbol, direction, level, phase, sequence,
                 entry, sl, tp, rr, qty, delta, vol_ratio,
                 adaptive, er, sd, ell, gann, dow, ensemble, auto_mode,
                 fourier, fractal, mtf_score, wavelet, rl_score,
                 filters_str, source))
            conn.commit()
            conn.close()
    except Exception as e:
        log.error(f"Log: {e}")



# --- journal_stats ---
def journal_stats():
    """Журнал статистикасы"""
    try:
        conn = sqlite3.connect(JOURNAL_DB)
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(result='TP'), SUM(result='SL') FROM signals")
        t, tp, sl = c.fetchone(); conn.close()
        return t or 0, tp or 0, sl or 0
    except Exception: return 0, 0, 0



# --- features_save ---
def features_save(symbol, fd):
    """Features сақтау (ML үшін) — 14 feature + thread-safe"""
    try:
        with _db_lock:
            conn = sqlite3.connect(FEATURE_DB, timeout=30)
            c = conn.cursor()
            c.execute("""INSERT INTO features
                (ts, symbol, vol_ratio, delta_pct, adaptive, atr_pct,
                 mfi, ad, body_atr, close_loc, hour,
                 direction, entry, sl, tp,
                 fourier, fractal, mtf_score, wavelet, market_state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (int(time.time()), symbol,
                 float(fd.get("vol_ratio", 0) or 0),
                 float(fd.get("delta_pct", 0) or 0),
                 float(fd.get("adaptive", 1.0) or 1.0),
                 float(fd.get("atr_pct", 0) or 0),
                 float(fd.get("mfi", 50) or 50),
                 float(fd.get("ad", 0) or 0),
                 float(fd.get("body_atr", 0) or 0),
                 float(fd.get("close_loc", 0.5) or 0.5),
                 int(fd.get("hour", 0) or 0),
                 str(fd.get("direction", "") or ""),
                 float(fd.get("entry", 0) or 0),
                 float(fd.get("sl", 0) or 0),
                 float(fd.get("tp", 0) or 0),
                 float(fd.get("fourier", 0.5) or 0.5),
                 float(fd.get("fractal", 1.5) or 1.5),
                 float(fd.get("mtf_score", 0.5) or 0.5),
                 float(fd.get("wavelet", 0) or 0),
                 str(fd.get("market_state", "UNKNOWN") or "UNKNOWN")))
            conn.commit()
            conn.close()
    except Exception as e:
        log.debug(f"features_save: {e}")



# --- features_update_labels ---
def features_update_labels():
    """Features label жаңарту (TP/SL анықтау)"""
    try:
        conn = sqlite3.connect(FEATURE_DB)
        c = conn.cursor()
        c.execute("SELECT id, symbol, direction, entry, sl, tp FROM features WHERE label = -1")
        rows = c.fetchall()
        for row in rows:
            fid, sym, d, entry, sl, tp = row
            tick = mt5_symbol_info_tick(sym)
            if not tick: continue
            price = tick.bid
            label = -1
            if d == "BUY":
                if price >= tp: label = 1
                elif price <= sl: label = 0
            else:
                if price <= tp: label = 1
                elif price >= sl: label = 0
            if label != -1:
                c.execute("UPDATE features SET label=? WHERE id=?", (label, fid))
        conn.commit(); conn.close()
    except Exception: pass


# ============================================================
# MARKET STATUS
# ============================================================


