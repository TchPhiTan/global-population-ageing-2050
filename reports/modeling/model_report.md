# Báo cáo Mô hình Hoá Dự báo Dân số & Xu hướng Già hoá Dân số đến 2050 (Phase 3)

> **Cập nhật**: 2026-09-26 | **Script**: `scripts/forecast_population.py`
> **Nguồn dữ liệu gốc**: UN WPP 2024 via [Our World in Data](https://ourworldindata.org/) | **Nguồn so sánh**: UN WPP Medium Scenario

---

## 1. Kiến trúc Hai Trụ cột Mô hình Học máy

### 1.1 Trụ cột 1: Dự báo Chuỗi Giá trị Liên tục (Linear Regression)
- Dự báo quy mô dân số (`Population`) và quy mô người cao tuổi (`Older_People_65plus`) từ năm **2027 đến năm 2050** cho **237 quốc gia/vùng lãnh thổ**.
- Dữ liệu huấn luyện: Chuỗi ước tính lịch sử 1950–2023 từ [OWID: Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) và [OWID: Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections).

### 1.2 Trụ cột 2: Phân loại Rủi ro Nhị phân Kép (Logistic Regression)
- **Mô hình 2A (Depopulation Risk)**: Đánh giá xác suất quốc gia bước vào chu kỳ suy giảm dân số kéo dài trước năm 2050.
- **Mô hình 2B (Super-Aged Society Risk)**: Đánh giá xác suất quốc gia trở thành **Xã hội Siêu già vào năm 2050** (Tỷ lệ người cao tuổi 65+ vượt ngưỡng 20%).
- Đặc trưng đầu vào: `Population growth rate` ([OWID](https://ourworldindata.org/grapher/population-growth-rates)), `TFR` ([OWID](https://ourworldindata.org/grapher/children-born-per-woman)), `Median age` ([OWID](https://ourworldindata.org/grapher/median-age)), `Life expectancy` ([OWID](https://ourworldindata.org/grapher/life-expectancy)), `Share 65+` ([OWID](https://ourworldindata.org/age-structure)).

---

## 2. Kết quả Đánh giá Mô hình Dự báo Dân số (Linear Regression)

Kiểm định mô hình theo phương pháp phân chia thời gian (Time-based train/test split: Train ≤ 2015, Test 2016–2023):

| Chỉ số Đánh giá | Giá trị Đạt được | Ý nghĩa Thực tiễn |
| :--- | :---: | :--- |
| **Hệ số xác định ($R^2$)** | **0.9956** | Giải thích được 99.6% biến động quy mô dân số trên tập kiểm định độc lập |
| **Sai số tuyệt đối trung bình (MAE)** | **2,496,461 người** | Độ lệch trung bình trên quy mô từng quốc gia |
| **Căn bậc hai sai số toàn phương (RMSE)** | **8,882,820 người** | Độ tin cậy rất cao cho dự báo chu kỳ trung hạn đến 2050 |

---

## 3. Kết quả Hai Mô hình Phân loại Rủi ro (Logistic Regression)

| Mô hình | Accuracy | F1-Score | Bộ đặc trưng đầu vào |
| :--- | :---: | :---: | :--- |
| **2A. Nguy cơ Suy giảm Dân số** | **93.33%** | **88.89%** | Growth rate 2026, TFR, Population (log10), Median age, Share 65+ |
| **2B. Nguy cơ Xã hội Siêu già 2050** | **98.33%** | **98.18%** | Share 65+ 2026, Median age, TFR, Life expectancy |

---

## 4. Top 10 Quốc gia Nguy cơ Suy giảm Dân số Cao nhất

| # | Quốc gia | Mã ISO | Điểm Nguy cơ | Phân loại |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Cook Islands | COK | 100.00% | High Risk |
| 2 | Marshall Islands | MHL | 100.00% | High Risk |
| 3 | Saint Martin (French part) | MAF | 100.00% | High Risk |
| 4 | Saint Helena | SHN | 99.87% | High Risk |
| 5 | Saint Pierre and Miquelon | SPM | 99.64% | High Risk |
| 6 | Monaco | MCO | 99.59% | High Risk |
| 7 | Northern Mariana Islands | MNP | 99.56% | High Risk |
| 8 | American Samoa | ASM | 99.54% | High Risk |
| 9 | Martinique | MTQ | 99.49% | High Risk |
| 10 | United States Virgin Islands | VIR | 99.36% | High Risk |

---

## 5. Top 10 Quốc gia Dự báo trở thành Xã hội Siêu già 2050

| # | Quốc gia | Mã ISO | Xác suất Siêu già (65+ ≥ 20%) | Phân loại |
| :---: | :--- | :---: | :---: | :---: |
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

---

## 6. So sánh Dự báo: Mô hình ML vs Kịch bản Chuẩn UN WPP

| Phạm vi | Chỉ số so sánh | Độ lệch trung bình | Nhận xét |
| :--- | :--- | :--- | :--- |
| **Toàn cầu** | Share 65+ (%) | MAE < **0.8%** | ML bám sát UN WPP trên phạm vi macro |
| **Ấn Độ** | Population | < 2% | Quán tính tăng trưởng ổn định → ML chính xác cao |
| **Việt Nam** | Share 65+ 2050 | 20.5% (ML) vs 21.1% (UN) | Cả 2 đồng thuận Việt Nam = Xã hội Siêu già |
| **Hàn Quốc** | Share 65+ 2050 | UN cao hơn ML ~2-3% | UN dùng Cohort-Component micro → phản ánh sốc TFR mạnh hơn |

**Khác biệt phương pháp luận**:
- **Linear Regression**: Ngoại suy tuyến tính dựa trên quán tính gia tốc chuỗi 30 năm gần nhất (1996–2026).
- **UN WPP Medium Scenario**: Mô hình thành phần Cohort-Component vi mô kết hợp bảng sống (Life Tables) + giả định mức sinh hồi phục nhẹ sau 2040.

---

## 7. Danh mục Tệp Đầu ra & Tham khảo

### 7.1 File Đầu ra Mô hình Hoá

| # | File | Mô tả | Số dòng |
| :---: | :--- | :--- | :---: |
| 1 | `data/processed/population_forecast_2050.csv` | Dự báo dân số & 65+ (ML + UN WPP) | 29,625 |
| 2 | `data/processed/model_vs_un_wpp_comparison_2050.csv` | Bảng so sánh định lượng ML vs UN | 5,688 |
| 3 | `data/processed/country_risk_classification_2050.csv` | Điểm rủi ro suy giảm & siêu già | 237 |
| 4 | `reports/modeling/confusion_matrix.png` | Ma trận nhầm lẫn 2 mô hình Logistic | – |
| 5 | `reports/modeling/forecast_trends_2050.png` | Đồ thị xu hướng dự phóng 1950–2050 | – |
| 6 | `reports/modeling/forecast_comparison_ageing.png` | So sánh ML vs UN về tỷ lệ già hoá | – |

### 7.2 Nguồn Dữ liệu OWID Sử dụng cho Mô hình

| Chỉ số | URL OWID | Vai trò trong Mô hình |
| :--- | :--- | :--- |
| Population | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | Biến mục tiêu (Linear Regression) |
| Age groups (65+) | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) | Biến mục tiêu (Linear Regression) + Dẫn xuất Share 65+ |
| Growth rate | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | Đặc trưng (Logistic 2A) |
| TFR | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) | Đặc trưng (Logistic 2A + 2B) |
| Median age | [Median Age](https://ourworldindata.org/grapher/median-age) | Đặc trưng (Logistic 2A + 2B) |
| Life expectancy | [Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) | Đặc trưng (Logistic 2B) |

---

*Xem đặc tả Dashboard Tableau tại [`docs/tableau-dashboard-spec.md`](../../docs/tableau-dashboard-spec.md).*
