# Báo cáo Mô hình Hóa Dự báo Dân số và Nguy cơ Suy giảm (Phase 3)

## 1. Mục tiêu và Kiến trúc Mô hình
- **Mô hình 1 (Hồi quy Tuyến tính - Linear Regression)**: Dự báo giá trị quy mô dân số liên tục từ năm 2027 đến năm 2050 cho 237 quốc gia/vùng lãnh thổ.
- **Mô hình 2 (Hồi quy Logistic - Logistic Regression)**: Phân loại nhị phân nguy cơ một quốc gia bước vào chu kỳ suy giảm dân số kéo dài trước năm 2050 (`Depopulation_Risk`), không dùng để dự báo trực tiếp quy mô dân số.

## 2. Kết quả Đánh giá Mô hình Dự báo Dân số (Linear Regression)
Kiểm định mô hình theo phương pháp phân chia thời gian (Time-based train/test split):
- **Tập huấn luyện (Train set)**: Giai đoạn 1950 - 2015.
- **Tập kiểm định (Test set)**: Giai đoạn 2016 - 2023.

| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa |
| :--- | :---: | :--- |
| **Hệ số xác định ($R^2$)** | **0.9956** | Mô hình giải thích được hơn 99.6% phương sai biến động dân số trên tập kiểm định |
| **Sai số tuyệt đối trung bình (MAE)** | **2,496,461 người** | Độ lệch trung bình trên quy mô quốc gia |
| **Căn bậc hai sai số toàn phương (RMSE)** | **8,882,820 người** | Mức độ tin cậy cao trên chu kỳ trung hạn |

- **Dữ liệu đầu ra**: Toàn bộ chuỗi 1950 - 2050 đã được xuất ra file [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv).

## 3. Kết quả Phân loại Nguy cơ Suy giảm Dân số (Logistic Regression)
Mô hình phân loại nhị phân đánh giá xác suất quốc gia có nguy cơ suy giảm dân số đến năm 2050 dựa trên 4 đặc trưng: Tốc độ tăng trưởng 2026, Mức sinh TFR 2023, Quy mô dân số log10 và Độ suy giảm tăng trưởng 5 năm gần nhất.

| Chỉ số Phân loại | Giá trị Kiểm định (Test Set) |
| :--- | :---: |
| **Độ chính xác (Accuracy)** | **98.33%** |
| **Độ chuẩn xác (Precision)** | **100.00%** |
| **Độ thu hồi (Recall)** | **94.12%** |
| **Điểm F1-Score** | **96.97%** |

### Ma trận nhầm lẫn (Confusion Matrix):
- True Negatives (Dự báo tăng trưởng - Thực tế tăng trưởng): 43
- False Positives (Dự báo suy giảm - Thực tế tăng trưởng): 0
- False Negatives (Dự báo tăng trưởng - Thực tế suy giảm): 1
- True Positives (Dự báo suy giảm - Thực tế suy giảm): 16

## 4. Top 10 Quốc gia có Nguy cơ Suy giảm Dân số Cao nhất (High Depopulation Risk)
| Thứ hạng | Quốc gia | Mã ISO | Điểm Nguy cơ (Risk Probability) | Phân loại |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Saint Martin (French part) | MAF | 100.00% | High Risk |
| 2 | Marshall Islands | MHL | 100.00% | High Risk |
| 3 | Cook Islands | COK | 100.00% | High Risk |
| 4 | American Samoa | ASM | 99.92% | High Risk |
| 5 | Northern Mariana Islands | MNP | 99.77% | High Risk |
| 6 | Tuvalu | TUV | 99.72% | High Risk |
| 7 | Saint Helena | SHN | 99.46% | High Risk |
| 8 | Saint Pierre and Miquelon | SPM | 99.39% | High Risk |
| 9 | Moldova | MDA | 98.74% | High Risk |
| 10 | United States Virgin Islands | VIR | 98.51% | High Risk |

## 5. Hướng dẫn Tích hợp vào Dashboard Tableau (Phase 4)
1. Nạp file [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv) vào Tableau.
2. Tạo bộ lọc theo cột `DataStatus` (`estimate`, `projected`, `forecast`) để người xem có thể quan sát từng giai đoạn lịch sử - hiện tại - tương lai.
3. Sử dụng trường `Model` để phân biệt dữ liệu điều tra thực tế với giá trị dự báo toán học.
