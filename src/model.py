import joblib
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

from features import prepare_features

def train_model(crypto_dfs, target_crypto_idx=0, alpha=1.0):
    X, y = prepare_features(crypto_dfs, target_crypto_idx)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = Ridge(alpha=alpha)
    model.fit(X_scaled, y)

    joblib.dump(model, 'models/crypto_model.pkl')
    joblib.dump(scaler, 'models/crypto_scaler.pkl')

    return {'model': model, 'scaler': scaler, 'feature_names': X.columns}