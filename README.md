# Phân tích Biến động Dân số Toàn cầu & Xu hướng Già hoá Dân số đến năm 2050

Dự án Phân tích Dữ liệu Trực quan (TTDLTQ) nghiên cứu sự chuyển dịch nhân khẩu học toàn cầu giai đoạn **1950 – 2050** theo hai trụ cột song song:
1. **Biến động Dân số**: Quy mô dân số, tốc độ tăng trưởng hàng năm, mức sinh (TFR) và so sánh kịch bản chuẩn UN WPP Medium Scenario với dữ liệu kiểm chứng độc lập World Population Review.
2. **Xu hướng Già hoá Dân số**: Chuyển dịch cơ cấu 3 nhóm tuổi (Trẻ em 0–14, Lao động 15–64, Người cao tuổi 65+), tuổi trung vị (Median age), tỷ số phụ thuộc người cao tuổi (Old-age dependency ratio), và dự phóng làn sóng các Xã hội Siêu già (Super-aged society $\ge 20\%$) vào năm 2050.

---

## 1. Cấu trúc Dự án

```text
├── data/
│   ├── raw/                  # Dữ liệu thô tải từ Our World in Data & WPR
│   │   ├── children-born-per-woman.csv
│   │   ├── life-expectancy.csv
│   │   ├── median-age.csv
│   │   ├── population-growth-rates.csv
│   │   ├── population-with-un-projections.csv
│   │   ├── population-young-working-elderly-with-projections.csv
│   │   └── world-population-review-2024-2026.csv
│   └── processed/            # Dữ liệu sạch, sẵn sàng nạp vào Tableau & ML
│       ├── population_fact_long.csv           # Fact table dạng long (>352.000 dòng, 10 chỉ số)
│       ├── population_fact_wide.csv           # Fact table dạng wide (>39.000 dòng)
│       ├── population_forecast_2050.csv       # Dữ liệu dự báo dân số & già hóa đến 2050
│       ├── country_risk_classification_2050.csv # Điểm rủi ro suy giảm & xã hội siêu già
│       ├── world_population_review_validation.csv # Bảng kiểm chứng chéo WPR (100% khớp)
│       ├── continent_mapping.csv              # Ánh xạ quốc gia - châu lục
│       ├── data_dictionary.csv                # Từ điển dữ liệu
│       └── data_quality_report.json           # Báo cáo kiểm định chất lượng
├── docs/                     # Tài liệu thiết kế & đặc tả
│   ├── implementation-plan.md        # Kế hoạch thực thi chi tiết
│   ├── tableau-dashboard-spec.md     # Đặc tả 10 biểu đồ & thiết kế Tableau
│   └── data-sources-and-phases.md    # Phân kỳ dữ liệu
├── reports/
│   ├── eda/                  # 8 Biểu đồ EDA và tóm tắt phân tích (eda_summary.md)
│   └── modeling/             # Báo cáo mô hình học máy (model_report.md) & đồ thị đánh giá
├── scripts/                  # Mã nguồn tự động hóa toàn bộ quy trình
│   ├── preprocess_population_data.py # Tiền xử lý, trích xuất & làm sạch fact table
│   ├── run_eda.py                    # Khám phá dữ liệu & xuất 8 biểu đồ
│   └── forecast_population.py        # Mô hình hồi quy tuyến tính & Logistic regression
└── README.md
```

---

## 2. Quy trình Thực thi (Pipeline Execution)

Mọi bước trong dự án đều có thể tái lập từ đầu bằng Python:

```bash
# 1. Chạy tiền xử lý và sinh các bảng dữ liệu chuẩn hóa
python3 scripts/preprocess_population_data.py

# 2. Chạy khám phá dữ liệu (EDA) và xuất 8 biểu đồ chuyên sâu
python3 scripts/run_eda.py

# 3. Huấn luyện 2 mô hình học máy (Linear Regression & Logistic Regression) và xuất dự báo 2050
python3 scripts/forecast_population.py
```

---

## 3. Kết quả Mô hình Hóa Học máy (Machine Learning)

* **Hồi quy Tuyến tính (Linear Regression)**:
  - Dự báo quy mô dân số và người cao tuổi từ 2027 đến 2050 cho 237 quốc gia/vùng lãnh thổ.
  - Đánh giá trên tập kiểm nghiệm độc lập (Test Set): **$R^2 = 0.9956$**, **MAE = 2.49 triệu người**.
* **Hồi quy Logistic (Logistic Regression)**:
  - **Mô hình 1 (Nguy cơ suy giảm dân số)**: Độ chính xác đạt **93.33%**, F1-score đạt **88.89%**.
  - **Mô hình 2 (Nguy cơ trở thành Xã hội Siêu già năm 2050 - 65+ tuổi $\ge 20\%$)**: Độ chính xác đạt **98.33%**, F1-score đạt **98.18%**.

---

## 4. Tích hợp Tableau Dashboard

Bộ dữ liệu chuẩn hóa trong `data/processed/` đã được thiết kế sẵn sàng để nạp trực tiếp vào Tableau với đầy đủ các trường:
* Đo lường biến động dân số: `Population`, `Growth Rate (%)`, `Total Fertility Rate`.
* Đo lường già hóa dân số: `Median Age`, `Share 65+ (%)`, `Old-age Dependency Ratio`, `Ageing Stage`.
* Xem chi tiết hướng dẫn thiết lập biểu đồ, bộ lọc và calculated fields tại [`docs/tableau-dashboard-spec.md`](docs/tableau-dashboard-spec.md).

---

## 5. Kho lưu trữ GitHub
- **Repository**: [https://github.com/TchPhiTan/global-population-ageing-2050](https://github.com/TchPhiTan/global-population-ageing-2050)
