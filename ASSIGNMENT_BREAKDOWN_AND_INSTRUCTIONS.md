# Comprehensive Assignment Breakdown & Execution Roadmap
**Course**: Machine Learning Fundamentals (AIC354)  
**Institution**: COMSATS University Islamabad, Lahore Campus  
**Instructor**: Dr. Rao Muhammad Adeel Nawab  
**Program Batch**: BS (CS) — Fall 2026  
**Maximum Marks**: 40  
**Submission Deadline**: Sunday, October 25, 2026 at 23:59  

---

## 1. Executive Summary & Core Objectives

The goal of this assignment is to master the end-to-end Machine Learning lifecycle on large, real-world tabular datasets using **K-Fold Cross-Validation**, **Google Colab**, and **Cloud Web Deployment**.

The assignment adopts a **"half-cooked" pedagogical approach**:
- **Task 1** provides a complete reference implementation for a *Car Price Prediction System*.
- **Task 2** requires you to choose a new, similar real-world regression problem, evaluate **5 new ML algorithms** (strictly excluding those used in Task 1) using **10-Fold Cross-Validation**, and deploy the trained model as a live web application on the cloud.

---

## 2. Key Policies & Deadlines

| Parameter | Policy Details |
| :--- | :--- |
| **Deadline** | Sunday, October 25, 2026 at 23:59 |
| **Late Submission Penalty** | 5% deduction per day |
| **Hard Cutoff** | Submissions made > 3 days late receive **0 Marks** |
| **Plagiarism Policy** | Strict institutional enforcement; all code and problem choices must be authentic |
| **Deployment Requirement** | The **live cloud deployment link must appear at the VERY TOP** of the submitted Jupyter Notebook |

---

## 3. Deep-Dive: Task 1 (Reference System Analysis)

### 3.1 Provided Artifacts
In `3 - Car Price Prediction K-Fold Cross Validation.zip`:
- `car_price_kfold_100_instances_3fold.ipynb`: Quick-run prototype (100 instances, 3 folds).
- `car_price_kfold_full_dataset_10fold.ipynb`: Full dataset benchmark (11,914 instances, 10 folds).
- `car_price.csv`: Kaggle car features dataset.
- GitHub Source: [https://github.com/haqnawaz99/ml-teaching-notebooks](https://github.com/haqnawaz99/ml-teaching-notebooks)

### 3.2 Algorithms Used in Task 1 (**FORBIDDEN FOR TASK 2**)
The instructor's reference benchmark already evaluated these 5 algorithms:
1. **Linear Regression** (`LinearRegression`)
2. **K-Nearest Neighbors** (`KNeighborsRegressor`)
3. **Decision Tree** (`DecisionTreeRegressor`)
4. **Random Forest** (`RandomForestRegressor`)
5. **Gradient Boosting** (`GradientBoostingRegressor`)

> **CRITICAL RULE**: In Task 2, you **CANNOT** use any of these 5 algorithms. You must choose 5 completely distinct algorithms.

### 3.3 The Instructor's Standard 12-Step Architecture
To obtain maximum marks, Task 2's notebook should strictly follow this exact 12-step structure:
- **Header**: Live Deployment URL, Title, Introduction, Input/Output definitions, Problem context.
- **Step 1: Import Libraries**: pandas, numpy, scikit-learn, matplotlib, seaborn, tqdm, pickle/joblib.
- **Step 2: Load Data**: Google Colab file upload integration & `pd.read_csv()`.
- **Step 3: Understand & Pre-process Data**: Shape, `.info()`, `.describe()`, missing values handling, target variable distribution (skewness analysis).
- **Step 4: Feature Extraction**: Clear segregation of `numeric_features` and `categorical_features`.
- **Step 5: Build Pre-processing Pipeline**: `ColumnTransformer` with `SimpleImputer`, `StandardScaler`, and `OneHotEncoder(handle_unknown='ignore')`.
- **Step 6: Define 5 Machine Learning Algorithms**: Instantiating 5 distinct models.
- **Step 7: Set Up 10-Fold Cross-Validation**: `KFold(n_splits=10, shuffle=True, random_state=42)`.
- **Step 8: Run 10-Fold CV for All 5 Algorithms**: `tqdm` progress bar, measuring validation RMSE for each fold.
- **Step 9: Compare Algorithms**:
  - Fold-by-fold RMSE table
  - Summary comparison table (Mean RMSE, Std Dev RMSE)
  - Visual comparisons (Boxplots of fold distributions, Bar charts with error bars)
  - In-depth analytical observations
- **Step 10: Train Final Model**:
  - Automatically select the best performing algorithm (lowest Mean RMSE)
  - Fit on 100% of the dataset
  - Serialize model with `pickle.dump()` or `joblib.dump()`
- **Step 11: Execute Application Phase**:
  - Interactive or default feature input dictionary
  - Conversion to DataFrame matching pipeline features
  - Reloading serialized model
  - Real-time inference
- **Step 12: Execute Feedback Phase & Conclusion**:
  - Discussion of model limitations, hyperparameter tuning, feature additions, and production feedback mechanisms.

---

## 4. Deep-Dive: Task 2 Requirements (Your Assignment Deliverables)

### Requirement 1: Select a Machine Learning Problem
- Must be a tabular regression problem on a large, real-world dataset (similar scale and richness to the Car Price dataset).
- Recommended domains:
  1. **Real Estate / House Price Prediction** (e.g., Ames Housing or California Housing extended dataset)
  2. **Laptop / Smartphone Price Prediction** (rich categorical + numerical specs)
  3. **Flight Ticket Price Prediction** (airlines, dates, stops, duration, source/destination)
  4. **Medical Insurance Cost Prediction** (age, bmi, smoking, region, charges)

### Requirement 2: Full Dataset Acquisition
- Download the complete dataset (not a mini-sample).
- Ensure it contains both numeric and categorical variables to utilize `ColumnTransformer`.

### Requirement 3: 5 Distinct Machine Learning Algorithms
Select 5 algorithms that were **not** in Task 1. Recommended candidate suite:
1. **Ridge Regression** (or **Lasso** / **ElasticNet** / **BayesianRidge**) — Regularized linear models
2. **Support Vector Regressor (`SVR`)** (with RBF or Linear kernel)
3. **Extra Trees Regressor (`ExtraTreesRegressor`)** — Extremely randomized ensemble trees
4. **AdaBoost Regressor (`AdaBoostRegressor`)** — Adaptive boosting ensemble
5. **XGBoost Regressor (`XGBRegressor`)** or **HistGradientBoostingRegressor** or **LightGBM (`LGBMRegressor`)** or **Multi-layer Perceptron (`MLPRegressor`)**

### Requirement 4: 10-Fold Cross-Validation on Google Colab
- Implement 10-Fold CV on the full dataset.
- Report RMSE for every fold and compute mean $\pm$ standard deviation.
- Provide progress bars, comparison tables, and visual distribution charts.

### Requirement 5: Model Deployment & Web Application
- Build a user-friendly web interface (e.g., **Streamlit**).
- Allow users to enter values for all input features.
- Pass input to the loaded pre-processing + model pipeline and display predicted value.
- Host the application on a public cloud provider:
  - **Streamlit Community Cloud** (recommended: free, connects directly to GitHub, zero-configuration)
  - **Hugging Face Spaces** (Streamlit / Gradio)
  - **Render** or **Railway**
- **Crucial**: Place the live URL at the very top of the notebook!

---

## 5. Submission Checklist & Package Structure

When submitting to Google Classroom, ensure you have:
```text
Submission Package:
│
├── Notebook/
│   └── [Your_Name]_Assignment_3_[Problem_Name].ipynb   (With Live Cloud URL on Line 1)
│
├── Dataset/
│   └── dataset.csv                                     (Full dataset file)
│
├── Model/
│   └── trained_model.pkl                               (Exported pipeline artifact)
│
└── Web_App/
    ├── app.py                                          (Streamlit / Web app interface)
    ├── requirements.txt                                (Dependencies for cloud deployment)
    └── README.md                                       (Deployment link and instructions)
```

---

## 6. Recommended Next Steps

1. **Step 1**: Choose and confirm the Machine Learning problem and dataset (e.g., Laptop Price Prediction or Flight Fare Prediction).
2. **Step 2**: Download and inspect the full dataset.
3. **Step 3**: Develop the complete 12-step Jupyter Notebook following the instructor's exact conventions.
4. **Step 4**: Execute and validate the 10-Fold Cross-Validation, generating all metrics and comparison charts.
5. **Step 5**: Save the trained pipeline (`.pkl`) and build the Streamlit web application.
6. **Step 6**: Deploy the web app to Streamlit Community Cloud / Hugging Face Spaces and verify the live URL.
7. **Step 7**: Embed the live URL at the top of the notebook and prepare the final submission archive.
