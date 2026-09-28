# Báo cáo Phân tích Khám phá Dữ liệu (EDA): Biến động Dân số & Xu hướng Già hoá Toàn cầu đến năm 2050

> **Cập nhật**: 2026-09-26 | **Script**: `scripts/run_eda.py` | **Nguồn dữ liệu**: UN WPP 2024 via [Our World in Data](https://ourworldindata.org/)

---

## 1. Trụ cột 1: Biến động Quy mô & Tăng trưởng Dân số Toàn cầu (1950 – 2050)

* **Quy mô dân số mốc hiện tại (2026)**: Đạt xấp xỉ **8,300,678,396 người (~8.30 tỷ người)**.
* **Dự báo dân số đến năm 2050 (UN WPP Medium Scenario)**: Đạt xấp xỉ **9,664,378,585 người (~9.66 tỷ người)**.
* **Đỉnh tăng trưởng**: Tốc độ tăng trưởng hàng năm đạt đỉnh vào thập niên 1960 (~2.1%/năm) và liên tục giảm dần, dự kiến chỉ còn dưới 0.4%/năm vào năm 2050.
* **Phân hoá tăng trưởng năm 2026**:
  - Đã có **65 quốc gia/vùng lãnh thổ** ghi nhận mức tăng trưởng âm (suy giảm dân số), chủ yếu tập trung tại Đông Á (Hàn Quốc, Nhật Bản, Trung Quốc) và Đông/Nam Âu.
  - Còn **172 quốc gia/vùng lãnh thổ** duy trì tăng trưởng dương, dẫn đầu bởi các nước Châu Phi cận Sahara.
* **Top 10 quốc gia đông dân nhất 2026**:
  1. Ấn Độ (1,476.6M) – chính thức vượt Trung Quốc
  2. Trung Quốc (1,412.9M)
  3. Hoa Kỳ (349.0M)
  4. Indonesia (287.9M)
  5. Pakistan (259.3M)

---

## 2. Trụ cột 2: Xu hướng Già hoá Dân số Toàn diện đến Năm 2050

* **Tỷ lệ người cao tuổi (65+ tuổi) tăng gấp 3 lần**:
  - Năm 1950: Chỉ chiếm **5.1%** dân số toàn cầu.
  - Năm 2026: Đã tăng lên **10.6%** (vượt ngưỡng xã hội già hoá 7%).
  - Đến năm 2050: Dự báo đạt **16.3%** dân số toàn cầu (chính thức bước vào ngưỡng Xã hội Già theo chuẩn LHQ >= 14%).
* **Tuổi trung vị toàn cầu (Median Age)**:
  - Năm 1950: **22.2 tuổi**.
  - Năm 2026: **31.1 tuổi**.
  - Năm 2050: **36.1 tuổi** (các khu vực như Châu Âu và Đông Á tuổi trung vị sẽ vượt ngưỡng 45-48 tuổi).
* **Tỷ số phụ thuộc người cao tuổi (Old-age Dependency Ratio)**:
  - Tăng từ **8.4%** (1950) lên **16.2%** (2026) và dự kiến đạt **25.8%** vào năm 2050.
  - Nghĩa là vào năm 2050, cứ khoảng 4 người trong độ tuổi lao động sẽ phải gánh hơn 1 người cao tuổi, tạo áp lực khổng lồ lên an sinh xã hội và y tế.
* **Làn sóng các Xã hội Siêu già (Super-aged Society – Tỷ lệ 65+ >= 20%)**:
  - Đến năm 2050, hơn **60 quốc gia** sẽ trở thành xã hội siêu già. Những nước đứng đầu bao gồm Hàn Quốc, Nhật Bản, Ý, Tây Ban Nha, Hồng Kông với tỷ lệ 65+ dự kiến vượt ngưỡng **35% – 40%**.

---

## 3. Danh mục 8 Biểu đồ EDA & Nguồn Dữ liệu OWID Tương ứng

| # | File Biểu đồ | Nội dung | Chỉ số (Indicator) | Nguồn OWID |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `01-global-population-trend.png` | Xu hướng Quy mô Dân số Toàn cầu (1950–2050) | `Population` | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) |
| 2 | `02-top-populations.png` | Top 10 Quốc gia Đông dân nhất 2026 | `Population` | *(cùng nguồn #1)* |
| 3 | `03-growth-rate-distribution.png` | Phân phối Tốc độ Tăng trưởng 2026 | `Population growth rate` | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) |
| 4 | `04-fertility-growth-scatter.png` | Tương quan TFR & Tăng trưởng | `TFR` + `Growth rate` | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) + [Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) |
| 5 | `05-population-heatmap.png` | Ma trận Quy mô top 15 qua Thập kỷ | `Population` | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) |
| 6 | `06-global-ageing-trend-2050.png` | Chuyển dịch 3 Khối Tuổi (1950–2050) | `Children <15`, `Working 15-64`, `Older 65+` | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) |
| 7 | `07-median-age-by-continent.png` | Tuổi Trung vị theo Khu vực đến 2050 | `Median age` | [Median Age](https://ourworldindata.org/grapher/median-age) |
| 8 | `08-top-super-aged-societies-2050.png` | Top 10 Quốc gia Già nhất 2050 (65+) | `Share of population aged 65+` | [Age Structure](https://ourworldindata.org/age-structure) |

---

*Xem chi tiết đặc tả Dashboard Tableau tại [`docs/tableau-dashboard-spec.md`](../../docs/tableau-dashboard-spec.md).*
