# Kế hoạch Thực thi Dự án: Phân tích Biến động Dân số Toàn cầu & Xu hướng Già hoá Dân số đến năm 2050

> **Cập nhật lần cuối**: 2026-09-26 | **Trạng thái**: ✅ Hoàn thành toàn bộ 4 Phase

---

## 1. Mục tiêu Đề tài

Nghiên cứu sự chuyển dịch nhân khẩu học toàn cầu theo hai trụ cột song song:

1. **Biến động dân số**: Quy mô dân số, tốc độ tăng trưởng, mức sinh (TFR) trong giai đoạn 1950 – 2023 và so sánh với kịch bản chuẩn UN WPP Medium Scenario.
2. **Xu hướng già hoá dân số**: Sự biến đổi cơ cấu 3 nhóm tuổi (0-14, 15-64, 65+), tốc độ tăng trưởng tuổi trung vị (Median age), tỷ số phụ thuộc người cao tuổi (Old-age dependency ratio), và dự phóng làn sóng các Xã hội Siêu già (Super-aged societies) đến năm 2050.

---

## 2. Phạm vi & Nguyên tắc Dữ liệu

| Hạng mục | Chi tiết |
| :--- | :--- |
| **Nguồn chính** | UN World Population Prospects 2024 Revision (biên tập bởi [Our World in Data](https://ourworldindata.org/)) |
| **Nguồn kiểm chứng** | [World Population Review](https://worldpopulationreview.com/) (2024–2026) |
| **Khung thời gian** | **1950 – 2050** (chuỗi dữ liệu kéo dài đến 2100) |
| **Phân định trạng thái** | `estimate` (1950–2023), `projected` (2024–2100), `forecast` (ML 2024–2050) |
| **Khoá chính Fact table** | `Entity`, `Code`, `Year`, `Indicator`, `DataStatus` |
| **Số quốc gia/vùng lãnh thổ** | 237 |
| **Tổng số chỉ số** | 10 (xem danh sách bên dưới) |

---

## 3. Danh mục Sản phẩm Bàn giao (Deliverables)

### Phase 1: Thu thập & Tiền xử lý Dữ liệu ✅

| # | Sản phẩm | Mô tả | Trạng thái |
| :---: | :--- | :--- | :---: |
| 1 | `scripts/crawl_world_population_review.py` | Thu thập dữ liệu WPR tự động | ✅ |
| 2 | `scripts/preprocess_population_data.py` | Pipeline làm sạch, trích xuất, chuẩn hoá | ✅ |
| 3 | `data/processed/population_fact_long.csv` | Fact table dạng long (348,338 dòng, 7 cột, 10 chỉ số) | ✅ |
| 4 | `data/processed/population_fact_wide.csv` | Fact table dạng wide (39,476 dòng, data source chính Tableau) | ✅ |
| 5 | `data/processed/world_population_review_validation.csv` | Đối chiếu chéo WPR (705/705 = 100% khớp) | ✅ |
| 6 | `data/processed/continent_mapping.csv` | Ánh xạ 237 quốc gia → 6 châu lục | ✅ |
| 7 | `data/processed/data_dictionary.csv` | Từ điển dữ liệu | ✅ |
| 8 | `data/processed/data_quality_report.json` | Báo cáo kiểm định – vượt qua mọi Quality Gates | ✅ |

**10 Chỉ số trong Fact Table**:

| # | Indicator | Đơn vị | Nguồn OWID |
| :---: | :--- | :--- | :--- |
| 1 | `Population` | người | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) |
| 2 | `Population growth rate` | % | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) |
| 3 | `Total fertility rate` | con/phụ nữ | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) |
| 4 | `Median age` | tuổi | [Median Age](https://ourworldindata.org/grapher/median-age) |
| 5 | `Life expectancy` | tuổi | [Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) |
| 6 | `Older people (65+ years)` | người | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) |
| 7 | `Working-age adults (15-64 years)` | người | *(cùng nguồn #6)* |
| 8 | `Children (under-15s)` | người | *(cùng nguồn #6)* |
| 9 | `Share of population aged 65+` | % | Dẫn xuất (#6/#1 × 100) |
| 10 | `Old-age dependency ratio` | % | Dẫn xuất (#6/#7 × 100) |

---

### Phase 2: Phân tích Khám phá Dữ liệu (EDA) ✅

| # | Sản phẩm | Mô tả | Trạng thái |
| :---: | :--- | :--- | :---: |
| 1 | `scripts/run_eda.py` | Kịch bản phân tích & vẽ biểu đồ tự động | ✅ |
| 2 | `reports/eda/eda_summary.md` | Báo cáo phân tích insight chi tiết | ✅ |

**8 Biểu đồ EDA** tại `reports/eda/`:

| # | File | Nội dung | Chỉ số Sử dụng |
| :---: | :--- | :--- | :--- |
| 1 | `01-global-population-trend.png` | Xu hướng quy mô dân số thế giới 1950–2050 | Population |
| 2 | `02-top-populations.png` | Top 10 quốc gia đông dân nhất 2023 | Population |
| 3 | `03-growth-rate-distribution.png` | Phân phối tốc độ tăng trưởng 2023 | Population growth rate |
| 4 | `04-fertility-growth-scatter.png` | Tương quan TFR & tăng trưởng | TFR + Growth rate |
| 5 | `05-population-heatmap.png` | Ma trận quy mô top 15 qua thập kỷ | Population |
| 6 | `06-global-ageing-trend-2050.png` | Chuyển dịch 3 nhóm tuổi 1950–2050 | Age groups |
| 7 | `07-median-age-by-continent.png` | Tuổi trung vị các châu lục đến 2050 | Median age |
| 8 | `08-top-super-aged-societies-2050.png` | Top 10 quốc gia già nhất 2050 | Share 65+ |

---

### Phase 3: Mô hình Hoá Học máy (Modeling) ✅

| # | Sản phẩm | Mô tả | Trạng thái |
| :---: | :--- | :--- | :---: |
| 1 | `scripts/forecast_population.py` | Pipeline huấn luyện mô hình & dự phóng 2050 | ✅ |
| 2 | `data/processed/population_forecast_2050.csv` | Dự báo dân số & 65+ (30,336 dòng, ML + UN WPP) | ✅ |
| 3 | `data/processed/model_vs_un_wpp_comparison_2050.csv` | So sánh định lượng ML vs UN (6,399 dòng) | ✅ |
| 4 | `data/processed/country_risk_classification_2050.csv` | Điểm rủi ro suy giảm & siêu già (237 nước) | ✅ |
| 5 | `reports/modeling/model_report.md` | Báo cáo đánh giá mô hình học máy | ✅ |
| 6 | `reports/modeling/confusion_matrix.png` | Ma trận nhầm lẫn 2 mô hình Logistic | ✅ |
| 7 | `reports/modeling/forecast_trends_2050.png` | Đồ thị xu hướng dự phóng 1950–2050 | ✅ |
| 8 | `reports/modeling/forecast_comparison_ageing.png` | So sánh ML vs UN về tỷ lệ già hoá | ✅ |

**Kết quả Mô hình**:

| Mô hình | Chỉ số Chính | Giá trị |
| :--- | :--- | :--- |
| Linear Regression (Dự báo dân số) | $R^2$ | **0.9956** |
| Linear Regression | MAE | **2.50 triệu người** |
| Logistic (Suy giảm dân số) | Accuracy / F1 | **95.00%** / **90.32%** |
| Logistic (Xã hội Siêu già 2050) | Accuracy / F1 | **95.00%** / **94.55%** |

---

### Phase 4: Đặc tả Dashboard Tableau ✅

| # | Sản phẩm | Mô tả | Trạng thái |
| :---: | :--- | :--- | :---: |
| 1 | `docs/tableau-dashboard-spec.md` | Đặc tả chi tiết 4 Cụm, 10 loại biểu đồ, bộ lọc, KPI, Story Points | ✅ |
| 2 | `TTDLTQ FINAL.twb` | Workbook Tableau Desktop chính (194 KB) | ✅ |

**10 Loại Biểu đồ trên Dashboard** (chi tiết tại `docs/tableau-dashboard-spec.md`):

| Chart # | Tên | Loại | Cụm |
| :---: | :--- | :--- | :--- |
| 1 | Bản đồ Dân số | Filled Map (Choropleth) | Cụm 1: Quy mô & Phân bố |
| 2 | Chuyển đổi Nhân khẩu học | Animated Scatter Plot | Cụm 1: Quy mô & Phân bố |
| 3 | Top 10 Đông dân | Horizontal Bar | Cụm 1 |
| 4 | Xu hướng 1950–2050 | Area + Line | Cụm 2: Tiến trình Lịch sử |
| 5 | Đổi ngôi Thứ hạng | Bump Chart | Cụm 2 |
| 6 | Phân phối Tăng trưởng | Histogram | Cụm 3: Nguyên nhân & Phân hoá |
| 7 | TFR vs Tăng trưởng | Scatter Plot | Cụm 3 |
| 8 | 3 Khối Tuổi | 100% Stacked Area | Cụm 4: Già hoá & Dự báo ML |
| 9 | Ma trận Già hoá | Heatmap / Highlight Table | Cụm 4 |
| 10 | ML vs UN WPP | Dual-Axis Line | Cụm 4 |

---

## 4. Trạng thái Triển khai Tổng thể

- [x] Thiết lập Git repository và đẩy lên GitHub: [`TchPhiTan/global-population-ageing-2050`](https://github.com/TchPhiTan/global-population-ageing-2050)
- [x] Tải đầy đủ 6 bộ dữ liệu từ Our World in Data + 1 bộ WPR
- [x] Cập nhật pipeline preprocessing – đạt mọi Quality Gates
- [x] Tạo 8 biểu đồ EDA và báo cáo insight toàn diện
- [x] Huấn luyện 2 mô hình học máy (Linear Regression R²=0.9956, Logistic Acc=98.3%)
- [x] Tạo bảng so sánh ML vs UN WPP (`model_vs_un_wpp_comparison_2050.csv`)
- [x] Cập nhật đặc tả Tableau Dashboard với 2 trụ cột Biến động & Già hoá
- [x] Viết README, tài liệu nguồn dữ liệu, và hướng dẫn Tableau chi tiết

---

## 5. Hướng dẫn Sử dụng Nhanh

```bash
# Clone repository
git clone https://github.com/TchPhiTan/global-population-ageing-2050.git
cd global-population-ageing-2050

# Cài đặt thư viện Python (nếu chưa có)
pip install pandas numpy scikit-learn matplotlib seaborn requests beautifulsoup4

# Chạy toàn bộ pipeline
python3 scripts/preprocess_population_data.py
python3 scripts/run_eda.py
python3 scripts/forecast_population.py

# Mở Tableau
# Mở file "TTDLTQ FINAL.twb" bằng Tableau Desktop / Tableau Public
# Xem hướng dẫn chi tiết tại docs/tableau-dashboard-spec.md
```

---

*Phiên bản: 2026-09-26. Xem chi tiết nguồn dữ liệu tại [`docs/data-sources-and-phases.md`](data-sources-and-phases.md).*