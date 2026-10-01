# Báo cáo Mô hình Hóa Dự báo Dân số & Xu hướng Già hoá Dân số đến 2050 (Phase 3)

## 1. Kiến trúc Hai Trụ cột Mô hình Học máy
- **Trụ cột 1: Dự báo Chuỗi Giá trị Liên tục (Linear Regression)**:
  - Dự báo quy mô dân số (`Population`) và quy mô người cao tuổi (`Older_People_65plus`) từ năm 2024 đến năm 2050 cho 237 quốc gia/vùng lãnh thổ.
- **Trụ cột 2: Phân loại Rủi ro Nhị phân Kép (Logistic Regression)**:
  - **Mô hình 2A (Depopulation Risk)**: Đánh giá xác suất một quốc gia bước vào chu kỳ suy giảm dân số kéo dài trước năm 2050.
  - **Mô hình 2B (Super-Aged Society Risk)**: Đánh giá xác suất một quốc gia trở thành **Xã hội Siêu già vào năm 2050** (Tỷ lệ người cao tuổi 65+ vượt ngưỡng 20%).

## 2. Kết quả Đánh giá Mô hình Dự báo Dân số (Linear Regression)
Kiểm định mô hình theo phương pháp phân chia thời gian (Time-based train/test split: Train <= 2015, Test 2016-2023):

| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa Thực tiễn |
| :--- | :---: | :--- |
| **Hệ số xác định ($R^2$)** | **0.9956** | Giải thích được 99.6% biến động quy mô dân số trên tập kiểm định độc lập |
| **Sai số tuyệt đối trung bình (MAE)** | **2,496,461 người** | Độ lệch trung bình trên quy mô từng quốc gia |
| **Căn bậc hai sai số toàn phương (RMSE)** | **8,882,820 người** | Độ tin cậy rất cao cho dự báo chu kỳ trung hạn đến 2050 |

## 3. Kết quả Hai Mô hình Phân loại Rủi ro (Logistic Regression)

| Mô hình Phân loại | Độ chính xác (Accuracy) | F1-Score | Mục tiêu & Bộ đặc trưng đầu vào (Features) |
| :--- | :---: | :---: | :--- |
| **2A. Nguy cơ Suy giảm Dân số** | **95.00%** | **90.32%** | Dự báo đà thu hẹp dân số dựa trên Tốc độ tăng trưởng 2023, Mức sinh TFR, Quy mô dân số log10, Tuổi trung vị và Tỷ lệ 65+ |
| **2B. Nguy cơ Xã hội Siêu già 2050** | **95.00%** | **94.55%** | Phân loại quốc gia vượt ngưỡng 20% người cao tuổi dựa trên Tỷ lệ 65+ 2023, Tuổi trung vị, Mức sinh TFR và Tuổi thọ trung bình |

## 4. Top 10 Quốc gia có Nguy cơ Suy giảm Dân số Cao nhất (Depopulation Risk)
| Thứ hạng | Quốc gia | Mã ISO | Điểm Nguy cơ Suy giảm | Phân loại |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Saint Martin (French part) | MAF | 100.00% | High Risk |
| 2 | Vatican | VAT | 99.93% | High Risk |
| 3 | Cook Islands | COK | 99.90% | High Risk |
| 4 | Marshall Islands | MHL | 99.54% | High Risk |
| 5 | Greece | GRC | 98.96% | High Risk |
| 6 | Monaco | MCO | 98.58% | High Risk |
| 7 | Saint Helena | SHN | 97.86% | High Risk |
| 8 | Northern Mariana Islands | MNP | 97.20% | High Risk |
| 9 | Ukraine | UKR | 94.89% | High Risk |
| 10 | Saint Pierre and Miquelon | SPM | 94.61% | High Risk |

## 5. Top 10 Quốc gia được Dự báo trở thành Xã hội Siêu già năm 2050 (Super-Aged)
| Thứ hạng | Quốc gia | Mã ISO | Xác suất Siêu già (65+ >= 20%) | Phân loại Dự báo |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Andorra | AND | 100.00% | Super-Aged Expected |
| 2 | Austria | AUT | 100.00% | Super-Aged Expected |
| 3 | Belgium | BEL | 100.00% | Super-Aged Expected |
| 4 | Bermuda | BMU | 100.00% | Super-Aged Expected |
| 5 | Bosnia and Herzegovina | BIH | 100.00% | Super-Aged Expected |
| 6 | Bulgaria | BGR | 100.00% | Super-Aged Expected |
| 7 | Canada | CAN | 100.00% | Super-Aged Expected |
| 8 | Croatia | HRV | 100.00% | Super-Aged Expected |
| 9 | Czechia | CZE | 100.00% | Super-Aged Expected |
| 10 | Denmark | DNK | 100.00% | Super-Aged Expected |

## 6. Danh mục Tệp Đầu ra Mô hình Hóa
1. [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv): Bảng dự báo quy mô dân số và người cao tuổi 65+ đến 2050.
2. [`data/processed/country_risk_classification_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/country_risk_classification_2050.csv): Bảng điểm số rủi ro suy giảm dân số và xác suất xã hội siêu già.
3. [`reports/modeling/confusion_matrix.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/confusion_matrix.png): Ma trận nhầm lẫn của cả 2 mô hình phân loại.
4. [`reports/modeling/forecast_trends_2050.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/forecast_trends_2050.png): Đồ thị đường xu hướng dự báo 1950 - 2050.
