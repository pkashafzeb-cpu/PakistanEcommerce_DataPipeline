# Pakistan E-Commerce Data Analysis and Order Status Prediction

## 1. Project Overview

This project explores Pakistan's Largest E-Commerce Dataset through data inspection, cleaning, exploratory data analysis, visualization, SQL analysis, and machine learning.

The project is divided into two parts:

- **Part A – Data Analysis:** Inspecting, cleaning, analyzing, and visualizing the dataset using Python, Pandas, NumPy, Matplotlib, Seaborn, and SQLite.
- **Part B – Tabular Machine Learning:** Building and evaluating classification models to predict whether an e-commerce transaction will be completed or canceled using Scikit-learn.

The overall objective is to develop a reproducible data pipeline and explore the application of machine learning to historical e-commerce transactions.

## 2. Dataset

**Dataset:** Pakistan's Largest E-Commerce Dataset

The original dataset contains:
- 1,048,575 rows
- 26 columns

After removing completely empty rows and columns, the dataset contains:
- 584,524 records
- 21 columns

The original dataset is kept unchanged.

For Part B, transactions with `complete` and `canceled` statuses were selected, resulting in 434,934 records.

## 3. Project Structure

```text
Pakistan_Ecommerceproj/
│
├── Pakistan Largest Ecommerce Dataset.csv
│
├── docs/
│
├── models/
│   └── decision_tree_pipeline.joblib
│
├── notebooks/
│   ├── 01inspection.ipynb
│   ├── 02cleaning.ipynb
│   ├── 03dataanalysis.ipynb
│   └── Part B04_ml_pipeline.ipynb
│
├── outputs/
│   ├── processed/
│   │   └── pakistan_ecommerce_cleaned.csv
│   └── missing_values_report.csv
│
├── .gitignore
├── requirements.txt
└── README.md
```

**Note:** The original dataset and processed CSV are excluded from Git because of their size and data redistribution considerations. They must be available locally to run the notebooks.

## 4. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- SQLite
- Jupyter Notebook
- Joblib

## 5. Part A – Data Inspection and Cleaning

The following cleaning operations were performed:

1. Removed completely empty rows and columns.
2. Standardized missing-value markers such as `\N`, `NULL`, and empty strings.
3. Converted date columns into datetime format.
4. Converted integer-like columns into appropriate nullable integer types.
5. Checked duplicate records.
6. Inspected missing values and unusual numerical values.
7. Preserved questionable values when their meaning could not be verified.

The cleaned dataset was saved separately at:

`outputs/processed/pakistan_ecommerce_cleaned.csv`

## 6. Exploratory Data Analysis

The analysis includes:

- Numerical summary statistics.
- Categorical frequency analysis.
- Product category distribution.
- Order status distribution.
- Product price distribution.

### Visualizations

Three visualizations were created:

1. Top 10 Product Categories.
2. Top 10 Order Statuses.
3. Cumulative Distribution of Product Prices.

## 7. SQL Analysis

SQLite was used to perform queries on the cleaned dataset.

The analysis includes:

- Top five product categories.
- Order status distribution.
- Top ten payment methods.
- Monthly recorded transaction totals.
- Top ten products by ordered quantity.

## 8. Part B – End-to-End Tabular Machine Learning

### 8.1 Prediction Task

The objective is to predict whether an e-commerce transaction will be completed or canceled.

- **Problem type:** Binary Classification
- **Target variable:** `status`
- **Classes:** `complete` and `canceled`
- **Filtered records:** 434,934
- **Unique orders:** 318,158

### 8.2 Target Distribution

| Order Status | Records | Percentage |
|---|---:|---:|
| Complete | 233,685 | 53.73% |
| Canceled | 201,249 | 46.27% |
| **Total** | **434,934** | **100%** |

### 8.3 Data Preparation and Leakage Prevention

The following columns were excluded from model training:

- `BI Status`: Directly reveals information about the target.
- `increment_id`: Used for grouping during data splitting, not as a predictor.
- `item_id`: Identifier rather than a useful predictive feature.
- `Working Date`: Duplicates `created_at`.
- `MV`: Meaning unclear and highly redundant with transaction totals.
- `sales_commission_code`: Contains approximately 81.89% missing values.
- Redundant date columns: `Year`, `Month`, `M-Y`, and `FY`.

Date-based features were extracted from order and customer registration dates.

### 8.4 Train-Test Split

A GroupShuffleSplit with an 80:20 ratio was used.

Records belonging to the same order were kept in the same split to prevent order-level overlap.

| Dataset | Records |
|---|---:|
| Training | 347,439 |
| Testing | 87,495 |

The training and testing class proportions were nearly identical.

### 8.5 Feature Preprocessing

Scikit-learn `Pipeline` and `ColumnTransformer` were used to build a reproducible preprocessing workflow.

**Numerical features:**
- Median imputation.
- Standard scaling.

**Categorical features:**
- Most-frequent imputation.
- One-hot encoding.
- Unknown categories handled using `handle_unknown="ignore"`.

Preprocessing was fitted on training data only to prevent data leakage.

### 8.6 Models Evaluated

Three classification models were trained:

1. Logistic Regression
2. Decision Tree
3. Random Forest

Three-fold StratifiedGroupKFold cross-validation was used for model comparison.

### 8.7 Cross-Validation Results

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7903 | 0.7503 | 0.8200 | 0.7836 | 0.8710 |
| Decision Tree | 0.8039 | 0.7791 | 0.8050 | 0.7916 | 0.8939 |
| Random Forest | 0.7810 | 0.7465 | 0.7979 | 0.7713 | 0.8633 |

The Decision Tree was selected because it achieved the highest cross-validation accuracy, F1-score, and ROC-AUC.

*Note: Precision, recall, and F1-score in this comparison use `canceled` as the positive class.*

### 8.8 Final Test Results

The selected Decision Tree model was evaluated on the untouched test set.

| Metric | Result |
|---|---:|
| Accuracy | 80.29% |
| ROC-AUC | 89.65% |
| Canceled F1-score | 79% |
| Complete F1-score | 82% |

**Confusion Matrix**

| Actual / Predicted | Canceled | Complete |
|---|---:|---:|
| Canceled | 31,877 | 8,573 |
| Complete | 8,675 | 38,370 |

The model correctly classified 70,247 records and incorrectly classified 17,248 records.

### 8.9 Error Analysis

The model's overall test error rate was 19.71%.

The payment method analysis showed relatively high error rates for:
- Jazzwallet: 38.57%
- Internet Banking: 36.36%
- Jazzvoucher: 34.89%

The product category analysis showed relatively high error rates for:
- Computing: 28.32%
- Superstore: 27.84%
- Appliances: 27.66%

These findings indicate that prediction errors vary across payment methods and product categories. Small subgroup sizes and differences in category distributions should be considered before drawing conclusions.

### 8.10 Model Saving and Inference

The trained Decision Tree pipeline was saved using Joblib:

`models/decision_tree_pipeline.joblib`

The saved pipeline was successfully loaded and used to generate predictions on five held-out test records.

This verified that the saved model could be reused for inference.

## 9. Data Quality Summary

The following summary applies to the cleaned Part A dataset containing 584,524 records.

| Metric | Result |
|---|---:|
| Total records | 584,524 |
| Total columns | 21 |
| Missing values | 484,255 |
| Duplicate rows | 0 |
| Data completeness | 96.05% |
| Row uniqueness | 100% |

The highest missing-value percentage occurs in `sales_commission_code` (81.46%).

## 10. Assumptions and Limitations

### Part A

1. Missing values were retained when their correct replacements could not be established.
2. Missing commission codes do not necessarily indicate invalid transactions.
3. Zero prices may represent free items, promotions, or data inconsistencies.
4. Negative grand totals and discount amounts were preserved because their meaning could not be verified.
5. Extreme numerical values were retained rather than removed without sufficient evidence.
6. Multiple item records may belong to the same order.
7. Monthly `grand_total` represents recorded transaction values across all order statuses, not verified revenue.
8. The analysis is limited by missing values and the absence of detailed business definitions for some columns.

### Part B

1. The model achieved 80.29% test accuracy, meaning some transactions are still incorrectly classified.
2. Performance may change with newer transaction patterns.
3. Some payment methods and product categories have limited records.
4. Evaluation is item-level rather than unique-order-level.
5. Payment method, price, quantity, discount, grand total, and customer information are assumed to be available before the final order status is determined.
6. Historical relationships between transaction features and order status may change over time.

## 11. Intended Use

The machine learning model is intended as an experimental decision-support tool for identifying transactions that may be canceled or completed.

It should not automatically cancel orders or make final business decisions without further validation.

## 12. How to Run the Project

### Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Execution Order

Open the project folder in VS Code or Jupyter Notebook.

Execute the Part A notebooks in this order:

1. `01inspection.ipynb`
2. `02cleaning.ipynb`
3. `03dataanalysis.ipynb`

Then execute:

4. `Part B04_ml_pipeline.ipynb`

Run all cells in each notebook from top to bottom.

The cleaning notebook generates the cleaned dataset, which is used by the analysis and machine learning workflows.

### Dataset Availability

The original and processed datasets are excluded from Git. Place the original dataset in the project root using the expected filename and run the cleaning notebook to regenerate the processed dataset.

## 13. Outputs

The project produces:

- Cleaned dataset in CSV format.
- Missing-values report.
- Data analysis and visualizations.
- SQL query results.
- Trained Decision Tree pipeline.
- Model evaluation metrics.
- Confusion matrix and error analysis.

## 14. Conclusion

Part A examines the Pakistan E-Commerce Dataset through data inspection, cleaning, exploratory analysis, visualization, and SQL queries.

Part B extends the analysis by developing and evaluating machine learning models to predict e-commerce transaction status.

Among the three evaluated models, Decision Tree achieved the strongest cross-validation performance, with 80.29% final test accuracy and 89.65% ROC-AUC.

Overall, the project demonstrates a reproducible workflow covering data preparation, analytical exploration, model development, evaluation, and model saving. Further validation is necessary before applying the model to real-world business decisions.