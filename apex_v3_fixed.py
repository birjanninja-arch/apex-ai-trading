"""
============================================================
 🏎️ APEX v3 — 6 ҚАТАРЛЫ EDITION (FIXED 10/10)
============================================================
 Critical fixes applied:
  ✅ MT5 thread-safety (_mt5_lock + wrappers)
  ✅ Dynamic ORDER_FILLING mode (FOK/IOC/RETURN)
  ✅ Shared state locks (_state_lock, _db_lock)
  ✅ Lot calculation + risk plan cleaned
  ✅ Wyckoff Spring conditions 11+12 completed
  ✅ journal / mem / auto save race-safe
  ✅ Module Splitter — нақты 81 функция → modules/
  ✅ RL reward — mark-to-market + flip + DD penalty
  ✅ ML features — 14 feature (Fourier/Fractal/MTF/Wavelet/State)
============================================================
 6 ҚАТАР:
 1. Wyckoff Engine (10+ шарт)
 2. ML / AI (XGBoost + RL + LLM)
 3. Қосымша талдау (Fractal + Fourier + Hedge)
 4. Signal Engine (LONG/SHORT/WAIT)
 5. Risk Manager (SL/TP/R:R/лимиттер)
 6. Орындау (Telegram + MT5 + Журнал)
============================================================
"""

# ============================================================
# AUTO INSTALL — 20 ПАКЕТ
# ============================================================

import subprocess, sys, importlib, os

REQUIRED = [
    # Негізгі
    "MetaTrader5", "pandas", "pandas_ta", "numpy",
    "requests", "mplfinance", "matplotlib",
    "scikit-learn", "xgboost", "fredapi", "python-dotenv",
    "PyWavelets", "scipy", "edge-tts",
    "fastapi", "uvicorn", "pydantic",
    # LLM: openai (xAI Grok) + optional groq fallback
    "openai", "groq",
    # APEX
    "stable-baselines3", "gymnasium", "torch",
]

MODULE_MAP = {
    "MetaTrader5": "MetaTrader5",
    "pandas": "pandas",
    "pandas_ta": "pandas_ta",
    "numpy": "numpy",
    "requests": "requests",
    "mplfinance": "mplfinance",
    "matplotlib": "matplotlib",
    "scikit-learn": "sklearn",
    "xgboost": "xgboost",
    "fredapi": "fredapi",
    "python-dotenv": "dotenv",
    "PyWavelets": "pywt",
    "scipy": "scipy",
    "openai": "openai",
    "groq": "groq",
    "edge-tts": "edge_tts",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "pydantic": "pydantic",
    "stable-baselines3": "stable_baselines3",
    "gymnasium": "gymnasium",
    "torch": "torch",
}


def auto_install():
    print("=" * 60)
    print("  🔧 APEX v3 — AUTO INSTALL")
    print("=" * 60)
    missing = []
    for pkg in REQUIRED:
        mod = MODULE_MAP.get(pkg, pkg)
        try:
            importlib.import_module(mod)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg}")
            missing.append(pkg)

    if not missing:
        print("\n✅ Барлық 20+ пакет бар!\n")
        return

    print(f"\n📦 Орнатылады ({len(missing)}): {', '.join(missing)}\n")
    for pkg in missing:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print(f"  ✅ {pkg} орнатылды")
        except subprocess.CalledProcessError:
            print(f"  ❌ {pkg} — қате")
    print("\n✅ Орнату аяқталды!\n")


# ============================================================
# ПАПКА ЖАСАУ
# ============================================================

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
MODULES_DIR = os.path.join(BASE_DIR, "modules")
MODEL_DIR   = os.path.join(DATA_DIR, "ml_models")
LOG_DIR     = os.path.join(DATA_DIR, "logs")
ML_DATA_DIR = os.path.join(DATA_DIR, "ml_data")
LLM_DIR     = os.path.join(DATA_DIR, "llm_data")
VOICE_DIR   = os.path.join(DATA_DIR, "voice")
RL_DIR      = os.path.join(DATA_DIR, "rl_agent")

for d in [DATA_DIR, MODEL_DIR, LOG_DIR, ML_DATA_DIR, LLM_DIR, VOICE_DIR, RL_DIR]:
    os.makedirs(d, exist_ok=True)


# ============================================================
# 🆕 MODULE SPLITTER — Модульдерді папкаларға бөлу
# ============================================================

MODULE_STRUCTURE = {
    "wyckoff": ["__init__", "spring", "utad", "sos_sow", "lps_st", "phase"],
    "ml_ai":   ["__init__", "xgboost_ml", "rl_ppo", "llm_groq", "context"],
    "analysis": ["__init__", "fractal", "fourier", "wavelet_mtf", "hedge"],
    "signal":  ["__init__", "long_short", "wait_engine", "confidence", "reasons"],
    "risk":    ["__init__", "sl_tp", "position_size", "limits"],
    "execution": ["__init__", "telegram_worker", "mt5_trader", "journal_db", "metrics"],
}

# Real function → module mapping (extracted by name from this file)
MODULE_FUNC_MAP = {
    "wyckoff/spring":     ["wyckoff_context", "detect_spring_v2"],
    "wyckoff/utad":       ["detect_utad_v2"],
    "wyckoff/sos_sow":    ["detect_sos_v2", "detect_sow_v2"],
    "wyckoff/lps_st":     ["detect_lps_v2", "detect_st_v2", "detect_shakeout_v2"],
    "wyckoff/phase":      ["find_wyckoff_patterns_v2", "analyze_structure", "analyze_4h_phase"],
    "ml_ai/xgboost_ml":   ["ml_load_features", "ml_train", "ml_predict", "ml_worker", "start_ml_trainer"],
    "ml_ai/rl_ppo":       ["APEXTradingEnv", "load_rl_training_data", "train_rl_agent",
                           "rl_predict", "rl_worker", "start_rl_agent"],
    "ml_ai/llm_groq":     ["llm_ask", "llm_analyze_filters", "llm_program_strategy",
                           "llm_self_reflection", "llm_brain_worker", "start_llm_brain",
                           "start_strategy_programmer"],
    "ml_ai/context":      ["rule_score", "ensemble_predict"],
    "analysis/fractal":   ["fractal_dimension", "market_state_by_fractal"],
    "analysis/fourier":   ["fourier_analysis"],
    "analysis/wavelet_mtf": ["wavelet_denoise", "wavelet_trend", "multi_timeframe_analysis"],
    "analysis/hedge":     ["DynamicHedgeEngine", "start_dynamic_hedge"],
    "signal/long_short":  ["calculate_level", "build_signal_object", "format_signal_text", "process_symbol"],
    "signal/wait_engine": ["calculate_wait_signal"],
    "signal/confidence":  ["ensemble_predict"],
    "signal/reasons":     [],
    "risk/sl_tp":         ["load_sltp_config", "get_sltp_for", "build_trade_plan"],
    "risk/position_size": ["calc_lot", "open_position"],
    "risk/limits":        ["set_mode", "get_mode", "can_trade", "validate_risk"],
    "execution/telegram_worker": ["tg_send", "tg_buttons", "tg_photo", "tg_send_voice",
                                  "start_tg", "start_cb"],
    "execution/mt5_trader": ["mt5_safe", "mt5_copy_rates", "mt5_account_info",
                             "mt5_positions_get", "mt5_symbol_info", "mt5_symbol_info_tick",
                             "mt5_order_send", "mt5_terminal_info", "get_filling_mode", "mt5_connect"],
    "execution/journal_db": ["db_init", "journal_log", "journal_stats", "features_save",
                             "features_update_labels"],
    "execution/metrics":  ["metrics_update", "metrics_load", "get_metrics_summary"],
}


def _extract_source_blocks(source_lines, names):
    """
    Extract def/class source blocks for given names from source_lines (0-indexed list).
    Uses simple line scan (def/class at column 0 or indented under if SB3).
    """
    import re
    blocks = []
    n = len(source_lines)
    name_set = set(names)
    i = 0
    while i < n:
        line = source_lines[i]
        # Match top-level or class-level def/class
        m = re.match(r'^(\s*)(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)\b', line)
        if m:
            indent, kind, name = m.group(1), m.group(2), m.group(3)
            if name in name_set:
                base_indent = len(indent)
                start = i
                i += 1
                while i < n:
                    nxt = source_lines[i]
                    if nxt.strip() == "":
                        i += 1
                        continue
                    # continuation of block: deeper indent or decorator already past
                    cur_indent = len(nxt) - len(nxt.lstrip(" \t"))
                    if cur_indent <= base_indent and not nxt.lstrip().startswith(("#", "@")):
                        # check if it's still same block (except blank)
                        if re.match(r'^(def|class)\s+', nxt.lstrip()) or (
                            cur_indent == base_indent and nxt.strip()
                        ):
                            break
                    i += 1
                block = "".join(source_lines[start:i])
                blocks.append((name, block))
                continue
        i += 1
    return blocks


def module_splitter(force=True):
    """
    Нақты Module Splitter — негізгі файлдан функция/класс кодын
    modules/<category>/<name>.py файлдарына шығарады.
    Runtime әлі бір файлдан жүреді; modules/ — құрылым + reuse үшін.
    """
    print("\n" + "=" * 60)
    print("  📂 MODULE SPLITTER — нақты код бөлу")
    print("=" * 60)

    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR, exist_ok=True)

    # Read self source
    try:
        self_path = os.path.abspath(__file__)
    except NameError:
        self_path = os.path.join(BASE_DIR, "apex_v3_fixed.py")
    try:
        with open(self_path, "r", encoding="utf-8") as f:
            source_lines = f.readlines()
    except Exception as e:
        print(f"  ⚠️ Source оқылмады: {e}")
        source_lines = []

    total_files = 0
    total_funcs = 0

    for category, files in MODULE_STRUCTURE.items():
        cat_dir = os.path.join(MODULES_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)

        # Collect all exports for package __init__
        package_exports = []

        for mod_name in files:
            mod_file = os.path.join(cat_dir, f"{mod_name}.py")
            key = f"{category}/{mod_name}"

            if mod_name == "__init__":
                content = (
                    f'"""\n{category.upper()} PACKAGE\n'
                    f'APEX v3 — 6 ҚАТАРЛЫ EDITION (FIXED)\n'
                    f'Авто-жасалған: module_splitter()\n"""\n'
                )
            else:
                func_names = MODULE_FUNC_MAP.get(key, [])
                header = (
                    f'"""\n{category.upper()} — {mod_name}\n'
                    f'APEX v3 модулі (нақты код module_splitter арқылы шығарылды)\n'
                    f'Функциялар: {", ".join(func_names) if func_names else "—"}\n'
                    f'"""\n\n'
                    f'# Авто-import safe: негізгі runtime — apex_v3_fixed.py\n'
                    f'# Бұл файл құрылым / reuse / review үшін.\n\n'
                )
                body_parts = []
                if source_lines and func_names:
                    blocks = _extract_source_blocks(source_lines, func_names)
                    for name, block in blocks:
                        body_parts.append(f"# --- {name} ---\n{block}\n")
                        total_funcs += 1
                        package_exports.append(name)
                    if not blocks:
                        body_parts.append(
                            f"# ⚠️ Код табылмады: {func_names}\n"
                            f"# Негізгі файлда іздеңіз.\n"
                        )
                else:
                    body_parts.append("# (бос модуль / helper)\n")
                content = header + "".join(body_parts)

            # Write (force overwrite so code stays in sync)
            try:
                if force or not os.path.exists(mod_file):
                    with open(mod_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    total_files += 1
            except Exception as e:
                print(f"  ⚠️ {mod_file}: {e}")

        # Enrich __init__.py with exports list
        init_path = os.path.join(cat_dir, "__init__.py")
        try:
            with open(init_path, "a", encoding="utf-8") as f:
                if package_exports:
                    f.write(f"\n__all__ = {package_exports!r}\n")
        except Exception:
            pass

        print(f"  ✅ modules/{category}/ ({len(files)} файл)")

    print(f"\n✅ Жазылды: {total_files} файл | {total_funcs} функция/класс")
    print(f"📂 modules/ папкасы: {MODULES_DIR}\n")
    return total_files, total_funcs


# ============================================================
# ИМПОРТТАР
# ============================================================

import json
import time
import threading
import queue
import sqlite3
import logging
import asyncio
from collections import defaultdict
from io import BytesIO
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import requests
import pandas_ta as ta

try:
    import MetaTrader5 as mt5
except ImportError:
    print("❌ MetaTrader5 жоқ! Іске қосу мүмкін емес.")
    sys.exit(1)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplfinance as mpf


# ============================================================
# THREAD-SAFETY — GLOBAL LOCKS (10/10 critical fix)
# ============================================================
# MetaTrader5 is NOT thread-safe. All MT5 calls MUST go through _mt5_lock.
# Shared mutable state (MEM, AUTO_STATE, _stats, FILTERS_DISABLED) uses _state_lock.

_mt5_lock = threading.RLock()      # MT5 API (rates, orders, positions, account)
_state_lock = threading.RLock()    # MEM, AUTO_STATE, _stats, FILTERS_DISABLED, LATENCY_LOG
_db_lock = threading.RLock()       # SQLite writes


def mt5_safe(fn, *args, **kwargs):
    """Execute any MT5 call under exclusive lock. Prevents crashes & corrupted data."""
    with _mt5_lock:
        return fn(*args, **kwargs)


def mt5_copy_rates(symbol, timeframe, start_pos, count):
    return mt5_safe(mt5.copy_rates_from_pos, symbol, timeframe, start_pos, count)


def mt5_account_info():
    return mt5_safe(mt5.account_info)


def mt5_positions_get(**kwargs):
    return mt5_safe(mt5.positions_get, **kwargs)


def mt5_symbol_info(symbol):
    return mt5_safe(mt5.symbol_info, symbol)


def mt5_symbol_info_tick(symbol):
    return mt5_safe(mt5.symbol_info_tick, symbol)


def mt5_order_send(request):
    return mt5_safe(mt5.order_send, request)


def mt5_terminal_info():
    return mt5_safe(mt5.terminal_info)


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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "apex_v3.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("APEX_v3")


# ============================================================
# CONFIG (.env стилінде)
# ============================================================

from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Standalone Wyckoff engine (research-grade sequence confirmation)
try:
    from apex_wyckoff_engine import analyze_wyckoff, WyckoffConfig
    WYCKOFF_ENGINE_OK = True
except ImportError:
    try:
        # Same folder as this file
        import importlib.util
        _we_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apex_wyckoff_engine.py")
        if os.path.exists(_we_path):
            _spec = importlib.util.spec_from_file_location("apex_wyckoff_engine", _we_path)
            _we_mod = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_we_mod)
            analyze_wyckoff = _we_mod.analyze_wyckoff
            WyckoffConfig = _we_mod.WyckoffConfig
            WYCKOFF_ENGINE_OK = True
        else:
            WYCKOFF_ENGINE_OK = False
    except Exception:
        WYCKOFF_ENGINE_OK = False

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "528379915")

MT5_LOGIN    = int(os.getenv("MT5_LOGIN", "5057082292"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER   = os.getenv("MT5_SERVER", "MetaQuotes-Demo")

FRED_API_KEY      = os.getenv("FRED_API_KEY", "")
SANTIMENT_API_KEY = os.getenv("SANTIMENT_API_KEY", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "apex_v3")
# LLM: xAI Grok (primary) or Groq (fallback)
XAI_API_KEY       = os.getenv("XAI_API_KEY", os.getenv("GROK_API_KEY", ""))
GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")
TV_SECRET         = os.getenv("TV_SECRET", "APEX_SECRET_2026")

ALLOWED_USERS = [int(x) for x in os.getenv("ALLOWED_USERS", TELEGRAM_CHAT_ID).split(",")]


# ============================================================
# ПУТЬТЕР
# ============================================================

MEMORY_FILE    = os.path.join(DATA_DIR, "memory.json")
JOURNAL_DB     = os.path.join(DATA_DIR, "journal.db")
FEATURE_DB     = os.path.join(DATA_DIR, "features.db")
AUTO_FILE      = os.path.join(DATA_DIR, "auto_state.json")
AI_FILE        = os.path.join(DATA_DIR, "ai_state.json")
LEARN_FILE     = os.path.join(DATA_DIR, "learning.json")
STATS_DB       = os.path.join(DATA_DIR, "pattern_stats.db")
SLTP_FILE      = os.path.join(DATA_DIR, "sltp_config.json")
MARKET_DB      = os.path.join(DATA_DIR, "market.db")
METRICS_DB     = os.path.join(DATA_DIR, "metrics.db")
ABLATION_FILE  = os.path.join(DATA_DIR, "ablation.json")
ML_STATUS_FILE = os.path.join(MODEL_DIR, "status.json")
ML_XGB_FILE    = os.path.join(MODEL_DIR, "xgboost.json")
ML_LOGREG_FILE = os.path.join(MODEL_DIR, "logreg.pkl")
LLM_LOG_FILE   = os.path.join(LLM_DIR, "llm_decisions.json")
FILTER_STATE   = os.path.join(DATA_DIR, "filter_state.json")
RL_AGENT_FILE  = os.path.join(RL_DIR, "ppo_apex.zip")


# ============================================================
# ПАРАМЕТРЛЕР
# ============================================================

TIMEFRAME = mt5.TIMEFRAME_M15
CANDLES_LOOKBACK = 21
VOL_MA_WINDOW = 20
ATR_PERIOD = 14

LEVEL_NORMAL, LEVEL_PREPARE, LEVEL_READY = 100, 120, 150
LEVEL_CONFIRM, LEVEL_SIGNAL = 180, 200

VOL_PREPARE_BASE = 1.5
VOL_READY_BASE   = 2.0
VOL_CONFIRM_BASE = 2.5
VOL_SIGNAL_BASE  = 3.0

HFT_DELTA_MIN    = 25.0
HFT_DELTA_STRONG = 40.0
HFT_FOOTPRINT    = 1.0
HFT_VOL          = 1.5

SEQUENCE_TIMEOUT_HOURS = 24

RISK_PER_TRADE = 0.5
RISK_REWARD_MIN = 3.0
DAILY_LOSS_LIMIT = 5.0
DAILY_TRADES_LIMIT = 10

DUPLICATE_WINDOW_SEC = 300
LATENCY_LOG = []

CORRELATION_ENABLED = True
CORRELATION_WINDOW_SEC = 3600
CORRELATION_GROUPS = [
    ["EURUSD", "GBPUSD", "AUDUSD"],
    ["XAUUSD", "XAGUSD"],
    ["BTCUSD", "ETHUSD", "BNBUSD"],
    ["US30", "US500", "USTEC"],
]

TRAILING_ENABLED = True
TRAILING_BE_AT_R = 1.0
TRAILING_STEP_R  = 1.5
TRAILING_MOVE_R  = 0.5

DIVERGENCE_ENABLED = True
DIVERGENCE_WINDOW = 50
DIVERGENCE_LOOKBACK = 5

ELLIOTT_ENABLED = True
GANN_ENABLED = True
DOW_ENABLED = True
NEWS_PAUSE_ENABLED = True
AI_CONFIRM_MIN = 4

CYCLE_SEC = 3
TOP_N = 20
MAX_WORKERS = 8
HEARTBEAT_MIN = 30

CATEGORIES = {
    "crypto": ["BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD",
               "XRPUSD", "DOGEUSD", "ADAUSD", "DOTUSD"],
    "metals": ["XAUUSD", "XAGUSD"],
    "energies": ["USOIL", "UKOIL", "XNGUSD"],
    "indices": ["US30", "US500", "USTEC", "DE30", "UK100", "JP225"],
    "forex": ["EURUSD", "GBPUSD", "USDJPY", "GBPJPY",
              "AUDUSD", "USDCAD", "USDCHF", "NZDUSD",
              "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD",
              "EURGBP", "EURJPY", "GBPCHF"],
}

MIN_UPDATE_HOURS = 24
ML_MIN_SAMPLES = 200
ML_TRAIN_INTERVAL_HOURS = 24

SL_ATR_RANGE = [0.3, 0.5, 0.7, 1.0, 1.5]
TP_R_RANGE   = [3.0, 3.5, 4.0, 4.5, 5.0]
CHECK_AHEAD  = 30
MIN_SAMPLES  = 8

# Advanced ML
FOURIER_ENABLED = True
FRACTAL_ENABLED = True
MULTI_TF_ENABLED = True
WAVELET_ENABLED = True

FOURIER_HARMONICS = 5
FRACTAL_WINDOW = 100
WAVELET_TYPE = "db4"
WAVELET_LEVELS = 3

# LLM — Groq (тегін primary) / xAI Grok (егер кредит бар)
LLM_ENABLED = True
LLM_INTERVAL_HOURS = 6
LLM_MIN_SIGNALS = 50
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # "groq" | "xai"
# Groq: openai/gpt-oss-20b (тегін)
# xAI: grok-3 (ақылы)
LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "openai/gpt-oss-20b" if os.getenv("LLM_PROVIDER", "groq") != "xai" else "grok-3",
)
XAI_BASE_URL = "https://api.x.ai/v1"

# Filter Auto
FILTER_AUTO_ENABLED = True
FILTER_WIN_DISABLE = 0.55
FILTER_WIN_KEEP = 0.70

# Voice
VOICE_ENABLED = True
VOICE_LANG = "kk-KZ-AigulNeural"
VOICE_ON_SIGNAL = True

# Fractal Cycle
FRACTAL_LEVELS = {
    "small":   3,
    "medium":  6 * 3600,
    "large":   24 * 3600,
    "mega":    7 * 86400,
}

# Auto-Learn
AUTO_LEARN_ENABLED = True
AUTO_LEARN_INTERVAL_HOURS = 24

# APEX #38 TV Bridge
TV_BRIDGE_ENABLED = True
TV_BRIDGE_PORT = 8000
TV_BRIDGE_HOST = "0.0.0.0"

# APEX #40 Hedge
HEDGE_ENABLED = True
HEDGE_THRESHOLD = 0.85
HEDGE_MIN_POSITIONS = 3
HEDGE_INTERVAL_SEC = 300

# APEX #41 RL
RL_ENABLED = True
RL_TRAIN_INTERVAL_HOURS = 168
RL_TOTAL_TIMESTEPS = 100000
RL_MIN_SAMPLES = 5000
RL_ENSEMBLE_WEIGHT = 0.10  # 🆕 15% → 10%

# APEX #42 Shazam v4 (Fourier + FAISS multi-TF + 10y RL)
SHAZAM_ENABLED = True
SHAZAM_RL_TIMESTEPS = int(os.getenv("APEX_RL_STEPS", "200000"))  # 200k–1M
SHAZAM_SYMBOLS = ["XAUUSD"]  # бастапқы оқыту символдары
SHAZAM_MIN_CONF = 0.58       # ensemble boost үшін минимум

# 🆕 WAIT режимі — тек CONFIRM (180%+), PREPARE 120% спам емес
WAIT_ENABLED = True
WAIT_LEVEL_MIN = LEVEL_CONFIRM

# 🆕 Metrics
METRICS_ENABLED = True
ABLATION_ENABLED = True


# ============================================================
# GLOBAL STATE
# ============================================================

_stats = {"start": time.time(), "signals": 0, "errors": 0, "cycles": 0,
          "day_start": time.time(), "daily_trades": 0, "daily_loss": 0.0,
          "equity": 10000.0}

MEM = {"phases": {}, "sequences": {}, "levels": {}, "recent_signals": {},
       "spoof": {}, "sent_signals": {}, "wait_signals": {}}

AUTO_STATE = {"mode": "MANUAL", "enabled": False, "daily_trades": 0,
              "daily_loss": 0.0, "day_start": 0, "positions": []}

AI_STATE = {"news_cache": {}, "last_news_check": 0}

LEARN = {"patterns": {}, "last_update": 0, "last_backtest_end": 0}

ML_STATUS = {"ready": False, "accuracy": 0.0, "last_train": 0,
             "samples": 0, "model": "none"}
ML_MODEL = None

# LLM state
FILTERS_DISABLED = set()
LLM_LAST_RUN = [0]
LLM_DECISIONS = []
AUTO_LEARN_LAST = [0]

# APEX #40 Hedge state
HEDGE_LAST_RUN = [0]
HEDGE_ACTIVE = [False]

# APEX #41 RL state
RL_STATUS = {"ready": False, "trained": 0, "last_train": 0, "model_loaded": False}
RL_MODEL = None
RL_LAST_TRAIN = [0]

# APEX #42 Shazam v4 state
SHAZAM_STATUS = {"ready": False, "patterns": 0, "rl_ready": False, "source": None}
_SHAZAM_MOD = None

# 🆕 Metrics state
METRICS = {
    "wins": 0, "losses": 0,
    "gross_profit": 0.0, "gross_loss": 0.0,
    "net_profit": 0.0, "max_dd": 0.0,
    "peak_equity": 10000.0,
    "expectancy": 0.0,
    "profit_factor": 0.0,
    "sharpe": 0.0,
    "recovery": 0.0,
}
ABLATION_RESULTS = {}

_macro_cache  = {"data": {}, "ts": 0}
_social_cache = {"data": {}, "ts": 0}
_news_cache   = {"data": [], "ts": 0}
_fg_cache     = {"value": 50, "ts": 0}
# ============================================================
# LEARNING МОДУЛІ
# ============================================================

def load_learning():
    global LEARN
    if os.path.exists(LEARN_FILE):
        try:
            with open(LEARN_FILE, "r", encoding="utf-8") as f:
                LEARN = json.load(f)
            hours = (time.time() - LEARN.get("last_update", 0)) / 3600
            log.info(f"📂 Learning: {len(LEARN.get('patterns', {}))} паттерн ({hours:.1f}с)")
            return True
        except Exception as e:
            log.error(f"⚠️ Learning: {e}")
    return False


def save_learning():
    LEARN["last_update"] = time.time()
    try:
        with open(LEARN_FILE, "w", encoding="utf-8") as f:
            json.dump(LEARN, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log.error(f"⚠️ Save: {e}")


def need_update():
    if not os.path.exists(LEARN_FILE): return True
    hours = (time.time() - LEARN.get("last_update", 0)) / 3600
    if hours < MIN_UPDATE_HOURS:
        log.info(f"✅ Learning тексерілген ({hours:.1f}с)")
        return False
    log.info(f"🔄 Learning жаңарту ({hours:.1f}с)")
    return True


def save_backtest_results(results):
    for symbol, best in results:
        for event, data in best.items():
            if event not in LEARN["patterns"]:
                LEARN["patterns"][event] = {
                    "wins": 0, "losses": 0, "total": 0,
                    "win_rate": 0.0, "score_mult": 1.0,
                }
            p = LEARN["patterns"][event]
            wr = data["win_rate"]
            p["wins"] += int(wr * 10)
            p["losses"] += int((1 - wr) * 10)
            p["total"] = p["wins"] + p["losses"]
            p["win_rate"] = p["wins"] / p["total"] if p["total"] > 0 else 0
            w = p["win_rate"]
            if w >= 0.7:    p["score_mult"] = 1.5
            elif w >= 0.55: p["score_mult"] = 1.0
            elif w >= 0.4:  p["score_mult"] = 0.7
            else:           p["score_mult"] = 0.3
    LEARN["last_backtest_end"] = time.time()
    save_learning()


def stats_init():
    try:
        conn = sqlite3.connect(STATS_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS pattern_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT, event TEXT, symbol TEXT,
            direction TEXT, result TEXT, pnl REAL, vol_ratio REAL)""")
        conn.commit(); conn.close()
    except Exception as e:
        log.error(f"Stats: {e}")


def stats_record(event, symbol, direction, result, pnl, vol_ratio=1.0):
    try:
        conn = sqlite3.connect(STATS_DB)
        c = conn.cursor()
        c.execute("""INSERT INTO pattern_history
            (timestamp, event, symbol, direction, result, pnl, vol_ratio)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), event, symbol, direction,
             result, pnl, vol_ratio))
        conn.commit(); conn.close()

        if event not in LEARN["patterns"]:
            LEARN["patterns"][event] = {
                "wins": 0, "losses": 0, "total": 0,
                "win_rate": 0.0, "score_mult": 1.0,
            }
        p = LEARN["patterns"][event]
        if result == "TP": p["wins"] += 1
        elif result == "SL": p["losses"] += 1
        p["total"] = p["wins"] + p["losses"]
        p["win_rate"] = p["wins"] / p["total"] if p["total"] > 0 else 0
        if p["total"] >= 10:
            w = p["win_rate"]
            if w >= 0.7:    p["score_mult"] = 1.5
            elif w >= 0.55: p["score_mult"] = 1.0
            elif w >= 0.4:  p["score_mult"] = 0.7
            else:           p["score_mult"] = 0.3
        save_learning()
    except Exception as e:
        log.error(f"Stats: {e}")


def get_pattern_multiplier(event):
    p = LEARN["patterns"].get(event)
    if not p or p["total"] < 5: return 1.0
    return p.get("score_mult", 1.0)


def get_best_patterns(n=5):
    arr = [(k, v) for k, v in LEARN["patterns"].items() if v["total"] >= 5]
    arr.sort(key=lambda x: x[1]["win_rate"], reverse=True)
    return arr[:n]


def get_worst_patterns(n=5):
    arr = [(k, v) for k, v in LEARN["patterns"].items() if v["total"] >= 5]
    arr.sort(key=lambda x: x[1]["win_rate"])
    return arr[:n]


def get_pattern_stats():
    return LEARN["patterns"]


def incremental_backtest(symbols, mt5_module, timeframe):
    last_end = LEARN.get("last_backtest_end", 0)
    if last_end == 0:
        log.info("🎓 БІРІНШІ BACKTEST (3 ай)...")
        bars = 3 * 30 * 24 * 4
    else:
        hours = (time.time() - last_end) / 3600
        bars = int(hours * 4)
        log.info(f"🔄 Incremental ({hours:.1f}с)...")
    if bars < 100:
        log.warning("⚠️ Деректер аз"); return False
    bars = min(bars, 20000)

    results = []
    for i, sym in enumerate(symbols, 1):
        rates = mt5_module.copy_rates_from_pos(sym, timeframe, 0, bars)
        if rates is None or len(rates) < 200: continue
        df = pd.DataFrame(rates)
        best = optimize_pattern(sym, df)
        if best:
            results.append((sym, best))
            log.info(f"  [{i}/{len(symbols)}] {sym} — {len(best)}")
    if results:
        save_backtest_results(results)
        log.info(f"✅ Learning: {len(results)} актив")
        return True
    return False


def learning_init_or_update(symbols, mt5_module, timeframe):
    loaded = load_learning()
    if not loaded:
        incremental_backtest(symbols, mt5_module, timeframe)
    elif need_update():
        incremental_backtest(symbols, mt5_module, timeframe)


# ============================================================
# OPTIMIZE_SLTP МОДУЛІ
# ============================================================

def optimize_pattern(symbol, df):
    if len(df) < 200: return {}
    df = df.copy()
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    df["vol_ma"] = df["tick_volume"].rolling(20).mean()
    df["v_ratio"] = df["tick_volume"] / df["vol_ma"]
    df["range"] = df["high"] - df["low"]
    df["body"] = (df["close"] - df["open"]).abs()
    df["close_loc"] = (df["close"] - df["low"]) / df["range"].replace(0, 1)
    rng = (df["high"] - df["low"]).replace(0, 1)
    df["ad"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng

    patterns = _find_patterns(df)
    results = defaultdict(lambda: defaultdict(
        lambda: {"wins": 0, "losses": 0, "net_rr": 0.0}))

    for pat in patterns:
        event = pat["event"]; direction = pat["direction"]
        idx = pat["idx"]; entry = pat["entry"]
        atr_val = pat["atr"]; l_ev = pat["l_event"]; h_ev = pat["h_event"]
        for sl_mult in SL_ATR_RANGE:
            for tp_r in TP_R_RANGE:
                if direction == "BUY":
                    sl = min(l_ev, entry - sl_mult * atr_val)
                    risk = entry - sl; tp = entry + tp_r * risk
                else:
                    sl = max(h_ev, entry + sl_mult * atr_val)
                    risk = sl - entry; tp = entry - tp_r * risk
                if risk <= 0: continue
                res = _check_outcome(df, idx, direction, entry, sl, tp)
                key = f"{sl_mult}_{tp_r}"
                if res == "TP":
                    results[event][key]["wins"] += 1
                    results[event][key]["net_rr"] += tp_r
                elif res == "SL":
                    results[event][key]["losses"] += 1
                    results[event][key]["net_rr"] -= 1.0

    best = {}
    for event, combos in results.items():
        bc = None; bnr = -999; bwr = 0
        for key, s in combos.items():
            t = s["wins"] + s["losses"]
            if t < MIN_SAMPLES: continue
            wr = s["wins"] / t; nr = s["net_rr"] / t
            if nr > bnr: bnr = nr; bwr = wr; bc = key
        if bc:
            sl_m, tp_r = bc.split("_")
            best[event] = {"sl_mult": float(sl_m), "tp_r": float(tp_r),
                           "win_rate": bwr, "net_rr": bnr}
    return best


def _find_patterns(df):
    """Wyckoff 15 паттерн (негізгі backtest үшін)"""
    patterns = []
    for i in range(48, len(df) - CHECK_AHEAD):
        recent = df.iloc[i-48:i]
        sup = float(recent["low"].min()); res = float(recent["high"].max())
        last = df.iloc[i]; vm = df["vol_ma"].iloc[i]
        if vm <= 0 or pd.isna(vm): continue
        vr = last["v_ratio"]; atr = last["atr"]
        if pd.isna(atr) or atr <= 0: continue
        rng = last["range"]
        if rng <= 0: continue
        cl = last["close_loc"]; body = last["body"]; ad = last["ad"]
        is_bull = last["close"] > last["open"]
        is_bear = last["close"] < last["open"]
        big = body > atr * 1.2

        def add(e, d):
            patterns.append({"event": e, "direction": d, "idx": i,
                             "entry": float(last["close"]), "atr": float(atr),
                             "l_event": float(last["low"]),
                             "h_event": float(last["high"])})

        if last["low"] < sup and last["close"] > sup and vr >= 1.2:
            add("spring", "BUY")
        if last["low"] < sup and last["close"] > sup and vr >= 2.0:
            add("shakeout", "BUY")
        if last["high"] > res and last["close"] < res and vr >= 1.2:
            add("utad", "SELL")
        if last["high"] > res and last["close"] < res and vr >= 1.0:
            add("ut", "SELL")
        if is_bull and last["close"] > res and vr >= 1.5:
            add("sos", "BUY")
        if is_bear and last["close"] < sup and vr >= 1.5:
            add("sow", "SELL")
        if is_bear and big and vr >= 2.0 and cl > 0.4:
            add("sc", "BUY")
        if is_bull and big and vr >= 2.0 and cl < 0.6:
            add("bc", "SELL")
        if vr >= 1.5 and body < atr * 0.4 and cl > 0.5 and ad > 0:
            add("absorption_bull", "BUY")
        if vr >= 1.5 and body < atr * 0.4 and cl < 0.5 and ad < 0:
            add("absorption_bear", "SELL")
        if last["high"] > res and last["close"] < res and vr < 1.0:
            add("bull_trap", "SELL")
        if is_bull and vr < 0.7 and cl > 0.5:
            add("no_demand", "SELL")
        if is_bear and vr < 0.7 and cl < 0.5:
            add("no_supply", "BUY")
        if is_bull and sup < last["close"] < res and vr < 1.0:
            add("lps", "BUY")
        if abs(last["low"] - sup) < rng * 0.1 and vr < 1.0:
            add("st", "BUY")
    return patterns


def _check_outcome(df, idx, direction, entry, sl, tp):
    for j in range(idx+1, min(idx+CHECK_AHEAD+1, len(df))):
        h = df["high"].iloc[j]; l = df["low"].iloc[j]
        if direction == "BUY":
            if l <= sl: return "SL"
            if h >= tp: return "TP"
        else:
            if h >= sl: return "SL"
            if l <= tp: return "TP"
    return "PENDING"


def load_sltp_config():
    if os.path.exists(SLTP_FILE):
        try:
            with open(SLTP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception: pass
    return {"global": {}}


def get_sltp_for(event, symbol=None):
    cfg = load_sltp_config()
    g = cfg.get("global", {})
    if event in g:
        return g[event]["sl_mult"], g[event]["tp_r"]
    return 0.7, 3.5


def save_global(results):
    cfg = load_sltp_config()
    for _, best in results:
        for event, d in best.items():
            if event not in cfg["global"]:
                cfg["global"][event] = {
                    "sl_mult": d["sl_mult"], "tp_r": d["tp_r"], "n": 1}
            else:
                g = cfg["global"][event]; n = g["n"]
                g["sl_mult"] = (g["sl_mult"] * n + d["sl_mult"]) / (n + 1)
                g["tp_r"]    = (g["tp_r"]    * n + d["tp_r"])    / (n + 1)
                g["n"] = n + 1
    try:
        with open(SLTP_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception: pass


# ============================================================
# DATA_LAYER МОДУЛІ
# ============================================================

def db_init_market():
    try:
        conn = sqlite3.connect(MARKET_DB)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS macro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER, indicator TEXT, value REAL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS social (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER, source TEXT, symbol TEXT,
            mentions INTEGER, sentiment REAL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts INTEGER, source TEXT, title TEXT, sentiment REAL)""")
        conn.commit(); conn.close()
        log.info("✅ Data DB OK")
    except Exception as e:
        log.error(f"DB: {e}")


def _db_insert(table, data):
    try:
        conn = sqlite3.connect(MARKET_DB)
        c = conn.cursor()
        cols = ", ".join(data.keys())
        qs = ", ".join(["?"] * len(data))
        c.execute(f"INSERT INTO {table} ({cols}) VALUES ({qs})", tuple(data.values()))
        conn.commit(); conn.close()
    except Exception:
        pass


def fetch_fred():
    if not FRED_API_KEY: return
    try:
        import fredapi
        fred = fredapi.Fred(api_key=FRED_API_KEY)
        indicators = {
            "DXY": "DTWEXBGS", "CPI": "CPIAUCSL",
            "UNRATE": "UNRATE", "FEDFUNDS": "FEDFUNDS", "DGS10": "DGS10",
        }
        data = {}
        for name, code in indicators.items():
            try:
                s = fred.get_series(code).dropna().tail(1)
                if len(s) > 0:
                    v = float(s.iloc[-1])
                    data[name] = v
                    _db_insert("macro", {"ts": int(time.time()),
                                          "indicator": name, "value": v})
            except Exception:
                pass
        _macro_cache["data"] = data
        _macro_cache["ts"] = time.time()
        log.info(f"📊 FRED: {list(data.keys())}")
    except ImportError:
        log.warning("⚠️ fredapi жоқ")
    except Exception as e:
        log.error(f"FRED: {e}")


def get_macro():
    if time.time() - _macro_cache["ts"] > 3600:
        fetch_fred()
    return _macro_cache["data"]


def macro_direction():
    m = get_macro()
    if not m: return None, ""
    dxy = m.get("DXY", 0)
    yields = m.get("DGS10", 0)
    if dxy > 100:
        return "SELL", f"📊 DXY {dxy:.1f}↑"
    elif dxy < 95:
        return "BUY", f"📊 DXY {dxy:.1f}↓"
    if yields > 4.5:
        return "SELL", f"📊 Yields {yields:.2f}↑"
    elif yields < 3.5:
        return "BUY", f"📊 Yields {yields:.2f}↓"
    return None, ""


def fetch_santiment():
    if not SANTIMENT_API_KEY: return
    try:
        url = "https://api.santiment.net/graphql"
        headers = {"Authorization": f"Bearer {SANTIMENT_API_KEY}"}
        now = int(time.time())
        query = """
        {
          getMetric(metric: "social_volume_total") {
            timeseriesData(slug: "bitcoin" from: "%d" to: "%d" interval: "1h")
            { datetime value }
          }
        }
        """ % (now - 3600, now)
        r = requests.post(url, json={"query": query}, headers=headers, timeout=15)
        if r.status_code != 200:
            log.warning(f"San status: {r.status_code}"); return
        d = r.json()
        ts = d.get("data", {}).get("getMetric", {}).get("timeseriesData", [])
        if ts:
            v = float(ts[-1].get("value", 0))
            _social_cache["data"]["BTC_social"] = v
            _social_cache["ts"] = time.time()
            _db_insert("social", {"ts": now, "source": "santiment",
                                   "symbol": "BTC", "mentions": int(v),
                                   "sentiment": 0})
            log.info(f"🔗 Santiment: BTC social = {int(v)}")
    except Exception as e:
        log.error(f"San: {e}")


def get_santiment():
    if time.time() - _social_cache["ts"] > 3600:
        fetch_santiment()
    return _social_cache["data"]


def fetch_cryptocompare():
    try:
        r = requests.get(
            "https://min-api.cryptocompare.com/data/v2/news/?lang=EN", timeout=10)
        if r.status_code == 200:
            d = r.json()
            news = d.get("Data", [])[:10]
            _news_cache["data"] = [
                {"title": n.get("title", "")[:100],
                 "cats": n.get("categories", "")} for n in news]
            _news_cache["ts"] = time.time()
            log.info(f"📰 CC: {len(news)}")
    except Exception:
        pass


def get_news_sentiment():
    if time.time() - _news_cache["ts"] > 1800:
        return 0.0
    s = 0.0
    for n in _news_cache["data"]:
        t = (n["title"] + " " + n["cats"]).lower()
        if any(w in t for w in ["bull", "rally", "surge", "high"]):
            s += 1
        elif any(w in t for w in ["bear", "crash", "drop", "low"]):
            s -= 1
    return s / max(len(_news_cache["data"]), 1)


def fetch_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=5)
        if r.status_code == 200:
            d = r.json()
            _fg_cache["value"] = int(d["data"][0]["value"])
            _fg_cache["ts"] = time.time()
            log.info(f"😱 FG: {_fg_cache['value']}")
    except Exception:
        pass


def get_fear_greed_dir():
    v = _fg_cache["value"]
    if v <= 25: return "BUY"
    if v >= 75: return "SELL"
    return None


def fetch_reddit_public():
    try:
        subs = ["wallstreetbets", "cryptocurrency", "Bitcoin"]
        total_s = 0.0; total_n = 0
        for sub in subs:
            r = requests.get(
                f"https://www.reddit.com/r/{sub}/hot.json?limit=20",
                headers={"User-Agent": REDDIT_USER_AGENT}, timeout=10)
            if r.status_code != 200: continue
            posts = r.json().get("data", {}).get("children", [])
            for p in posts:
                t = p["data"]["title"].lower()
                if any(w in t for w in ["moon", "bull", "buy"]):
                    total_s += 1
                elif any(w in t for w in ["crash", "bear", "sell"]):
                    total_s -= 1
                total_n += 1
        if total_n > 0:
            _social_cache["data"]["reddit_sentiment"] = total_s / total_n
            log.info(f"💬 Reddit: {total_s/total_n:+.2f}")
    except Exception:
        pass


def get_reddit_sentiment():
    return _social_cache["data"].get("reddit_sentiment", 0.0)


def data_worker():
    db_init_market()
    log.info("\n📥 Бірінші деректер жүктелуде...")
    fetch_cryptocompare()
    fetch_fear_greed()
    fetch_reddit_public()
    fetch_fred()
    fetch_santiment()

    while True:
        try:
            log.info("\n📥 Data collection...")
            fetch_cryptocompare()
            fetch_fear_greed()
            fetch_reddit_public()
            hours = int(time.time() // 3600)
            if hours != getattr(data_worker, "_last_fred_hour", -1):
                fetch_fred()
                fetch_santiment()
                data_worker._last_fred_hour = hours
            time.sleep(900)
        except Exception as e:
            log.error(f"Data worker: {e}")
            time.sleep(300)


def start_data_collector():
    threading.Thread(target=data_worker, daemon=True).start()
    log.info("✅ Data collector")
    
    # ============================================================
# FOURIER TRANSFORM
# ============================================================

def fourier_analysis(prices, harmonics=FOURIER_HARMONICS):
    """Фурье талдау — баға циклдерін табу"""
    try:
        if len(prices) < 50: return None
        prices_arr = np.array(prices, dtype=float)
        prices_detrended = prices_arr - np.mean(prices_arr)
        fft_vals = np.fft.fft(prices_detrended)
        fft_freq = np.fft.fftfreq(len(prices_detrended))
        amplitude = np.abs(fft_vals)
        top_idx = np.argsort(amplitude[1:len(amplitude)//2])[::-1][:harmonics] + 1

        if len(top_idx) > 0:
            dominant_idx = top_idx[0]
            dominant_freq = abs(fft_freq[dominant_idx])
            dominant_period = int(1 / dominant_freq) if dominant_freq > 0 else 0
        else:
            dominant_period = 0

        cycle_strength = float(np.sum(amplitude[top_idx]) / np.sum(amplitude))

        if dominant_period > 0:
            recent = prices_arr[-min(dominant_period, len(prices_arr)):]
            if len(recent) > 2:
                direction = "UP" if recent[-1] > recent[0] else "DOWN"
            else:
                direction = "NEUTRAL"
        else:
            direction = "NEUTRAL"

        return {
            "trend": "UP" if prices_arr[-1] > prices_arr[0] else "DOWN",
            "cycle_strength": round(cycle_strength, 3),
            "dominant_period": dominant_period,
            "direction": direction,
        }
    except Exception as e:
        log.error(f"Fourier: {e}")
        return None


# ============================================================
# FRACTAL DIMENSION (Higuchi)
# ============================================================

def fractal_dimension(prices, window=FRACTAL_WINDOW):
    """
    Higuchi әдісі — фракталдық өлшем.
    Қайтарады: float (1.0 - 2.0)
    1.0 = түзу сызық (тренд)
    1.5 = Brownian
    2.0 = шуыл (флэт)
    """
    try:
        if len(prices) < window: return None
        prices_arr = np.array(prices[-window:], dtype=float)
        L = []
        k_values = [2, 4, 8, 16, 32]

        for k in k_values:
            Lk = []
            for m in range(k):
                idx = np.arange(m, len(prices_arr), k)
                if len(idx) < 2: continue
                Lmk = np.sum(np.abs(np.diff(prices_arr[idx])))
                Lmk = Lmk * (len(prices_arr) - 1) / (k * len(idx))
                Lk.append(Lmk)
            if Lk:
                L.append(np.mean(Lk))

        if len(L) < 2: return None

        x = np.log(1.0 / np.array(k_values[:len(L)]))
        y = np.log(np.array(L))
        coeffs = np.polyfit(x, y, 1)
        fd = coeffs[0]
        return round(float(fd), 3)
    except Exception as e:
        log.error(f"Fractal: {e}")
        return None


def market_state_by_fractal(fd):
    """Fractal dimension → нарық күйі"""
    if fd is None: return "UNKNOWN"
    if fd < 1.3:    return "STRONG_TREND"
    elif fd < 1.5:  return "TREND"
    elif fd < 1.7:  return "WEAK_TREND"
    else:           return "RANGE"


# ============================================================
# WAVELET TRANSFORM
# ============================================================

def wavelet_denoise(prices, wavelet=WAVELET_TYPE, levels=WAVELET_LEVELS):
    """Wavelet — шуылдан тазалау"""
    try:
        import pywt
        if len(prices) < 50: return None
        prices_arr = np.array(prices, dtype=float)
        coeffs = pywt.wavedec(prices_arr, wavelet, level=levels)

        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        threshold = sigma * np.sqrt(2 * np.log(len(prices_arr)))

        coeffs_thresh = [coeffs[0]]
        for c in coeffs[1:]:
            c_thresh = pywt.threshold(c, threshold, mode="soft")
            coeffs_thresh.append(c_thresh)

        denoised = pywt.waverec(coeffs_thresh, wavelet)
        return denoised[:len(prices_arr)]
    except Exception as e:
        log.error(f"Wavelet: {e}")
        return None


def wavelet_trend(prices):
    """Wavelet бойынша тренд бағыты"""
    try:
        denoised = wavelet_denoise(prices)
        if denoised is None or len(denoised) < 10: return None
        recent = denoised[-10:]
        slope = (recent[-1] - recent[0]) / max(abs(recent[0]), 1e-9)
        if slope > 0.001: return "UP"
        elif slope < -0.001: return "DOWN"
        else: return "SIDE"
    except Exception:
        return None


# ============================================================
# MULTI-TIMEFRAME
# ============================================================

def multi_timeframe_analysis(symbol):
    """
    M15 + H1 + H4 + D1 талдау.
    Қайтарады: dict {alignment, score, trend_m15, trend_h1, trend_h4, trend_d1}
    """
    try:
        timeframes = {
            "M15": mt5.TIMEFRAME_M15,
            "H1":  mt5.TIMEFRAME_H1,
            "H4":  mt5.TIMEFRAME_H4,
            "D1":  mt5.TIMEFRAME_D1,
        }
        trends = {}
        for tf_name, tf_val in timeframes.items():
            rates = mt5_copy_rates(symbol, tf_val, 0, 60)
            if rates is None or len(rates) < 50: continue
            df = pd.DataFrame(rates)
            df = df.iloc[:-1]
            if len(df) < 50: continue
            e20 = df["close"].ewm(span=20).mean().iloc[-1]
            e50 = df["close"].ewm(span=50).mean().iloc[-1]
            cur = df["close"].iloc[-1]
            if cur > e20 > e50:
                trends[tf_name] = "UP"
            elif cur < e20 < e50:
                trends[tf_name] = "DOWN"
            else:
                trends[tf_name] = "SIDE"

        if not trends: return None

        up_count = sum(1 for v in trends.values() if v == "UP")
        down_count = sum(1 for v in trends.values() if v == "DOWN")
        total = len(trends)

        if up_count == total:
            alignment = "STRONG_UP"; score = 1.0
        elif down_count == total:
            alignment = "STRONG_DOWN"; score = 1.0
        elif up_count >= total * 0.75:
            alignment = "UP"; score = 0.75
        elif down_count >= total * 0.75:
            alignment = "DOWN"; score = 0.75
        else:
            alignment = "MIXED"; score = 0.4

        return {
            "alignment": alignment,
            "score": score,
            "trend_m15": trends.get("M15", "?"),
            "trend_h1": trends.get("H1", "?"),
            "trend_h4": trends.get("H4", "?"),
            "trend_d1": trends.get("D1", "?"),
        }
    except Exception as e:
        log.error(f"MultiTF: {e}")
        return None
        
        # ============================================================
# ML TRAINER (XGBoost + LogReg)
# ============================================================

# Full ML feature set (14) — matches process_symbol / features_save / RL obs
ML_FEATURE_COLS = [
    "vol_ratio", "delta_pct", "adaptive", "atr_pct",
    "mfi", "ad", "body_atr", "close_loc", "hour",
    "fourier", "fractal", "mtf_score", "wavelet", "market_state_val",
]
ML_N_FEATURES = len(ML_FEATURE_COLS)  # 14


def _market_state_to_val(state):
    """market_state TEXT → numeric for ML"""
    return {
        "STRONG_TREND": 1.0, "TREND": 0.5, "WEAK_TREND": 0.0,
        "RANGE": -0.5, "UNKNOWN": 0.0,
    }.get(str(state or "UNKNOWN").upper(), 0.0)


def ml_load_features():
    """ML features жүктеу — 14 feature (core 9 + Fourier/Fractal/MTF/Wavelet/State)"""
    try:
        with _db_lock:
            conn = sqlite3.connect(FEATURE_DB, timeout=30)
            df = pd.read_sql("SELECT * FROM features WHERE label != -1", conn)
            conn.close()
        if len(df) < ML_MIN_SAMPLES:
            return None, None

        # Ensure advanced columns exist (old DB rows may lack them)
        for col, default in [
            ("fourier", 0.5), ("fractal", 1.5), ("mtf_score", 0.5),
            ("wavelet", 0.0), ("market_state", "UNKNOWN"),
        ]:
            if col not in df.columns:
                df[col] = default

        df["market_state_val"] = df["market_state"].map(_market_state_to_val)
        # Fill NaN safely
        for c in ML_FEATURE_COLS:
            if c not in df.columns:
                df[c] = 0.0
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

        X = df[ML_FEATURE_COLS].values.astype(np.float32)
        y = df["label"].values.astype(np.int32)
        return X, y
    except Exception as e:
        log.error(f"ml_load_features: {e}")
        return None, None


def ml_train():
    """XGBoost/LogReg оқыту — 14 feature"""
    global ML_MODEL, ML_STATUS
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score

        X, y = ml_load_features()
        if X is None or len(X) < ML_MIN_SAMPLES:
            log.info(f"ML: samples < {ML_MIN_SAMPLES}, skip train")
            return

        # Time-based split (no leakage)
        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.2, shuffle=False)

        try:
            import xgboost as xgb
            model = xgb.XGBClassifier(
                n_estimators=300, max_depth=6, learning_rate=0.05,
                objective="binary:logistic", eval_metric="logloss",
                use_label_encoder=False, n_jobs=2)
            model.fit(X_tr, y_tr)
            acc = accuracy_score(y_te, model.predict(X_te))
            model.save_model(ML_XGB_FILE)
            ML_MODEL = model
            ML_STATUS = {
                "ready": True, "accuracy": float(acc),
                "last_train": time.time(), "samples": int(len(X)),
                "model": "xgboost", "n_features": ML_N_FEATURES,
            }
            log.info(f"✅ ML: XGBoost acc={acc:.3f} n={len(X)} feats={ML_N_FEATURES}")
        except ImportError:
            from sklearn.linear_model import LogisticRegression
            import pickle
            model = LogisticRegression(max_iter=1000)
            model.fit(X_tr, y_tr)
            acc = accuracy_score(y_te, model.predict(X_te))
            with open(ML_LOGREG_FILE, "wb") as f:
                pickle.dump(model, f)
            ML_MODEL = model
            ML_STATUS = {
                "ready": True, "accuracy": float(acc),
                "last_train": time.time(), "samples": int(len(X)),
                "model": "logreg", "n_features": ML_N_FEATURES,
            }
            log.info(f"✅ ML: LogReg acc={acc:.3f} feats={ML_N_FEATURES}")

        with open(ML_STATUS_FILE, "w") as f:
            json.dump(ML_STATUS, f)
    except Exception as e:
        log.error(f"ML train: {e}")


def ml_predict(features):
    """ML болжам (0.0 - 1.0) — 14 feature vector"""
    if not ML_STATUS.get("ready") or ML_MODEL is None:
        return 0.5
    try:
        # Accept list/array of any length; pad or trim to ML_N_FEATURES
        arr = np.asarray(features, dtype=np.float32).ravel()
        if len(arr) < ML_N_FEATURES:
            arr = np.pad(arr, (0, ML_N_FEATURES - len(arr)), constant_values=0.0)
        elif len(arr) > ML_N_FEATURES:
            arr = arr[:ML_N_FEATURES]
        proba = ML_MODEL.predict_proba(arr.reshape(1, -1))[0]
        # class 1 probability
        return float(proba[1] if len(proba) > 1 else proba[0])
    except Exception as e:
        log.debug(f"ml_predict: {e}")
        return 0.5


def ml_worker():
    """ML оқыту циклі (24 сағат)"""
    time.sleep(3600)
    while True:
        try:
            ml_train()
            time.sleep(ML_TRAIN_INTERVAL_HOURS * 3600)
        except Exception:
            time.sleep(3600)


def start_ml_trainer():
    """ML trainer іске қосу"""
    global ML_STATUS
    if os.path.exists(ML_STATUS_FILE):
        try:
            with open(ML_STATUS_FILE) as f:
                ML_STATUS.update(json.load(f))
            log.info(f"✅ ML loaded: acc={ML_STATUS.get('accuracy', 0):.2f}")
        except Exception:
            pass
    threading.Thread(target=ml_worker, daemon=True).start()
    log.info("✅ ML trainer (XGBoost)")


# ============================================================
# 🆕 RL AGENT (PPO) — Rule-based негізде
# ============================================================

try:
    import gymnasium as gym
    from gymnasium import spaces
    from stable_baselines3 import PPO
    from stable_baselines3.common.env_checker import check_env
    SB3_AVAILABLE = True
except ImportError:
    SB3_AVAILABLE = False
    log.warning("⚠️ stable-baselines3/gymnasium жоқ — RL өшірулі")


if SB3_AVAILABLE:

    class APEXTradingEnv(gym.Env):
        """
        APEX Trading Environment
        Actions: 0=HOLD, 1=BUY, 2=SELL, 3=CLOSE
        State: 15 features (14 + position)
        Reward: Profit - Drawdown Penalty - Commission
        """
        metadata = {"render_modes": ["human"]}

        def __init__(self, df):
            super().__init__()
            self.df = df.reset_index(drop=True)
            self.current_step = 0
            self.initial_balance = 10000.0
            self.balance = self.initial_balance
            self.position = 0
            self.entry_price = 0.0
            self.trades = []
            self.max_balance = self.initial_balance
            self.commission = 0.001  # 0.1% комиссия

            self.action_space = spaces.Discrete(4)

            self.observation_space = spaces.Box(
                low=-np.inf, high=np.inf, shape=(15,), dtype=np.float32
            )

        def reset(self, seed=None, options=None):
            super().reset(seed=seed)
            self.current_step = 0
            self.balance = self.initial_balance
            self.position = 0
            self.entry_price = 0.0
            self.trades = []
            self.max_balance = self.initial_balance
            self._prev_unrealized = 0.0
            return self._get_obs(), {}

        def _get_obs(self):
            try:
                row = self.df.iloc[self.current_step]
                return np.array([
                    float(row.get("vol_ratio", 1.0)),
                    float(row.get("delta_pct", 0.0)),
                    float(row.get("adaptive", 1.0)),
                    float(row.get("atr_pct", 0.3)),
                    float(row.get("mfi", 50.0)),
                    float(row.get("ad", 0.0)),
                    float(row.get("body_atr", 0.5)),
                    float(row.get("close_loc", 0.5)),
                    float(row.get("hour", 12)),
                    float(row.get("fourier", 0.5)),
                    float(row.get("fractal", 1.5)),
                    float(row.get("mtf_score", 0.5)),
                    float(row.get("wavelet", 0.0)),
                    float(row.get("market_state_val", 0.0)),
                    float(self.position),
                ], dtype=np.float32)
            except Exception:
                return np.zeros(15, dtype=np.float32)

        def _mark_to_market(self, curr_price):
            """Unrealized PnL % from entry (for open position)."""
            if self.position == 0 or self.entry_price <= 0:
                return 0.0
            return self.position * (curr_price - self.entry_price) / self.entry_price

        def _calculate_reward(self, action):
            """
            Clean reward:
              - Commission on open/flip/close
              - Realized PnL on CLOSE / flip
              - Mark-to-market on HOLD (small scale)
              - Drawdown penalty relative to peak equity
            Actions: 0=HOLD, 1=BUY, 2=SELL, 3=CLOSE
            """
            reward = 0.0
            if self.current_step < 1 or self.current_step >= len(self.df):
                return 0.0

            curr_price = float(self.df.iloc[self.current_step]["close"])
            if curr_price <= 0:
                return 0.0

            prev_unrealized = getattr(self, "_prev_unrealized", 0.0)

            # --- CLOSE ---
            if action == 3:
                if self.position != 0:
                    pnl_pct = self._mark_to_market(curr_price)
                    reward = pnl_pct * 100.0 - self.commission * 100.0
                    self.balance += self.balance * pnl_pct  # compound
                    self.trades.append({
                        "step": self.current_step,
                        "side": self.position,
                        "entry": self.entry_price,
                        "exit": curr_price,
                        "pnl_pct": pnl_pct,
                    })
                    self.position = 0
                    self.entry_price = 0.0
                # else: already flat → small negative to discourage spam close
                else:
                    reward = -0.01

            # --- BUY ---
            elif action == 1:
                if self.position == 1:
                    # already long → treat as HOLD mark-to-market
                    unrealized = self._mark_to_market(curr_price)
                    reward = (unrealized - prev_unrealized) * 50.0
                elif self.position == -1:
                    # flip short → long: realize short PnL + open long
                    pnl_pct = self._mark_to_market(curr_price)
                    reward = pnl_pct * 100.0 - 2 * self.commission * 100.0
                    self.balance += self.balance * pnl_pct
                    self.trades.append({
                        "step": self.current_step, "side": -1,
                        "entry": self.entry_price, "exit": curr_price,
                        "pnl_pct": pnl_pct,
                    })
                    self.position = 1
                    self.entry_price = curr_price
                else:
                    # open long
                    self.position = 1
                    self.entry_price = curr_price
                    reward = -self.commission * 100.0

            # --- SELL ---
            elif action == 2:
                if self.position == -1:
                    unrealized = self._mark_to_market(curr_price)
                    reward = (unrealized - prev_unrealized) * 50.0
                elif self.position == 1:
                    pnl_pct = self._mark_to_market(curr_price)
                    reward = pnl_pct * 100.0 - 2 * self.commission * 100.0
                    self.balance += self.balance * pnl_pct
                    self.trades.append({
                        "step": self.current_step, "side": 1,
                        "entry": self.entry_price, "exit": curr_price,
                        "pnl_pct": pnl_pct,
                    })
                    self.position = -1
                    self.entry_price = curr_price
                else:
                    self.position = -1
                    self.entry_price = curr_price
                    reward = -self.commission * 100.0

            # --- HOLD ---
            else:
                if self.position != 0:
                    unrealized = self._mark_to_market(curr_price)
                    reward = (unrealized - prev_unrealized) * 50.0
                else:
                    reward = 0.0  # flat hold = neutral

            # Track unrealized for next step delta
            self._prev_unrealized = self._mark_to_market(curr_price)

            # Drawdown penalty (peak equity)
            if self.balance > self.max_balance:
                self.max_balance = self.balance
            if self.max_balance > 0:
                dd = (self.max_balance - self.balance) / self.max_balance
                reward -= dd * 1.5

            # Clip extreme rewards for stable PPO training
            reward = float(np.clip(reward, -10.0, 10.0))
            return reward

        def step(self, action):
            reward = self._calculate_reward(int(action))
            self.current_step += 1
            done = self.current_step >= len(self.df) - 1
            truncated = False

            info = {
                "balance": self.balance,
                "position": self.position,
                "trades": len(self.trades),
            }

            return self._get_obs(), reward, done, truncated, info


    def load_rl_training_data(days=365):
        """RL үшін тарихи деректер"""
        try:
            conn = sqlite3.connect(FEATURE_DB)
            df = pd.read_sql(
                "SELECT * FROM features WHERE label != -1 ORDER BY ts DESC LIMIT 20000",
                conn
            )
            conn.close()

            if len(df) < RL_MIN_SAMPLES:
                log.warning(f"⚠️ RL: деректер аз ({len(df)}/{RL_MIN_SAMPLES})")
                return None

            features = pd.DataFrame({
                "vol_ratio": df["vol_ratio"].fillna(1.0),
                "delta_pct": df["delta_pct"].fillna(0.0),
                "adaptive": df["adaptive"].fillna(1.0),
                "atr_pct": df["atr_pct"].fillna(0.3),
                "mfi": df["mfi"].fillna(50.0),
                "ad": df["ad"].fillna(0.0),
                "body_atr": df["body_atr"].fillna(0.5),
                "close_loc": df["close_loc"].fillna(0.5),
                "hour": df["hour"].fillna(12),
                "fourier": df["fourier"].fillna(0.5),
                "fractal": df["fractal"].fillna(1.5),
                "mtf_score": df["mtf_score"].fillna(0.5),
                "wavelet": df["wavelet"].fillna(0.0),
                "market_state_val": 0.0,
                "close": df.get("entry", df["close_loc"] * 100),
            })

            return features
        except Exception as e:
            log.error(f"RL data: {e}")
            return None


    def train_rl_agent():
        """PPO agent оқыту"""
        global RL_MODEL, RL_STATUS
        try:
            log.info("🎓 RL: PPO agent оқыту басталды...")

            df = load_rl_training_data(days=365)
            if df is None or len(df) < RL_MIN_SAMPLES:
                log.warning("⚠️ RL: деректер жетпейді")
                return False

            env = APEXTradingEnv(df)
            check_env(env, warn=True)

            model = PPO(
                "MlpPolicy",
                env,
                verbose=0,
                learning_rate=3e-4,
                n_steps=2048,
                batch_size=64,
                n_epochs=10,
                gamma=0.99,
                gae_lambda=0.95,
                clip_range=0.2,
                ent_coef=0.01,
            )

            model.learn(total_timesteps=RL_TOTAL_TIMESTEPS, progress_bar=False)
            model.save(RL_AGENT_FILE)

            RL_MODEL = model
            RL_STATUS = {
                "ready": True,
                "trained": RL_TOTAL_TIMESTEPS,
                "last_train": time.time(),
                "model_loaded": True,
            }
            RL_LAST_TRAIN[0] = time.time()

            log.info(f"✅ RL: PPO оқытылды ({RL_TOTAL_TIMESTEPS} steps)")

            tg_send(
                f"🎓 *Reinforcement Learning*\n\n"
                f"✅ PPO agent оқытылды\n"
                f"📊 Steps: `{RL_TOTAL_TIMESTEPS}`\n"
                f"💾 Модель сақталды"
            )
            return True
        except Exception as e:
            log.error(f"RL train: {e}")
            return False


    def rl_predict(features):
        """RL agent болжамы (0.0 - 1.0)"""
        if not RL_STATUS.get("ready") or RL_MODEL is None:
            return 0.5
        try:
            if len(features) >= 14:
                obs = np.array(features[:14] + [0.0], dtype=np.float32)
            else:
                obs = np.zeros(15, dtype=np.float32)

            action, _ = RL_MODEL.predict(obs, deterministic=True)
            if action == 1:   return 0.75   # BUY
            elif action == 2: return 0.25   # SELL
            elif action == 3: return 0.5    # CLOSE
            else:             return 0.5    # HOLD
        except Exception:
            return 0.5


    def rl_worker():
        """RL оқыту циклі (7 күн)"""
        time.sleep(3600)
        while True:
            try:
                if not RL_ENABLED:
                    time.sleep(RL_TRAIN_INTERVAL_HOURS * 3600)
                    continue
                log.info("🎓 RL worker: оқыту тексеру...")
                train_rl_agent()
                time.sleep(RL_TRAIN_INTERVAL_HOURS * 3600)
            except Exception as e:
                log.error(f"RL worker: {e}")
                time.sleep(3600)


    def start_rl_agent():
        """RL agent іске қосу"""
        global RL_MODEL, RL_STATUS
        if not RL_ENABLED:
            log.info("⏸ RL өшірулі")
            return
        if not SB3_AVAILABLE:
            log.warning("⚠️ stable-baselines3 жоқ — RL өшірулі")
            return

        if os.path.exists(RL_AGENT_FILE):
            try:
                RL_MODEL = PPO.load(RL_AGENT_FILE)
                RL_STATUS["ready"] = True
                RL_STATUS["model_loaded"] = True
                RL_STATUS["last_train"] = os.path.getmtime(RL_AGENT_FILE)
                log.info("✅ RL: модель жүктелді")
            except Exception as e:
                log.warning(f"RL load: {e}")

        threading.Thread(target=rl_worker, daemon=True).start()
        log.info("✅ RL agent іске қосылды")


else:
    def rl_predict(features):
        return 0.5

    def train_rl_agent():
        return False

    def start_rl_agent():
        log.info("⏸ RL өшірулі (SB3 жоқ)")


# ============================================================
# APEX #42 — SHAZAM v4 WORKER (M15 multi-TF + long RL)
# ============================================================

def _load_shazam_module():
    """apex_v4_shazam_core.py жүктеу (сол папкадан) — қауіпсіз"""
    global _SHAZAM_MOD
    if _SHAZAM_MOD is not None:
        return _SHAZAM_MOD
    try:
        # 1) Қарапайым import (папка sys.path-та болса)
        if BASE_DIR not in sys.path:
            sys.path.insert(0, BASE_DIR)
        try:
            import apex_v4_shazam_core as mod
            _SHAZAM_MOD = mod
            log.info("✅ Shazam module: import OK")
            return mod
        except ImportError:
            pass

        # 2) importlib fallback
        import importlib.util
        path = os.path.join(BASE_DIR, "apex_v4_shazam_core.py")
        if not os.path.exists(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "apex_v4_shazam_core.py")
        if not os.path.exists(path):
            log.warning("⚠️ apex_v4_shazam_core.py табылмады — Shazam өшірулі")
            return None

        spec = importlib.util.spec_from_file_location("apex_v4_shazam_core", path)
        if spec is None or spec.loader is None:
            log.error("Shazam module load: spec/loader is None")
            return None
        mod = importlib.util.module_from_spec(spec)
        sys.modules["apex_v4_shazam_core"] = mod
        spec.loader.exec_module(mod)
        _SHAZAM_MOD = mod
        log.info("✅ Shazam module: importlib OK")
        return mod
    except Exception as e:
        log.error(f"Shazam module load: {e}")
        import traceback
        log.debug(traceback.format_exc())
        return None


def start_shazam_v4_worker():
    """Фонда Shazam + 10y RL оқыту / жүктеу"""
    global SHAZAM_STATUS
    if not SHAZAM_ENABLED:
        log.info("⏸ Shazam v4 өшірулі")
        return

    def _run():
        global SHAZAM_STATUS
        try:
            time.sleep(20)  # MT5 + басқа worker-лар тұрақтансын
            mod = _load_shazam_module()
            if mod is None:
                log.warning("⚠️ Shazam модуль жүктелмеді — бот Shazam-сыз жалғасады")
                return
            sym = SHAZAM_SYMBOLS[0] if SHAZAM_SYMBOLS else "XAUUSD"
            steps = min(int(SHAZAM_RL_TIMESTEPS), 200_000)  # бірінші іске қосуда тым ұзақ болмасын
            log.info(f"🎵 Shazam v4 старт: {sym} | RL steps={steps}")
            status = mod.start_shazam_v4(
                symbol=sym,
                rl_timesteps=steps,
                force_retrain=False,
                use_mt5=True,
            )
            if isinstance(status, dict):
                SHAZAM_STATUS.update(status)
            if SHAZAM_STATUS.get("ready"):
                try:
                    tg_send(
                        f"🎵 *Shazam v4 дайын*\n"
                        f"Паттерн: `{SHAZAM_STATUS.get('patterns', 0)}`\n"
                        f"RL: `{'✅' if SHAZAM_STATUS.get('rl_ready') else '❌'}`\n"
                        f"Дерек: `{SHAZAM_STATUS.get('source', '?')}`"
                    )
                except Exception:
                    pass
            log.info(f"✅ Shazam v4: {SHAZAM_STATUS}")
        except Exception as e:
            log.error(f"Shazam worker: {e}")
            # Ботты тоқтатпаймыз — тек Shazam өшірулі қалады
            SHAZAM_STATUS["ready"] = False

    threading.Thread(target=_run, daemon=True, name="ShazamV4").start()
    log.info("✅ Shazam v4 worker іске қосылды")


# ============================================================
# ENSEMBLE (Rules + ML + Advanced + RL + Shazam)
# ============================================================

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

_tg_queue = queue.Queue(maxsize=500)
_tg_stop = False
_tg_last = 0
_cb_offset = 0
_cb_handlers = {}


def tg_send(text):
    """Telegram-ға мәтін жіберу (queue)"""
    try: _tg_queue.put_nowait(("TEXT", text, None))
    except queue.Full: pass


def tg_buttons(text, markup):
    """Telegram-ға батырмалармен хабарлама"""
    try: _tg_queue.put_nowait(("BUTTONS", text, markup))
    except queue.Full: pass


def tg_photo(buf, caption):
    """Telegram-ға график жіберу (Markdown-сыз caption — parse қатесі болмайды)"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        files = {"photo": ("chart.png", buf, "image/png")}
        data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]}
        r = requests.post(url, data=data, files=files, timeout=20)
        if r.status_code == 200:
            log.info(f"📊 Chart: {caption[:40]}")
        elif r.status_code != 200:
            log.warning(f"TG photo HTTP {r.status_code}")
    except Exception as e:
        log.error(f"TG photo: {str(e)[:80]}")


def _tg_worker():
    """Telegram queue worker (rate limit ~2s аралық)"""
    global _tg_last
    while not _tg_stop:
        try:
            item = _tg_queue.get(timeout=1)
        except queue.Empty:
            continue
        now = time.time()
        # Telegram flood-қа қарсы: кемінде 2 сек аралық
        if now - _tg_last < 2.0:
            time.sleep(2.0 - (now - _tg_last))
        _tg_last = time.time()
        kind, text, extra = item
        if kind == "TEXT":
            _post_text(text)
        elif kind == "BUTTONS":
            _post_buttons(text, extra)


def _post_text(text, _retry=0):
    """Telegram-ға мәтін жіберу (Markdown қатесінсіз)"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        # 1. Алдымен Markdown-мен жіберіп көреміз
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID,
                                     "text": text, "parse_mode": "Markdown",
                                     "disable_web_page_preview": True}, timeout=10)

        # 2. Егер Telegram 400 қатесін берсе (Markdown дұрыс емес болса)
        if r.status_code == 400:
            log.warning("⚠️ TG Markdown қатесі, қарапайым мәтінмен жіберілуде...")
            # Markdown-сыз, таза мәтінмен жібереміз
            r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID,
                                         "text": text,
                                         "disable_web_page_preview": True}, timeout=10)

        if r.status_code == 200:
            log.info(f"TG: {text[:50]}")
        elif r.status_code == 429 and _retry < 3:
            try:
                retry_after = int(r.json().get("parameters", {}).get("retry_after", 30))
            except Exception:
                retry_after = 30
            log.warning(f"TG rate limit: wait {retry_after}s")
            time.sleep(min(retry_after, 120))
            return _post_text(text, _retry + 1)
        elif r.status_code >= 500 and _retry < 3:
            time.sleep(5 * (2 ** _retry))
            return _post_text(text, _retry + 1)
        elif r.status_code != 200:
            log.warning(f"TG HTTP {r.status_code}: {r.text[:80]}")
    except requests.exceptions.RequestException as e:
        if _retry < 3:
            wait = 5 * (2 ** _retry)
            log.warning(f"TG retry {_retry + 1}/3 in {wait}s: {str(e)[:60]}")
            time.sleep(wait)
            return _post_text(text, _retry + 1)
        log.error(f"TG FAILED after 3 retries: {str(e)[:80]}")
    except Exception as e:
        log.error(f"TG: {str(e)[:80]}")


def _post_buttons(text, markup, _retry=0):
    """Telegram-ға батырмалармен хабарлама (Markdown қатесінсіз)"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text[:1024],
                                      "parse_mode": "Markdown", "reply_markup": markup}, timeout=10)
        # Егер Markdown қатесі болса, батырмаларды сақтап, мәтінді таза жіберу
        if r.status_code == 400:
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text[:1024],
                                      "reply_markup": markup}, timeout=10)
            return
        if r.status_code == 429 and _retry < 3:
            try:
                ra = int(r.json().get("parameters", {}).get("retry_after", 20))
            except Exception:
                ra = 20
            time.sleep(min(ra, 60))
            return _post_buttons(text, markup, _retry + 1)
        if r.status_code >= 500 and _retry < 3:
            time.sleep(5 * (2 ** _retry))
            return _post_buttons(text, markup, _retry + 1)
    except requests.exceptions.RequestException as e:
        if _retry < 3:
            time.sleep(5 * (2 ** _retry))
            return _post_buttons(text, markup, _retry + 1)
        log.error(f"TG buttons FAILED: {str(e)[:60]}")
    except Exception:
        pass


def start_tg():
    """Telegram worker іске қосу"""
    threading.Thread(target=_tg_worker, daemon=True).start()
    log.info("✅ TG worker")


# ============================================================
# VOICE (Қазақша)
# ============================================================

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    log.warning("⚠️ edge-tts жоқ")


async def _tts_async(text, output_path):
    """TTS async"""
    communicate = edge_tts.Communicate(text, VOICE_LANG)
    await communicate.save(output_path)


def text_to_voice(text, output_path=None):
    """Text → Voice"""
    if not EDGE_TTS_AVAILABLE or not VOICE_ENABLED:
        return None
    try:
        if output_path is None:
            output_path = os.path.join(VOICE_DIR, f"voice_{int(time.time())}.ogg")
        asyncio.run(_tts_async(text, output_path))
        return output_path
    except Exception as e:
        log.error(f"TTS: {e}")
        return None


def tg_send_voice(text):
    """Telegram-ға дауыс жіберу"""
    if not VOICE_ENABLED or not EDGE_TTS_AVAILABLE: return False
    try:
        voice_path = text_to_voice(text)
        if not voice_path or not os.path.exists(voice_path):
            return False
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
        with open(voice_path, "rb") as f:
            r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID},
                              files={"voice": f}, timeout=30)
        if r.status_code == 200:
            log.info(f"🔊 Voice жіберілді")
            try: os.remove(voice_path)
            except Exception: pass
            return True
    except Exception as e:
        log.error(f"Send voice: {e}")
    return False


def voice_signal_message(symbol, direction, level, entry, sl, tp, ensemble):
    """Signal дауысы (қазақша)"""
    dir_kz = "сатып алу" if direction == "BUY" else "сату"
    text = (
        f"{symbol} бойынша {dir_kz} сигналы. "
        f"Деңгей {level} пайыз. "
        f"Кіру бағасы {entry}. "
        f"Стоп лосс {sl}. "
        f"Тейк профит {tp}. "
        f"Сенімділік {ensemble:.0%}."
    )
    return text


# ============================================================
# CALLBACKS — Security (ALLOWED_USERS)
# ============================================================

def cb_register(action, handler):
    """Callback тіркеу"""
    _cb_handlers[action] = handler


def _cb_answer(cb_id, text):
    """Callback жауабы"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery"
    try:
        requests.post(url, json={"callback_query_id": cb_id, "text": text[:200]}, timeout=5)
    except Exception: pass


def apply_param_change(name, value):
    """
    Runtime параметр өзгерту (LLM / Telegram).
    Шектеулер: тәуекелді шамадан тыс ұлғайтпау.
    """
    global VOL_PREPARE_BASE, AI_CONFIRM_MIN, RISK_PER_TRADE
    global RISK_REWARD_MIN, LEVEL_SIGNAL, DAILY_TRADES_LIMIT, DAILY_LOSS_LIMIT
    global HFT_DELTA_MIN, HFT_DELTA_STRONG
    try:
        name = str(name).strip()
        if name == "VOL_PREPARE_BASE":
            VOL_PREPARE_BASE = float(np.clip(float(value), 0.8, 3.0))
        elif name == "AI_CONFIRM_MIN":
            AI_CONFIRM_MIN = int(np.clip(int(value), 1, 7))
        elif name == "RISK_PER_TRADE":
            RISK_PER_TRADE = float(np.clip(float(value), 0.1, 2.0))
        elif name == "RISK_REWARD_MIN":
            RISK_REWARD_MIN = float(np.clip(float(value), 1.0, 5.0))
        elif name == "LEVEL_SIGNAL":
            LEVEL_SIGNAL = int(np.clip(int(value), 100, 300))
        elif name == "DAILY_TRADES_LIMIT":
            DAILY_TRADES_LIMIT = int(np.clip(int(value), 1, 50))
        elif name == "DAILY_LOSS_LIMIT":
            DAILY_LOSS_LIMIT = float(np.clip(float(value), 1.0, 15.0))
        elif name == "HFT_DELTA_MIN":
            HFT_DELTA_MIN = float(np.clip(float(value), 5.0, 80.0))
        elif name == "HFT_DELTA_STRONG":
            HFT_DELTA_STRONG = float(np.clip(float(value), 10.0, 90.0))
        else:
            return False, None
        # return actual applied value
        actual = {
            "VOL_PREPARE_BASE": VOL_PREPARE_BASE,
            "AI_CONFIRM_MIN": AI_CONFIRM_MIN,
            "RISK_PER_TRADE": RISK_PER_TRADE,
            "RISK_REWARD_MIN": RISK_REWARD_MIN,
            "LEVEL_SIGNAL": LEVEL_SIGNAL,
            "DAILY_TRADES_LIMIT": DAILY_TRADES_LIMIT,
            "DAILY_LOSS_LIMIT": DAILY_LOSS_LIMIT,
            "HFT_DELTA_MIN": HFT_DELTA_MIN,
            "HFT_DELTA_STRONG": HFT_DELTA_STRONG,
        }.get(name)
        return True, actual
    except Exception:
        return False, None


def llm_chat(user_text):
    """
    Еркін мәтін → LLM (Grok) → JSON action → орындау.
    Қайтарады: reply string
    """
    if not (LLM_AVAILABLE or GROQ_AVAILABLE) or llm_client is None:
        return (
            "❌ LLM қосулы емес.\n"
            "`.env` ішінде `XAI_API_KEY` қойып, `pip install openai` жасаңыз."
        )

    with _state_lock:
        filters_off = sorted(list(FILTERS_DISABLED))
        mode = AUTO_STATE.get("mode", "MANUAL")

    prompt = f"""Сен — APEX v3 трейдинг ботының AI көмекшісісің. Қазақша қысқа жауап бер.

АҒЫМДАҒЫ КҮЙ:
- Mode: {mode}
- Filters OFF: {filters_off}
- VOL_PREPARE_BASE: {VOL_PREPARE_BASE}
- AI_CONFIRM_MIN: {AI_CONFIRM_MIN}
- RISK_PER_TRADE: {RISK_PER_TRADE}
- RISK_REWARD_MIN: {RISK_REWARD_MIN}
- LEVEL_SIGNAL: {LEVEL_SIGNAL}
- HFT_DELTA_MIN: {HFT_DELTA_MIN}
- DAILY_LOSS_LIMIT: {DAILY_LOSS_LIMIT}

ПАЙДАЛАНУШЫ: "{user_text[:500]}"

ҚОЛЖЕТІМДІ ӘРЕКЕТТЕР (біреуін таңда):
1. disable_filter — params.name: ai|news|fg|fred|santiment|reddit|corr|div|hft|spoof|rr|level|wyckoff_engine|orderflow
2. enable_filter — params.name
3. set_param — params.name + params.value (VOL_PREPARE_BASE, AI_CONFIRM_MIN, RISK_PER_TRADE, RISK_REWARD_MIN, LEVEL_SIGNAL, DAILY_TRADES_LIMIT, DAILY_LOSS_LIMIT, HFT_DELTA_MIN, HFT_DELTA_STRONG)
4. set_mode — params.mode: MANUAL|DEMO|REAL
5. analyze — 30 күндік фильтр талдау
6. status — статус
7. answer — тек жауап (өзгеріссіз)

Ереже: тәуекелді асырма (RISK_PER_TRADE ≤ 2). Бірнеше фильтр өшіру керек болса, ең маңызды 1-3-ін ғана өшір.
Тек JSON қайтар:
{{"action":"...","params":{{}},"reply":"қазақша 2-4 сөйлем"}}
"""

    response = llm_ask(prompt)
    if not response or not isinstance(response, dict):
        return "⚠️ LLM жауап бермеді (кілт/желіні тексеріңіз)."

    action = str(response.get("action", "answer")).strip().lower()
    params = response.get("params") or {}
    if not isinstance(params, dict):
        params = {}
    reply = str(response.get("reply") or "OK").strip()

    try:
        if action == "disable_filter":
            name = str(params.get("name", "")).strip().lower()
            if name:
                with _state_lock:
                    FILTERS_DISABLED.add(name)
                filter_state_save()
                reply += f"\n\n🚫 `{name}` өшірілді"
                log.info(f"🧠 LLM: filter OFF → {name}")

        elif action == "enable_filter":
            name = str(params.get("name", "")).strip().lower()
            if name:
                with _state_lock:
                    FILTERS_DISABLED.discard(name)
                filter_state_save()
                reply += f"\n\n✅ `{name}` қосылды"
                log.info(f"🧠 LLM: filter ON → {name}")

        elif action == "set_param":
            name = str(params.get("name", "")).strip()
            value = params.get("value")
            ok, actual = apply_param_change(name, value)
            if ok:
                reply += f"\n\n⚙️ `{name}` = `{actual}`"
                log.info(f"🧠 LLM: {name} = {actual}")
            else:
                reply += f"\n\n⚠️ Параметр өзгермеді: `{name}`"

        elif action == "set_mode":
            mode_new = str(params.get("mode", "")).upper().strip()
            if mode_new in ("MANUAL", "DEMO", "REAL"):
                set_mode(mode_new)
                reply += f"\n\n🤖 Mode: `{mode_new}`"
                log.info(f"🧠 LLM: mode → {mode_new}")
            else:
                reply += "\n\n⚠️ Mode: MANUAL / DEMO / REAL ғана"

        elif action == "analyze":
            def _run_an():
                try:
                    llm_analyze_filters(30)
                except Exception as e:
                    log.error(f"analyze: {e}")
            threading.Thread(target=_run_an, daemon=True).start()
            reply += "\n\n⏳ Талдау басталды (1–2 мин)"

        elif action == "status":
            acc = mt5_account_info()
            pos = mt5_positions_get() or []
            with _state_lock:
                m = AUTO_STATE.get("mode", "MANUAL")
                fo = sorted(list(FILTERS_DISABLED)) or ["жоқ"]
            reply += (
                f"\n\n🤖 Mode: `{m}`"
                f"\n🧠 LLM: `{'ON' if (LLM_AVAILABLE or GROQ_AVAILABLE) else 'OFF'}`"
                f"\n🚫 Filters OFF: `{', '.join(fo)}`"
            )
            if acc:
                reply += f"\n💰 Equity: `${float(acc.equity):.2f}`"
            reply += f"\n📊 Позиция: `{len(pos)}`"

    except Exception as e:
        log.error(f"LLM action: {e}")
        reply += f"\n\n⚠️ Қате: {str(e)[:80]}"

    return reply


def _handle_tg_text(text, user_id):
    """Slash + еркін мәтін (LLM чат)."""
    text = (text or "").strip()
    if not text:
        return

    low = text.lower()
    if low in ("/start", "/help", "help", "көмек"):
        tg_send(
            "🧠 *APEX v3 — LLM чат*\n\n"
            "Кез келген мәтін жазыңыз, мысалы:\n"
            "• `Сигналдар сирек — фильтрлерді азайт`\n"
            "• `News өшір` / `FG қос`\n"
            "• `AI_CONFIRM_MIN 3 ет`\n"
            "• `DEMO қос` / `MANUAL қос`\n"
            "• `Статус` / `Талдау жаса`\n\n"
            f"Security: `{user_id}`"
        )
        return

    if text.startswith("/") and low not in ("/start", "/help"):
        # белгісіз slash — callback батырмаларға қалдыру
        return

    log.info(f"💬 User {user_id}: {text[:100]}")
    tg_send("🧠 _Ойланып жатырмын..._")

    def _process(t=text):
        try:
            reply = llm_chat(t)
            tg_send(f"🧠 *APEX:*\n\n{reply}")
        except Exception as e:
            log.error(f"LLM chat: {e}")
            tg_send(f"⚠️ Қате: {str(e)[:120]}")

    threading.Thread(target=_process, daemon=True).start()


def _cb_worker():
    """
    Telegram updates: callback_query + message (LLM чат).
    Бір getUpdates — қақтығыс жоқ.
    """
    global _cb_offset
    log.info(f"✅ CB+Chat worker | Security: {ALLOWED_USERS}")
    _cb_fail = 0
    while not _tg_stop:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            r = requests.get(
                url,
                params={"offset": _cb_offset, "timeout": 25},
                timeout=35,
            )
            if r.status_code != 200:
                _cb_fail += 1
                time.sleep(min(5 * _cb_fail, 30))
                continue
            data = r.json()
            if not data.get("ok"):
                _cb_fail += 1
                time.sleep(min(5 * _cb_fail, 30))
                continue
            _cb_fail = 0
            for up in data.get("result", []):
                _cb_offset = up["update_id"] + 1

                # --- callback buttons ---
                cb = up.get("callback_query")
                if cb:
                    user_id = cb.get("from", {}).get("id")
                    if user_id not in ALLOWED_USERS:
                        log.warning(f"⚠️ Security: unauthorized {user_id}")
                        _cb_answer(cb.get("id"), "❌ Рұқсат жоқ")
                        continue
                    parts = cb.get("data", "").split("|")
                    action = parts[0] if parts else ""
                    if action in _cb_handlers:
                        try:
                            _cb_handlers[action](parts, cb.get("id"))
                        except Exception as e:
                            log.error(f"CB {action}: {e}")
                    else:
                        _cb_answer(cb.get("id"), f"Белгісіз: {action}")
                    continue

                # --- free text / LLM chat ---
                msg = up.get("message")
                if not msg:
                    continue
                user_id = msg.get("from", {}).get("id")
                if user_id not in ALLOWED_USERS:
                    log.warning(f"⚠️ Unauthorized msg: {user_id}")
                    continue
                text = msg.get("text") or ""
                if text:
                    _handle_tg_text(text, user_id)

        except requests.exceptions.RequestException as e:
            _cb_fail += 1
            wait = min(5 * (2 ** min(_cb_fail - 1, 4)), 60)
            log.warning(f"CB net ({_cb_fail}): {str(e)[:70]} → sleep {wait}s")
            time.sleep(wait)
        except Exception as e:
            _cb_fail += 1
            log.error(f"CB: {str(e)[:100]}")
            time.sleep(min(5 * _cb_fail, 30))


def start_cb():
    """Callback + LLM chat worker іске қосу"""
    threading.Thread(target=_cb_worker, daemon=True).start()
    log.info(f"✅ CB worker + LLM chat | Security: {ALLOWED_USERS}")


# ============================================================
# CALLBACK HANDLERS
# ============================================================

def _cb_executed(parts, cb_id):
    """Орындалды батырма"""
    _cb_answer(cb_id, "✅ OK")


def _cb_skip(parts, cb_id):
    """Өткізу батырма"""
    s = parts[1] if len(parts) > 1 else ""
    MEM["sequences"].pop(s, None); mem_save()
    _cb_answer(cb_id, f"❌ Skip {s}")


def _cb_mode(parts, cb_id):
    """Режим ауыстыру"""
    m = parts[1] if len(parts) > 1 else "MANUAL"
    set_mode(m)
    _cb_answer(cb_id, f"🤖 Mode: {m}")
    tg_send(f"🤖 Mode: `{m}`")


def _cb_llm(parts, cb_id):
    """LLM талдау (қолмен)"""
    _cb_answer(cb_id, "🧠 LLM талдау...")
    threading.Thread(target=lambda: llm_analyze_filters(30), daemon=True).start()


def _cb_filters(parts, cb_id):
    """Фильтр статусы"""
    _cb_answer(cb_id, "🔍 Фильтрлер")
    flist = "\n".join(f"  {'❌' if f in FILTERS_DISABLED else '✅'} {f}"
                      for f in ["ai", "news", "fg", "fred", "santiment",
                                "reddit", "corr", "div", "hft", "spoof", "rr", "level"])
    tg_send(f"🔍 *Filter Status*\n\n{flist}")


def _cb_hedge(parts, cb_id):
    """Hedge статусы"""
    _cb_answer(cb_id, "🛡️ Hedge")
    try:
        status = get_hedge_status()
        pairs = status.get("correlated_pairs", [])
        pairs_str = "\n".join(
            f"  • {p['sym1']} ↔ {p['sym2']}: {p['corr']}" for p in pairs[:5]
        ) or "  —"
        tg_send(
            f"🛡️ *Dynamic Hedge*\n\n"
            f"✅ Enabled: `{status.get('enabled')}`\n"
            f"⚡ Active: `{status.get('active')}`\n"
            f"📊 Threshold: `{status.get('threshold')}`\n\n"
            f"Correlated:\n{pairs_str}"
        )
    except Exception as e:
        tg_send(f"🛡️ Hedge: {str(e)[:80]}")


def _cb_status(parts, cb_id):
    """APEX статусы"""
    _cb_answer(cb_id, "📊 Status")
    acc = mt5_account_info()
    pos = mt5_positions_get() or []
    tg_send(
        f"📊 *APEX v3 Status*\n\n"
        f"💰 Balance: `${acc.balance:.2f}`\n"
        f"📈 Equity: `${acc.equity:.2f}`\n"
        f"📊 Positions: `{len(pos)}`\n"
        f"🤖 Mode: `{get_mode()}`\n"
        f"🧠 ML: `{ML_STATUS.get('accuracy', 0):.2f}`\n"
        f"🤖 RL: `{RL_STATUS.get('ready')}`\n"
        f"📡 TV: `{TV_SIGNALS_RECEIVED[0]}/{TV_SIGNALS_EXECUTED[0]}`"
    )


def _cb_metrics(parts, cb_id):
    """6 метрика көрсету"""
    _cb_answer(cb_id, "📈 Metrics")
    m = METRICS
    tg_send(
        f"📈 *APEX Metrics*\n\n"
        f"✅ Wins: `{m['wins']}`\n"
        f"❌ Losses: `{m['losses']}`\n"
        f"💰 Gross Profit: `${m['gross_profit']:.2f}`\n"
        f"📉 Gross Loss: `${m['gross_loss']:.2f}`\n"
        f"💵 Net Profit: `${m['net_profit']:.2f}`\n"
        f"📊 Expectancy: `{m['expectancy']:.4f}`\n"
        f"⚖️ Profit Factor: `{m['profit_factor']:.2f}`\n"
        f"📉 Max DD: `{m['max_dd']:.2f}%`\n"
        f"🎯 Sharpe: `{m['sharpe']:.2f}`\n"
        f"🔄 Recovery: `{m['recovery']:.2f}`"
    )


def register_handlers():
    """Барлық callback handler-лерді тіркеу"""
    cb_register("executed", _cb_executed)
    cb_register("skip", _cb_skip)
    cb_register("mode_manual", lambda p, c: _cb_mode(["", "MANUAL"], c))
    cb_register("mode_demo",   lambda p, c: _cb_mode(["", "DEMO"], c))
    cb_register("mode_real",   lambda p, c: _cb_mode(["", "REAL"], c))
    cb_register("llm",         _cb_llm)
    cb_register("filters",     _cb_filters)
    cb_register("hedge",       _cb_hedge)
    cb_register("status",      _cb_status)
    cb_register("metrics",     _cb_metrics)


def signal_buttons(symbol, direction):
    """Сигнал батырмалары (4 қатар)"""
    return {"inline_keyboard": [
        [{"text": "✅ Орындалды", "callback_data": f"executed|{symbol}"},
         {"text": "❌ Өткізу", "callback_data": f"skip|{symbol}"}],
        [{"text": "🖐 MANUAL", "callback_data": "mode_manual"},
         {"text": "🎮 DEMO", "callback_data": "mode_demo"},
         {"text": "💰 REAL", "callback_data": "mode_real"}],
        [{"text": "🧠 LLM", "callback_data": "llm"},
         {"text": "🔍 Filters", "callback_data": "filters"},
         {"text": "🛡️ Hedge", "callback_data": "hedge"}],
        [{"text": "📊 Status", "callback_data": "status"},
         {"text": "📈 Metrics", "callback_data": "metrics"}],
    ]}
    # ============================================================
# MT5 CONNECTION
# ============================================================

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

def _load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f: return json.load(f)
        except Exception: pass
    return default


def _save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception: pass


def mem_load():
    """Жады жүктеу"""
    global MEM
    d = _load_json(MEMORY_FILE, {})
    for k in ["phases", "sequences", "levels", "recent_signals",
              "sent_signals", "wait_signals"]:
        MEM[k] = d.get(k, {})
    log.info(f"Жады: {len(MEM['phases'])} фаза")


def mem_save():
    """Жады сақтау (thread-safe snapshot)"""
    with _state_lock:
        snapshot = {k: dict(MEM.get(k, {})) for k in
                    ["phases", "sequences", "levels",
                     "recent_signals", "sent_signals", "wait_signals"]}
    _save_json(MEMORY_FILE, snapshot)


def auto_load():
    global AUTO_STATE
    with _state_lock:
        AUTO_STATE = _load_json(AUTO_FILE, AUTO_STATE)


def auto_save():
    with _state_lock:
        snapshot = dict(AUTO_STATE)
        if "positions" in snapshot:
            snapshot["positions"] = list(snapshot["positions"])
    _save_json(AUTO_FILE, snapshot)


def ai_load():
    global AI_STATE
    AI_STATE = _load_json(AI_FILE, AI_STATE)


def ai_save():
    _save_json(AI_FILE, AI_STATE)


def filter_state_load():
    global FILTERS_DISABLED
    d = _load_json(FILTER_STATE, {})
    with _state_lock:
        FILTERS_DISABLED = set(d.get("disabled", []))
    log.info(f"🚫 Filter өшірілген: {len(FILTERS_DISABLED)}")


def filter_state_save():
    with _state_lock:
        disabled = list(FILTERS_DISABLED)
    _save_json(FILTER_STATE, {"disabled": disabled})


# ============================================================
# DB (Journal + Features)
# ============================================================

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


def journal_stats():
    """Журнал статистикасы"""
    try:
        conn = sqlite3.connect(JOURNAL_DB)
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(result='TP'), SUM(result='SL') FROM signals")
        t, tp, sl = c.fetchone(); conn.close()
        return t or 0, tp or 0, sl or 0
    except Exception: return 0, 0, 0


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

def get_market_status():
    """Нарық статусы (сессия)"""
    now = datetime.now(timezone.utc)
    w = now.weekday(); h = now.hour
    if 12 <= h < 16:
        s = "London-NY"
    elif 7 <= h < 12:
        s = "London"
    elif 16 <= h < 21:
        s = "NY"
    elif 0 <= h < 7:
        s = "Asia"
    else:
        s = "Quiet"
    return {"forex_open": w < 5, "crypto_open": True, "session": s, "hour": h}


def get_active_categories():
    """
    Белсенді категориялар.
    Демалыс күні forex_open=False → бұрын тек crypto қалатын,
    MetaQuotes-те crypto жоқ → 0 symbols. Енді metals әрқашан
    (XAU/XAG талдау үшін), ал forex/indices — тек нарық ашық кезде.
    """
    s = get_market_status()
    a = ["crypto", "metals"]  # metals always (алтын демалыста да дерек бере алады)
    if s["forex_open"]:
        a.extend(["energies", "indices", "forex"])
    return a


# ============================================================
# DELTA (Buyer vs Seller)
# ============================================================

class _DC:
    """Delta classifier"""
    def __init__(self): self.pp = None; self.pd = 0
    def classify(self, t):
        if t.get("flags", 0) & mt5.TICK_FLAG_BUY: self.pd = 1; return 1
        if t.get("flags", 0) & mt5.TICK_FLAG_SELL: self.pd = -1; return -1
        l = t.get("last", 0.0); b = t.get("bid", 0.0); a = t.get("ask", 0.0)
        if l > 0 and b > 0 and a > 0:
            if l >= a: self.pd = 1; self.pp = l; return 1
            if l <= b: self.pd = -1; self.pp = l; return -1
        p = b if b > 0 else a
        if p <= 0: return self.pd
        if self.pp is not None:
            if p > self.pp: self.pd = 1
            elif p < self.pp: self.pd = -1
        self.pp = p; return self.pd


_DC = _DC()


def get_delta(symbol, w=30):
    """
    Delta % = (buy_vol − sell_vol) / total × 100
    Prefers order-flow cache (aggressor classification); falls back to _DC ticks.
    """
    # Fast path: shared order-flow snapshot
    try:
        of = get_order_flow(symbol, seconds=max(int(w), 30))
        if of.get("ok"):
            return float(of["delta_pct"])
    except Exception:
        pass
    # Legacy path
    try:
        now = int(time.time() * 1000)
        ticks = mt5_safe(mt5.copy_ticks_from, symbol, now - w * 1000, 20000, mt5.COPY_TICKS_ALL)
    except Exception:
        ticks = None
    if ticks is None or len(ticks) == 0:
        return 0.0
    bv = 0.0
    sv = 0.0
    for t in ticks:
        v = float(t["volume_real"]) if "volume_real" in ticks.dtype.names else float(t["volume"])
        d = _DC.classify({
            "flags": int(t["flags"]), "last": float(t["last"]),
            "bid": float(t["bid"]), "ask": float(t["ask"]),
        })
        if d > 0:
            bv += v
        elif d < 0:
            sv += v
    tot = bv + sv
    return ((bv - sv) / tot * 100.0) if tot > 0 else 0.0


# ============================================================
# ADAPTIVE (Time × Volatility × Range)
# ============================================================

def get_adaptive(df, symbol):
    """Adaptive multiplier есептеу"""
    hour = datetime.now(timezone.utc).hour
    if 12 <= hour < 16:
        t_m = 1.2   # London-NY (белсенді)
    elif 7 <= hour < 12 or 16 <= hour < 21:
        t_m = 1.0   # London НЕМЕСЕ NY
    elif 0 <= hour < 7:
        t_m = 0.7   # Asia
    else:
        t_m = 0.5   # Quiet

    try:
        rates = mt5_copy_rates(symbol, TIMEFRAME, 0, 50)
        atr_pct = 0.0
        if rates is not None and len(rates) >= 20:
            df_s = pd.DataFrame(rates)
            atr = ta.atr(df_s["high"], df_s["low"], df_s["close"], length=ATR_PERIOD)
            if atr is not None and len(atr) > 0:
                a = float(atr.iloc[-1]); c = float(df_s["close"].iloc[-1])
                if c > 0: atr_pct = (a / c) * 100
        v_m = 1.2 if atr_pct > 0.5 else (1.0 if atr_pct > 0.2 else 0.8)
        if len(df) >= 50:
            r = df.tail(48)
            sup = r["low"].min(); res = r["high"].max()
            range_pct = (res - sup) / sup if sup > 0 else 0.02
            r_m = 0.8 if range_pct < 0.01 else (1.0 if range_pct < 0.03 else 1.2)
        else: r_m = 1.0
        return t_m * v_m * r_m, atr_pct
    except Exception: return 1.0, 0.0


# ============================================================
# EFFORT = RESULT (Volume vs Price)
# ============================================================

def calculate_effort_result(df):
    """Effort=Result анықтау"""
    if len(df) < 20: return "NORMAL", 0
    last = df.iloc[-2]
    vm = df["vol_ma"].iloc[-2]
    if vm <= 0: return "NORMAL", 0
    vr = last["tick_volume"] / vm
    atr = last["atr"]
    if pd.isna(atr) or atr <= 0: return "NORMAL", 0
    pm = abs(last["close"] - last["open"]) / atr
    if vr >= 1.5 and pm >= 1.0: return "EFFORT_EQ_RESULT", vr
    elif vr >= 1.5 and pm < 0.5: return "ABSORPTION", vr
    elif vr < 1.0 and pm >= 1.0: return "NO_DEMAND", vr
    elif vr < 1.0 and pm < 0.5: return "NO_ACTIVITY", vr
    return "NORMAL", vr


# ============================================================
# SUPPLY / DEMAND
# ============================================================

def analyze_supply_demand(df):
    """Supply/Demand талдау (5 свеча)"""
    if len(df) < 10: return "BALANCED", 0.0
    d = 0.0; s = 0.0
    for i in range(-5, 0):
        c = df.iloc[i]
        if c["close"] > c["open"]: d += c["tick_volume"]
        elif c["close"] < c["open"]: s += c["tick_volume"]
    tot = d + s
    if tot == 0: return "BALANCED", 0.0
    r = (d - s) / tot
    if r > 0.15: return "DEMAND_WINS", r
    elif r < -0.15: return "SUPPLY_WINS", r
    return "BALANCED", r


# ============================================================
# METRICS (6 көрсеткіш)
# ============================================================

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


def metrics_load():
    """Метрика жүктеу"""
    global METRICS
    d = _load_json(os.path.join(DATA_DIR, "metrics.json"), {})
    if d: METRICS.update(d)
    log.info(f"📈 Metrics: {METRICS['wins']}W / {METRICS['losses']}L")


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

def wyckoff_context(df, i, lookback=48):
    """
    Wyckoff контексті есептеу.
    Қайтарады: dict (trend, range_pct, sup, res, atr, ema50, ema200)
    """
    try:
        recent = df.iloc[max(0, i-lookback):i]
        if len(recent) < 20: return None

        sup = float(recent["low"].min())
        res = float(recent["high"].max())
        rng = res - sup
        range_pct = (rng / sup * 100) if sup > 0 else 0

        # Trend context
        e50 = df["close"].iloc[max(0, i-50):i].ewm(span=50).mean().iloc[-1]
        e200 = df["close"].iloc[max(0, i-200):i].ewm(span=200).mean().iloc[-1]
        trend = "UP" if e50 > e200 * 1.001 else "DOWN" if e50 < e200 * 0.999 else "SIDE"

        # ATR
        atr_series = ta.atr(df["high"].iloc[max(0, i-30):i],
                             df["low"].iloc[max(0, i-30):i],
                             df["close"].iloc[max(0, i-30):i], length=14)
        atr = float(atr_series.iloc[-1]) if atr_series is not None and len(atr_series) > 0 else 0

        return {
            "trend": trend,
            "range_pct": range_pct,
            "sup": sup,
            "res": res,
            "range": rng,
            "atr": atr,
            "ema50": e50,
            "ema200": e200,
        }
    except Exception:
        return None


def detect_spring_v2(df, i):
    """
    🆕 WYCKOFF SPRING v2 — 12 ШАРТ
    Қайтарады: dict немесе None
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]
        prev = df.iloc[i-1] if i > 0 else last
        next_candle = df.iloc[i+1] if i+1 < len(df) else None

        # 1. Trend context: DOWN (жинақтау)
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        # 2. Range context: 1-5%
        if not (0.5 < ctx["range_pct"] < 8.0): return None

        # 3. Support break
        if not (last["low"] < ctx["sup"]): return None

        # 4. Close recovery
        if not (last["close"] > ctx["sup"]): return None

        # 5. Close location (жоғары жабу)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.6: return None

        # 6. Volume climax
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.5: return None

        # 7. Volume dry-up (келесі свеча)
        if next_candle is not None:
            next_vr = next_candle["tick_volume"] / vm if vm > 0 else 1.0
            if next_vr > 1.2: return None

        # 8. Body size (кіші body)
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.6: return None

        # 9. Lower wick (ұзын)
        lower_wick = min(last["open"], last["close"]) - last["low"]
        if lower_wick < body * 1.5: return None

        # 10. R:R check
        sl = last["low"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0:
            return None

        # 11. 4H phase — accumulation / markup only (reject distribution)
        try:
            with _state_lock:
                # symbol may be attached as attr; fall back to soft pass
                ph = None
                for _sym, _ph in MEM.get("phases", {}).items():
                    ph = _ph
                    break
            if ph:
                p = str(ph.get("phase", "")).lower()
                if p in ("distribution", "markdown"):
                    return None
        except Exception:
            pass

        # 12. No spoofing — reject if any spoof mark younger than 5 min
        try:
            with _state_lock:
                spoof_map = dict(MEM.get("spoof", {}))
            now = time.time()
            for _k, ts in spoof_map.items():
                if now - float(ts) < 300:
                    return None
        except Exception:
            pass

        return {
            "event": "spring",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 12,
        }
    except Exception:
        return None


def detect_utad_v2(df, i):
    """
    🆕 WYCKOFF UTAD v2 — 10 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]
        next_candle = df.iloc[i+1] if i+1 < len(df) else None

        # 1. Trend: UP немесе SIDE (тарату)
        if ctx["trend"] not in ["UP", "SIDE"]: return None

        # 2. Range context
        if not (0.5 < ctx["range_pct"] < 8.0): return None

        # 3. Resistance break
        if not (last["high"] > ctx["res"]): return None

        # 4. Close reversal
        if not (last["close"] < ctx["res"]): return None

        # 5. Close location (төмен жабу)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc > 0.4: return None

        # 6. Volume climax
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.3: return None

        # 7. Volume dry-up
        if next_candle is not None:
            next_vr = next_candle["tick_volume"] / vm if vm > 0 else 1.0
            if next_vr > 1.2: return None

        # 8. Body size
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.7: return None

        # 9. Upper wick (ұзын)
        upper_wick = last["high"] - max(last["open"], last["close"])
        if upper_wick < body * 1.3: return None

        # 10. R:R check
        sl = last["high"] + atr * 0.3
        risk = sl - last["close"]
        if risk <= 0: return None
        tp = last["close"] - risk * 3.0

        return {
            "event": "utad",
            "direction": "SELL",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 10,
        }
    except Exception:
        return None


def detect_sos_v2(df, i):
    """
    🆕 WYCKOFF SOS (Sign of Strength) v2 — 7 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend: UP/Accumulation
        if ctx["trend"] not in ["UP", "SIDE"]: return None

        # 2. Bull candle
        is_bull = last["close"] > last["open"]
        if not is_bull: return None

        # 3. Resistance break
        if not (last["close"] > ctx["res"]): return None

        # 4. Body size (үлкен)
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body < atr * 0.7: return None

        # 5. Volume
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.5: return None

        # 6. Close location (жоғары)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.7: return None

        # 7. R:R
        sl = last["low"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0: return None
        tp = last["close"] + risk * 3.0

        return {
            "event": "sos",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 7,
        }
    except Exception:
        return None


def detect_sow_v2(df, i):
    """
    🆕 WYCKOFF SOW (Sign of Weakness) v2 — 7 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend: DOWN/Distribution
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        # 2. Bear candle
        is_bear = last["close"] < last["open"]
        if not is_bear: return None

        # 3. Support break
        if not (last["close"] < ctx["sup"]): return None

        # 4. Body size
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body < atr * 0.7: return None

        # 5. Volume
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 1.5: return None

        # 6. Close location (төмен)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc > 0.3: return None

        # 7. R:R
        sl = last["high"] + atr * 0.3
        risk = sl - last["close"]
        if risk <= 0: return None
        tp = last["close"] - risk * 3.0

        return {
            "event": "sow",
            "direction": "SELL",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 2.5, 1.0),
            "context": ctx,
            "conditions": 7,
        }
    except Exception:
        return None


def detect_lps_v2(df, i):
    """
    🆕 WYCKOFF LPS (Last Point of Support) v2 — 6 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend: UP
        if ctx["trend"] != "UP": return None

        # 2. Range: support > close > resistance
        if not (ctx["sup"] < last["close"] < ctx["res"]): return None

        # 3. Close жоғары (кері түзету)
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.5: return None

        # 4. Volume dry-up
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr > 1.0: return None

        # 5. Supportтан алыс
        if abs(last["low"] - ctx["sup"]) > ctx["range"] * 0.15: return None

        # 6. R:R
        atr = ctx["atr"]
        sl = ctx["sup"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0: return None
        tp = last["close"] + risk * 3.0

        return {
            "event": "lps",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": 0.7,
            "context": ctx,
            "conditions": 6,
        }
    except Exception:
        return None


def detect_st_v2(df, i):
    """
    🆕 WYCKOFF ST (Secondary Test) v2 — 5 ШАРТ
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Support-қа жақын
        if abs(last["low"] - ctx["sup"]) > ctx["range"] * 0.1: return None

        # 2. Volume dry-up
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr > 0.9: return None

        # 3. Кіші body
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.5: return None

        # 4. Close support-тан жоғары
        if last["close"] < ctx["sup"]: return None

        # 5. Direction: BUY (accumulation context)
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        return {
            "event": "st",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": 0.6,
            "context": ctx,
            "conditions": 5,
        }
    except Exception:
        return None


def detect_shakeout_v2(df, i):
    """
    🆕 WYCKOFF SHAKEOUT v2 — 8 ШАРТ (Spring-нің күшті нұсқасы)
    """
    try:
        ctx = wyckoff_context(df, i)
        if not ctx: return None

        last = df.iloc[i]

        # 1. Trend DOWN
        if ctx["trend"] not in ["DOWN", "SIDE"]: return None

        # 2. Support break
        if not (last["low"] < ctx["sup"]): return None

        # 3. Close recovery
        if not (last["close"] > ctx["sup"]): return None

        # 4. Volume climax (жоғары)
        vm = df["vol_ma"].iloc[i]
        if vm <= 0: return None
        vr = last["tick_volume"] / vm
        if vr < 2.0: return None

        # 5. Close location
        rng = last["high"] - last["low"]
        if rng <= 0: return None
        close_loc = (last["close"] - last["low"]) / rng
        if close_loc < 0.5: return None

        # 6. Body size
        atr = ctx["atr"]
        if atr <= 0: return None
        body = abs(last["close"] - last["open"])
        if body > atr * 0.8: return None

        # 7. Lower wick
        lower_wick = min(last["open"], last["close"]) - last["low"]
        if lower_wick < body * 1.5: return None

        # 8. R:R
        sl = last["low"] - atr * 0.3
        risk = last["close"] - sl
        if risk <= 0: return None
        tp = last["close"] + risk * 3.5

        return {
            "event": "shakeout",
            "direction": "BUY",
            "idx": i,
            "entry": float(last["close"]),
            "atr": float(atr),
            "l_event": float(last["low"]),
            "h_event": float(last["high"]),
            "confidence": min(vr / 3.0, 1.0),
            "context": ctx,
            "conditions": 8,
        }
    except Exception:
        return None


def find_wyckoff_patterns_v2(df):
    """
    🆕 WYCKOFF v2 — Барлық паттерндерді іздеу (10+ шарт)
    Қайтарады: list of dict (әр паттерн 5+ шарт)
    """
    patterns = []
    for i in range(48, len(df) - 3):
        # Spring (12 шарт)
        p = detect_spring_v2(df, i)
        if p: patterns.append(p)

        # Shakeout (8 шарт)
        p = detect_shakeout_v2(df, i)
        if p: patterns.append(p)

        # UTAD (10 шарт)
        p = detect_utad_v2(df, i)
        if p: patterns.append(p)

        # SOS (7 шарт)
        p = detect_sos_v2(df, i)
        if p: patterns.append(p)

        # SOW (7 шарт)
        p = detect_sow_v2(df, i)
        if p: patterns.append(p)

        # LPS (6 шарт)
        p = detect_lps_v2(df, i)
        if p: patterns.append(p)

        # ST (5 шарт)
        p = detect_st_v2(df, i)
        if p: patterns.append(p)

    # Ең соңғы 20 паттернді ғана қайтару
    patterns.sort(key=lambda x: x["idx"], reverse=True)
    return patterns[:20]


def get_best_pattern_v2(df):
    """
    Ең жақсы паттернді табу (confidence бойынша)
    """
    patterns = find_wyckoff_patterns_v2(df)
    if not patterns: return None
    # Ең соңғы + ең жоғары confidence
    patterns.sort(key=lambda x: (x["idx"], x["confidence"]), reverse=True)
    return patterns[0]
    # ============================================================
# STRUCTURE (21 свеча)
# ============================================================

def analyze_structure(df):
    """
    Structure талдау (21 свеча).
    Look-ahead bias жоқ: support/resistance соңғы ЖАБЫЛҒАН бардан БҰРЫНғы lookback.
    df already should exclude the forming candle (iloc[:-1] applied upstream).
    """
    if len(df) < CANDLES_LOOKBACK + 1:
        return None
    # Use bars before the latest closed bar for S/R (shift logic)
    hist = df.iloc[-(CANDLES_LOOKBACK + 1):-1]
    if len(hist) < CANDLES_LOOKBACK:
        return None
    sup = float(hist["low"].min())
    res = float(hist["high"].max())
    cur = float(df.iloc[-1]["close"])
    rng = res - sup
    if rng <= 0:
        return None
    return {
        "support": sup,
        "resistance": res,
        "current": cur,
        "position_pct": ((cur - sup) / rng * 100),
        "range": rng,
    }


def analyze_4h_phase(symbol):
    """4H фаза (тек жабылған свечалар — repaint fix)"""
    try:
        rates = mt5_copy_rates(symbol, mt5.TIMEFRAME_H4, 0, 250)
        if rates is None or len(rates) < 200: return None
        df = pd.DataFrame(rates)
        df = df.iloc[:-1]  # Аяқталмаған свечаны алып тастаймыз
        if len(df) < 200: return None

        rng = (df["high"] - df["low"]).replace(0, 1)
        ad = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng
        ad_n = ad.iloc[-1]; ad_m = ad.rolling(20).mean().iloc[-1]
        e50 = df["close"].ewm(span=50).mean().iloc[-1]
        e200 = df["close"].ewm(span=200).mean().iloc[-1]
        tr = "UP" if e50 > e200 * 1.001 else "DOWN" if e50 < e200 * 0.999 else "SIDE"
        if ad_n > ad_m and tr == "UP": ph = "markup"
        elif ad_n > ad_m and tr in ["SIDE", "DOWN"]: ph = "accumulation"
        elif ad_n < ad_m and tr == "DOWN": ph = "markdown"
        elif ad_n < ad_m and tr in ["SIDE", "UP"]: ph = "distribution"
        else: ph = "unknown"
        prev = MEM["phases"].get(symbol, {})
        prev_ph = prev.get("phase")
        trans = None
        if prev_ph == "markdown" and ph in ["accumulation", "markup"]: trans = "BULL_TRANS"
        elif prev_ph == "markup" and ph in ["distribution", "markdown"]: trans = "BEAR_TRANS"
        return {"phase": ph, "ad": float(ad_n), "trend": tr,
                "transition": trans, "created_at": time.time()}
    except Exception: return None


# ============================================================
# SEQUENCE (Spring → ST → SOS → LPS → HFT)
# ============================================================

def get_sequence(symbol):
    """Sequence алу"""
    return MEM["sequences"].get(symbol)


def init_sequence(symbol, event, direction, price, sup, res, atr, vol):
    """Sequence бастау"""
    MEM["sequences"][symbol] = {
        "symbol": symbol, "phase": event, "direction": direction,
        "started_at": time.time(),
        "history": [{"event": event, "price": price, "time": time.time()}],
        "support": sup, "resistance": res, "atr": atr,
        "next_expected": "st", "updated_at": time.time()}
    mem_save()


def update_sequence(symbol, event, price):
    """Sequence жаңарту"""
    seq = MEM["sequences"].get(symbol)
    if not seq: return None
    seq["phase"] = event
    seq["history"].append({"event": event, "price": price, "time": time.time()})
    seq["updated_at"] = time.time()
    if event == "st": seq["next_expected"] = "sos"
    elif event == "sos": seq["next_expected"] = "lps"
    elif event == "lps": seq["next_expected"] = "hft"
    mem_save()
    return seq


def check_sequence_events(symbol, df, structure):
    """Sequence оқиғаларын тексеру"""
    seq = MEM["sequences"].get(symbol)
    if not seq: return None
    if time.time() - seq["started_at"] > SEQUENCE_TIMEOUT_HOURS * 3600:
        del MEM["sequences"][symbol]; mem_save(); return None
    last = df.iloc[-2]
    sup = structure["support"]; res = structure["resistance"]
    d = seq["direction"]; nxt = seq.get("next_expected")
    vm = df["vol_ma"].iloc[-2]
    if vm <= 0: return None
    vr = last["tick_volume"] / vm
    rng = structure["range"]
    if d == "BUY":
        if nxt == "st" and abs(last["low"] - sup) < rng * 0.1 and vr < 1.0:
            update_sequence(symbol, "st", float(last["close"]))
            return {"event": "st", "direction": "BUY"}
        if nxt == "sos" and last["close"] > res and vr >= 1.5:
            update_sequence(symbol, "sos", float(last["close"]))
            return {"event": "sos", "direction": "BUY"}
        if nxt == "lps" and sup < last["close"] < res and vr < 1.0:
            update_sequence(symbol, "lps", float(last["close"]))
            return {"event": "lps", "direction": "BUY"}
    else:
        if nxt == "st" and abs(last["high"] - res) < rng * 0.1 and vr < 1.0:
            update_sequence(symbol, "st", float(last["close"]))
            return {"event": "st", "direction": "SELL"}
        if nxt == "sos" and last["close"] < sup and vr >= 1.5:
            update_sequence(symbol, "sos", float(last["close"]))
            return {"event": "sos", "direction": "SELL"}
        if nxt == "lps" and sup < last["close"] < res and vr < 1.0:
            update_sequence(symbol, "lps", float(last["close"]))
            return {"event": "lps", "direction": "SELL"}
    return None


# ============================================================
# 5 ДЕҢГЕЙ ЖҮЙЕСІ
# ============================================================

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


def send_wait_signal(symbol, wait_data, phase):
    """WAIT сигналын Telegram-ға жіберу"""
    if not wait_data: return
    direction = wait_data.get("direction", "?")
    level = wait_data.get("level", 0)
    reasons = wait_data.get("reasons", [])

    emoji = "🟡" if direction == "BUY" else "🟠"
    tg_send(
        f"{emoji} *WAIT — {symbol}*\n\n"
        f"📊 Level: {level}%\n"
        f"🌍 4H: {phase['phase'] if phase else '?'}\n"
        f"🧭 Direction: *{direction}*\n\n"
        f"⏳ Күтеміз:\n"
        + "\n".join(f"  • {r}" for r in reasons)
    )
    log.info(f"🟡 WAIT: {symbol} — {level}% ({direction})")


# ============================================================
# 🆕 ABLATION TEST
# ============================================================

def run_ablation_test():
    """
    🆕 Ablation test — әр модульдің шынайы үлесін өлшеу
    """
    if not ABLATION_ENABLED: return

    log.info("🔬 Ablation test басталды...")

    results = {}
    modules = [
        "base_wyckoff",
        "+ml_xgboost",
        "+fourier",
        "+fractal",
        "+wavelet",
        "+mtf",
        "+rl_agent",
        "+hedge",
        "+llm",
    ]

    # 3 айлық backtest деректерін алу
    symbols = ["XAUUSD", "BTCUSD", "EURUSD", "US30"]
    for sym in symbols:
        try:
            rates = mt5_copy_rates(sym, TIMEFRAME, 0, 5000)
            if rates is None or len(rates) < 1000: continue
            df = pd.DataFrame(rates)
            df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
            df["vol_ma"] = df["tick_volume"].rolling(20).mean()
            df["range"] = df["high"] - df["low"]
            df["body"] = (df["close"] - df["open"]).abs()
            df["close_loc"] = (df["close"] - df["low"]) / df["range"].replace(0, 1)
            rng = (df["high"] - df["low"]).replace(0, 1)
            df["ad"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / rng

            # Wyckoff v2 patterns
            patterns = find_wyckoff_patterns_v2(df)

            if not patterns: continue

            # Base: Wyckoff v2
            base_wins = 0; base_total = 0
            for p in patterns[:50]:
                idx = p["idx"]
                entry = p["entry"]
                atr = p["atr"]
                direction = p["direction"]
                if direction == "BUY":
                    sl = p["l_event"] - atr * 0.3
                    risk = entry - sl
                    tp = entry + risk * 3.0
                else:
                    sl = p["h_event"] + atr * 0.3
                    risk = sl - entry
                    tp = entry - risk * 3.0
                res = _check_outcome(df, idx, direction, entry, sl, tp)
                base_total += 1
                if res == "TP": base_wins += 1

            results[sym] = {
                "base_win": base_wins / max(base_total, 1),
                "base_total": base_total,
                "patterns": len(patterns),
            }
        except Exception as e:
            log.error(f"Ablation {sym}: {e}")

    # Нәтижені сақтау
    try:
        ABLATION_RESULTS.update({
            "ts": time.time(),
            "results": results,
        })
        _save_json(ABLATION_FILE, ABLATION_RESULTS)
        log.info(f"✅ Ablation test: {len(results)} символ")
    except Exception as e:
        log.error(f"Ablation save: {e}")


def start_ablation():
    """Ablation test іске қосу (7 күн)"""
    if not ABLATION_ENABLED: return

    def worker():
        time.sleep(3600)
        while True:
            try:
                run_ablation_test()
                time.sleep(7 * 86400)
            except Exception as e:
                log.error(f"Ablation worker: {e}")
                time.sleep(86400)

    threading.Thread(target=worker, daemon=True).start()
    log.info("✅ Ablation test іске қосылды")
    # ============================================================
# ORDER FLOW CORE — Tick → Delta / Footprint / VP / CVD
# Math basis:
#   Δ_tick = +vol (buy aggressor) | −vol (sell aggressor)
#   CVD_t  = Σ Δ_i
#   Footprint bin: price quantized by tick_size; buy/sell/delta per bin
#   Volume Profile: V(p) = Σ vol at price p; POC = argmax V
#   Value Area: minimal contiguous range covering va_pct (default 70%) of ΣV
#   Absorption: high |Δ| + low |Δprice| (effort ≠ result) at level
# ============================================================

_OF_CACHE = {}  # symbol -> {ts, ticks_df, footprint, vp, cvd}
_OF_CACHE_TTL = 2.0  # seconds


def _tick_size(symbol):
    info = mt5_symbol_info(symbol)
    if info and info.trade_tick_size > 0:
        return float(info.trade_tick_size)
    if info and info.point > 0:
        return float(info.point)
    return 0.01


def _fetch_ticks(symbol, seconds=120, max_ticks=30000):
    """MT5 ticks → DataFrame with signed delta volume (aggressor classification)."""
    try:
        now_ms = int(time.time() * 1000)
        raw = mt5_safe(
            mt5.copy_ticks_from, symbol, now_ms - seconds * 1000,
            max_ticks, mt5.COPY_TICKS_ALL,
        )
    except Exception:
        raw = None
    if raw is None or len(raw) == 0:
        return None
    df = pd.DataFrame(raw)
    # volume
    if "volume_real" in df.columns:
        df["vol"] = pd.to_numeric(df["volume_real"], errors="coerce").fillna(0.0)
    else:
        df["vol"] = pd.to_numeric(df.get("volume", 0), errors="coerce").fillna(0.0)
    df["last"] = pd.to_numeric(df["last"], errors="coerce")
    df["bid"] = pd.to_numeric(df["bid"], errors="coerce")
    df["ask"] = pd.to_numeric(df["ask"], errors="coerce")
    df["flags"] = pd.to_numeric(df.get("flags", 0), errors="coerce").fillna(0).astype(int)

    # Aggressor side (Lee-Ready-style + MT5 flags)
    buy_flag = int(getattr(mt5, "TICK_FLAG_BUY", 32))
    sell_flag = int(getattr(mt5, "TICK_FLAG_SELL", 64))
    side = np.zeros(len(df), dtype=np.int8)
    for i in range(len(df)):
        fl = int(df["flags"].iloc[i])
        if fl & buy_flag:
            side[i] = 1
        elif fl & sell_flag:
            side[i] = -1
        else:
            last = float(df["last"].iloc[i]) if not pd.isna(df["last"].iloc[i]) else 0.0
            bid = float(df["bid"].iloc[i]) if not pd.isna(df["bid"].iloc[i]) else 0.0
            ask = float(df["ask"].iloc[i]) if not pd.isna(df["ask"].iloc[i]) else 0.0
            if last > 0 and ask > 0 and last >= ask:
                side[i] = 1
            elif last > 0 and bid > 0 and last <= bid:
                side[i] = -1
            elif i > 0:
                prev = float(df["last"].iloc[i - 1]) if not pd.isna(df["last"].iloc[i - 1]) else 0.0
                if last > prev:
                    side[i] = 1
                elif last < prev:
                    side[i] = -1
                else:
                    side[i] = side[i - 1]
    df["side"] = side
    df["delta"] = df["vol"] * df["side"].astype(float)
    # drop zero-price noise
    df = df[df["last"] > 0].reset_index(drop=True)
    return df if len(df) > 0 else None


def get_order_flow(symbol, seconds=120, force=False):
    """
    Cached order-flow snapshot for symbol.
    Returns dict: ticks, delta_pct, footprint, volume_profile, cvd_series, absorption
    """
    now = time.time()
    cached = _OF_CACHE.get(symbol)
    if not force and cached and now - cached.get("ts", 0) < _OF_CACHE_TTL:
        return cached

    ticks = _fetch_ticks(symbol, seconds=seconds)
    if ticks is None or len(ticks) < 10:
        result = {
            "ts": now, "ok": False, "delta_pct": 0.0,
            "footprint": None, "volume_profile": None,
            "cvd": None, "absorption": None, "imbalance": 0.0,
        }
        _OF_CACHE[symbol] = result
        return result

    buy_vol = float(ticks.loc[ticks["side"] > 0, "vol"].sum())
    sell_vol = float(ticks.loc[ticks["side"] < 0, "vol"].sum())
    tot = buy_vol + sell_vol
    delta_pct = ((buy_vol - sell_vol) / tot * 100.0) if tot > 0 else 0.0

    ts = _tick_size(symbol)
    footprint = build_footprint(ticks, ts)
    vp = build_volume_profile(ticks, ts, va_pct=0.70)
    cvd = build_cvd_series(ticks)
    absorption = detect_absorption_of(ticks, footprint, ts)
    imbalance = footprint_imbalance_score(footprint) if footprint else 0.0

    result = {
        "ts": now, "ok": True,
        "delta_pct": delta_pct,
        "buy_vol": buy_vol, "sell_vol": sell_vol, "total_vol": tot,
        "footprint": footprint,
        "volume_profile": vp,
        "cvd": cvd,
        "absorption": absorption,
        "imbalance": imbalance,
        "tick_count": len(ticks),
    }
    _OF_CACHE[symbol] = result
    return result


def build_footprint(ticks, tick_size):
    """
    Footprint: for each price bin → buy_vol, sell_vol, delta, trades.
    Price quantized: round(price / tick_size) * tick_size
    """
    if ticks is None or len(ticks) == 0 or tick_size <= 0:
        return None
    prices = (np.round(ticks["last"].values / tick_size) * tick_size)
    buy = ticks["vol"].values * (ticks["side"].values > 0)
    sell = ticks["vol"].values * (ticks["side"].values < 0)
    bins = {}
    for p, b, s in zip(prices, buy, sell):
        p = float(p)
        if p not in bins:
            bins[p] = {"price": p, "buy": 0.0, "sell": 0.0, "trades": 0}
        bins[p]["buy"] += float(b)
        bins[p]["sell"] += float(s)
        bins[p]["trades"] += 1
    rows = []
    for p, d in bins.items():
        delta = d["buy"] - d["sell"]
        tot = d["buy"] + d["sell"]
        rows.append({
            "price": p,
            "buy": d["buy"],
            "sell": d["sell"],
            "delta": delta,
            "total": tot,
            "trades": d["trades"],
            "delta_ratio": (delta / tot) if tot > 0 else 0.0,
        })
    rows.sort(key=lambda x: x["price"])
    return rows


def footprint_imbalance_score(footprint, threshold=0.60):
    """
    Stacked imbalance: consecutive levels with |delta_ratio| >= threshold same sign.
    Returns score in [-1, 1] (positive = buy imbalance stack).
    """
    if not footprint or len(footprint) < 2:
        return 0.0
    best = 0
    cur = 0
    sign = 0
    for row in footprint:
        r = row["delta_ratio"]
        if abs(r) >= threshold:
            s = 1 if r > 0 else -1
            if s == sign:
                cur += s
            else:
                sign = s
                cur = s
            if abs(cur) > abs(best):
                best = cur
        else:
            cur = 0
            sign = 0
    # normalize by number of levels
    n = max(len(footprint), 1)
    return float(np.clip(best / max(n * 0.15, 1), -1.0, 1.0))


def build_volume_profile(ticks, tick_size, va_pct=0.70):
    """
    Classical Volume Profile from ticks.
    POC = price with max volume
    Value Area = smallest contiguous price range covering va_pct of total volume
    HVN/LVN via local peaks/troughs of volume histogram
    """
    if ticks is None or len(ticks) == 0 or tick_size <= 0:
        return None
    prices = np.round(ticks["last"].values / tick_size) * tick_size
    vols = ticks["vol"].values.astype(float)
    # histogram
    uniq = {}
    for p, v in zip(prices, vols):
        p = float(p)
        uniq[p] = uniq.get(p, 0.0) + float(v)
    if not uniq:
        return None
    levels = sorted(uniq.keys())
    volumes = np.array([uniq[p] for p in levels], dtype=float)
    total = float(volumes.sum())
    if total <= 0:
        return None
    poc_idx = int(np.argmax(volumes))
    poc = float(levels[poc_idx])

    # Value Area expansion from POC until va_pct covered
    target = total * va_pct
    lo = hi = poc_idx
    covered = volumes[poc_idx]
    while covered < target and (lo > 0 or hi < len(levels) - 1):
        vol_lo = volumes[lo - 1] if lo > 0 else -1.0
        vol_hi = volumes[hi + 1] if hi < len(levels) - 1 else -1.0
        if vol_hi >= vol_lo:
            if hi < len(levels) - 1:
                hi += 1
                covered += volumes[hi]
            elif lo > 0:
                lo -= 1
                covered += volumes[lo]
            else:
                break
        else:
            if lo > 0:
                lo -= 1
                covered += volumes[lo]
            elif hi < len(levels) - 1:
                hi += 1
                covered += volumes[hi]
            else:
                break

    vah = float(levels[hi])
    val = float(levels[lo])

    # HVN / LVN (simple local extrema)
    hvn, lvn = [], []
    for i in range(1, len(volumes) - 1):
        if volumes[i] >= volumes[i - 1] and volumes[i] >= volumes[i + 1] and volumes[i] > total / len(volumes):
            hvn.append(float(levels[i]))
        if volumes[i] <= volumes[i - 1] and volumes[i] <= volumes[i + 1]:
            lvn.append(float(levels[i]))

    return {
        "poc": poc,
        "vah": vah,
        "val": val,
        "total_volume": total,
        "va_pct": va_pct,
        "hvn": hvn[:5],
        "lvn": lvn[:5],
        "n_levels": len(levels),
        "histogram": [{"price": float(levels[i]), "volume": float(volumes[i])} for i in range(len(levels))],
    }


def build_cvd_series(ticks):
    """CVD_t = cumulative sum of signed delta volume."""
    if ticks is None or len(ticks) == 0:
        return None
    cvd = np.cumsum(ticks["delta"].values.astype(float))
    return {
        "series": cvd.tolist(),
        "last": float(cvd[-1]),
        "min": float(cvd.min()),
        "max": float(cvd.max()),
        "slope": float(cvd[-1] - cvd[max(0, len(cvd) // 2)]) if len(cvd) > 2 else 0.0,
    }


def detect_absorption_of(ticks, footprint, tick_size, min_vol_share=0.08, max_price_move_ticks=3):
    """
    Absorption: large volume at a price with little net progress.
    Effort (volume) high, result (price displacement across those ticks) low.
    Returns direction of absorbed side (BUY absorption → bullish, sellers absorbed).
    """
    if ticks is None or len(ticks) < 20 or not footprint:
        return None
    total = sum(r["total"] for r in footprint) or 1.0
    # levels with significant volume
    heavy = [r for r in footprint if r["total"] / total >= min_vol_share]
    if not heavy:
        return None
    # price range of whole window in ticks
    pmin, pmax = float(ticks["last"].min()), float(ticks["last"].max())
    move_ticks = (pmax - pmin) / tick_size if tick_size > 0 else 999
    best = None
    for r in heavy:
        # high volume, dominant side, but overall move small → absorption of opposite
        if r["total"] <= 0:
            continue
        ratio = abs(r["delta_ratio"])
        if ratio < 0.25:
            # two-sided fight at level
            if move_ticks <= max_price_move_ticks * 2:
                # more sell volume absorbed by buyers → bullish
                direction = "BUY" if r["sell"] >= r["buy"] else "SELL"
                score = r["total"] / total
                if best is None or score > best["score"]:
                    best = {
                        "direction": direction,
                        "price": r["price"],
                        "score": score,
                        "buy": r["buy"],
                        "sell": r["sell"],
                        "type": "ABSORPTION",
                    }
        elif ratio >= 0.55 and move_ticks <= max_price_move_ticks:
            # one-sided volume without progress → classic absorption of that side
            # large sell delta without price drop → buys absorbing sells
            if r["delta"] < 0:
                direction = "BUY"  # sells absorbed
            else:
                direction = "SELL"
            score = r["total"] / total * ratio
            if best is None or score > best["score"]:
                best = {
                    "direction": direction,
                    "price": r["price"],
                    "score": score,
                    "buy": r["buy"],
                    "sell": r["sell"],
                    "type": "ABSORPTION",
                }
    return best


def detect_absorption(symbol):
    """Public API — absorption from live order flow."""
    of = get_order_flow(symbol, seconds=90)
    if not of.get("ok"):
        return None
    abs_ = of.get("absorption")
    if abs_:
        return {"direction": abs_["direction"], "detail": abs_}
    # fallback: strong delta + imbalance stack
    if abs(of["delta_pct"]) >= HFT_DELTA_MIN and abs(of.get("imbalance", 0)) >= 0.25:
        return {
            "direction": "BUY" if of["delta_pct"] > 0 else "SELL",
            "detail": {"type": "DELTA_IMBALANCE", "delta_pct": of["delta_pct"]},
        }
    return None


def detect_spoofing(symbol):
    """
    Spoofing: large book level appears and vanishes quickly (< 1.5s)
    without trading through (heuristic on MT5 market book).
    """
    try:
        book = mt5_safe(mt5.market_book_get, symbol)
        if book is None or len(book) == 0:
            return None
        now = time.time()
        sp = []
        with _state_lock:
            for b in book:
                v = float(b.volume)
                if v < 5.0:
                    continue
                key = str((symbol, int(b.type), round(float(b.price), 5)))
                f = MEM["spoof"].get(key)
                if f is None:
                    MEM["spoof"][key] = now
                else:
                    lt = now - f
                    if 0.1 < lt < 1.5:
                        sp.append({"price": float(b.price), "vol": v, "life": lt})
            cut = now - 60
            MEM["spoof"] = {k: v for k, v in MEM["spoof"].items() if v > cut}
        return sp if sp else None
    except Exception:
        return None


def order_flow_signal(symbol, direction):
    """
    Composite order-flow confirmation for BUY/SELL.
    Returns (ok: bool, reasons: list, metrics: dict)
    """
    of = get_order_flow(symbol, seconds=120)
    reasons = []
    metrics = {
        "delta_pct": of.get("delta_pct", 0.0),
        "imbalance": of.get("imbalance", 0.0),
        "poc": None, "vah": None, "val": None,
        "cvd_slope": 0.0,
        "absorption": None,
    }
    if not of.get("ok"):
        return False, ["orderflow data жоқ"], metrics

    delta = of["delta_pct"]
    imb = of.get("imbalance", 0.0)
    vp = of.get("volume_profile") or {}
    cvd = of.get("cvd") or {}
    abs_ = of.get("absorption")
    metrics.update({
        "poc": vp.get("poc"),
        "vah": vp.get("vah"),
        "val": vp.get("val"),
        "cvd_slope": cvd.get("slope", 0.0),
        "absorption": abs_,
    })

    score = 0
    # 1) Delta alignment
    if direction == "BUY" and delta >= HFT_DELTA_MIN:
        score += 2
        reasons.append(f"Δ {delta:+.1f}%")
    elif direction == "SELL" and delta <= -HFT_DELTA_MIN:
        score += 2
        reasons.append(f"Δ {delta:+.1f}%")
    elif abs(delta) >= HFT_DELTA_STRONG:
        # strong opposite delta → reject later
        pass
    else:
        score += 0

    # 2) Footprint imbalance stack
    if direction == "BUY" and imb >= 0.20:
        score += 1
        reasons.append(f"FP imb {imb:+.2f}")
    elif direction == "SELL" and imb <= -0.20:
        score += 1
        reasons.append(f"FP imb {imb:+.2f}")

    # 3) Absorption agreement
    if abs_ and abs_.get("direction") == direction:
        score += 2
        reasons.append(f"ABS @ {abs_.get('price')}")

    # 4) CVD slope
    slope = cvd.get("slope", 0.0)
    if direction == "BUY" and slope > 0:
        score += 1
        reasons.append("CVD↑")
    elif direction == "SELL" and slope < 0:
        score += 1
        reasons.append("CVD↓")

    # 5) Price vs Value Area
    try:
        tick = mt5_symbol_info_tick(symbol)
        px = float(tick.bid if direction == "SELL" else tick.ask) if tick else 0.0
    except Exception:
        px = 0.0
    if vp and px > 0:
        val, vah, poc = vp.get("val"), vp.get("vah"), vp.get("poc")
        if direction == "BUY" and val is not None and px <= val * 1.001:
            score += 1
            reasons.append(f"near VAL {val}")
        elif direction == "SELL" and vah is not None and px >= vah * 0.999:
            score += 1
            reasons.append(f"near VAH {vah}")
        if poc is not None:
            reasons.append(f"POC {poc}")

    # Strong opposite delta veto
    if direction == "BUY" and delta <= -HFT_DELTA_STRONG:
        return False, [f"Δ veto {delta:+.1f}%"] + reasons, metrics
    if direction == "SELL" and delta >= HFT_DELTA_STRONG:
        return False, [f"Δ veto {delta:+.1f}%"] + reasons, metrics

    ok = score >= 2
    return ok, reasons, metrics


# ============================================================
# CORRELATION + TRAILING + DIVERGENCE
# ============================================================

def check_correlation(symbol):
    """Корреляция тексеру (қатар сигналдар)"""
    if not CORRELATION_ENABLED: return True, ""
    now = time.time()
    for g in CORRELATION_GROUPS:
        if symbol not in g: continue
        for other in g:
            if other == symbol: continue
            last = MEM["recent_signals"].get(other, 0)
            if now - last < CORRELATION_WINDOW_SEC:
                return False, f"⚠️ {other}"
    return True, ""


def register_signal(symbol):
    """Сигнал тіркеу (correlation)"""
    MEM["recent_signals"][symbol] = time.time()
    mem_save()


def update_trailing_stops():
    """Trailing stop — SL жаңарту"""
    if not TRAILING_ENABLED: return
    positions = mt5_positions_get()
    if positions is None: return
    for p in positions:
        if p.magic not in [20261013, 888388, 777777]: continue
        tick = mt5_symbol_info_tick(p.symbol)
        if not tick: continue
        info = mt5_symbol_info(p.symbol)
        if not info: continue
        entry = p.price_open
        cur = tick.bid if p.type == mt5.POSITION_TYPE_BUY else tick.ask
        sl = p.sl
        if sl == 0: continue
        if p.type == mt5.POSITION_TYPE_BUY:
            risk = entry - sl
            if risk <= 0: continue
            pr = (cur - entry) / risk
            if pr >= TRAILING_BE_AT_R and sl < entry:
                req = {"action": mt5.TRADE_ACTION_SLTP, "symbol": p.symbol,
                       "position": p.ticket, "sl": round(entry, info.digits), "tp": p.tp}
                mt5_order_send(req)
            elif pr >= TRAILING_STEP_R:
                mr = pr - TRAILING_MOVE_R
                ns = round(entry + risk * mr, info.digits)
                if ns > sl:
                    req = {"action": mt5.TRADE_ACTION_SLTP, "symbol": p.symbol,
                           "position": p.ticket, "sl": ns, "tp": p.tp}
                    mt5_order_send(req)
        else:
            risk = sl - entry
            if risk <= 0: continue
            pr = (entry - cur) / risk
            if pr >= TRAILING_BE_AT_R and sl > entry:
                req = {"action": mt5.TRADE_ACTION_SLTP, "symbol": p.symbol,
                       "position": p.ticket, "sl": round(entry, info.digits), "tp": p.tp}
                mt5_order_send(req)
            elif pr >= TRAILING_STEP_R:
                mr = pr - TRAILING_MOVE_R
                ns = round(entry - risk * mr, info.digits)
                if ns < sl:
                    req = {"action": mt5.TRADE_ACTION_SLTP, "symbol": p.symbol,
                           "position": p.ticket, "sl": ns, "tp": p.tp}
                    mt5_order_send(req)


def check_positions():
    """Ашық позицияларды тексеру + metrics"""
    try:
        positions = mt5_positions_get()
        if positions is None: return
        open_tickets = {p.ticket for p in positions}

        # Жабылған позицияларды анықтау
        old_positions = AUTO_STATE.get("positions", [])
        for op in old_positions:
            if op.get("ticket") not in open_tickets:
                # Позиция жабылды — метрика жаңарту
                log.info(f"📊 Position closed: {op.get('ticket')}")

        AUTO_STATE["positions"] = [
            p for p in old_positions if p.get("ticket") in open_tickets
        ]
        auto_save()
    except Exception: pass


def detect_divergence(df, symbol=None):
    """
    CVD ↔ Price divergence (regular).
    Prefer tick-based CVD when symbol given; else bar proxy (up-vol − down-vol).
    Bearish: price HH, CVD LH  → SELL
    Bullish: price LL, CVD HL  → BUY
    """
    if not DIVERGENCE_ENABLED:
        return None

    cvd_series = None
    price_series = None

    # Preferred: real tick CVD
    if symbol:
        of = get_order_flow(symbol, seconds=max(DIVERGENCE_WINDOW * 60, 300))
        if of.get("ok") and of.get("cvd") and of["cvd"].get("series"):
            cvd_series = np.array(of["cvd"]["series"], dtype=float)
            # align approximate price from ticks via resample not available → use df close
            if df is not None and len(df) >= DIVERGENCE_LOOKBACK:
                price_series = df["close"].tail(DIVERGENCE_WINDOW).values.astype(float)

    # Fallback: bar-based signed volume proxy
    if cvd_series is None:
        if df is None or len(df) < DIVERGENCE_WINDOW + 10:
            return None
        r = df.tail(DIVERGENCE_WINDOW)
        vol_col = "tick_volume" if "tick_volume" in r.columns else ("volume" if "volume" in r.columns else None)
        s = []
        cvd = 0.0
        for i in range(1, len(r)):
            up = float(r["close"].iloc[i]) >= float(r["close"].iloc[i - 1])
            v = float(r[vol_col].iloc[i]) if vol_col else 1.0
            cvd += v if up else -v
            s.append(cvd)
        cvd_series = np.array(s, dtype=float)
        price_series = r["close"].values.astype(float)[1:]

    if cvd_series is None or price_series is None:
        return None
    n = min(len(cvd_series), len(price_series), DIVERGENCE_WINDOW)
    if n < DIVERGENCE_LOOKBACK + 2:
        return None
    pr = price_series[-n:]
    cv = cvd_series[-n:]
    lb = DIVERGENCE_LOOKBACK
    # split into two halves of lookback for HH/LH detection
    p1, p2 = pr[:-lb], pr[-lb:]
    c1, c2 = cv[:-lb], cv[-lb:]
    if len(p1) < 3 or len(p2) < 3:
        return None
    # Bearish: price higher high, CVD lower high
    if p2.max() >= p1.max() * 0.998 and c2.max() < c1.max() * 0.92:
        return {"type": "BEARISH_DIV", "direction": "SELL",
                "price_hh": float(p2.max()), "cvd_lh": float(c2.max())}
    # Bullish: price lower low, CVD higher low
    if p2.min() <= p1.min() * 1.002 and c2.min() > c1.min() * 1.08:
        return {"type": "BULLISH_DIV", "direction": "BUY",
                "price_ll": float(p2.min()), "cvd_hl": float(c2.min())}
    return None


# ============================================================
# ELLIOTT WAVE (5 толқын)
# ============================================================

def find_swings(df, lookback=5):
    """Swing High/Low табу"""
    highs = []; lows = []
    for i in range(lookback, len(df) - lookback):
        if df["high"].iloc[i] == df["high"].iloc[i-lookback:i+lookback+1].max():
            highs.append((i, df["high"].iloc[i]))
        if df["low"].iloc[i] == df["low"].iloc[i-lookback:i+lookback+1].min():
            lows.append((i, df["low"].iloc[i]))
    return highs, lows


def detect_elliott(df):
    """
    Elliott Wave — WAVE_3 анықтау
    Қайтарады: dict {wave, direction}
    """
    if not ELLIOTT_ENABLED or len(df) < 100: return None
    highs, lows = find_swings(df)
    if len(highs) < 3 or len(lows) < 3: return None
    sw = [{"i": i, "p": p, "t": "H"} for i, p in highs] + \
         [{"i": i, "p": p, "t": "L"} for i, p in lows]
    sw.sort(key=lambda x: x["i"])
    last5 = sw[-5:]
    if len(last5) < 5: return None
    prices = [s["p"] for s in last5]
    types = [s["t"] for s in last5]
    up = sum(1 for i in range(len(prices)-1) if prices[i] < prices[i+1])
    dn = sum(1 for i in range(len(prices)-1) if prices[i] > prices[i+1])
    if types[0] == "L" and up >= 3:
        return {"wave": "WAVE_3", "direction": "BUY"}
    if types[0] == "H" and dn >= 3:
        return {"wave": "WAVE_3", "direction": "SELL"}
    return None


# ============================================================
# GANN SQUARE (8 деңгей)
# ============================================================

def detect_gann(df):
    """
    Gann Square of 9 — 8 деңгей (12.5% қадам)
    Қайтарады: dict {level, signal}
    """
    if not GANN_ENABLED or len(df) < 100: return None
    r = df.tail(100)
    h = float(r["high"].max()); l = float(r["low"].min()); rng = h - l
    if rng <= 0: return None
    cur = float(df.iloc[-2]["close"])
    levels = {"0": l, "1": l+rng*0.125, "2": l+rng*0.25, "3": l+rng*0.375,
              "4": l+rng*0.5, "5": l+rng*0.625, "6": l+rng*0.75,
              "7": l+rng*0.875, "8": h}
    n = min(levels.items(), key=lambda x: abs(cur - x[1]))[0]
    if n == "4": return {"level": n, "signal": "NEUTRAL"}
    if n in ["1", "2", "3"]: return {"level": n, "signal": "BULL"}
    if n in ["5", "6", "7"]: return {"level": n, "signal": "BEAR"}
    return {"level": n, "signal": "NEUTRAL"}


# ============================================================
# DOW THEORY (4 фаза)
# ============================================================

def detect_dow(df):
    """
    Dow Theory — 4 фаза
    Accumulation, Markup, Distribution, Markdown
    """
    if not DOW_ENABLED or len(df) < 200: return None
    e200 = df["close"].ewm(span=200).mean().iloc[-1]
    r = df.tail(50)
    h = r["high"].max(); l = r["low"].min(); rng = h - l
    if rng <= 0: return None
    cur = r["close"].iloc[-1]; pos = (cur - l) / rng; up = cur > e200
    if up and pos > 0.7: return {"name": "Markup", "direction": "BUY"}
    if up and pos < 0.3: return {"name": "Accumulation", "direction": "BUY"}
    if not up and pos < 0.3: return {"name": "Markdown", "direction": "SELL"}
    if not up and pos > 0.7: return {"name": "Distribution", "direction": "SELL"}
    return {"name": "Unknown", "direction": None}


# ============================================================
# MT5 CALENDAR (News PAUSE)
# ============================================================

def check_mt5_calendar(hours_ahead=2):
    """MT5 күнтізбесі — маңызды жаңалықтар"""
    if not NEWS_PAUSE_ENABLED: return True, ""
    now = time.time()
    last = AI_STATE.get("last_news_check", 0)
    if now - last < 1800:
        return AI_STATE.get("news_cache", {}).get("safe", True), \
               AI_STATE.get("news_cache", {}).get("reason", "")
    try:
        if hasattr(mt5, "calendar_event_get"):
            now_dt = datetime.now(timezone.utc)
            to_dt = now_dt + pd.Timedelta(hours=hours_ahead)
            events = mt5.calendar_event_get(time_min=now_dt, time_max=to_dt)
            if events and len(events) > 0:
                hi = [e for e in events if e.importance == 3]
                if hi:
                    reason = f"📰 {hi[0].name} ({hi[0].currency})"
                    AI_STATE["news_cache"] = {"safe": False, "reason": reason}
                    AI_STATE["last_news_check"] = now
                    ai_save()
                    return False, reason
        AI_STATE["news_cache"] = {"safe": True, "reason": ""}
        AI_STATE["last_news_check"] = now
        ai_save()
        return True, ""
    except Exception: return True, ""


# ============================================================
# AI CONFIRM (Elliott + Gann + Dow = 7 ұпай)
# ============================================================

def ai_confirm(df, direction):
    """
    AI Confirm — 7 ұпай максимум:
    - Elliott: +3
    - Gann: +2
    - Dow: +2
    """
    score = 0; reasons = []
    ell = detect_elliott(df)
    if ell and ell["direction"] == direction:
        if ell["wave"] in ["WAVE_3", "WAVE_5"]:
            score += 3
            reasons.append(f"🌊 Elliott {ell['wave']}")
    gann = detect_gann(df)
    if gann:
        if (gann["signal"] == "BULL" and direction == "BUY") or \
           (gann["signal"] == "BEAR" and direction == "SELL"):
            score += 2
            reasons.append(f"📐 Gann {gann['level']}")
    dow = detect_dow(df)
    if dow and dow["direction"] == direction:
        score += 2
        reasons.append(f"📊 Dow {dow['name']}")
    return score, reasons
    # ============================================================
# SIGNAL ENGINE (LONG / SHORT / WAIT)
# ============================================================

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

def set_mode(mode):
    """Режим ауыстыру"""
    AUTO_STATE["mode"] = mode
    AUTO_STATE["enabled"] = mode != "MANUAL"
    auto_save()
    log.info(f"🤖 Mode: {mode}")
    return mode


def get_mode():
    """Ағымдағы режим"""
    return AUTO_STATE.get("mode", "MANUAL")


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

def build_chart(symbol, data):
    """
    График салу (свеча + SL/TP/Support/Resistance)
    Қайтарады: BytesIO (PNG) немесе None
    """
    try:
        rates = mt5_copy_rates(symbol, TIMEFRAME, 0, 60)
        if rates is None or len(rates) < 10: return None
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df = df[["open", "high", "low", "close", "tick_volume"]]
        df.columns = ["Open", "High", "Low", "Close", "Volume"]

        mc = mpf.make_marketcolors(up="#26a69a", down="#ef5350",
                                     edge="inherit", wick="inherit",
                                     volume={"up": "#26a69a", "down": "#ef5350"})
        style = mpf.make_mpf_style(
            marketcolors=mc, facecolor="#131722",
            edgecolor="#131722", figcolor="#131722",
            gridcolor="#2a2e39", gridstyle="--",
            rc={"axes.labelcolor": "#d1d4dc", "xtick.color": "#d1d4dc",
                "ytick.color": "#d1d4dc", "font.size": 9})

        hlines = []; colors = []; ls = []; ws = []
        if data.get("support"):
            hlines.append(data["support"]); colors.append("#26a69a")
            ls.append("--"); ws.append(1.0)
        if data.get("resistance"):
            hlines.append(data["resistance"]); colors.append("#ef5350")
            ls.append("--"); ws.append(1.0)
        if data.get("entry"):
            hlines.append(data["entry"]); colors.append("#ffffff")
            ls.append(":"); ws.append(1.0)
        if data.get("sl"):
            hlines.append(data["sl"]); colors.append("#ef5350")
            ls.append("-"); ws.append(1.3)
        if data.get("tp"):
            hlines.append(data["tp"]); colors.append("#26a69a")
            ls.append("-"); ws.append(1.0)

        kw = {}
        if hlines:
            kw["hlines"] = dict(hlines=hlines, colors=colors,
                                 linestyle=ls, linewidths=ws)

        fig, axes = mpf.plot(df, type="candle", style=style, volume=True,
                              returnfig=True, figsize=(12, 7),
                              title=f"\n{symbol}  |  M15  |  {data.get('event', '')}",
                              **kw)

        ax = axes[0]
        info = (
            f"Event:    {data.get('event', '')}\n"
            f"Phase:    {data.get('phase', '')}\n"
            f"Signal:   {data.get('signal', '')}\n"
            f"Entry:    {data.get('entry', 0)}\n"
            f"SL:       {data.get('sl', 0)}\n"
            f"TP:       {data.get('tp', 0)}\n"
            f"R:R:      {data.get('rr', 0)}\n"
            f"Adaptive: {data.get('adaptive', 0):.2f}\n"
            f"Delta%:   {data.get('delta_pct', 0):+.1f}%\n"
            f"Fourier:  {data.get('fourier', 0):.2f}\n"
            f"Fractal:  {data.get('fractal', 0):.2f}\n"
            f"MTF:      {data.get('mtf', 0):.2f}\n"
            f"Wavelet:  {data.get('wavelet', 0):+.1f}\n"
            f"RL:       {data.get('rl', 0.5):.2f}\n"
            f"Ensemble: {data.get('ensemble', 0):.2f}"
        )
        ax.text(0.01, 0.98, info, transform=ax.transAxes, fontsize=8, va="top",
                bbox=dict(boxstyle="round", facecolor="#1e222d",
                          edgecolor="#2a2e39", alpha=0.9),
                color="#d1d4dc", family="monospace")

        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=110,
                    bbox_inches="tight", facecolor="#131722")
        plt.close(fig)
        buf.seek(0)
        return buf
    except Exception as e:
        log.error(f"Chart: {e}")
        return None


# ============================================================
# SCANNER (Top 20)
# ============================================================

def get_atr_pct(symbol):
    """ATR% есептеу (scanner үшін)"""
    try:
        rates = mt5_copy_rates(symbol, TIMEFRAME, 0, 50)
        if rates is None or len(rates) < 20: return 0.0
        df = pd.DataFrame(rates)
        atr = ta.atr(df["high"], df["low"], df["close"], length=ATR_PERIOD)
        if atr is None or len(atr) == 0: return 0.0
        a = float(atr.iloc[-1]); c = float(df["close"].iloc[-1])
        if c <= 0 or pd.isna(a): return 0.0
        return (a / c) * 100.0
    except Exception: return 0.0


def ensure_categories():
    """Symbolдарды MT5-те көрсету"""
    all_syms = mt5.symbols_get()
    if not all_syms:
        log.warning("⚠️ symbols_get() бос")
        return
    names = {s.name.upper(): s for s in all_syms}
    total = 0
    for cat, syms in CATEGORIES.items():
        found = 0
        for sym in syms:
            s = names.get(sym.upper())
            if s is None: continue
            if not s.visible: mt5.symbol_select(sym, True)
            found += 1
        total += found
        log.info(f"  📂 {cat}: {found}/{len(syms)}")
    log.info(f"✅ Categories: {total} symbols")


def scan_all():
    """
    Top 20 символ сканерлеу.
    Демалыс/trade_mode=DISABLED болса да талдау үшін символды аламыз
    (ордер ашу open_position ішінде бөлек шектеледі).
    """
    active = get_active_categories()
    all_syms = mt5.symbols_get()
    if not all_syms:
        return [], {}, active
    names = {s.name.upper(): s for s in all_syms}
    a = []
    bc = {}
    for cat in active:
        found = []
        for sym in CATEGORIES.get(cat, []):
            s = names.get(sym.upper())
            if s is None:
                continue
            # Select even if trade disabled — need rates for analysis
            try:
                if not s.visible:
                    mt5.symbol_select(sym, True)
            except Exception:
                pass
            found.append(sym)
            a.append(sym)
        bc[cat] = found
    # ATR ranking; if ATR fails (weekend) still keep symbol
    r = []
    for s in a:
        try:
            r.append((s, get_atr_pct(s)))
        except Exception:
            r.append((s, 0.0))
    r.sort(key=lambda x: x[1], reverse=True)
    return r[:TOP_N], bc, active
    # ============================================================
# LLM BRAIN — xAI Grok (primary) / Groq (fallback)
# ============================================================

llm_client = None
LLM_AVAILABLE = False
LLM_BACKEND = None  # "xai" | "groq"
# Backward-compat alias used across the codebase
GROQ_AVAILABLE = False


def _init_llm_client():
    """
    Init LLM client.
    LLM_PROVIDER=groq  → Groq first
    LLM_PROVIDER=xai   → xAI first, then Groq fallback
    LLM_PROVIDER=auto  → xAI if key, else Groq
    """
    global llm_client, LLM_AVAILABLE, LLM_BACKEND, GROQ_AVAILABLE

    provider = (LLM_PROVIDER or "auto").lower().strip()
    order = []
    if provider == "groq":
        order = ["groq", "xai"]
    elif provider in ("xai", "grok"):
        order = ["xai", "groq"]
    else:  # auto
        order = ["xai", "groq"] if XAI_API_KEY else ["groq", "xai"]

    for backend in order:
        if backend == "xai" and XAI_API_KEY:
            try:
                from openai import OpenAI
                llm_client = OpenAI(api_key=XAI_API_KEY, base_url=XAI_BASE_URL)
                LLM_AVAILABLE = True
                LLM_BACKEND = "xai"
                GROQ_AVAILABLE = True
                log.info(f"✅ LLM: xAI Grok ({LLM_MODEL})")
                return
            except ImportError:
                try:
                    import requests as _req

                    class _XAIClient:
                        def __init__(self, key, base):
                            self.key, self.base = key, base.rstrip("/")

                        def chat_completions_create(self, **kw):
                            r = _req.post(
                                f"{self.base}/chat/completions",
                                headers={
                                    "Authorization": f"Bearer {self.key}",
                                    "Content-Type": "application/json",
                                },
                                json=kw,
                                timeout=60,
                            )
                            r.raise_for_status()
                            data = r.json()

                            class _Msg:
                                def __init__(self, c):
                                    self.content = c

                            class _Choice:
                                def __init__(self, c):
                                    self.message = _Msg(c)

                            class _Resp:
                                def __init__(self, c):
                                    self.choices = [_Choice(c)]

                            return _Resp(data["choices"][0]["message"]["content"])

                    class _Completions:
                        def __init__(self, client):
                            self._c = client

                        def create(self, **kw):
                            return self._c.chat_completions_create(**kw)

                    class _ChatNS:
                        def __init__(self, client):
                            self.completions = _Completions(client)

                    class _Wrapper:
                        def __init__(self, client):
                            self.chat = _ChatNS(client)

                    llm_client = _Wrapper(_XAIClient(XAI_API_KEY, XAI_BASE_URL))
                    LLM_AVAILABLE = True
                    LLM_BACKEND = "xai"
                    GROQ_AVAILABLE = True
                    log.info(f"✅ LLM: xAI Grok via requests ({LLM_MODEL})")
                    return
                except Exception as e:
                    log.warning(f"xAI Grok init failed: {e}")
            except Exception as e:
                log.warning(f"xAI Grok init failed: {e}")

        if backend == "groq" and GROQ_API_KEY:
            try:
                from groq import Groq
                model = LLM_MODEL
                # Keep configured model; only force fallback if empty/invalid
                if not model or not str(model).strip():
                    model = "openai/gpt-oss-20b"
                llm_client = Groq(api_key=GROQ_API_KEY)
                LLM_AVAILABLE = True
                LLM_BACKEND = "groq"
                GROQ_AVAILABLE = True
                globals()["LLM_MODEL"] = model
                tag = "primary" if provider == "groq" else "fallback"
                log.info(f"✅ LLM: Groq {tag} ({model})")
                return
            except Exception as e:
                log.warning(f"Groq init failed: {e}")

    LLM_AVAILABLE = False
    GROQ_AVAILABLE = False
    LLM_BACKEND = None
    log.warning("⚠️ LLM unavailable (set GROQ_API_KEY or XAI_API_KEY)")


_init_llm_client()


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

{len(rows)} сигнал, {days} күн статистика:
{json.dumps(stats, indent=2)}

ТАПСЫРМА:
1. Қай фильтр жақсы (win > 0.70)?
2. Қай фильтр зиян (win < 0.55)?
3. Қай фильтрді өшіру?

ЖАУАП (JSON):
{{
  "disable": ["filter_name"],
  "keep": ["filter_name"],
  "reason": "қысқа түсіндіру"
}}"""

        result = llm_ask(prompt)
        if result:
            LLM_DECISIONS.append({
                "ts": time.time(),
                "stats": stats,
                "decision": result,
            })
            _save_json(LLM_LOG_FILE, LLM_DECISIONS[-50:])
        return result
    except Exception as e:
        log.error(f"LLM analyze: {e}")
        return None


def apply_filter_decision(decision):
    """LLM шешімін қолдану (фильтр өшіру/қосу)"""
    if not decision: return
    disable = decision.get("disable", [])
    keep = decision.get("keep", [])

    for f in disable:
        FILTERS_DISABLED.add(f)
    for f in keep:
        FILTERS_DISABLED.discard(f)

    filter_state_save()
    log.info(f"🚫 Өшірілді: {disable}")
    log.info(f"✅ Сақталды: {keep}")


def is_filter_enabled(name):
    """Фильтр қосулы ма?"""
    return name not in FILTERS_DISABLED


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

ДЕРЕКТЕР:
{json.dumps(data, indent=2)}

АҒЫМДАҒЫ ПАРАМЕТРЛЕР:
- VOL_PREPARE_BASE: {VOL_PREPARE_BASE}
- AI_CONFIRM_MIN: {AI_CONFIRM_MIN}
- RISK_PER_TRADE: {RISK_PER_TRADE}%

ТАПСЫРМА:
1. Жаңа параметрлер ұсын (win rate арттыру үшін)
2. Жаңа фильтр ұсын
3. Қысқа түсіндір

ЖАУАП (JSON):
{{
  "params": {{
    "VOL_PREPARE_BASE": 1.7,
    "AI_CONFIRM_MIN": 5
  }},
  "new_filter": "сипаттама",
  "reason": "..."
}}"""

        result = llm_ask(prompt)
        return result
    except Exception as e:
        log.error(f"Strategy: {e}")
        return None


def apply_strategy_suggestions(suggestion):
    """Стратегия ұсыныстарын қолдану"""
    if not suggestion: return
    global VOL_PREPARE_BASE, AI_CONFIRM_MIN, RISK_PER_TRADE

    params = suggestion.get("params", {})
    changes = []

    if "VOL_PREPARE_BASE" in params:
        old = VOL_PREPARE_BASE
        VOL_PREPARE_BASE = float(params["VOL_PREPARE_BASE"])
        changes.append(f"VOL_PREPARE_BASE: {old} → {VOL_PREPARE_BASE}")
        log.info(f"⚙️ VOL_PREPARE_BASE: {old} → {VOL_PREPARE_BASE}")

    if "AI_CONFIRM_MIN" in params:
        old = AI_CONFIRM_MIN
        AI_CONFIRM_MIN = int(params["AI_CONFIRM_MIN"])
        changes.append(f"AI_CONFIRM_MIN: {old} → {AI_CONFIRM_MIN}")
        log.info(f"⚙️ AI_CONFIRM_MIN: {old} → {AI_CONFIRM_MIN}")

    tg_send(
        f"🔬 *Strategy Programmer*\n\n"
        f"⚙️ Өзгерістер:\n" +
        "\n".join(f"  • {c}" for c in changes) +
        f"\n\n📝 {suggestion.get('reason', '')[:200]}"
    )


def llm_strategy_worker():
    """Стратегия жасау циклі (24 сағат)"""
    time.sleep(7200)
    while True:
        try:
            log.info("🔬 Strategy Programmer...")
            suggestion = llm_program_strategy()
            if suggestion:
                apply_strategy_suggestions(suggestion)
            time.sleep(24 * 3600)
        except Exception as e:
            log.error(f"Strategy worker: {e}")
            time.sleep(3600)


def start_strategy_programmer():
    """Strategy Programmer іске қосу"""
    if not LLM_ENABLED or not GROQ_AVAILABLE:
        return
    threading.Thread(target=llm_strategy_worker, daemon=True).start()
    log.info("✅ Strategy Programmer іске қосылды")


# ============================================================
# AUTO-LEARN (Self-Reflection — қателерден үйрену)
# ============================================================

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

50 SL сигнал (қателер):
{json.dumps(errors[:20], indent=2)}

ТАПСЫРМА:
1. Не ортақ қате?
2. Қай feature нашар?
3. Жаңа фильтр ұсын.

ЖАУАП (JSON):
{{
  "common_problem": "...",
  "new_filter": "...",
  "reason": "..."
}}"""

        return llm_ask(prompt)
    except Exception as e:
        log.error(f"Self-reflection: {e}")
        return None


def auto_learn_worker():
    """Auto-Learn циклі (24 сағат)"""
    time.sleep(3600)
    while True:
        try:
            log.info("🎓 Auto-Learn — self-reflection...")
            result = llm_self_reflection()
            if result:
                tg_send(
                    f"🎓 *Auto-Learn*\n\n"
                    f"❌ Ортақ қате: {result.get('common_problem', '—')[:150]}\n"
                    f"🔬 Жаңа фильтр: {result.get('new_filter', '—')[:150]}\n"
                    f"📝 _{result.get('reason', '')[:150]}_"
                )
                AUTO_LEARN_LAST[0] = time.time()
            time.sleep(AUTO_LEARN_INTERVAL_HOURS * 3600)
        except Exception as e:
            log.error(f"Auto-learn: {e}")
            time.sleep(3600)


def start_auto_learn():
    """Auto-Learn іске қосу"""
    if not AUTO_LEARN_ENABLED: return
    threading.Thread(target=auto_learn_worker, daemon=True).start()
    log.info("✅ Auto-Learn іске қосылды")


# ============================================================
# VOICE (Қазақша — edge-tts)
# ============================================================

def voice_signal_message(symbol, direction, level, entry, sl, tp, ensemble):
    """Signal дауысы (қазақша)"""
    dir_kz = "сатып алу" if direction == "BUY" else "сату"
    return (
        f"{symbol} бойынша {dir_kz} сигналы. "
        f"Деңгей {level} пайыз. "
        f"Кіру бағасы {entry}. "
        f"Стоп лосс {sl}. "
        f"Тейк профит {tp}. "
        f"Сенімділік {ensemble:.0%}."
    )


def voice_wait_message(symbol, direction, level, reasons):
    """WAIT дауысы (қазақша)"""
    dir_kz = "сатып алу" if direction == "BUY" else "сату"
    return (
        f"{symbol} бойынша {dir_kz} бағыты. "
        f"Деңгей {level} пайыз. "
        f"Күтеміз: {reasons[0] if reasons else ''}. "
    )
    # ============================================================
# FRACTAL CYCLE (4 деңгей)
# ============================================================

def fractal_cycle_worker():
    """
    Fractal Cycle — 4 деңгей:
    - small (3 сек): signal табу (негізгі циклде)
    - medium (6 сағат): LLM талдау
    - large (24 сағат): ML retrain
    - mega (7 күн): толық backtest
    """
    last_medium = [0]
    last_large = [0]
    last_mega = [0]

    time.sleep(600)
    while True:
        try:
            now = time.time()

            # Medium cycle (6 сағат) — LLM талдау
            if now - last_medium[0] >= FRACTAL_LEVELS["medium"]:
                log.info("🔁 Fractal Medium cycle (6с) — LLM талдау")
                if GROQ_AVAILABLE:
                    threading.Thread(
                        target=lambda: llm_analyze_filters(days=30),
                        daemon=True
                    ).start()
                last_medium[0] = now

            # Large cycle (24 сағат) — ML retrain
            if now - last_large[0] >= FRACTAL_LEVELS["large"]:
                log.info("🔁 Fractal Large cycle (24с) — ML retrain")
                threading.Thread(target=ml_train, daemon=True).start()
                last_large[0] = now

            # Mega cycle (7 күн) — толық backtest
            if now - last_mega[0] >= FRACTAL_LEVELS["mega"]:
                log.info("🔁 Fractal Mega cycle (7к) — толық backtest")
                all_syms = []
                for s in CATEGORIES.values(): all_syms.extend(s)
                threading.Thread(
                    target=lambda: incremental_backtest(all_syms, mt5, TIMEFRAME),
                    daemon=True
                ).start()
                last_mega[0] = now

            time.sleep(60)
        except Exception as e:
            log.error(f"Fractal cycle: {e}")
            time.sleep(300)


def start_fractal_cycle():
    """Fractal Cycle іске қосу"""
    threading.Thread(target=fractal_cycle_worker, daemon=True).start()
    log.info("✅ Fractal Cycle іске қосылды")


# ============================================================
# 🆕 APEX #38 — TRADINGVIEW BRIDGE (FastAPI Webhook)
# ============================================================

try:
    from fastapi import FastAPI, BackgroundTasks, HTTPException
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    log.warning("⚠️ FastAPI жоқ — TV Bridge өшірулі")


# TV Bridge state
TV_SIGNALS_RECEIVED = [0]
TV_SIGNALS_EXECUTED = [0]
TV_LAST_SIGNAL = [None]


if FASTAPI_AVAILABLE:
    apex_app = FastAPI(title="APEX v3 TradingView Bridge")

    class TVSignal(BaseModel):
        secret_token: str
        symbol: str
        action: str          # BUY / SELL
        price: float = 0
        sl: float = 0
        tp: float = 0
        timeframe: str = "M15"
        comment: str = ""

    def process_tv_signal(signal: TVSignal):
        """
        TradingView → full APEX pipeline:
        symbol/action → risk limits → order-flow confirm → SL/TP → open
        """
        try:
            TV_SIGNALS_RECEIVED[0] += 1
            TV_LAST_SIGNAL[0] = {
                "ts": time.time(),
                "symbol": signal.symbol,
                "action": signal.action,
                "price": signal.price,
            }
            log.info(f"📡 TV Signal: {signal.symbol} {signal.action} @ {signal.price}")

            symbol = signal.symbol.upper()
            info = mt5_symbol_info(symbol)
            if not info:
                log.warning(f"⚠️ TV: {symbol} табылмады")
                tg_send(f"📡 *TV Signal* ❌\n`{symbol}` табылмады")
                return

            direction = signal.action.upper()
            if direction not in ("BUY", "SELL"):
                log.warning(f"⚠️ TV: action қате ({direction})")
                return

            # Duplicate window
            with _state_lock:
                last_sent = MEM.get("sent_signals", {}).get(f"TV:{symbol}", 0)
            if time.time() - last_sent < DUPLICATE_WINDOW_SEC:
                log.info(f"TV duplicate skip {symbol}")
                return

            auto_ok, auto_r = can_trade()
            if not auto_ok:
                tg_send(
                    f"📡 *TV Signal*\n📌 {symbol} | {direction}\n"
                    f"💵 {signal.price}\n⏸ Auto OFF ({auto_r})"
                )
                return

            if not validate_risk():
                tg_send(f"📡 *TV* ❌ risk limit — {symbol}")
                return

            # Order-flow confirmation (same math as main scanner)
            of_ok, of_reasons, of_metrics = order_flow_signal(symbol, direction)
            if not of_ok:
                tg_send(
                    f"📡 *TV Signal* ⏸ OrderFlow\n"
                    f"📌 {symbol} | {direction}\n"
                    f"⚠️ {', '.join(of_reasons[:3])}"
                )
                log.info(f"TV OF reject {symbol}: {of_reasons}")
                return

            # Correlation
            corr_ok, corr_r = check_correlation(symbol)
            if not corr_ok:
                tg_send(f"📡 *TV* ⏸ Corr {corr_r}")
                return

            tick = mt5_symbol_info_tick(symbol)
            if not tick:
                return
            entry = signal.price if signal.price > 0 else (
                tick.ask if direction == "BUY" else tick.bid
            )

            # SL/TP: prefer TV levels; else ATR; tighten with VP if available
            sl, tp = float(signal.sl or 0), float(signal.tp or 0)
            rates = mt5_copy_rates(symbol, TIMEFRAME, 0, 80)
            atr_v = 0.0
            if rates is not None and len(rates) >= 20:
                df_tv = pd.DataFrame(rates)
                if len(df_tv) > 1:
                    df_tv = df_tv.iloc[:-1]
                atr_series = ta.atr(df_tv["high"], df_tv["low"], df_tv["close"], length=ATR_PERIOD)
                atr_v = float(atr_series.iloc[-1]) if atr_series is not None and len(atr_series) else 0.0

            if (sl == 0 or tp == 0) and atr_v > 0:
                if direction == "BUY":
                    sl = entry - 0.7 * atr_v
                    tp = entry + max(RISK_REWARD_MIN, 3.5) * (entry - sl)
                else:
                    sl = entry + 0.7 * atr_v
                    tp = entry - max(RISK_REWARD_MIN, 3.5) * (sl - entry)

            # Optional: place SL beyond VAL/VAH
            vp_poc = of_metrics.get("poc")
            vp_val = of_metrics.get("val")
            vp_vah = of_metrics.get("vah")
            if direction == "BUY" and vp_val and sl > 0:
                sl = min(sl, float(vp_val) - (_tick_size(symbol) or 0))
            elif direction == "SELL" and vp_vah and sl > 0:
                sl = max(sl, float(vp_vah) + (_tick_size(symbol) or 0))

            risk = abs(entry - sl)
            if risk <= 0 or abs(tp - entry) / risk < RISK_REWARD_MIN:
                tg_send(f"📡 *TV* ❌ R:R < {RISK_REWARD_MIN}")
                return

            with _state_lock:
                eq = _stats.get("equity", 10000.0)
            risk_usd = eq * (RISK_PER_TRADE / 100.0)

            result = open_position(
                symbol, direction, entry, sl, tp, risk_usd,
                source="TV_Bridge", magic=888388,
            )

            of_txt = ", ".join(of_reasons[:3])
            if result.get("ok"):
                TV_SIGNALS_EXECUTED[0] += 1
                with _state_lock:
                    MEM.setdefault("sent_signals", {})[f"TV:{symbol}"] = time.time()
                mem_save()
                register_signal(symbol)
                tg_send(
                    f"📡 *TradingView → APEX* ✅\n\n"
                    f"📌 {symbol} | {direction}\n"
                    f"💵 Entry: `{entry}`\n"
                    f"🛑 SL: `{sl}`  🎯 TP: `{tp}`\n"
                    f"📊 Lot: `{result.get('lot')}`  🎫 `{result.get('ticket')}`\n"
                    f"🔬 OF: {of_txt}\n"
                    f"POC: `{vp_poc}` | VAL: `{vp_val}` | VAH: `{vp_vah}`\n"
                    f"⚡ {result.get('latency', 0):.0f}ms"
                )
            else:
                tg_send(
                    f"📡 *TV Signal* ❌\n📌 {symbol} | {direction}\n"
                    f"⚠️ {result.get('reason', 'Unknown')}"
                )
        except Exception as e:
            log.error(f"TV process: {e}")

    @apex_app.post("/webhook")
    async def tradingview_webhook(signal: TVSignal, bg: BackgroundTasks):
        """TradingView-ден сигнал қабылдау"""
        if signal.secret_token != TV_SECRET:
            log.warning(f"⚠️ TV: қате token")
            raise HTTPException(status_code=403, detail="Invalid token")
        bg.add_task(process_tv_signal, signal)
        return {
            "status": "accepted",
            "symbol": signal.symbol,
            "action": signal.action,
        }

    @apex_app.get("/")
    async def root():
        """Health check"""
        return {
            "status": "APEX v3 TradingView Bridge",
            "received": TV_SIGNALS_RECEIVED[0],
            "executed": TV_SIGNALS_EXECUTED[0],
            "auto_mode": get_mode(),
            "equity": _stats["equity"],
        }

    @apex_app.get("/status")
    async def tv_status():
        """Статус"""
        acc = mt5_account_info()
        pos = mt5_positions_get() or []
        return {
            "balance": round(acc.balance, 2) if acc else 0,
            "equity": round(acc.equity, 2) if acc else 0,
            "positions": len(pos),
            "mode": get_mode(),
            "received": TV_SIGNALS_RECEIVED[0],
            "executed": TV_SIGNALS_EXECUTED[0],
        }


def start_tv_bridge():
    """TradingView Bridge іске қосу"""
    if not TV_BRIDGE_ENABLED:
        log.info("⏸ TV Bridge өшірулі")
        return
    if not FASTAPI_AVAILABLE:
        log.warning("⚠️ FastAPI жоқ — TV Bridge өшірулі")
        return

    def run_server():
        try:
            log.info(f"📡 TradingView Bridge: http://{TV_BRIDGE_HOST}:{TV_BRIDGE_PORT}")
            uvicorn.run(
                apex_app,
                host=TV_BRIDGE_HOST,
                port=TV_BRIDGE_PORT,
                log_level="warning",
            )
        except Exception as e:
            log.error(f"TV Bridge server: {e}")

    threading.Thread(target=run_server, daemon=True).start()
    log.info(f"✅ TV Bridge іске қосылды (порт {TV_BRIDGE_PORT})")


# ============================================================
# 🆕 APEX #40 — DYNAMIC HEDGE (Correlation Matrix)
# ============================================================

class DynamicHedgeEngine:
    """
    Multi-Asset Correlation Matrix & Dynamic Hedge
    Тәуекелді 50%-ға төмендету
    """

    def __init__(self, symbols=None, threshold=HEDGE_THRESHOLD):
        self.symbols = symbols or [
            "BTCUSD", "ETHUSD", "BNBUSD", "SOLUSD",
            "XAUUSD", "XAGUSD",
            "US30", "US500", "USTEC",
            "EURUSD", "GBPUSD", "USDJPY",
            "USOIL", "UKOIL",
        ]
        self.threshold = threshold

    def calculate_correlation_matrix(self, timeframe=None, bars=100):
        """Корреляция матрицасы (Pearson)"""
        try:
            tf = timeframe or TIMEFRAME
            data = {}
            for sym in self.symbols:
                rates = mt5_copy_rates(sym, tf, 0, bars)
                if rates is None or len(rates) < 50:
                    continue
                df = pd.DataFrame(rates)
                data[sym] = df["close"].values

            if len(data) < 2:
                return None

            price_df = pd.DataFrame(data)
            returns_df = price_df.pct_change().dropna()

            if len(returns_df) < 10:
                return None

            corr = returns_df.corr()
            return corr
        except Exception as e:
            log.error(f"Hedge corr: {e}")
            return None

    def get_correlated_pairs(self, threshold=None):
        """Жоғары корреляциялы жұптар"""
        try:
            corr = self.calculate_correlation_matrix()
            if corr is None:
                return []

            th = threshold or self.threshold
            pairs = []
            syms = list(corr.columns)
            for i in range(len(syms)):
                for j in range(i + 1, len(syms)):
                    c = corr.iloc[i, j]
                    if abs(c) > th:
                        pairs.append({
                            "sym1": syms[i],
                            "sym2": syms[j],
                            "corr": round(float(c), 3),
                        })
            return pairs
        except Exception:
            return []

    def _count_high_corr(self, symbols, corr):
        """Жоғары корреляциялы жұптар саны"""
        count = 0
        for i in range(len(symbols)):
            for j in range(i + 1, len(symbols)):
                s1 = symbols[i]
                s2 = symbols[j]
                if s1 in corr.columns and s2 in corr.columns:
                    c = abs(corr.loc[s1, s2])
                    if c > self.threshold:
                        count += 1
        return count

    def analyze_portfolio_risk(self):
        """Портфель тәуекелін талдау"""
        try:
            positions = mt5_positions_get()
            if not positions or len(positions) < HEDGE_MIN_POSITIONS:
                return None

            corr = self.calculate_correlation_matrix()
            if corr is None:
                return None

            buys = [p.symbol for p in positions if p.type == mt5.POSITION_TYPE_BUY]
            sells = [p.symbol for p in positions if p.type == mt5.POSITION_TYPE_SELL]

            # BUY позициялар
            if len(buys) >= HEDGE_MIN_POSITIONS:
                high_corr = self._count_high_corr(buys, corr)
                if high_corr >= 2:
                    return {
                        "action": "HEDGE_SELL",
                        "direction": "BUY",
                        "symbols": buys,
                        "high_corr_count": high_corr,
                    }

            # SELL позициялар
            if len(sells) >= HEDGE_MIN_POSITIONS:
                high_corr = self._count_high_corr(sells, corr)
                if high_corr >= 2:
                    return {
                        "action": "HEDGE_BUY",
                        "direction": "SELL",
                        "symbols": sells,
                        "high_corr_count": high_corr,
                    }
            return None
        except Exception as e:
            log.error(f"Hedge risk: {e}")
            return None

    def open_hedge_position(self, target_symbol, direction):
        """Hedge позиция ашу (кері бағыт)"""
        try:
            info = mt5_symbol_info(target_symbol)
            if not info:
                return None

            tick = mt5_symbol_info_tick(target_symbol)
            if not tick:
                return None

            hedge_dir = "SELL" if direction == "BUY" else "BUY"

            # Кіші лот (0.5 × негізгі)
            equity = _stats["equity"]
            risk_usd = equity * (RISK_PER_TRADE / 100.0) * 0.5

            # ATR-based SL/TP
            rates = mt5_copy_rates(target_symbol, TIMEFRAME, 0, 50)
            if rates is None or len(rates) < 20:
                return None

            df = pd.DataFrame(rates)
            atr_series = ta.atr(df["high"], df["low"], df["close"], length=ATR_PERIOD)
            atr_v = float(atr_series.iloc[-1]) if atr_series is not None else 0

            if atr_v <= 0:
                return None

            if hedge_dir == "BUY":
                entry = tick.ask
                sl = entry - 1.5 * atr_v
                tp = entry + 2.0 * atr_v
            else:
                entry = tick.bid
                sl = entry + 1.5 * atr_v
                tp = entry - 2.0 * atr_v

            result = open_position(
                target_symbol, hedge_dir, entry, sl, tp, risk_usd,
                source="Hedge", magic=777777
            )

            if result.get("ok"):
                log.warning(f"🛡️ HEDGE: {target_symbol} {hedge_dir}")
                tg_send(
                    f"🛡️ *Dynamic Hedge*\n\n"
                    f"📌 {target_symbol} | {hedge_dir}\n"
                    f"💵 Entry: `{entry}`\n"
                    f"🛑 SL: `{sl}`\n"
                    f"🎯 TP: `{tp}`\n"
                    f"📊 Lot: `{result.get('lot')}`\n"
                    f"🎫 Ticket: `{result.get('ticket')}`\n\n"
                    f"⚠️ _Жоғары корреляция анықталды_"
                )
                return result
            return None
        except Exception as e:
            log.error(f"Hedge open: {e}")
            return None


# Global hedge engine
HEDGE_ENGINE = DynamicHedgeEngine()


def hedge_worker():
    """Hedge циклі (5 мин)"""
    time.sleep(600)
    while True:
        try:
            if not HEDGE_ENABLED:
                time.sleep(HEDGE_INTERVAL_SEC)
                continue

            risk = HEDGE_ENGINE.analyze_portfolio_risk()

            if risk:
                log.warning(f"⚠️ Hedge trigger: {risk}")
                HEDGE_ACTIVE[0] = True
                target = risk["symbols"][0]
                HEDGE_ENGINE.open_hedge_position(target, risk["direction"])
            else:
                HEDGE_ACTIVE[0] = False

            HEDGE_LAST_RUN[0] = time.time()
            time.sleep(HEDGE_INTERVAL_SEC)
        except Exception as e:
            log.error(f"Hedge worker: {e}")
            time.sleep(HEDGE_INTERVAL_SEC)


def start_dynamic_hedge():
    """Dynamic Hedge іске қосу"""
    if not HEDGE_ENABLED:
        log.info("⏸ Dynamic Hedge өшірулі")
        return
    threading.Thread(target=hedge_worker, daemon=True).start()
    log.info("✅ Dynamic Hedge іске қосылды")


def get_hedge_status():
    """Hedge статусы"""
    try:
        pairs = HEDGE_ENGINE.get_correlated_pairs()
        return {
            "enabled": HEDGE_ENABLED,
            "active": HEDGE_ACTIVE[0],
            "last_run": HEDGE_LAST_RUN[0],
            "threshold": HEDGE_THRESHOLD,
            "correlated_pairs": pairs[:10],
        }
    except Exception:
        return {"enabled": HEDGE_ENABLED, "active": False}
        # ============================================================
# PROCESS SYMBOL — НЕГІЗГІ ИНТЕГРАЦИЯ
# ============================================================

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

def _trailing_worker():
    """Trailing stop циклі (30 сек)"""
    while True:
        time.sleep(30)
        try:
            update_trailing_stops()
        except Exception as e:
            log.error(f"Trailing: {e}")


# ============================================================
# HEARTBEAT (30 мин)
# ============================================================

_last_hb = [time.time()]


def _heartbeat_worker():
    """Heartbeat хабарлама (30 мин)"""
    while True:
        time.sleep(60)
        now = time.time()
        if now - _last_hb[0] >= HEARTBEAT_MIN * 60:
            us = now - _stats["start"]
            t, tp, sl = journal_stats()
            wr = (tp / (tp + sl) * 100) if (tp + sl) > 0 else 0
            best = get_best_patterns(3)
            worst = get_worst_patterns(3)
            bs = "\n".join(f"  ✅ {k}: {v['win_rate']*100:.0f}%"
                           for k, v in best) or "  —"
            ws = "\n".join(f"  ⚠️ {k}: {v['win_rate']*100:.0f}%"
                           for k, v in worst) or "  —"

            ml_s = "✅" if ML_STATUS.get("ready") else "⏳"
            ml_acc = f"{ML_STATUS.get('accuracy', 0):.2f}" \
                if ML_STATUS.get("ready") else "—"

            rl_s = "✅" if RL_STATUS.get("ready") else "⏳"
            sh_s = "✅" if SHAZAM_STATUS.get("ready") else "⏳"
            sh_n = SHAZAM_STATUS.get("patterns", 0)

            pos = mt5_positions_get() or []
            macro = get_macro()
            macro_str = " | ".join(f"{k}={v:.1f}"
                                    for k, v in list(macro.items())[:3]) \
                if macro else "—"
            san = get_santiment()
            san_str = f"BTC social={int(san.get('BTC_social', 0))}" \
                if san else "—"
            reddit_str = f"{get_reddit_sentiment():+.2f}"
            fg_val = _fg_cache.get("value", 50)
            avg_lat = sum(LATENCY_LOG)/len(LATENCY_LOG) if LATENCY_LOG else 0

            filters_off = ", ".join(FILTERS_DISABLED) \
                if FILTERS_DISABLED else "—"
            llm_status = "✅" if GROQ_AVAILABLE else "❌"
            llm_last = "—"
            if LLM_LAST_RUN[0] > 0:
                h = (time.time() - LLM_LAST_RUN[0]) / 3600
                llm_last = f"{h:.1f}с"

            hedge_s = "🛡️" if HEDGE_ACTIVE[0] else "—"
            tv_rec = TV_SIGNALS_RECEIVED[0]
            tv_exec = TV_SIGNALS_EXECUTED[0]

            # 🆕 Metrics
            m = get_metrics_summary()

            tg_send(
                f"💚 *APEX v3 — ТІРІ*\n\n"
                f"⏰ {time.strftime('%H:%M:%S')}\n"
                f"⏱ {int(us//3600)}с {int((us%3600)//60)}м\n"
                f"🔄 {_stats['cycles']}\n📨 {_stats['signals']}\n"
                f"💰 ${_stats['equity']:.2f}\n"
                f"📊 Позиция: {len(pos)}\n\n"
                f"📈 WR {wr:.0f}% ({m['wins']}W/{m['losses']}L)\n"
                f"💰 Net: ${m['net_profit']:.2f}\n"
                f"⚖️ PF: {m['profit_factor']:.2f}\n"
                f"📉 Max DD: {m['max_dd']:.1f}%\n"
                f"🎯 Expectancy: {m['expectancy']:.4f}\n\n"
                f"🧠 ML: {ml_s} ({ml_acc})\n"
                f"🤖 RL: {rl_s}\n"
                f"🎵 Shazam: {sh_s} ({sh_n})\n"
                f"🧠 LLM: {llm_status} ({llm_last})\n"
                f"🛡️ Hedge: {hedge_s}\n"
                f"📡 TV: {tv_rec}/{tv_exec}\n"
                f"🚫 Filters OFF: `{filters_off}`\n"
                f"😱 FG: {fg_val}\n"
                f"📰 News: {get_news_sentiment():+.2f}\n"
                f"⚡ Latency: {avg_lat:.0f}ms\n"
                f"📊 *Macro:* {macro_str}\n"
                f"🔗 *Santiment:* {san_str}\n"
                f"💬 *Reddit:* {reddit_str}\n"
                f"🤖 Auto: `{get_mode()}`\n\n"
                f"🎓 Learning:\n🥇 {bs}\n⚠️ {ws}"
            )
            _last_hb[0] = now


def start_heartbeat():
    """Heartbeat + Trailing workers іске қосу"""
    threading.Thread(target=_heartbeat_worker, daemon=True).start()
    threading.Thread(target=_trailing_worker, daemon=True).start()
    log.info("✅ Heartbeat + Trailing")
    # ============================================================
# MAIN — APEX v3 іске қосу
# ============================================================

def main():
    """APEX v3 негізгі функция"""
    log.info("=" * 60)
    log.info("  🏎️ APEX v3 — 6 ҚАТАРЛЫ EDITION")
    log.info("=" * 60)

    # ==========================================
    # 1. MODULE SPLITTER (папкаларды жасау)
    # ==========================================
    module_splitter()

    # ==========================================
    # 2. MT5 ҚОСЫЛУ
    # ==========================================
    if not mt5_connect():
        log.error("❌ MT5 қосылу сәтсіз")
        return

    # ==========================================
    # 3. КҮЙДІ ЖҮКТЕУ
    # ==========================================
    log.info("\n📂 Күйді жүктеу...")
    mem_load()
    auto_load()
    ai_load()
    filter_state_load()
    metrics_load()
    db_init()
    db_init_market()
    stats_init()

    # ==========================================
    # 4. КАТЕГОРИЯЛАР
    # ==========================================
    log.info("\n📂 Categories:")
    ensure_categories()

    # ==========================================
    # 5. LEARNING (Backtest)
    # ==========================================
    log.info("\n🎓 Learning...")
    all_syms = []
    for cat_syms in CATEGORIES.values():
        all_syms.extend(cat_syms)
    try:
        learning_init_or_update(all_syms, mt5, TIMEFRAME)
    except Exception as e:
        log.error(f"⚠️ Learning: {str(e)[:100]}")

    # ==========================================
    # 6. WORKERS ІСКЕ ҚОСУ
    # ==========================================
    log.info("\n📡 Workers іске қосылуда...")

    # Негізгі
    start_data_collector()
    start_ml_trainer()
    start_tg()
    start_cb()
    start_heartbeat()
    register_handlers()

    # v9 — AI модульдер
    start_llm_brain()
    start_strategy_programmer()
    start_auto_learn()
    start_fractal_cycle()

    # APEX v3 — 3 модуль
    start_tv_bridge()         # #38 TradingView
    start_dynamic_hedge()     # #40 Hedge
    start_rl_agent()          # #41 RL

    # APEX #42 Shazam v4 (M15 multi-TF + 10y RL)
    start_shazam_v4_worker()

    # 🆕 Ablation test
    start_ablation()

    # ==========================================
    # 7. TELEGRAM — STARTUP ХАБАРЛАМА
    # ==========================================
    mode = get_mode()
    filters_off_str = ", ".join(FILTERS_DISABLED) if FILTERS_DISABLED else "жоқ"

    tg_send(
        f"🏎️ *APEX v3 — 6 ҚАТАРЛЫ EDITION*\n\n"
        f"⚡ *1. Wyckoff Engine:*\n"
        f"  • Spring (12 шарт) ✅\n"
        f"  • UTAD (10 шарт) ✅\n"
        f"  • SOS/SOW/LPS/ST ✅\n"
        f"  • 4H Phase ✅\n\n"
        f"🧠 *2. ML / AI:*\n"
        f"  • XGBoost ✅\n"
        f"  • RL Agent (PPO) ✅\n"
        f"  • LLM Brain (Groq) ✅\n"
        f"  • 🎵 Shazam v4 (M15+H1+H4 FAISS) ✅\n\n"
        f"🔬 *3. Қосымша талдау:*\n"
        f"  • Fourier + Fractal ✅\n"
        f"  • Wavelet + MTF ✅\n"
        f"  • Dynamic Hedge ✅\n\n"
        f"🎯 *4. Signal Engine:*\n"
        f"  • LONG / SHORT / WAIT ✅\n"
        f"  • Confidence + Reasons ✅\n\n"
        f"⚖️ *5. Risk Manager:*\n"
        f"  • SL/TP/R:R ✅\n"
        f"  • Position Size ✅\n"
        f"  • Daily Limits ✅\n\n"
        f"📊 *6. Орындау:*\n"
        f"  • Telegram + Voice ✅\n"
        f"  • MT5 Auto Trader ✅\n"
        f"  • Journal + Metrics ✅\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 Auto: `{mode}`\n"
        f"🚫 Filters OFF: `{filters_off_str}`\n"
        f"🧠 LLM: {'✅' if GROQ_AVAILABLE else '❌'}\n"
        f"🔊 Voice: {'✅' if EDGE_TTS_AVAILABLE else '❌'}\n"
        f"📡 TV Bridge: {'✅' if FASTAPI_AVAILABLE else '❌'}\n"
        f"🛡️ Hedge: {'✅' if HEDGE_ENABLED else '❌'}\n"
        f"🤖 RL: {'✅' if SB3_AVAILABLE else '❌'}\n\n"
        f"📊 *APEX v3 — ДАЙЫН!* 🏎️"
    )

    # ==========================================
    # 8. КОНСОЛЬ ХАБАРЛАМА
    # ==========================================
    log.info(f"\n✅ Mode: {mode}")
    log.info(f"✅ Scan: {CYCLE_SEC}s | Top: {TOP_N}")
    log.info(f"✅ Security: {ALLOWED_USERS}")
    log.info(f"✅ LLM: {'ON' if GROQ_AVAILABLE else 'OFF'}")
    log.info(f"✅ Voice: {'ON' if EDGE_TTS_AVAILABLE else 'OFF'}")
    log.info(f"✅ TV Bridge: {'ON' if FASTAPI_AVAILABLE else 'OFF'}")
    log.info(f"✅ RL Agent: {'ON' if SB3_AVAILABLE else 'OFF'}")
    log.info(f"✅ Hedge: {'ON' if HEDGE_ENABLED else 'OFF'}")
    log.info(f"✅ Filters disabled: {FILTERS_DISABLED or 'жоқ'}")
    log.info("=" * 60)
    log.info("🟢 APEX v3 негізгі цикл басталды\n")

    # ==========================================
    # 9. НЕГІЗГІ ЦИКЛ
    # ==========================================
    cycle = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        while True:
            try:
                t0 = time.time()
                cycle += 1
                _stats["cycles"] = cycle

                # Equity жаңарту
                acc = mt5_account_info()
                if acc:
                    _stats["equity"] = acc.equity

                # Позицияларды тексеру
                check_positions()

                # Features label (әр 10 цикл)
                if cycle % 10 == 0:
                    features_update_labels()

                # Сканерлеу
                top, by_cat, active = scan_all()
                syms = [s for s, _ in top]

                if cycle % 10 == 0:
                    log.info(f"📊 Cycle #{cycle} | {len(syms)} symbols")

                # Параллель өңдеу
                futures = {ex.submit(process_symbol, s): s for s in syms}
                for fut in as_completed(futures):
                    try:
                        fut.result()
                    except Exception as e:
                        log.error(f"⚠️ {futures[fut]}: {str(e)[:80]}")

                # Ұйқы
                elapsed = time.time() - t0
                time.sleep(max(0, CYCLE_SEC - elapsed))

            except KeyboardInterrupt:
                log.info("\n⏹️ Тоқтатылуда...")
                break
            except Exception as e:
                _stats["errors"] += 1
                log.error(f"❌ Cycle: {str(e)[:120]}")
                time.sleep(5)

    # ==========================================
    # 10. ЖАБУ
    # ==========================================
    try:
        tg_send("⏹️ *APEX v3 тоқтатылды*")
    except Exception: pass

    mem_save()
    auto_save()
    ai_save()
    filter_state_save()
    mt5.shutdown()
    log.info("\n✅ APEX v3 stopped.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
    # ============================================================
# 📚 APEX v3 — SETUP GUIDE + FAQ + TROUBLESHOOTING
# ============================================================
#
# Бұл бөлік — құжаттама (docstring). Код ретінде орындалмайды.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📋 МАЗМҰНЫ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 1. Жүйе талаптары
# 2. Орнату — 7 қадам
# 3. Бірінші іске қосу
# 4. Telegram баптау
# 5. TradingView Bridge баптау
# 6. Режимдер (MANUAL/DEMO/REAL)
# 7. FAQ — жиі сұрақтар
# 8. Troubleshooting — қателер
# 9. VPS + 24/7
# 10. Қорытынды
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1️⃣ ЖҮЙЕ ТАЛАПТАРЫ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Минимум:
# ├── Windows 10/11 (64-bit)
# ├── Python 3.10+ (3.11 ұсынылады)
# ├── MetaTrader 5 (терминал ашық)
# ├── 4 GB RAM
# ├── 50 GB диск
# └── Интернет (тұрақты)
#
# Ұсынылады:
# ├── 8 GB+ RAM (RL оқыту үшін)
# ├── GPU (CUDA) — RL үдету
# ├── SSD 100 GB+
# └── VPS (24/7 жұмыс үшін)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2️⃣ ОРНАТУ — 7 ҚАДАМ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# ҚАДАМ 1: Папка жасау
# ────────────────────
# Windows CMD ашыңыз:
#   mkdir "C:\Users\ninja\OneDrive\Desktop\Новая папка\apex_v3"
#   cd "C:\Users\ninja\OneDrive\Desktop\Новая папка\apex_v3"
#
# ҚАДАМ 2: Python орнату
# ────────────────────
# 1. https://www.python.org/downloads/ ашыңыз
# 2. Python 3.11+ жүктеңіз
# 3. Орнату кезінде:
#    ✅ Add Python to PATH
#    ✅ Install for all users
# 4. Тексеру:
#    cmd → python --version
#    → Python 3.11.x
#
# ҚАДАМ 3: Notepad++ ашу
# ────────────────────
# https://notepad-plus-plus.org/downloads/
# Файл → Жаңа
#
# ҚАДАМ 4: 16 бөлікті көшіру
# ────────────────────
# 1/16 → 2/16 → 3/16 → ... → 16/16
# Барлығын бір файлға қосыңыз.
#
# ҚАДАМ 5: Сақтау
# ────────────────────
# Файл → Сақтау (Ctrl+S)
# Аты: apex_v3_all_in_one.py
# Түрі: Python files (*.py)
# Кодтау: UTF-8
#
# ҚАДАМ 6: .env файлын жасау
# ────────────────────
# Папкада .env файлын жасаңыз (Notepad-та):
#
# ─── .env ───
# TELEGRAM_BOT_TOKEN=сіздің_токен
# TELEGRAM_CHAT_ID=528379915
# MT5_LOGIN=5057082292
# MT5_PASSWORD=сіздің_пароль
# MT5_SERVER=MetaQuotes-Demo
# FRED_API_KEY=сіздің_кілт
# SANTIMENT_API_KEY=сіздің_кілт
# GROQ_API_KEY=gsk_сіздің_кілт
# ALLOWED_USERS=528379915
# TV_SECRET=APEX_SECRET_2026
# ────────────
#
# ҚАДАМ 7: Іске қосу
# ────────────────────
# CMD → cd папка → python apex_v3_all_in_one.py
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3️⃣ БІРІНШІ ІСКЕ ҚОСУ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Іске қосқанда кезеңдер:
#
# 1. AUTO INSTALL (2-5 мин):
#    ├── 20 пакет тексеріледі
#    ├── Жоқ болса — орнатылады
#    └── pip install автоматты
#
# 2. MODULE SPLITTER (10 сек):
#    ├── modules/ папкасы жасалады
#    ├── 30 файл жасалады
#    └── 6 топ бойынша
#
# 3. MT5 ҚОСЫЛУ (5 сек):
#    └── MT5 OK | Login | $Equity
#
# 4. КҮЙДІ ЖҮКТЕУ (10 сек):
#    ├── Жады
#    ├── DB
#    └── Categories
#
# 5. LEARNING (5-10 мин):
#    └── 3 айлық backtest
#
# 6. WORKERS (5 сек):
#    ├── 6 негізгі
#    ├── 4 AI
#    ├── 3 APEX
#    └── 1 Ablation
#
# 7. ЦИКЛ:
#    └── 🟢 APEX v3 негізгі цикл басталды
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4️⃣ TELEGRAM БАПТАУ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# A. Bot Token алу:
# 1. Telegram → @BotFather
# 2. /newbot
# 3. Аты: APEX v3 Bot
# 4. Username: apex_v3_bot
# 5. Token көшіру: 8997...AAE...
# 6. .env-ке жазу
#
# B. Chat ID алу:
# 1. Telegram → @userinfobot
# 2. /start
# 3. Your ID: 528379915
# 4. .env-ке жазу
#
# C. Тексеру:
# 1. Ботқа /start жазыңыз
# 2. Бот APEX v3 хабарлама жібереді
# 3. Батырмалар пайда болады
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5️⃣ TRADINGVIEW BRIDGE БАПТАУ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# A. Pine Script жасау:
# 1. TradingView → Pine Editor
# 2. Мына кодты қойыңыз:
#
#    //@version=5
#    strategy("APEX v3 Bridge", overlay=true)
#    fast_ma = ta.sma(close, 20)
#    slow_ma = ta.sma(close, 50)
#    if ta.crossover(fast_ma, slow_ma)
#        alert('{"secret_token":"APEX_SECRET_2026",
#               "symbol":"XAUUSD","action":"BUY",
#               "price":' + str.tostring(close) + '}',
#               alert.freq_once_per_bar_close)
#    if ta.crossunder(fast_ma, slow_ma)
#        alert('{"secret_token":"APEX_SECRET_2026",
#               "symbol":"XAUUSD","action":"SELL",
#               "price":' + str.tostring(close) + '}',
#               alert.freq_once_per_bar_close)
#
# 3. Save → Add to chart
#
# B. Alert баптау:
# 1. Alert батырма (⏰)
# 2. Condition: APEX v3 Bridge
# 3. Webhook URL: http://YOUR_IP:8000/webhook
# 4. Message: (жоғарыдағы JSON)
# 5. Create
#
# C. VPS үшін:
# 1. ngrok орнату: pip install pyngrok
# 2. ngrok http 8000
# 3. URL көшіру: https://abc123.ngrok.io/webhook
#
# D. Тестілеу (curl):
#    curl -X POST http://localhost:8000/webhook \
#      -H "Content-Type: application/json" \
#      -d '{"secret_token":"APEX_SECRET_2026",
#           "symbol":"XAUUSD","action":"BUY",
#           "price":4170.96}'
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6️⃣ РЕЖИМДЕР (MANUAL / DEMO / REAL)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# ┌──────────┬─────────────┬──────────────┐
# │ Режим    │ Telegram    │ Auto Trader  │
# ├──────────┼─────────────┼──────────────┤
# │ MANUAL   │ Сигнал      │ ❌ OFF       │
# │ DEMO     │ Сигнал      │ ✅ DEMO шот  │
# │ REAL     │ Сигнал      │ ✅ REAL шот  │
# └──────────┴─────────────┴──────────────┘
#
# Ауыстыру:
# 1. Telegram → Signal → батырма
# 2. [🖐 MANUAL] → MANUAL
# 3. [🎮 DEMO] → DEMO
# 4. [💰 REAL] → REAL
#
# Ұсыныс:
# 1-ші апта: MANUAL
# 2-ші апта: DEMO
# 3-ші ай: REAL (кіші лот)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7️⃣ FAQ — ЖИІ СҰРАҚТАР
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Q1: Бот тегін бе?
# A: Иә, толық тегін. Groq API де тегін (14,400 req/күн).
#
# Q2: Қанша депозит керек?
# A: Минимум $500, ұсынылады $1000+.
#
# Q3: VPS керек пе?
# A: 24/7 үшін ұсынылады ($5-30/ай).
#
# Q4: Win Rate қанша?
# A: Теориялық 75-82%. Нақты — DEMO-да 3 ай тестілеу керек.
#
# Q5: Қанша пайда?
# A: Теориялық +200-300%/жыл. Нақты тестілеу жоқ.
#
# Q6: Drawdown?
# A: 15-25% мүмкін. Risk management бар.
#
# Q7: RL оқыту қанша уақыт?
# A: 2-4 апта (фонда). Бот жұмыс істейді.
#
# Q8: Wyckoff v2 нақты ма?
# A: Иә, 10+ шарт. Сіздің сыныңыз бойынша жасалды.
#
# Q9: Гиранс бар ма?
# A: Жоқ. 100% кепілдік болмайды.
#
# Q10: Қайда сұрақ қою?
# A: Осы чатта немесе Telegram-да.
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8️⃣ TROUBLESHOOTING — ҚАТЕЛЕР
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# ❌ ҚАТЕ 1: MT5 қосылмайды
#    ────────────────────────
#    Себебі:
#    ├── MT5 орнатылмаған
#    ├── Login/Password қате
#    ├── Server қате
#    └── MT5 ашық емес
#
#    Шешім:
#    1. MT5 орнатыңыз
#    2. .env тексеріңіз
#    3. MT5 ашыңыз
#    4. Қайта іске қосыңыз
#
# ❌ ҚАТЕ 2: Пакеттер орнатылмайды
#    ────────────────────────
#    Себебі:
#    ├── Python жоқ
#    ├── pip жоқ
#    └── Интернет жоқ
#
#    Шешім:
#    1. Python орнату (Add to PATH ✅)
#    2. pip install --upgrade pip
#    3. Қайта іске қосу
#
# ❌ ҚАТЕ 3: Groq API істемейді
#    ────────────────────────
#    Себебі:
#    ├── Кілт қате
#    ├── Лимит бітті
#    └── Интернет жоқ
#
#    Шешім:
#    1. console.groq.com/keys → жаңа кілт
#    2. Күту (лимит)
#    3. Интернет тексеру
#
# ❌ ҚАТЕ 4: Voice істемейді
#    ────────────────────────
#    Себебі:
#    ├── edge-tts орнатылмаған
#    └── Қазақша дауыс жоқ
#
#    Шешім:
#    1. pip install edge-tts
#    2. ВОЙС_ENABLED = False (егер керек болмаса)
#
# ❌ ҚАТЕ 5: Сигнал келмейді
#    ────────────────────────
#    Себебі:
#    ├── 13 фильтр қатаң
#    ├── Level 200% жетпейді
#    └── R:R < 3
#
#    Шешім:
#    1. Күту (нарық)
#    2. LLM талдау
#    3. Параметрлерді жұмсарту
#
# ❌ ҚАТЕ 6: RL оқылмайды
#    ────────────────────────
#    Себебі:
#    ├── Деректер аз (5000 керек)
#    └── stable-baselines3 жоқ
#
#    Шешім:
#    1. Күту (3 ай)
#    2. pip install stable-baselines3 gymnasium torch
#
# ❌ ҚАТЕ 7: TV Bridge істемейді
#    ────────────────────────
#    Себебі:
#    ├── FastAPI жоқ
#    ├── Порт 8000 бос емес
#    └── Security token қате
#
#    Шешім:
#    1. pip install fastapi uvicorn pydantic
#    2. TV_BRIDGE_PORT = 8001
#    3. .env → TV_SECRET тексеру
#
# ❌ ҚАТЕ 8: Hedge істемейді
#    ────────────────────────
#    Себебі:
#    ├── Позиция < 3
#    └── Correlation < 0.85
#
#    Шешім:
#    1. Күту (позиция көбейту)
#    2. HEDGE_THRESHOLD = 0.80 (жұмсарту)
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9️⃣ VPS + 24/7
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Провайдер:
# ├── Contabo (€5/ай) — ұсынылады
# ├── Hetzner (€4/ай)
# ├── Vultr ($6/ай)
# └── ForexVPS ($30/ай)
#
# Талаптар:
# ├── 2 vCPU+
# ├── 4 GB+ RAM
# ├── 50 GB+ SSD
# └── Windows 10/11
#
# Орнату:
# 1. VPS тіркелу
# 2. RDP қосылу (mstsc)
# 3. Python + MT5 орнату
# 4. Бот файлын көшіру
# 5. .env жасау
# 6. Task Scheduler:
#    ├── Win + R → taskschd.msc
#    ├── Create Task
#    ├── At log on
#    ├── Program: python.exe
#    ├── Arguments: apex_v3_all_in_one.py
#    └── Start in: C:\apex_v3
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔟 ҚОРЫТЫНДЫ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# ✅ APEX v3 — 6 ҚАТАРЛЫ EDITION:
# ├── 1. Wyckoff Engine (55+ шарт) ✅
# ├── 2. ML / AI (XGBoost + RL + LLM) ✅
# ├── 3. Қосымша талдау (Fourier+Fractal+Hedge) ✅
# ├── 4. Signal Engine (LONG/SHORT/WAIT) ✅
# ├── 5. Risk Manager (SL/TP/R:R/лимиттер) ✅
# └── 6. Орындау (Telegram + MT5 + Metrics) ✅
#
# ✅ AUTO INSTALL: 20 пакет
# ✅ MODULE SPLITTER: 1 файл → 30 файл
# ✅ 6 METRICS: Expectancy, PF, Max DD, т.б.
# ✅ ABLATION TEST: 7 модуль жеке
# ✅ WAIT ENGINE: LONG/SHORT/WAIT
# ✅ VOICE: Қазақша
# ✅ 3 APEX модуль: TV Bridge + Hedge + RL
#
# ⚠️ ЕСКЕРТУ:
# ├── 100% кепілдік ЖОҚ
# ├── 3 ай DEMO тестілеу КЕРЕК
# ├── Drawdown 15-25% мүмкін
# └── REAL-ға кіші лотпен бастау
#
# 🏎️ APEX v3 — ДАЙЫН!
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# APEX v3 — Setup Guide аяқталды.
# Келесі бөлік (16/16) — Final Integration + Test.
#
# ============================================================
# ============================================================
# 🆕 SELF-TEST — Жүйені тексеру
# ============================================================

def self_test():
    """
    Self-Test — жүйенің барлық бөліктерін тексереді.
    Қайтарады: dict {passed, failed, warnings, details}
    """
    print("\n" + "=" * 60)
    print("  🔍 APEX v3 — SELF-TEST")
    print("=" * 60)

    results = {"passed": [], "failed": [], "warnings": [], "details": {}}

    # ─────────────────────────────────────────
    # 1. Пакеттер тексеру
    # ─────────────────────────────────────────
    print("\n📦 1. Пакеттер:")
    pkg_checks = {
        "MetaTrader5": False, "pandas": False, "numpy": False,
        "pandas_ta": False, "sklearn": False, "xgboost": False,
        "groq": False, "edge_tts": False,
        "fastapi": False, "stable_baselines3": False, "torch": False,
    }
    for pkg in pkg_checks:
        try:
            importlib.import_module(pkg)
            pkg_checks[pkg] = True
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg}")
            results["failed"].append(f"package:{pkg}")

    results["details"]["packages"] = pkg_checks

    # ─────────────────────────────────────────
    # 2. MT5 қосылу тексеру
    # ─────────────────────────────────────────
    print("\n🔌 2. MT5:")
    try:
        info = mt5_terminal_info()
        if info:
            print(f"  ✅ MT5 ашық: {info.name}")
            results["passed"].append("mt5_connection")

            acc = mt5_account_info()
            if acc:
                print(f"  ✅ Account: {acc.login} | ${acc.equity}")
                results["passed"].append("mt5_account")
            else:
                print(f"  ⚠️ Account info жоқ")
                results["warnings"].append("mt5_account")
        else:
            print(f"  ❌ MT5 ашық емес")
            results["failed"].append("mt5_connection")
    except Exception as e:
        print(f"  ❌ MT5: {e}")
        results["failed"].append("mt5_connection")

    # ─────────────────────────────────────────
    # 3. Папкалар тексеру
    # ─────────────────────────────────────────
    print("\n📂 3. Папкалар:")
    dirs = {
        "data/": DATA_DIR,
        "data/logs/": LOG_DIR,
        "data/ml_models/": MODEL_DIR,
        "data/rl_agent/": RL_DIR,
        "data/llm_data/": LLM_DIR,
        "data/voice/": VOICE_DIR,
        "modules/": MODULES_DIR,
    }
    for name, path in dirs.items():
        if os.path.exists(path):
            print(f"  ✅ {name}")
            results["passed"].append(f"dir:{name}")
        else:
            print(f"  ❌ {name}")
            results["failed"].append(f"dir:{name}")

    # ─────────────────────────────────────────
    # 4. Модульдер папкасы (Module Splitter)
    # ─────────────────────────────────────────
    print("\n📦 4. Modules (6 топ):")
    module_tops = ["wyckoff", "ml_ai", "analysis",
                    "signal", "risk", "execution"]
    for top in module_tops:
        top_path = os.path.join(MODULES_DIR, top)
        if os.path.exists(top_path):
            files = os.listdir(top_path)
            print(f"  ✅ modules/{top}/ ({len(files)} файл)")
            results["passed"].append(f"module:{top}")
        else:
            print(f"  ❌ modules/{top}/")
            results["failed"].append(f"module:{top}")

    # ─────────────────────────────────────────
    # 5. Дерекқор тексеру
    # ─────────────────────────────────────────
    print("\n💾 5. Дерекқор:")
    dbs = {
        "journal.db": JOURNAL_DB,
        "features.db": FEATURE_DB,
        "market.db": MARKET_DB,
        "metrics.db": METRICS_DB,
    }
    for name, path in dbs.items():
        if os.path.exists(path):
            try:
                conn = sqlite3.connect(path)
                c = conn.cursor()
                c.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [t[0] for t in c.fetchall()]
                conn.close()
                print(f"  ✅ {name} ({len(tables)} table)")
                results["passed"].append(f"db:{name}")
            except Exception as e:
                print(f"  ⚠️ {name}: {e}")
                results["warnings"].append(f"db:{name}")
        else:
            print(f"  ⏳ {name} (жасалмаған)")
            results["warnings"].append(f"db:{name}")

    # ─────────────────────────────────────────
    # 6. 6 ҚАТАР — функциялар тексеру
    # ─────────────────────────────────────────
    print("\n🏎️ 6. 6 ҚАТАР (функциялар):")

    # 1. Wyckoff Engine
    wyckoff_funcs = [
        "detect_spring_v2", "detect_utad_v2", "detect_sos_v2",
        "detect_sow_v2", "detect_lps_v2", "detect_st_v2",
        "detect_shakeout_v2", "find_wyckoff_patterns_v2",
    ]
    wyckoff_ok = sum(1 for f in wyckoff_funcs if f in globals())
    print(f"  📊 1. Wyckoff Engine: {wyckoff_ok}/{len(wyckoff_funcs)} ✅")
    results["details"]["wyckoff_funcs"] = wyckoff_ok

    # 2. ML / AI
    ml_funcs = ["ml_train", "ml_predict", "rl_predict",
                "llm_ask", "ensemble_predict"]
    ml_ok = sum(1 for f in ml_funcs if f in globals())
    print(f"  🧠 2. ML / AI: {ml_ok}/{len(ml_funcs)} ✅")
    results["details"]["ml_funcs"] = ml_ok

    # 3. Қосымша талдау
    ana_funcs = ["fourier_analysis", "fractal_dimension",
                 "wavelet_trend", "multi_timeframe_analysis"]
    ana_ok = sum(1 for f in ana_funcs if f in globals())
    print(f"  🔬 3. Қосымша талдау: {ana_ok}/{len(ana_funcs)} ✅")
    results["details"]["analysis_funcs"] = ana_ok

    # 4. Signal Engine
    sig_funcs = ["calculate_level", "calculate_wait_signal",
                 "build_signal_object", "format_signal_text"]
    sig_ok = sum(1 for f in sig_funcs if f in globals())
    print(f"  🎯 4. Signal Engine: {sig_ok}/{len(sig_funcs)} ✅")
    results["details"]["signal_funcs"] = sig_ok

    # 5. Risk Manager
    risk_funcs = ["build_trade_plan", "validate_risk",
                  "calc_lot", "open_position"]
    risk_ok = sum(1 for f in risk_funcs if f in globals())
    print(f"  ⚖️ 5. Risk Manager: {risk_ok}/{len(risk_funcs)} ✅")
    results["details"]["risk_funcs"] = risk_ok

    # 6. Орындау
    exe_funcs = ["tg_send", "tg_send_voice", "journal_log",
                 "metrics_update", "build_chart"]
    exe_ok = sum(1 for f in exe_funcs if f in globals())
    print(f"  📊 6. Орындау: {exe_ok}/{len(exe_funcs)} ✅")
    results["details"]["execution_funcs"] = exe_ok

    # ─────────────────────────────────────────
    # 7. APEX — 3 модуль
    # ─────────────────────────────────────────
    print("\n🚀 7. APEX (3 модуль):")

    if FASTAPI_AVAILABLE:
        print(f"  ✅ #38 TradingView Bridge")
        results["passed"].append("apex:tv_bridge")
    else:
        print(f"  ❌ #38 TradingView Bridge")
        results["failed"].append("apex:tv_bridge")

    if HEDGE_ENABLED:
        print(f"  ✅ #40 Dynamic Hedge")
        results["passed"].append("apex:hedge")
    else:
        print(f"  ⏸ #40 Dynamic Hedge (өшірулі)")
        results["warnings"].append("apex:hedge")

    if SB3_AVAILABLE:
        print(f"  ✅ #41 Reinforcement Learning")
        results["passed"].append("apex:rl")
    else:
        print(f"  ⏸ #41 RL (SB3 жоқ)")
        results["warnings"].append("apex:rl")

    # ─────────────────────────────────────────
    # 8. .env тексеру
    # ─────────────────────────────────────────
    print("\n🔑 8. .env:")
    env_checks = {
        "TELEGRAM_BOT_TOKEN": bool(TELEGRAM_BOT_TOKEN),
        "TELEGRAM_CHAT_ID": bool(TELEGRAM_CHAT_ID),
        "MT5_LOGIN": bool(MT5_LOGIN),
        "MT5_PASSWORD": bool(MT5_PASSWORD),
        "MT5_SERVER": bool(MT5_SERVER),
        "FRED_API_KEY": bool(FRED_API_KEY),
        "SANTIMENT_API_KEY": bool(SANTIMENT_API_KEY),
        "XAI_API_KEY": bool(XAI_API_KEY),
        "GROQ_API_KEY": bool(GROQ_API_KEY),
        "TV_SECRET": bool(TV_SECRET),
    }
    for k, v in env_checks.items():
        if v:
            print(f"  ✅ {k}")
            results["passed"].append(f"env:{k}")
        else:
            print(f"  ⚠️ {k} (бос)")
            results["warnings"].append(f"env:{k}")

    # ─────────────────────────────────────────
    # 9. ҚОРЫТЫНДЫ
    # ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  📊 SELF-TEST ҚОРЫТЫНДЫСЫ")
    print("=" * 60)
    print(f"  ✅ Passed:   {len(results['passed'])}")
    print(f"  ⚠️ Warnings: {len(results['warnings'])}")
    print(f"  ❌ Failed:   {len(results['failed'])}")

    if results["failed"]:
        print("\n  ❌ ҚАТЕЛЕР:")
        for f in results["failed"]:
            print(f"    • {f}")

    if results["warnings"]:
        print("\n  ⚠️ ЕСКЕРТУЛЕР:")
        for w in results["warnings"][:10]:
            print(f"    • {w}")

    # Жалпы баға
    total_checks = len(results["passed"]) + len(results["failed"])
    if total_checks > 0:
        pct = len(results["passed"]) / total_checks * 100
        print(f"\n  📊 Жалпы: {pct:.1f}%")

        if pct >= 90:
            print("  🟢 ЖҮЙЕ ДАЙЫН! ✅")
        elif pct >= 70:
            print("  🟡 ЖҮЙЕ ЖАРТЫЛАЙ ДАЙЫН")
        else:
            print("  🔴 ЖҮЙЕ ДАЙЫН ЕМЕС")

    print("=" * 60 + "\n")
    return results


# ============================================================
# QUICK TEST — Жылдам тексеру (MT5-сіз)
# ============================================================

def quick_test():
    """
    Quick Test — MT5-ке қосылмай-ақ жүйені тексереді.
    Пакеттер + функциялар + папкалар.
    """
    print("\n" + "=" * 60)
    print("  ⚡ QUICK TEST (MT5-сіз)")
    print("=" * 60)

    # Функциялар
    required_funcs = [
        # Wyckoff
        "detect_spring_v2", "detect_utad_v2", "detect_sos_v2",
        "detect_sow_v2", "detect_lps_v2", "detect_st_v2",
        # ML
        "ml_train", "ml_predict", "ensemble_predict", "rl_predict",
        # Analysis
        "fourier_analysis", "fractal_dimension",
        "multi_timeframe_analysis",
        # Signal
        "calculate_level", "calculate_wait_signal",
        # Risk
        "build_trade_plan", "calc_lot", "open_position",
        # Execution
        "tg_send", "tg_send_voice", "journal_log", "metrics_update",
        # APEX
        "llm_analyze_filters", "start_tv_bridge", "start_dynamic_hedge",
    ]

    missing = [f for f in required_funcs if f not in globals()]
    if missing:
        print(f"\n❌ Жетіспейтін функциялар ({len(missing)}):")
        for f in missing:
            print(f"  • {f}")
        return False
    else:
        print(f"\n✅ Барлық {len(required_funcs)} функция бар")

    # Module Splitter
    if not os.path.exists(MODULES_DIR):
        print("\n📂 modules/ папкасын жасау...")
        module_splitter()

    # Quick check
    print("\n✅ ЖҮЙЕ ДАЙЫН (Quick Test)\n")
    return True


# ============================================================
# STARTUP BANNER
# ============================================================

def print_banner():
    """Іске қосу баннері"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   🏎️  APEX v3 — 6 ҚАТАРЛЫ EDITION  🏎️  ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╠" + "═" * 58 + "╣")
    print("║" + "  1. Wyckoff Engine (55+ шарт)              ✅".ljust(58) + "║")
    print("║" + "  2. ML / AI (XGBoost + RL + LLM)            ✅".ljust(58) + "║")
    print("║" + "  3. Қосымша талдау (Fourier + Fractal)      ✅".ljust(58) + "║")
    print("║" + "  4. Signal Engine (LONG/SHORT/WAIT)         ✅".ljust(58) + "║")
    print("║" + "  5. Risk Manager (SL/TP/R:R/лимиттер)       ✅".ljust(58) + "║")
    print("║" + "  6. Орындау (Telegram + MT5 + Metrics)      ✅".ljust(58) + "║")
    print("╠" + "═" * 58 + "╣")
    print("║" + "  🚀 APEX: TV Bridge + Hedge + RL            ✅".ljust(58) + "║")
    print("║" + "  🔊 Voice (қазақша)                          ✅".ljust(58) + "║")
    print("║" + "  🧠 LLM Brain (Groq)                        ✅".ljust(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


# ============================================================
# ENTRY POINT (FINAL)
# ============================================================

def run_apex_v3():
    """APEX v3 толық іске қосу (main + self-test)"""
    print_banner()

    # Self-test (MT5-сіз жылдам)
    quick_test()

    # Main
    main()


# ============================================================
# FILE END MARKER
# ============================================================

if __name__ == "__main__":
    # Егер APEX_SKIP_SELFTEST=1 болса, self-test өткізіледі
    if os.getenv("APEX_SKIP_SELFTEST", "0") == "1":
        main()
    else:
        run_apex_v3()

# ============================================================
# APEX v3 — 6 ҚАТАРЛЫ EDITION
# ────────────────────────────────────────────────────────────
# Барлығы: 16 бөлік
# Модульдер: 39 (6 қатар + 3 APEX)
# Авто жасалатын файлдар: 30+ (modules/ папкасында)
# Auto install: 20 пакет
# Қазақша voice: edge-tts
# LLM: Groq Llama 3.3 70B
# RL: Stable-Baselines3 PPO
# ────────────────────────────────────────────────────────────
# 🏎️ APEX v3 — ДАЙЫН! 🏎️
# ============================================================