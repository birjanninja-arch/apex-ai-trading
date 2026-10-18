"""
ML_AI — rl_ppo
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: APEXTradingEnv, load_rl_training_data, train_rl_agent, rl_predict, rl_worker, start_rl_agent
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- APEXTradingEnv ---
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



# --- load_rl_training_data ---
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



# --- train_rl_agent ---
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



# --- rl_predict ---
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



# --- rl_worker ---
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



# --- start_rl_agent ---
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

# --- rl_predict ---
    def rl_predict(features):
        return 0.5


# --- train_rl_agent ---
    def train_rl_agent():
        return False


# --- start_rl_agent ---
    def start_rl_agent():
        log.info("⏸ RL өшірулі (SB3 жоқ)")


# ============================================================
# APEX #42 — SHAZAM v4 WORKER (M15 multi-TF + long RL)
# ============================================================


