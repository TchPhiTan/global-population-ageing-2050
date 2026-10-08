# Báo cáo Mô hình Hóa Dự báo Dân số & Xu hướng Già hoá Dân số đến 2050 (Chuẩn hóa 2026)

## 1. Chuẩn hóa Lát cắt Dữ liệu Toàn diện
- **Giai đoạn Lịch sử (`historical`)**: Từ năm 1950 đến hết năm **2026** (quan sát thực tế và thẩm định đa nguồn).
- **Giai đoạn Dự phóng (`projected`)**: Từ năm **2027 đến năm 2050** (ngoại suy mô hình học máy và kịch bản can thiệp).

## 2. Kết quả Tuyển chọn Đặc trưng (Feature Selection & Correlation)
Dựa trên Ma trận Tương quan Tuyến tính Pearson (`correlation_matrix.png`), các đặc trưng nhân khẩu học được tuyển chọn chặt chẽ:
- **Tuổi trung vị (`Median age`)**: Tương quan thuận cực mạnh ($r = +0.927$) với tỷ lệ già hóa 65+.
- **Tăng trưởng tự nhiên (`Natural growth`)**: Tương quan nghịch cực mạnh ($r = -0.834$) với già hóa và thuận ($r = +0.605$) với tăng trưởng tổng.
- **Mức sinh (`Total fertility rate`)**: Đòn bẩy chính sách có tương quan nghịch mạnh ($r = -0.677$) với già hóa.
- **Kỳ vọng sống (`Life expectancy`)**: Tương quan thuận ($r = +0.615$) với mức độ tích lũy người già.

## 3. Kết quả Đánh giá Mô hình Hồi quy Tuyến tính (Linear Regression)
Kiểm định Backtesting theo thời gian thực (Train: $\le 2020$, Test độc lập: $2021 - 2026$):

| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa Thực tiễn |
| :--- | :---: | :--- |
| **Hệ số xác định ($R^2$)** | **0.9942** | Mô hình giải thích được 99.42% biến thiên quy mô dân số trên tập kiểm định độc lập |
| **Sai số tuyệt đối trung bình (MAE)** | **2,638,108 người** | Độ lệch trung bình trên quy mô từng quốc gia giai đoạn 2021-2026 |
| **Căn bậc hai sai số toàn phương (RMSE)** | **10,405,944 người** | Độ tin cậy rất cao cho ngoại suy trung hạn đến 2050 |

## 4. Kết quả Hai Mô hình Phân loại Rủi ro (Logistic Regression)

| Mô hình Phân loại | Độ chính xác (Accuracy) | F1-Score | Mục tiêu & Bộ đặc trưng đầu vào (Baseline 2026) |
| :--- | :---: | :---: | :--- |
| **4A. Nguy cơ Suy giảm Dân số** | **93.33%** | **88.89%** | Dự báo đà thu hẹp dân số 2050 dựa trên Tốc độ tăng trưởng 2026, Mức sinh TFR 2026, Quy mô log10, Tuổi trung vị và Tỷ lệ 65% |
| **4B. Nguy cơ Xã hội Siêu già 2050** | **98.33%** | **98.18%** | Phân loại quốc gia vượt ngưỡng 20% người cao tuổi dựa trên Tỷ lệ 65% 2026, Tuổi trung vị, Mức sinh TFR và Tuổi thọ trung bình |

## 5. Top 10 Quốc gia có Nguy cơ Suy giảm Dân số Cao nhất (Depopulation Risk)
| Thứ hạng | Quốc gia | Mã ISO | Điểm Nguy cơ Suy giảm | Phân loại |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Cook Islands | COK | 100.00% | High Risk |
| 2 | Marshall Islands | MHL | 100.00% | High Risk |
| 3 | Saint Martin (French part) | MAF | 100.00% | High Risk |
| 4 | Saint Helena | SHN | 99.87% | High Risk |
| 5 | Saint Pierre and Miquelon | SPM | 99.64% | High Risk |
| 6 | Monaco | MCO | 99.57% | High Risk |
| 7 | American Samoa | ASM | 99.54% | High Risk |
| 8 | Northern Mariana Islands | MNP | 99.53% | High Risk |
| 9 | Martinique | MTQ | 99.46% | High Risk |
| 10 | United States Virgin Islands | VIR | 99.34% | High Risk |

## 6. Top 10 Quốc gia được Dự báo trở thành Xã hội Siêu già năm 2050 (Super-Aged)
| Thứ hạng | Quốc gia | Mã ISO | Xác suất Siêu già (65+ >= 20%) | Phân loại Dự báo |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Andorra | AND | 100.00% | Super-Aged Expected |
| 2 | Aruba | ABW | 100.00% | Super-Aged Expected |
| 3 | Australia | AUS | 100.00% | Super-Aged Expected |
| 4 | Austria | AUT | 100.00% | Super-Aged Expected |
| 5 | Belarus | BLR | 100.00% | Super-Aged Expected |
| 6 | Belgium | BEL | 100.00% | Super-Aged Expected |
| 7 | Bermuda | BMU | 100.00% | Super-Aged Expected |
| 8 | Bosnia and Herzegovina | BIH | 100.00% | Super-Aged Expected |
| 9 | Bulgaria | BGR | 100.00% | Super-Aged Expected |
| 10 | Canada | CAN | 100.00% | Super-Aged Expected |

## 7. Danh mục Tệp Dữ liệu Đầu ra
1. [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv): Dự báo dân số với nhãn `historical` (<=2026) và `projected` (2027-2050).
2. [`data/processed/model_vs_un_wpp_comparison_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/model_vs_un_wpp_comparison_2050.csv): So sánh đối chiếu ML vs UN kèm cột Residual và Residual_Pct (2027-2050).
3. [`data/processed/population_policy_scenarios_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_policy_scenarios_2050.csv): Bảng 4 kịch bản chính sách can thiệp (Baseline, Khuyến sinh, Tuổi hưu, Toàn diện).
4. [`data/processed/country_risk_classification_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/country_risk_classification_2050.csv): Điểm số rủi ro suy giảm và xác suất xã hội siêu già 2050.
5. [`reports/modeling/correlation_matrix.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/correlation_matrix.png): Ma trận nhiệt tương quan tuyến tính Pearson.
6. [`reports/modeling/confusion_matrix.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/confusion_matrix.png): Ma trận nhầm lẫn của 2 bài toán phân loại.
7. [`reports/modeling/forecast_trends_2050.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/reports/modeling/forecast_trends_2050.png): Đường xu hướng dự báo 1950 - 2050.
