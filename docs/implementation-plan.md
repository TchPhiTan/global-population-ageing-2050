# Kế hoạch Thực thi Dự án: Phân tích Biến động Dân số Toàn cầu & Xu hướng Già hoá Dân số đến năm 2050

## 1. Mục tiêu Đề tài
Nghiên cứu sự chuyển dịch nhân khẩu học toàn cầu theo hai trụ cột song song:
1. **Biến động dân số**: Quy mô dân số, tốc độ tăng trưởng, mức sinh (TFR) trong giai đoạn 1950 – 2026 và so sánh với kịch bản chuẩn UN WPP Medium Scenario.
2. **Xu hướng già hoá dân số**: Sự biến đổi cơ cấu 3 nhóm tuổi (0-14, 15-64, 65+), tốc độ tăng trưởng tuổi trung vị (Median age), tỷ số phụ thuộc người cao tuổi (Old-age dependency ratio), và dự phóng làn sóng các Xã hội Siêu già (Super-aged societies) đến năm 2050.

## 2. Phạm vi & Nguyên tắc Dữ liệu
- **Nguồn chính**: UN World Population Prospects (bản sửa đổi 2024 do Our World in Data biên tập).
- **Khung thời gian chuẩn hóa**: **1950 – 2050** (chuỗi dữ liệu kéo dài đến 2100).
- **Phân định trạng thái**: Luôn phân tách rõ ràng `DataStatus` gồm `estimate` (1950–2023), `projected` (2024–2026/2100) và `forecast` (kết quả mô hình học máy).
- **Nguồn kiểm chứng độc lập**: World Population Review (2024–2026) dùng để đối chiếu chéo số liệu thực tế hiện tại.
- Khóa chính logic của bảng Fact: `Entity`, `Code`, `Year`, `Indicator`, `DataStatus`.

## 3. Danh mục Sản phẩm Bàn giao (Deliverables)

### 3.1 Dữ liệu & Xử lý (Data Processing)
- `scripts/preprocess_population_data.py`: Pipeline làm sạch, trích xuất và chuẩn hóa dữ liệu.
- `data/processed/population_fact_long.csv`: Bảng fact dạng long (>350.000 dòng, 10 chỉ số).
- `data/processed/population_fact_wide.csv`: Bảng fact dạng wide phục vụ Tableau & Heatmap.
- `data/processed/world_population_review_validation.csv`: Kết quả đối chiếu chéo WPR (100% khớp).
- `data/processed/data_dictionary.csv`: Từ điển dữ liệu định nghĩa từng trường.
- `data/processed/data_quality_report.json`: Báo cáo kiểm định chất lượng dữ liệu vượt qua mọi Quality Gates.

**10 Chỉ số trong Fact Table**:
1. `Population` (người)
2. `Population growth rate` (%)
3. `Total fertility rate` (con/phụ nữ)
4. `Median age` (tuổi)
5. `Life expectancy` (tuổi)
6. `Older people (65+ years)` (người)
7. `Working-age adults (15-64 years)` (người)
8. `Children (under-15s)` (người)
9. `Share of population aged 65+` (%)
10. `Old-age dependency ratio` (%)

### 3.2 Phân tích Khám phá Dữ liệu (EDA)
- `scripts/run_eda.py`: Kịch bản phân tích và vẽ biểu đồ.
- 8 Biểu đồ chuyên sâu tại `reports/eda/`:
  - `01-global-population-trend.png`: Xu hướng quy mô dân số thế giới (1950–2050).
  - `02-top-populations.png`: Top 10 quốc gia đông dân nhất năm 2026.
  - `03-growth-rate-distribution.png`: Phân phối tốc độ tăng trưởng quốc gia năm 2026.
  - `04-fertility-growth-scatter.png`: Tương quan mức sinh (TFR) và tăng trưởng dân số.
  - `05-population-heatmap.png`: Ma trận quy mô dân số top 15 nước qua các thập kỷ.
  - `06-global-ageing-trend-2050.png`: Chuyển dịch cơ cấu 3 nhóm tuổi toàn cầu (1950–2050).
  - `07-median-age-by-continent.png`: Tăng trưởng tuổi trung vị của các châu lục đến 2050.
  - `08-top-super-aged-societies-2050.png`: Top 10 quốc gia già nhất thế giới năm 2050.
- `reports/eda/eda_summary.md`: Báo cáo phân tích insight chi tiết.

### 3.3 Mô hình Hóa Học máy (Modeling)
- `scripts/forecast_population.py`: Pipeline huấn luyện mô hình và dự phóng đến 2050.
- `data/processed/population_forecast_2050.csv`: Chuỗi dự báo quy mô dân số và người cao tuổi.
- `data/processed/country_risk_classification_2050.csv`: Điểm rủi ro suy giảm dân số & xã hội siêu già.
- `reports/modeling/model_report.md`: Báo cáo đánh giá mô hình học máy.
- `reports/modeling/confusion_matrix.png`: Ma trận nhầm lẫn của 2 mô hình phân loại Logistic Regression.
- `reports/modeling/forecast_trends_2050.png`: Đồ thị xu hướng dự phóng tương lai.

### 3.4 Đặc tả Dashboard Tableau (Dashboard Specification)
- `docs/tableau-dashboard-spec.md`: Đặc tả chi tiết 4 Dashboard Tab, 10 loại biểu đồ, bản đồ địa lý, bộ lọc liên động, công thức tính toán và kịch bản thuyết trình.

## 4. Trạng thái Triển khai
- [x] Thiết lập Git repository và đẩy lên GitHub: `TchPhiTan/global-population-ageing-2050`.
- [x] Tải bổ sung dữ liệu già hóa (Median age, Age groups, Life expectancy).
- [x] Cập nhật pipeline preprocessing và đạt mọi Quality Gates.
- [x] Tạo 8 biểu đồ EDA và báo cáo insight toàn diện.
- [x] Huấn luyện 2 mô hình học máy (Linear Regression R2=0.9956, Logistic Regression Acc=98.3%).
- [x] Cập nhật đặc tả Tableau Dashboard với 2 trụ cột Biến động & Già hóa.