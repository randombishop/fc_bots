from dotenv import load_dotenv
load_dotenv()
import os
import xgboost
import shap


print('Loading bird model...')
bird = xgboost.Booster() 
model_dir = os.path.dirname(os.path.abspath(__file__))
bird.load_model(model_dir + 'bird_0_0_1.xgb.json')
bird_explainer = shap.TreeExplainer(bird)
features = bird.feature_names
print('Bird model loaded.')
print('XGBoost features: ' + str(features))


def bird(df):
  df_features = df[features]
  dmatrix = xgboost.DMatrix(df_features)
  predict = bird.predict(dmatrix)
  shap_values = bird_explainer(dmatrix)
  shap_values.feature_names = features  
  return predict, df_features, shap_values

