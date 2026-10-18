"""
EXECUTION — telegram_worker
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: tg_send, tg_buttons, tg_photo, tg_send_voice, start_tg, start_cb
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- tg_send ---
def tg_send(text):
    """Telegram-ға мәтін жіберу (queue)"""
    try: _tg_queue.put_nowait(("TEXT", text, None))
    except queue.Full: pass



# --- tg_buttons ---
def tg_buttons(text, markup):
    """Telegram-ға батырмалармен хабарлама"""
    try: _tg_queue.put_nowait(("BUTTONS", text, markup))
    except queue.Full: pass



# --- tg_photo ---
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



# --- start_tg ---
def start_tg():
    """Telegram worker іске қосу"""
    threading.Thread(target=_tg_worker, daemon=True).start()
    log.info("✅ TG worker")


# ============================================================
# VOICE (Қазақша)
# ============================================================


# --- tg_send_voice ---
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



# --- start_cb ---
def start_cb():
    """Callback + LLM chat worker іске қосу"""
    threading.Thread(target=_cb_worker, daemon=True).start()
    log.info(f"✅ CB worker + LLM chat | Security: {ALLOWED_USERS}")


# ============================================================
# CALLBACK HANDLERS
# ============================================================


