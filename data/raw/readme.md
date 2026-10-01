# Dữ liệu Thô (Raw Data) – Nguồn gốc & Hướng dẫn

> **Cập nhật**: 2026-09-26 | **Phiên bản dữ liệu**: UN WPP 2024 Revision (Interim Update 2026-01-19)

---

## 1. Tổng quan

Thư mục này chứa **6 bộ dữ liệu chính** tải từ [Our World in Data (OWID)](https://ourworldindata.org/) và **1 bộ dữ liệu kiểm chứng** từ [World Population Review (WPR)](https://worldpopulationreview.com/).

Mỗi file CSV đi kèm một file `.metadata.json` chứa thông tin trích dẫn, mô tả chỉ số, và cách OWID xử lý dữ liệu.

---

## 2. Bảng Ánh xạ: File CSV → Chỉ số → URL OWID → Chart Tableau

| # | File CSV | Chỉ số (Indicator) | Kích thước | URL Nguồn OWID | Chart Tableau sử dụng |
| :---: | :--- | :--- | :---: | :--- | :--- |
| **1** | `population-with-un-projections.csv` | Population (1950–2100) | 1.1 MB | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | Dashboard 1 (Map, Bar, Line), Dashboard 2 (Area), KPI 1 |
| **2** | `population-growth-rates.csv` | Population growth rate (1950–2100) | 1.0 MB | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | Dashboard 2 (Dual-Axis OWID line), KPI 2 |
| **3** | `children-born-per-woman.csv` | Total fertility rate (1950–2023) | 510 KB | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) | Dashboard 3 (TFR vs LE, TFR vs Median Age), KPI 4 |
| **4** | `median-age.csv` | Median age (1950–2100) | 1.0 MB | [Median Age](https://ourworldindata.org/grapher/median-age) | Dashboard 3 (Median Age vs TFR / Growth Rate) |
| **5** | `life-expectancy.csv` | Life expectancy at birth (1950–2023) | 605 KB | [Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) | Dashboard 3 (Gapminder Bubble Chart), ML Features |
| **6** | `population-young-working-elderly-with-projections.csv` | 3 Age groups: <15, 15-64, 65+ (1950–2100) | 1.8 MB | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) | Dashboard 2 (Stacked Area), Dashboard 4 (Support Ratio) |
| **7** | `world-population-review-2024-2026.csv` | Population (2024–2026) – Kiểm chứng chéo | 69 KB | [World Population Review](https://worldpopulationreview.com/) | Đối chiếu chéo với UN WPP |
| **8** | `natural-population-growth.csv` | Natural population growth rate (1950–2100) | 1.1 MB | [Natural Population Growth](https://ourworldindata.org/grapher/natural-population-growth) | Dashboard 3 (Natural growth vs Median Age) |
| **9** | `births-and-deaths-projected-to-2100.csv` | Births & Deaths (1950–2100) | 1.4 MB | [Births and Deaths](https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100) | Dashboard 3 (Cặp kéo Sinh - Tử / Demographic Scissors) |
| **10** | `population-by-five-year-age-group.csv` | Population by 5-year age groups (1950–2023) | 2.9 MB | [Population by Age Group](https://ourworldindata.org/grapher/population-by-five-year-age-group) | Dashboard 2 (Tháp tuổi 5 năm / Population Pyramid) |
| **11** | `gdp-per-capita-worldbank.csv` | GDP per capita PPP (1990–2025) | 277 KB | [GDP per Capita](https://ourworldindata.org/grapher/gdp-per-capita-worldbank) | Dashboard 4 (Ma trận Già trước khi giàu / 4-Quadrant) |

---

## 3. Cách Tải Dữ liệu từ Our World in Data

1. Truy cập URL nguồn OWID (cột "URL Nguồn OWID" ở bảng trên).
2. Bấm biểu tượng **↓ Download** ở góc dưới phải biểu đồ.
3. Chọn **"Full data (CSV)"** để tải toàn bộ chuỗi dữ liệu.
4. File `.csv` và `.metadata.json` sẽ được tải về cùng nhau.
5. Đặt vào thư mục `data/raw/`.

> **Lưu ý**: File CSV có Active Filters = None (tải toàn bộ, không lọc trước).

---

## 4. Cấu trúc CSV Chung (do OWID quy chuẩn)

Mỗi dòng là một quan sát cho một thực thể (quốc gia hoặc vùng) tại một thời điểm:

| Cột | Mô tả |
| :--- | :--- |
| `Entity` | Tên quốc gia/vùng lãnh thổ (VD: "Vietnam", "United States") |
| `Code` | Mã ISO alpha-3 (VD: "VNM", "USA"). Các thực thể lịch sử/đặc biệt có mã riêng OWID |
| `Year` | Năm quan sát (số nguyên) |
| *(Cột dữ liệu)* | Giá trị chỉ số – tên cột khác nhau tuỳ file |

---

## 5. Trích dẫn Nguồn Gốc (Citation)

### Nguồn chính: United Nations
```
United Nations, Department of Economic and Social Affairs, Population Division (2024).
World Population Prospects 2024, Online Edition.
- Published: 2024-07-11
- Interim Update: 2026-01-19 (cập nhật Togo)
- Retrieved: 2026-03-31
- Source: https://population.un.org/wpp/downloads/
- License: CC BY 3.0 IGO
```

### Biên tập & Phân phối: Our World in Data
```
Our World in Data – processed by Our World in Data
- Website: https://ourworldindata.org/
- ETL Pipeline: https://docs.owid.io/projects/etl/
```

### Kiểm chứng chéo: World Population Review
```
World Population Review – Live Population Clock
- Website: https://worldpopulationreview.com/
- Thu thập bởi: scripts/crawl_world_population_review.py
```

---

## 6. Lưu ý Phiên bản & Cập nhật

- **Phiên bản hiện tại**: UN WPP 2024 Revision (Published 2024-07-11), với Interim Update 2026-01-19 chỉ cập nhật Togo.
- **Lần cập nhật tiếp theo dự kiến**: **July 2027** (UN WPP 2026 Revision).
- Dữ liệu OWID được cập nhật tự động khi UN phát hành bản sửa đổi mới.
- Khi tải lại dữ liệu, cần chạy lại toàn bộ pipeline: `preprocess → run_eda → forecast_population`.

---

*Xem chi tiết nguồn dữ liệu & phương pháp luận tại [`docs/data-sources-and-phases.md`](../../docs/data-sources-and-phases.md).*