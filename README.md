# Phân tích Biến động Dân số Toàn cầu & Xu hướng Già hoá Dân số đến năm 2050

> **Đồ án Cuối kỳ – Trực quan hoá Dữ liệu Trực quan (TTDLTQ)**
> Ngày cập nhật: 2026-09-26 | Phiên bản: v2.0

Dự án nghiên cứu sự chuyển dịch nhân khẩu học toàn cầu giai đoạn **1950 – 2050** theo hai trụ cột song song:

1. **Biến động Dân số**: Quy mô dân số, tốc độ tăng trưởng hàng năm, mức sinh (TFR) và so sánh kịch bản chuẩn UN WPP Medium Scenario với dữ liệu kiểm chứng độc lập World Population Review.
2. **Xu hướng Già hoá Dân số**: Chuyển dịch cơ cấu 3 nhóm tuổi (Trẻ em 0–14, Lao động 15–64, Người cao tuổi 65+), tuổi trung vị (Median age), tỷ số phụ thuộc người cao tuổi (Old-age dependency ratio), và dự phóng làn sóng các Xã hội Siêu già (Super-aged society $\ge 20\%$) vào năm 2050.

---

## 1. Cấu trúc Dự án

```text
├── data/
│   ├── raw/                                    # Dữ liệu thô tải từ Our World in Data & WPR
│   │   ├── fertility-rate-with-projections.csv      (1.1 MB – TFR 1950–2100 UN WPP)
│   │   ├── children-born-per-woman.csv              (510 KB – TFR 1950–2023)
│   │   ├── children-born-per-woman.metadata.json
│   │   ├── life-expectancy.csv                      (605 KB – Tuổi thọ 1950–2023)
│   │   ├── life-expectancy.metadata.json
│   │   ├── median-age.csv                           (1.0 MB – Tuổi trung vị 1950–2100)
│   │   ├── median-age.metadata.json
│   │   ├── population-growth-rates.csv              (1.0 MB – Tốc độ tăng trưởng 1950–2100)
│   │   ├── population-growth-rates.metadata.json
│   │   ├── population-with-un-projections.csv       (1.1 MB – Quy mô dân số 1950–2100)
│   │   ├── population-with-un-projections.metadata.json
│   │   ├── population-young-working-elderly-with-projections.csv  (1.8 MB – 3 Nhóm tuổi)
│   │   ├── population-young-working-elderly-with-projections.metadata.json
│   │   ├── world-population-review-2024-2026.csv    (69 KB – Kiểm chứng chéo WPR)
│   │   ├── world-population-review-2024-2026.metadata.json
│   │   └── readme.md                                # Ghi chú nguồn gốc dữ liệu từ OWID
│   └── processed/                              # Dữ liệu sạch, chuẩn hoá historical (<=2026) & projected (2027-2050)
│       ├── population_fact_long.csv                 (23 MB, 373,873 dòng, 7 cột)
│       ├── population_fact_wide.csv                 (4.2 MB, 27,760 dòng – Data source chính Tableau)
│       ├── population_forecast_2050.csv             (29,625 dòng – Dự báo ML & UN WPP 2027-2050)
│       ├── model_vs_un_wpp_comparison_2050.csv      (5,856 dòng – So sánh ML vs UN kèm Residual)
│       ├── population_policy_scenarios_2050.csv     (41,001 dòng – 4 Kịch bản chính sách What-If)
│       ├── country_risk_classification_2050.csv     (16 KB, 237 quốc gia – Điểm rủi ro 2050)
│       ├── world_population_review_validation.csv   (26 KB, 705 dòng – Đối chiếu WPR)
│       ├── continent_mapping.csv                    (5.6 KB, 237 quốc gia – Ánh xạ châu lục)
│       ├── data_dictionary.csv                      (1.5 KB – Từ điển dữ liệu chuẩn)
│       └── data_quality_report.json                 (1.0 KB – Báo cáo kiểm định)
├── docs/                                       # Tài liệu thiết kế & đặc tả
│   ├── data-sources-and-phases.md                   # Nguồn dữ liệu & phương pháp luận
│   ├── implementation-plan.md                       # Kế hoạch thực thi chi tiết
│   └── tableau-dashboard-spec.md                    # Đặc tả 10 biểu đồ & thiết kế Tableau
├── notebooks/                                  # Jupyter Notebooks tương tác
│   ├── 01_crawl_data.ipynb                          # Thu thập dữ liệu từ WPR
│   ├── 02_preprocessing.ipynb                       # Tiền xử lý & chuẩn hoá
│   ├── 03_eda_population.ipynb                      # Phân tích khám phá dữ liệu (EDA)
│   └── 04_modeling_forecast_2050.ipynb              # Mô hình hoá & dự báo 2050
├── reports/
│   ├── eda/                                    # 8 Biểu đồ EDA & tóm tắt phân tích
│   │   ├── 01-global-population-trend.png
│   │   ├── 02-top-populations.png
│   │   ├── 03-growth-rate-distribution.png
│   │   ├── 04-fertility-growth-scatter.png
│   │   ├── 05-population-heatmap.png
│   │   ├── 06-global-ageing-trend-2050.png
│   │   ├── 07-median-age-by-continent.png
│   │   ├── 08-top-super-aged-societies-2050.png
│   │   └── eda_summary.md
│   └── modeling/                               # Báo cáo mô hình học máy & đồ thị đánh giá
│       ├── confusion_matrix.png
│       ├── forecast_comparison_ageing.png
│       ├── forecast_trends_2050.png
│       └── model_report.md
├── scripts/                                    # Mã nguồn tự động hoá toàn bộ quy trình
│   ├── crawl_world_population_review.py             # Thu thập dữ liệu WPR (kiểm chứng chéo)
│   ├── preprocess_population_data.py                # Tiền xử lý, trích xuất & làm sạch
│   ├── run_eda.py                                   # Khám phá dữ liệu & xuất 8 biểu đồ
│   └── forecast_population.py                       # Mô hình hồi quy & phân loại rủi ro
├── tableau/                                    # (Thư mục dự phòng cho xuất bản Tableau)
├── TTDLTQ FINAL.twb                            # Workbook Tableau Desktop chính (194 KB)
└── README.md
```

---

## 2. Nguồn Dữ liệu & Ánh xạ Chart ↔ Our World in Data

> **Nguồn chính**: UN World Population Prospects 2024 Revision, biên tập bởi [Our World in Data (OWID)](https://ourworldindata.org/).
> **Nguồn kiểm chứng chéo**: [World Population Review](https://worldpopulationreview.com/) (2024–2026).

### Bảng Ánh xạ: Nguồn dữ liệu OWID → Chỉ số → Chart Tableau

| Chỉ số (Indicator) | File CSV thô | URL nguồn OWID | Dùng cho Chart Tableau nào |
| :--- | :--- | :--- | :--- |
| **Population** | `population-with-un-projections.csv` | [OWID: Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | Chart 1 (Filled Map), Chart 2 (Scatter - Size), Chart 3 (Bar), Chart 4 (Area+Line), Chart 5 (Bump), KPI 1 |
| **Population growth rate** | `population-growth-rates.csv` | [OWID: Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | Chart 6 (Histogram), Chart 7 (Scatter - trục Y), KPI 2 |
| **Total fertility rate (TFR)** | `fertility-rate-with-projections.csv` | [OWID: Fertility Rate with Projections](https://ourworldindata.org/grapher/fertility-rate-with-projections) | Dashboard 3 (TFR vs 2.1), Đặc trưng ML, KPI 4 |
| **Median age** | `median-age.csv` | [OWID: Median Age](https://ourworldindata.org/grapher/median-age) | Dashboard 3 (Scatter plots), Đặc trưng ML |
| **Life expectancy** | `life-expectancy.csv` | [OWID: Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) | Dashboard 3 (Tuổi thọ vs Mức sinh), Đặc trưng Logistic Regression |
| **Age groups (0-14, 15-64, 65+)** | `population-young-working-elderly-with-projections.csv` | [OWID: Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) | Chart 8 (100% Stacked Area), Chart 9 (Heatmap), Chart 10 (Dual-Axis), KPI 3 |
| **Share 65+ (dẫn xuất)** | *(Tính từ Age groups / Population)* | [OWID: Age Structure](https://ourworldindata.org/age-structure) | Chart 9, Chart 10, KPI 3, Ageing Stage classification |
| **Old-age dependency ratio (dẫn xuất)** | *(Tính từ 65+ / 15-64)* | [OWID: Dependency Ratios](https://ourworldindata.org/grapher/age-dependency-ratio-projected-to-2100) | Phân tích EDA, đặc trưng mô hình ML |

> **Xem chi tiết đường dẫn nguồn và phương pháp luận**: [`docs/data-sources-and-phases.md`](docs/data-sources-and-phases.md)
> **Xem đặc tả 10 biểu đồ Tableau & hướng dẫn kéo thả**: [`docs/tableau-dashboard-spec.md`](docs/tableau-dashboard-spec.md)

---

## 3. Quy trình Thực thi (Pipeline Execution)

Mọi bước trong dự án đều có thể tái lập từ đầu bằng Python:

```bash
# Bước 0 (Tuỳ chọn): Thu thập dữ liệu kiểm chứng từ World Population Review
python3 scripts/crawl_world_population_review.py

# Bước 1: Chạy tiền xử lý và sinh các bảng dữ liệu chuẩn hoá
python3 scripts/preprocess_population_data.py

# Bước 2: Chạy khám phá dữ liệu (EDA) và xuất 8 biểu đồ chuyên sâu
python3 scripts/run_eda.py

# Bước 3: Huấn luyện 2 mô hình học máy và xuất dự báo 2050
python3 scripts/forecast_population.py
```

**Đầu ra chính**:
- `data/processed/` – 9 tệp dữ liệu chuẩn hoá sẵn sàng nạp vào Tableau
- `reports/eda/` – 8 biểu đồ PNG + báo cáo insight `eda_summary.md`
- `reports/modeling/` – 3 biểu đồ đánh giá + báo cáo `model_report.md`

---

## 4. Kết quả Mô hình Hoá Học máy (Machine Learning)

### 4.1 Hồi quy Tuyến tính (Linear Regression)
- Dự báo quy mô dân số và người cao tuổi từ **2027 đến 2050** cho **237 quốc gia/vùng lãnh thổ**.
- Đánh giá trên tập kiểm nghiệm độc lập (Test Set 2016–2023): **$R^2 = 0.9956$**, **MAE = 2.49 triệu người**, **RMSE = 8.88 triệu người**.

### 4.2 Hồi quy Logistic (Logistic Regression)
- **Mô hình 2A (Nguy cơ suy giảm dân số)**: Accuracy **93.33%**, F1-score **88.89%**.
- **Mô hình 2B (Nguy cơ Xã hội Siêu già 2050)**: Accuracy **98.33%**, F1-score **98.18%**.

### 4.3 So sánh Dự báo ML vs UN WPP
Mô hình Linear Regression bám sát kịch bản chuẩn UN WPP Medium Scenario với **độ lệch MAE < 0.8%** về tỷ lệ người già trên phạm vi toàn cầu. Dữ liệu so sánh chi tiết nằm tại `data/processed/model_vs_un_wpp_comparison_2050.csv`.

---

## 5. Tích hợp Tableau Dashboard

Bộ dữ liệu chuẩn hoá trong `data/processed/` đã được thiết kế sẵn sàng để nạp trực tiếp vào Tableau:

| Bảng dữ liệu | Vai trò trên Tableau | Số dòng |
| :--- | :--- | :---: |
| `population_fact_wide.csv` | ⭐ **Data source chính trên Tableau** (10 chỉ số dạng wide) | 39,476 |
| `population_fact_long.csv` | Bản lưu trữ / Phân tích Python-R (dạng long chuẩn) | 348,338 |
| `population_forecast_2050.csv` | So sánh ML vs UN WPP (Chart 10) | 29,625 |
| `model_vs_un_wpp_comparison_2050.csv` | Bảng chênh lệch định lượng (Tooltip Chart 10) | 5,688 |
| `country_risk_classification_2050.csv` | Điểm rủi ro suy giảm & siêu già | 237 |
| `continent_mapping.csv` | Left Join phân nhóm châu lục | 237 |

**10 loại biểu đồ khác nhau** được đặc tả chi tiết (bao gồm hướng dẫn kéo thả từng bước) tại [`docs/tableau-dashboard-spec.md`](docs/tableau-dashboard-spec.md).

---

## 6. Kho lưu trữ GitHub & Trích dẫn

- **Repository**: [https://github.com/TchPhiTan/global-population-ageing-2050](https://github.com/TchPhiTan/global-population-ageing-2050)
- **Dữ liệu gốc**: United Nations, Department of Economic and Social Affairs, Population Division (2024). *World Population Prospects 2024, Online Edition.* – Phân phối bởi [Our World in Data](https://ourworldindata.org/). Giấy phép: CC BY 3.0 IGO.
- **Kiểm chứng chéo**: [World Population Review](https://worldpopulationreview.com/) (2024–2026).
