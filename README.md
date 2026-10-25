# GemVal: Enterprise Diamond Valuation Engine

An end-to-end Machine Learning web application predicting diamond market retail value based on internationally recognized gemological standards (the 4Cs: Carat, Cut, Color, Clarity) and 3D facet caliper measurements.

## 🌐 Live Web Application
The deployed interactive valuation engine is live at:
👉 **[https://diamond-price-valuation.streamlit.app/](https://diamond-price-valuation.streamlit.app/)**

## Features
- **10-Fold Cross-Validation Benchmark**: Rigorous evaluation across 5 distinct algorithms on 53,920 records.
- **Production ML Pipeline**: Histogram Gradient Boosting Regressor (`HistGradientBoostingRegressor`) with sub-second inference and a 370 KB memory footprint.
- **Interactive UI**: Real-time fair market appraisal, confidence interval estimation, carat sensitivity curve, and valuation certificate export.

## Tech Stack
- **Framework**: Streamlit
- **ML & Pipelines**: Scikit-Learn (`Pipeline`, `ColumnTransformer`, `SimpleImputer`, `StandardScaler`, `OneHotEncoder`)
- **Data**: Pandas, NumPy
