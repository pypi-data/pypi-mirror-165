#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : shap_app
# @Time         : 2022/6/28 下午5:04
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 


import pandas as pd
from shapash.data.data_loader import data_loading
# 1.读取数据
house_df, house_dict = data_loading('house_prices')
y_df=house_df['SalePrice'].to_frame()
X_df=house_df[house_df.columns.difference(['SalePrice'])]

from category_encoders import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
# 2.数据预处理
categorical_features = [col for col in X_df.columns if X_df[col].dtype == 'object']
encoder = OrdinalEncoder(cols=categorical_features).fit(X_df)
X_df=encoder.transform(X_df)

## 3.模型训练预测
Xtrain, Xtest, ytrain, ytest = train_test_split(X_df, y_df, train_size=0.75)
reg = RandomForestRegressor(n_estimators=200, min_samples_leaf=2).fit(Xtrain,ytrain)
y_pred = pd.DataFrame(reg.predict(Xtest), columns=['pred'], index=Xtest.index)



from shapash.explainer.smart_explainer import SmartExplainer
# 4. 整体可视化
xpl = SmartExplainer(features_dict=house_dict) # Optional parameter
xpl.compile(
    x=Xtest,
    model=reg,
    preprocessing=encoder,# Optional: use inverse_transform method
    y_pred=y_pred # Optional
)

app = xpl.run_app()

