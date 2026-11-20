# Dataset Schema and Inspection Report

## 1. Dataset

-   **Dataset:** Pakistan's Largest E-Commerce Dataset
-   **Source:** [Kaggle
    dataset](https://www.kaggle.com/datasets/zusmani/pakistans-largest-ecommerce-dataset/code)
-   **Inspection notebook:** `01inspection.ipynb`
-   **Status:** Initial inspection documented; cleaning has not started.

## 2. Dataset dimensions

  Metric                         Observed value
  ---------------------------- ----------------
  Rows                                1,048,575
  Columns                                    26
  Non-empty rows                         584,524
  Fully empty rows                       464,051

The notebook confirms the empty-row count with
`df.isnull().all(axis=1).sum()`.

## 3. Column schema

These are the Pandas dtypes shown by `df.info()` in the notebook:
13 `float64` columns and 13 `str` columns.

  -----------------------------------------------------------------------------------
                     \# Column                    Reported dtype   Initial meaning /
                                                                   observation
  --------------------- ------------------------- ---------------- ------------------
                      1 `item_id`                 `float64`        Item identifier

                      2 `status`                  string           Order status;
                                                                   categorical

                      3 `created_at`              string           Creation
                                                                   date/time; inspect
                                                                   format

                      4 `sku`                     string           Product SKU;
                                                                   identifier

                      5 `price`                   `float64`        Price

                      6 `qty_ordered`             `float64`        Ordered quantity

                      7 `grand_total`             `float64`        Order total

                      8 `increment_id`            string           Order identifier

                      9 `category_name_1`         string           Product category

                     10 `sales_commission_code`   string           Commission code

                     11 `discount_amount`         `float64`        Discount amount

                     12 `payment_method`          string           Payment method;
                                                                   categorical

                     13 `Working Date`            string           Date-related
                                                                   field; inspect
                                                                   format

                     14 `BI Status`               string           Business
                                                                   intelligence
                                                                   status

                     15 ` MV `                    string           Name contains
                                                                   surrounding
                                                                   spaces; meaning
                                                                   needs confirmation

                     16 `Year`                    `float64`        Year

                     17 `Month`                   `float64`        Month

                     18 `Customer Since`          string           Customer-related
                                                                   date

                     19 `M-Y`                     string           Month-year

                     20 `FY`                      string           Fiscal year

                     21 `Customer ID`             `float64`        Customer
                                                                   identifier

                     22 `Unnamed: 21`             `float64`        Reported entirely
                                                                   empty

                     23 `Unnamed: 22`             `float64`        Reported entirely
                                                                   empty

                     24 `Unnamed: 23`             `float64`        Reported entirely
                                                                   empty

                     25 `Unnamed: 24`             `float64`        Reported entirely
                                                                   empty

                     26 `Unnamed: 25`             `float64`        Reported entirely
                                                                   empty
  -----------------------------------------------------------------------------------

## 4. Missing-value observations

  -----------------------------------------------------------------------
  Column(s)                                       Reported missing values
  ------------------------------ ----------------------------------------
  `item_id`, `created_at`,                                   464,051 each
  `price`, `qty_ordered`,        
  `grand_total`, `increment_id`, 
  `discount_amount`,             
  `payment_method`,              
  `Working Date`, `BI Status`,   
  ` MV `, `Year`, `Month`, `M-Y`,
  `FY`                           

  `status`                                                        464,066

  `sku`                                                           464,071

  `category_name_1`                                               464,215

  `sales_commission_code`                                         601,229

  `Customer Since`,                                          464,062 each
  `Customer ID`                  

  `Unnamed: 21`--`Unnamed: 25`                             1,048,575 each
  -----------------------------------------------------------------------

The counts above are the results of `df.isnull().sum()`; they count
actual Pandas nulls, not text values that look like missing data. The
categorical output also shows the literal `\N` 7,850 times in
`category_name_1` and 339,001 times in `sales_commission_code`. If `\N`
is treated as a missing-data marker, the corresponding totals become
472,065 and 940,230.

After excluding the 464,051 completely empty rows, the remaining actual
nulls are: 164 in `category_name_1`, 137,178 in
`sales_commission_code`, 15 in `status`, 20 in `sku`, and 11 each in
`Customer Since` and `Customer ID`.

## 5. Status distribution

  Status                 Count
  ------------------ ---------
  `complete`           233,685
  `canceled`           201,249
  `received`            77,290
  `order_refunded`      59,529
  `refund`               8,050
  `cod`                  2,859
  `paid`                 1,159
  `closed`                 494
  `payment_review`          57
  `pending`                 48
  `processing`              33
  `holded`                  31
  `fraud`                   10
  `pending_paypal`           7
  `exchange`                 4

These are observed category counts. Do not assume all statuses represent
mutually exclusive final outcomes without confirming their meaning.

## 6. Duplicate-row observation

The raw duplicate check reported 464,050 duplicated rows. After
excluding completely empty rows, the notebook reports **0** duplicate
rows. Therefore, the raw count is due to repeated completely empty
rows, not duplicated transactions.

Compare both values in the notebook:

``` python
df.duplicated().sum()

df_nonempty = df.dropna(how="all")
df_nonempty.duplicated().sum()
```

Do not automatically remove repeated `increment_id` values: an order may
contain multiple item-level rows.

## 7. Initial data-quality observations

1.  The file contains 464,051 completely empty rows.
2.  Five columns (`Unnamed: 21` to `Unnamed: 25`) are entirely empty.
3.  Identifier columns such as `item_id`, `increment_id`, and
    `Customer ID` should be treated as identifiers, not continuous
    measurements.
4.  Date-related columns are stored as strings and need format
    inspection before conversion.
5.  `sales_commission_code` has 137,178 actual nulls after excluding
    completely empty rows, plus 339,001 literal `\N` values.
6.  `category_name_1` has 164 actual nulls after excluding completely
    empty rows, plus 7,850 literal `\N` values.
7.  The column name ` MV ` contains surrounding spaces; its meaning is
    not yet established.
8.  There are no duplicate rows after excluding completely empty rows.

## 8. Assumptions and limitations

-   The inspection figures are taken from the saved notebook outputs;
    the raw CSV has not been independently re-read for this report.
-   No rows or columns have been deleted, renamed, imputed, or
    transformed.
-   No prediction target has been selected.
-   Unclear column meanings must be confirmed before cleaning or
    modelling.

## 9. Inspection checkpoint

-   [x] Dataset dimensions and 26 column names recorded.
-   [x] Initial data types recorded.
-   [x] Initial missing-value counts reviewed.
-   [x] Status value counts recorded.
-   [x] Exact fully empty row count and columns confirmed in the notebook.
-   [x] Duplicate count after excluding fully empty rows confirmed.
-   [x] Numerical summaries and categorical value counts reviewed and
    saved in the notebook.
-   [x] This report saved as `docs/schema.md`.

**Checkpoint status:** The initial inspection is documented and its
saved outputs have been checked. Cleaning has not started.