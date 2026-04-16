# Data Dictionary — Financial Data of State Governments

Source: `Financial Data of state Governments.xlsx`  
Total sheets: **35**

## Overview Table

| # | Sheet | Shape (rows × cols) | Classification | Revenue relevance |
|---|-------|--------------------|----------------|-------------------|
| 1 | `A1.1 Rev. Reciepts` | 68 × 14 | state-wise | Medium |
| 2 | `A1.2_Non Debt Cap. Rec.` | 313 × 24 | state-wise | Low |
| 3 | `A2.1 Comp. wise Rev Receipt ` | 403 × 25 | state-wise | High |
| 4 | `A2.2_SOTR_Components` | 209 × 11 | state-wise | High |
| 5 | `A3_Cap Receipts Components` | 314 × 26 | state-wise | Low |
| 6 | `A4_RevexCapexAndLA` | 79 × 32 | state-wise | Low |
| 7 | `A4 FC Grants` | 238 × 8 | state-wise | Medium |
| 8 | `A5_Revex & Capex` | 111 × 25 | state-wise | Medium |
| 9 | `A4_CapexWithAndWithoutLAByHQ` | 96 × 21 | state-wise | Low |
| 10 | `A6_Sectoral RevExp` | 162 × 24 | state-wise | Medium |
| 11 | `A7_SectoralCapex` | 214 × 26 | state-wise | Low |
| 12 | `A8_ Total_Secotral_Exp` | 177 × 11 | state-wise | Medium |
| 13 | `A09_PD_Account` | 120 × 11 | state-wise | Low |
| 14 | `A10_AC_Bill` | 31 × 11 | state-wise | Low |
| 15 | `A11_Committed Exp` | 220 × 24 | state-wise | Low |
| 16 | `A12_GIA` | 31 × 12 | state-wise | Low |
| 17 | `A13_ExpSubsidies` | 176 × 7 | state-wise | Low |
| 18 | `A14_RevEx Maj Functions` | 590 × 14 | mixed / partial state data | Medium |
| 19 | `A15_Capex Major Functions` | 503 × 15 | mixed / partial state data | Medium |
| 20 | `A16_EcoCat_SUM_v2` | 79 × 13 | mixed / partial state data | Medium |
| 21 | `Object Head_Dtld` | 880 × 15 | state-wise | Low |
| 22 | `Deduct_Recoveries` | 872 × 20 | mixed / partial state data | Medium |
| 23 | `A17_PD&PAL` | 222 × 15 | state-wise | Low |
| 24 | `fiscal deficit cal` | 31 × 14 | state-wise | Medium |
| 25 | `A18_WMA` | 151 × 12 | state-wise | Low |
| 26 | `A19_FRBM_FA` | 354 × 14 | state-wise | Medium |
| 27 | `A20 Office Memo` | 1 × 1 | component-wise | Low |
| 28 | `Sheet1` | 0 × 0 | component-wise | Low |
| 29 | `FRMB_Targets` | 30 × 10 | state-wise | Low |
| 30 | `Investment` | 30 × 4 | state-wise | Low |
| 31 | `PAL_Details` | 31 × 14 | state-wise | Low |
| 32 | `Loan and adv` | 47 × 15 | state-wise | Low |
| 33 | `Debt Receipts Repayments` | 44 × 21 | state-wise | Low |
| 34 | `SOTR components` | 75 × 22 | state-wise | High |
| 35 | `Infexible_exp` | 34 × 30 | state-wise | Low |

## Sheet Details

### `A1.1 Rev. Reciepts`

- **Shape:** 68 rows × 14 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 1.1 Revenue Receipts of the States (₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 1.1 Revenue Receipts of the States (₹ Crore)            NaN       NaN        NaN  ...       NaN       NaN        NaN NaN
                                                    #         States   2023-24    2022-23  ...   2015-16   2014-15    2013-14 NaN
                                                    1 Andhra Pradesh  173766.9  157768.03  ...  88647.81  90672.46  110718.84 NaN
```

### `A1.2_Non Debt Cap. Rec.`

- **Shape:** 313 rows × 24 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['#', 'Components', '2023-24', '2022-23', '2021-22', '2020-21', '2019-20', '2018-19']

```
  #             Components    2023-24    2022-23  ... NaN NaN NaN NaN
  1 Andhra Pradesh (Total)  193665.79  186019.77  ... NaN NaN NaN NaN
NaN Misc. Capital Receipts          0          0  ... NaN NaN NaN NaN
```

### `A2.1 Comp. wise Rev Receipt `

- **Shape:** 403 rows × 25 columns
- **Classification:** state-wise
- **Revenue relevance:** High
- **First row (header-like):** ['Annexure 2.1 Component wise Revenue Receipts of the States(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 2.1 Component wise Revenue Receipts of the States(₹ Crore)       NaN        NaN        NaN  ... NaN NaN NaN NaN
                                                         Components   2023-24    2022-23    2021-22  ... NaN NaN NaN NaN
                                             Andhra Pradesh (Total)  173766.9  157768.03  150552.31  ... NaN NaN NaN NaN
```

### `A2.2_SOTR_Components`

- **Shape:** 209 rows × 11 columns
- **Classification:** state-wise
- **Revenue relevance:** High
- **First row (header-like):** ['Annexure 2.2 State wise components of SOTR (₹ crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 2.2 State wise components of SOTR (₹ crore) NaN NaN NaN  ... NaN NaN NaN NaN
                                                 NaN NaN NaN NaN  ... NaN NaN NaN NaN
                                                 NaN NaN NaN NaN  ... NaN NaN NaN NaN
```

### `A3_Cap Receipts Components`

- **Shape:** 314 rows × 26 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 3 Component wise Capital Account Receipts(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 3 Component wise Capital Account Receipts(₹ Crore) NaN                    NaN        NaN  ... NaN NaN NaN                          NaN
                                                         Sr   #             Components    2023-24  ... NaN NaN NaN awaiting data from Rajasthan
                                                          1   1 Andhra Pradesh (Total)  193665.79  ... NaN NaN NaN                          NaN
```

### `A4_RevexCapexAndLA`

- **Shape:** 79 rows × 32 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['#', 'States', '2023-24', 'nan', 'nan', '2022-23', 'nan', 'nan']

```
  #         States    2023-24       NaN  ... NaN NaN NaN NaN
NaN            NaN        REx       CEx  ... NaN NaN NaN NaN
  1 Andhra Pradesh  212449.56  23330.48  ... NaN NaN NaN NaN
```

### `A4 FC Grants`

- **Shape:** 238 rows × 8 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 4 Finance Commission Grants(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 4 Finance Commission Grants(₹ Crore)      NaN       NaN     NaN      NaN      NaN      NaN      NaN
                                   Components  2023-24   2022-23 2021-22  2020-21  2019-20  2018-19  2017-18
                       Andhra Pradesh (Total)  9640.83  13174.27   20991  11576.2  5880.81  5548.16  6974.58
```

### `A5_Revex & Capex`

- **Shape:** 111 rows × 25 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 5 Revenue and Capital Expenditure of the States(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 5 Revenue and Capital Expenditure of the States(₹ Crore)    NaN     NaN NaN  ... NaN NaN NaN NaN
                                                                # States 2023-24 NaN  ... NaN NaN NaN NaN
                                                              NaN    NaN     REx CEx  ... NaN NaN NaN NaN
```

### `A4_CapexWithAndWithoutLAByHQ`

- **Shape:** 96 rows × 21 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['nan', 'Total capital expenditure', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
NaN Total capital expenditure     NaN     NaN  ... NaN NaN NaN NaN
  #                    States 2023-24 2022-23  ... NaN NaN NaN NaN
NaN                       NaN     NaN     CEx  ... NaN NaN NaN NaN
```

### `A6_Sectoral RevExp`

- **Shape:** 162 rows × 24 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 6 Sectoral Revenue Expenditure of the States(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 6 Sectoral Revenue Expenditure of the States(₹ Crore)        NaN        NaN        NaN  ... NaN NaN NaN NaN
                                                    Components    2023-24    2022-23    2021-22  ... NaN NaN NaN NaN
                                        Andhra Pradesh (Total)  212449.56  201255.53  159163.31  ... 1.0 1.0 1.0 1.0
```

### `A7_SectoralCapex`

- **Shape:** 214 rows × 26 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 7 Sectoral Capital Expenditure of the States (₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 7 Sectoral Capital Expenditure of the States (₹ Crore)                 NaN     NaN                         NaN  ... NaN NaN NaN NaN
                                                     Components 2023-24 without L&A     L&A Total 2023-24 including L&A  ... NaN NaN NaN NaN
                                         Andhra Pradesh (Total)            23330.47  730.53                       24061  ... NaN NaN NaN NaN
```

### `A8_ Total_Secotral_Exp`

- **Shape:** 177 rows × 11 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 8 Total Sectoral Expenditure of the States(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 8 Total Sectoral Expenditure of the States(₹ Crore)        NaN        NaN        NaN  ...        NaN       NaN        NaN       NaN
                                                  Components    2023-24    2022-23    2021-22  ...    2017-18   2016-17    2015-16   2014-15
                                      Andhra Pradesh (Total)  236510.56  210272.29  177674.07  ...  137485.19  131922.8  110794.98  127481.2
```

### `A09_PD_Account`

- **Shape:** 120 rows × 11 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 9 Details of PD Account ( Amount ₹ in Crores) (Source St. 21 of F.A.) (₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 9 Details of PD Account ( Amount ₹ in Crores) (Source St. 21 of F.A.) (₹ Crore)     NaN     NaN     NaN  ...     NaN     NaN     NaN     NaN
                                                                                     NaN     NaN     NaN     NaN  ...     NaN     NaN     NaN     NaN
                                                                              Components 2023-24 2022-23 2021-22  ... 2017-18 2016-17 2015-16 2014-15
```

### `A10_AC_Bill`

- **Shape:** 31 rows × 11 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 10 Details of Unadjusted AC Bill (₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 10 Details of Unadjusted AC Bill (₹ Crore)     NaN      NaN      NaN  ...     NaN     NaN     NaN      NaN
                                         Components 2023-24  2022-23  2021-22  ... 2017-18 2016-17 2015-16  2014-15
                                    Andhra Pradesh   333.57  1313.91  1531.35  ...  225.95  279.77  706.55  1058.94
```

### `A11_Committed Exp`

- **Shape:** 220 rows × 24 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['A11 Committed Expenditure of the States (₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
A11 Committed Expenditure of the States (₹ Crore)       NaN       NaN       NaN  ... NaN NaN NaN NaN
                                       Components   2023-24   2022-23   2021-22  ... NaN NaN NaN NaN
                           Andhra Pradesh (Total)  89037.77  84659.37  73204.88  ... NaN NaN NaN NaN
```

### `A12_GIA`

- **Shape:** 31 rows × 12 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 12 GIA Salary(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 12 GIA Salary(₹ Crore)      NaN       NaN       NaN  ...      NaN      NaN      NaN                    NaN
                     GIA Salary  2023-24   2022-23   2021-22  ...  2016-17  2015-16  2014-15       Source Verified 
                 Andhra Pradesh  17996.2  17066.91  13107.75  ...  9226.95  8095.55  5472.39 Received from State AG
```

### `A13_ExpSubsidies`

- **Shape:** 176 rows × 7 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 13 Expenditure on Subsidy for the year of 2023-24', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 13 Expenditure on Subsidy for the year of 2023-24           NaN                  NaN     NaN NaN NaN NaN
                                                     State (₹ in Crores) Major Heads Included Remarks NaN NaN NaN
                                            Andhra Pradesh      19430.81                  NaN     NaN NaN NaN NaN
```

### `A14_RevEx Maj Functions`

- **Shape:** 590 rows × 14 columns
- **Classification:** mixed / partial state data
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 14 Revenue Expenditure by Functions of the States (Major Functions) (₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 14 Revenue Expenditure by Functions of the States (Major Functions) (₹ Crore)        NaN        NaN        NaN  ...       NaN       NaN                       NaN NaN
                                                                            Components    2023-24    2022-23    2021-22  ...   2014-15   2013-14 Checked and found correct NaN
                                                                Andhra Pradesh (Total)  212449.56  201255.53  159163.31  ...  114865.7  110374.5                       NaN NaN
```

### `A15_Capex Major Functions`

- **Shape:** 503 rows × 15 columns
- **Classification:** mixed / partial state data
- **Revenue relevance:** Medium
- **First row (header-like):** ['Annexure 15 Capital Expenditure of the States (Major Functions)(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 15 Capital Expenditure of the States (Major Functions)(₹ Crore)                 NaN                 NaN           NaN  ...       NaN      NaN       NaN                       NaN
                                                              Components 2023-24 without L&A L&A 2023-24 \nst. 4 Total 2023-24  ...   2015-16  2014-15   2013-14                       NaN
                                                  Andhra Pradesh (Total)            23330.48              730.53      24061.01  ...  14845.32  12615.5  18969.34 Checked and found correct
```

### `A16_EcoCat_SUM_v2`

- **Shape:** 79 rows × 13 columns
- **Classification:** mixed / partial state data
- **Revenue relevance:** Medium
- **First row (header-like):** ['Components', '2023-24', '2022-23', '2021-22', '2020-21', '2019-20', '2018-19', '2017-18']

```
       Components    2023-24      2022-23      2021-22  ...     2015-16      2014-15      2013-14                       NaN
         Salaries  713756.11  665350.7036  608723.9917  ...  366315.249  337389.9657  301454.5094 Checked and found correct
Medical Treatment    5090.74      3405.73      2958.04  ...      1733.6      1500.31      1156.93                       NaN
```

### `Object Head_Dtld`

- **Shape:** 880 rows × 15 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['nan', '2023-24', '2022-23', '2021-22', '2020-21', '2019-20', '2018-19', '2017-18']

```
               NaN   2023-24   2022-23   2021-22  ...   2013-14                                                                                                                                                NaN NaN NaN
States / Salaries        NaN       NaN       NaN  ...       NaN                                                                                                                                                NaN NaN NaN
    Andhra Pradesh  37860.24  36583.14  30713.03  ...  22980.02 It is updated as per HQ email dated 12-06-2025 to include “Salaries”, “Salary Arrears”, and “Salary of Work Charged Establishment” in Statement-4B NaN NaN
```

### `Deduct_Recoveries`

- **Shape:** 872 rows × 20 columns
- **Classification:** mixed / partial state data
- **Revenue relevance:** Medium
- **First row (header-like):** ['STATES', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
        STATES       NaN       NaN       NaN  ... NaN NaN NaN NaN
Andhra Pradesh   2023-24   2022-23   2021-22  ... NaN NaN NaN NaN
      SALARIES  37860.24  45139.51  38898.66  ... NaN NaN NaN NaN
```

### `A17_PD&PAL`

- **Shape:** 222 rows × 15 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 17 Public Debt Liability & Public Account Liability (₹ Crore) As on 31st March of each year ', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 17 Public Debt Liability & Public Account Liability (₹ Crore) As on 31st March of each year        NaN        NaN       NaN  ...        NaN NaN                       NaN                                                 NaN
                                                                                           Components   2023-24    2022-23   2021-22  ...    2013-14 NaN                   Remarks                                      colour remarks
                                                                                       Andhra Pradesh  491734.3  429525.74  378086.6  ...  189740.92 NaN Checked and found correct 1). yellow = Rounding off problem(decimal problems)
```

### `fiscal deficit cal`

- **Shape:** 31 rows × 14 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['#', 'States', '2023-24-Expenditure', 'nan', 'nan', 'nan', 'nan', '2023-24-Receipts']

```
  #         States 2023-24-Expenditure       NaN  ...            NaN         2023-24          2023-24 NaN
NaN            NaN           Total REx       CEx  ... Total Receipts Revenue Deficit Fiscal \nDeficit NaN
  1 Andhra Pradesh           212449.56  23330.48  ...      173790.87       -38682.66         -62719.7 NaN
```

### `A18_WMA`

- **Shape:** 151 rows × 12 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 18: Ways & Means Advances of the States(₹ Crore)', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
Annexure 18: Ways & Means Advances of the States(₹ Crore)     NaN     NaN     NaN  ... Amount ₹ in Crore     NaN     NaN NaN
                                                   States 2023-24 2022-23 2021-22  ...           2016-17 2015-16 2014-15 NaN
                                           Andhra Pradesh     NaN     NaN     NaN  ...               NaN     NaN     NaN NaN
```

### `A19_FRBM_FA`

- **Shape:** 354 rows × 14 columns
- **Classification:** state-wise
- **Revenue relevance:** Medium
- **First row (header-like):** ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
                                                                               NaN     NaN     NaN     NaN  ...     NaN     NaN                   NaN                       NaN
Annexure 19 Fiscal Responsibility and Budget Management (FRBM) Parameters(₹ Crore)     NaN     NaN     NaN  ...     NaN     NaN                   NaN Checked and found correct
                                                      Fiscal Surplus(+)/Deficit(-) 2023-24 2022-23 2021-22  ... 2014-15 2013-14 Comments Finalization                       NaN
```

### `A20 Office Memo`

- **Shape:** 1 rows × 1 columns
- **Classification:** component-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Annexure 20 Office Memorandum']

```
Annexure 20 Office Memorandum
```

### `Sheet1`

- **Shape:** 0 rows × 0 columns
- **Classification:** component-wise
- **Revenue relevance:** Low
- **First row (header-like):** []

```
Empty DataFrame
Columns: []
Index: []
```

### `FRMB_Targets`

- **Shape:** 30 rows × 10 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['States', 'FRBM / MTFP Target', 'nan', 'nan', 'Actuals', 'nan', 'nan', 'nan']

```
        States    FRBM / MTFP Target            NaN                     NaN  ...                     NaN                                                  NaN                                                                                                                                                                                                      NaN                                              NaN
           NaN Rev Deficit / Surplus Fiscal Deficit Outstanding Liabilities  ... Outstanding Public Debt Outstanding Public Debt & Public Account liabilities                                                                                                                                                                                                  Remarks                                              NaN
Andhra Pradesh                  -3.3           -4.5                    36.3  ...                   27.77                                                32.95 According to SFAR Table 1.4 APFRBM Rev Deficit 3.3% for year 2022-23  was taken as -3.6\nfiscal deficit  4.5% for 2022-23 was taken as  -5\noutstainding Liabilities 36.3% for 2022-23 as taken as  35.6 All the parameters have been verified from SFAR.
```

### `Investment`

- **Shape:** 30 rows × 4 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Investment of Earmarked Funds', '2023-24', '2022-23', 'nan']

```
Investment of Earmarked Funds   2023-24   2022-23 NaN
               Andhra Pradesh  12314.07  11405.26 NaN
            Arunachal Pradesh   2500.64   2264.24 NaN
```

### `PAL_Details`

- **Shape:** 31 rows × 14 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['nan', '2023-24 (Amount in crore) Closing balance as on 31 March 2024', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
           NaN 2023-24 (Amount in crore) Closing balance as on 31 March 2024                             NaN                                 NaN  ... NaN NaN NaN NaN
         State                        Small Savings & State Provident Funds  Reserve Funds bearing Interests Reserve Funds Not bearing Interests  ... NaN NaN NaN NaN
Andhra Pradesh                                                      29791.68                         5289.99                             1995.02  ... NaN NaN NaN NaN
```

### `Loan and adv`

- **Shape:** 47 rows × 15 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
NaN                                         NaN     NaN     NaN  ...     NaN     NaN NaN NaN
NaN                                         NaN     NaN     NaN  ...     NaN     NaN NaN NaN
NaN States / Loans & Advances given by the Govt 2023-24 2022-23  ... 2014-15 2013-14 NaN NaN
```

### `Debt Receipts Repayments`

- **Shape:** 44 rows × 21 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['Rs. Crore', '2019-20', 'nan', 'nan', '2020-21', 'nan', 'nan', '2021-22']

```
     Rs. Crore       2019-20        NaN            NaN  ...       2023-24       NaN     NaN        Remarks
        States Debt Receipts Repayments Net Borrowings  ... Net Borrowing       NaN Def/Sur Data Incorrect
Andhra Pradesh     112428.23   79366.17       33062.06  ...      35832.83 39.434034 Deficit            NaN
```

### `SOTR components`

- **Shape:** 75 rows × 22 columns
- **Classification:** state-wise
- **Revenue relevance:** High
- **First row (header-like):** ['nan', '2023-24', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
          NaN   2023-24                        NaN                          NaN  ... NaN NaN NaN NaN
       States      SGST Taxes on Sales, Trade etc. Stamps and Registration Fees  ... NaN NaN NaN NaN
Andhrapradesh  31130.13                   18475.15                      9542.35  ... NaN NaN NaN NaN
```

### `Infexible_exp`

- **Shape:** 34 rows × 30 columns
- **Classification:** state-wise
- **Revenue relevance:** Low
- **First row (header-like):** ['nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan']

```
  NaN  NaN  NaN  NaN  ...   NaN NaN NaN NaN
  NaN  NaN  NaN  NaN  ...   NaN NaN NaN NaN
State NDRF SDRF SDMF  ... Total NaN NaN NaN
```

## Most Relevant Sheets for State Revenue Analysis

Sheets flagged as **High** relevance (contain revenue/tax/grants terms):

- `A2.1 Comp. wise Rev Receipt `
- `A2.2_SOTR_Components`
- `SOTR components`

## State-wise vs Component-wise

**State-wise sheets** (rows or columns enumerate Indian states):

- `A1.1 Rev. Reciepts`
- `A1.2_Non Debt Cap. Rec.`
- `A2.1 Comp. wise Rev Receipt `
- `A2.2_SOTR_Components`
- `A3_Cap Receipts Components`
- `A4_RevexCapexAndLA`
- `A4 FC Grants`
- `A5_Revex & Capex`
- `A4_CapexWithAndWithoutLAByHQ`
- `A6_Sectoral RevExp`
- `A7_SectoralCapex`
- `A8_ Total_Secotral_Exp`
- `A09_PD_Account`
- `A10_AC_Bill`
- `A11_Committed Exp`
- `A12_GIA`
- `A13_ExpSubsidies`
- `Object Head_Dtld`
- `A17_PD&PAL`
- `fiscal deficit cal`
- `A18_WMA`
- `A19_FRBM_FA`
- `FRMB_Targets`
- `Investment`
- `PAL_Details`
- `Loan and adv`
- `Debt Receipts Repayments`
- `SOTR components`
- `Infexible_exp`

**Component-wise sheets** (revenue/expenditure categories, no state breakdown):

- `A20 Office Memo`
- `Sheet1`