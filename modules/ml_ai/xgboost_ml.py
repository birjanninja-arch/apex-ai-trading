"""
ML_AI — xgboost_ml
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: ml_load_features, ml_train, ml_predict, ml_worker, start_ml_trainer
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- ml_load_features ---
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



# --- ml_train ---
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



# --- ml_predict ---
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



# --- ml_worker ---
def ml_worker():
    """ML оқыту циклі (24 сағат)"""
    time.sleep(3600)
    while True:
        try:
            ml_train()
            time.sleep(ML_TRAIN_INTERVAL_HOURS * 3600)
        except Exception:
            time.sleep(3600)



# --- start_ml_trainer ---
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


