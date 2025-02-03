import os
import xgboost
import shap


print('Loading bird model...')
bird_model = xgboost.Booster() 
model_dir = os.path.dirname(os.path.abspath(__file__))
bird_model.load_model(model_dir + '/' +'bird2.xgb.json')
bird_explainer = shap.TreeExplainer(bird_model)
features = bird_model.feature_names
print('Bird model loaded.')


def predict(df):
  dmatrix = xgboost.DMatrix(df[features])
  return bird_model.predict(dmatrix)


def bird(df):
  df_features = df[features]
  dmatrix = xgboost.DMatrix(df_features)
  predict = bird_model.predict(dmatrix)
  shap_values = bird_explainer(dmatrix)
  shap_values.feature_names = features  
  return predict, df_features, shap_values

