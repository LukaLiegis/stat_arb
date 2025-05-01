import joblib

from src.features import prepare_features


def generate_trading_signal(crypto_dfs, target_crypto_idx = 0):

    try:
        model = joblib.load('models/crypto_model.pkl')
        scaler = joblib.load('models/crypto_scaler.pkl')

        X, _ = prepare_features(crypto_dfs, target_crypto_idx)
        X_scaled = scaler.transform(X)

        prediction = model.predict(X_scaled)

        return prediction

    except Exception as e:
        print(f"Error generating signal: {e}")
        return 0