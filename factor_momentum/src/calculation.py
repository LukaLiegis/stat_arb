def calculate_monthly_returns(df):
        df['monthly_return'] = df['close'].astype(float).pct_change()
        return df