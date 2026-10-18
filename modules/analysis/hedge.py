"""
ANALYSIS — hedge
APEX v3 модулі (нақты код module_splitter арқылы шығарылды)
Функциялар: DynamicHedgeEngine, start_dynamic_hedge
"""

# Авто-import safe: негізгі runtime — apex_v3_fixed.py
# Бұл файл құрылым / reuse / review үшін.

# --- DynamicHedgeEngine ---
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

# --- start_dynamic_hedge ---
def start_dynamic_hedge():
    """Dynamic Hedge іске қосу"""
    if not HEDGE_ENABLED:
        log.info("⏸ Dynamic Hedge өшірулі")
        return
    threading.Thread(target=hedge_worker, daemon=True).start()
    log.info("✅ Dynamic Hedge іске қосылды")



