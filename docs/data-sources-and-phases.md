# Tài liệu Nguồn Dữ liệu & Phương pháp Luận (Data Sources & Methodology)

> **Cập nhật lần cuối**: 2026-09-26 | **Phiên bản dữ liệu**: UN WPP 2024 Revision (Interim Update 2026-01-19)

Tài liệu này lưu trữ đầy đủ đường dẫn nguồn gốc (URLs), đơn vị phát hành, phương pháp thu thập và mô tả chi tiết của từng chỉ số phục vụ cho việc trích dẫn trong Báo cáo Đồ án Cuối kỳ.

---

## 1. Nguồn Dữ liệu Chính: UN World Population Prospects (Biên tập bởi Our World in Data)

Tất cả các chuỗi dữ liệu lịch sử (1950 – 2023) và dự phóng kịch bản trung bình (2024 – 2100) đều được thu thập từ Ban Dân số Liên Hợp Quốc (**United Nations Population Division - UN WPP 2024 Revision**) thông qua hệ thống phân phối của **Our World in Data (OWID)**.

### 1.1 Bảng Chỉ số & Nguồn Gốc Chi tiết

| STT | Chỉ số (Indicator) | Đơn vị | Chu kỳ | File CSV thô | URL Nguồn OWID | Chart Tableau sử dụng |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- |
| **1** | **Quy mô Dân số**<br>`Population` | người | 1950–2100 | `population-with-un-projections.csv` (1.1 MB) | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | **Chart 1** (Filled Map), **Chart 2** (Scatter - Size), **Chart 3** (Bar), **Chart 4** (Area+Line), **Chart 5** (Bump), **KPI 1** |
| **2** | **Tốc độ Tăng trưởng Dân số**<br>`Population growth rate` | % | 1950–2100 | `population-growth-rates.csv` (1.0 MB) | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | **Chart 6** (Histogram), **Chart 7** (Scatter - trục Y), **KPI 2** |
| **3** | **Mức sinh Tổng cộng (TFR)**<br>`Total fertility rate` | con/phụ nữ | 1950–2100 | `fertility-rate-with-projections.csv` (1.1 MB) *(Cập nhật UN WPP 2024)* | [Fertility Rate with Projections](https://ourworldindata.org/grapher/fertility-rate-with-projections) | **Dashboard 3** (TFR 6 Châu lục vs 2.1), Đặc trưng ML |
| **4** | **Tuổi Trung vị**<br>`Median age` | tuổi | 1950–2100 | `median-age.csv` (1.0 MB) | [Median Age](https://ourworldindata.org/grapher/median-age) | **Dashboard 3** (Scatter plots), Đặc trưng ML |
| **5** | **Tuổi thọ Trung bình khi sinh**<br>`Life expectancy` | tuổi | 1950–2050 | `life-expectancy.csv` (605 KB + ngoại suy 2024-2050) | [Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) | **Dashboard 3** (Tuổi thọ vs Mức sinh), Đặc trưng Logistic Regression |
| **6** | **Cơ cấu 3 Nhóm Tuổi**<br>`Older (65+)`, `Working (15-64)`, `Children (<15)` | người | 1950–2100 | `population-young-working-elderly-with-projections.csv` (1.8 MB) | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) | **Dashboard 2** (100% Stacked Area), **Dashboard 4/5** (Support Ratio) |
| **7** | **Tỷ lệ Người cao tuổi 65+**<br>`Share of population aged 65+` | % | *(dẫn xuất)* | *(Tính: 65+ / Population × 100)* | [Age Structure](https://ourworldindata.org/age-structure) | **Dashboard 2**, **Dashboard 4/5**, phân cấp Ageing Stage |
| **8** | **Tỷ số Phụ thuộc Người già**<br>`Old-age dependency ratio` | % | *(dẫn xuất)* | *(Tính: 65+ / 15-64 × 100)* | [Dependency Ratios](https://ourworldindata.org/grapher/age-dependency-ratio-projected-to-2100) | Phân tích EDA, đặc trưng Logistic Regression |

### 1.2 Ghi chú Phương pháp cho Từng Chỉ số OWID

| Chỉ số | Phương pháp Thu thập & Xử lý bởi OWID |
| :--- | :--- |
| **Population** | Đo lường vào ngày 1/7 hàng năm theo biên giới hiện đại. Giai đoạn 2024–2100 theo UN Medium Scenario. OWID tổng hợp dân số theo nhóm tuổi đơn lẻ thành các khối lớn hơn. |
| **Growth rate** | Tỷ lệ gia tăng hàng năm kết hợp giữa mức tăng tự nhiên (sinh − tử) và di cư ròng. |
| **TFR** | Số con trung bình một phụ nữ sẽ sinh trong độ tuổi sinh đẻ. Ngưỡng thay thế chuẩn = 2.1. |
| **Median age** | Tuổi chia đôi dân số thành hai nửa bằng nhau. Thước đo tổng hợp trực quan nhất về già hoá. |
| **Life expectancy** | Số năm trung bình một đứa trẻ sơ sinh kỳ vọng sống nếu mức tử vong theo tuổi giữ nguyên suốt đời. |
| **Age groups** | Phân tách chuẩn mực LHQ: Dưới 15 tuổi, Độ tuổi lao động (15–64), Người cao tuổi (65+). Tổng hợp châu lục bởi OWID có thể lệch nhẹ so với UN do khác biệt nhóm quốc gia. |

### 1.3 Trích dẫn Chuẩn (Citation)

```
United Nations, Department of Economic and Social Affairs, Population Division (2024).
World Population Prospects 2024, Online Edition.
- Phiên bản chính: Published 2024-07-11
- Interim Update (Togo): Published 2026-01-19, Retrieved 2026-03-31
- Giấy phép: CC BY 3.0 IGO
- Nguồn gốc: https://population.un.org/wpp/downloads/
- Biên tập & Phân phối: Our World in Data (https://ourworldindata.org/)
```

---

## 2. Nguồn Kiểm chứng Chéo Độc lập: World Population Review (WPR)

| Thông tin | Giá trị |
| :--- | :--- |
| **Tên tệp thô** | `data/raw/world-population-review-2024-2026.csv` (69 KB) |
| **Nhà cung cấp** | [World Population Review (Live Population Clock)](https://worldpopulationreview.com/) |
| **Phương pháp thu thập** | Script tự động `scripts/crawl_world_population_review.py` |
| **Khung thời gian** | 2024 – 2026 |
| **Mục đích** | Nguồn độc lập đối chiếu, kiểm chứng chéo (Cross-validation) với dự báo UN WPP giai đoạn hiện tại |
| **Kết quả đối chiếu** | **100%** bản ghi (705/705 dòng) khớp hoàn hảo sau chuẩn hoá Alias Mapping. Độ lệch tương đối < **0.05%** |
| **Tệp kết quả** | `data/processed/world_population_review_validation.csv` (705 dòng) |

---

## 3. Ánh xạ Chi tiết: Chart Tableau ↔ Nguồn OWID ↔ Chỉ số

Bảng dưới đây liệt kê cụ thể **mỗi chart trên Tableau** tham khảo chart nào trên Our World in Data và sử dụng chỉ số gì:

| Chart # | Tên Chart Tableau | Loại Biểu đồ | Tham khảo Chart OWID | Chỉ số Sử dụng | Bảng Dữ liệu Tableau |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | Bản đồ Dân số Thế giới | Filled Map (Choropleth) | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | `Population` | `population_fact_wide.csv` |
| **2** | Chuyển đổi Nhân khẩu học | Animated Scatter Plot | [Fertility vs Life Expectancy](https://ourworldindata.org/grapher/fertility-rate-vs-life-expectancy) *(Hans Rosling)* | `Life expectancy` (X) + `TFR` (Y) + `Population` (Size) | `population_fact_wide.csv` |
| **3** | Top 10 Nước Đông dân | Horizontal Bar | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) – Chọn tab Table/Ranking | `Population` | `population_fact_wide.csv` |
| **4** | Xu hướng Dân số 1950–2050 | Area + Line | [World Population over Time](https://ourworldindata.org/grapher/population-with-un-projections?tab=chart&time=1950..2100&country=~OWID_WRL) | `Population` | `population_fact_wide.csv` |
| **5** | Đổi ngôi Thứ hạng Dân số | Bump Chart (Rank Line) | *(Tham khảo bài viết [Population Growth](https://ourworldindata.org/population-growth) – biểu đồ rank qua thời gian)* | `Population` (Rank) | `population_fact_wide.csv` |
| **6** | Phân phối Tốc độ Tăng trưởng | Histogram | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) – Chọn Tab: Distribution | `Population growth rate` | `population_fact_wide.csv` |
| **7** | Mức sinh TFR vs Tăng trưởng | Scatter Plot (Bubbles) | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) + [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | `TFR` (trục X) + `Growth Rate` (trục Y) + `Population` (Size) | `population_fact_wide.csv` |
| **8** | Chuyển dịch 3 Khối Tuổi | 100% Stacked Area | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) – Chọn Relative mode | `Children <15`, `Working 15-64`, `Older 65+` | `population_fact_wide.csv` |
| **9** | Ma trận Già hoá Thập kỷ | Heatmap / Highlight Table | [Age Structure](https://ourworldindata.org/age-structure) + [Median Age](https://ourworldindata.org/grapher/median-age) | `Share 65+` hoặc `Median Age` | `population_fact_wide.csv` |
| **10** | So sánh Dự báo ML vs UN | Dual-Axis Line | *(Biểu đồ riêng – đối chiếu ML tự xây dựng với UN WPP)* | `Share_65plus`, `Population` | `population_forecast_2050.csv` + `model_vs_un_wpp_comparison_2050.csv` |

---

## 4. Quy trình Tải Dữ liệu từ Our World in Data

### 4.1 Cách tải từng file CSV từ OWID

Mỗi biểu đồ trên Our World in Data đều có nút **Download** ở góc dưới phải:

1. Truy cập URL nguồn OWID (xem bảng mục 1.1).
2. Bấm biểu tượng **↓ Download** ở góc dưới phải biểu đồ.
3. Chọn **"Full data (CSV)"** để tải toàn bộ chuỗi dữ liệu 1950–2100.
4. File CSV và file `.metadata.json` sẽ được tải về cùng nhau.
5. Đặt vào thư mục `data/raw/`.

### 4.2 Lưu ý Về Phiên bản Dữ liệu

- Dữ liệu OWID được cập nhật tự động khi UN phát hành bản sửa đổi mới.
- Phiên bản hiện tại: **UN WPP 2024 Revision** (Published 2024-07-11), với **Interim Update** (2026-01-19) chỉ cập nhật Togo.
- Lần cập nhật tiếp theo dự kiến: **July 2027** (UN WPP 2026 Revision).

---

## 5. Quy chuẩn Thiết kế Dữ liệu trong Tableau (Data Design Principles)

### 5.1 Tối ưu hoá Hiệu năng & Dung lượng
- Các trường tĩnh lặp lại (`Source`, `SourceUrl`) đã được **lược bỏ hoàn toàn** khỏi Fact Table để giảm hơn **58%** kích thước tệp (từ 55MB xuống còn **23MB**), loại bỏ chiều phân loại rác.
- Toàn bộ nguồn gốc, đường dẫn và tài liệu tham khảo được quy chuẩn hoá tập trung trong tài liệu này.
- Fact table `population_fact_long.csv` chỉ còn đúng **7 cột chuẩn**: `Entity`, `Code`, `Year`, `Indicator`, `Value`, `Unit`, `DataStatus`.

### 5.2 Phân tách Rạch ròi Trạng thái Dữ liệu (`DataStatus`)

| Giá trị | Ý nghĩa | Giai đoạn | Nguồn |
| :--- | :--- | :--- | :--- |
| `estimate` | Dữ liệu điều tra thống kê lịch sử | 1950 – 2023 | UN WPP (Estimates) |
| `projected` | Dữ liệu viễn cảnh kịch bản chuẩn LHQ | 2024 – 2100 | UN WPP (Medium Scenario) |
| `forecast` | Dữ liệu dự báo của Mô hình ML tự xây dựng | 2027 – 2050 | Linear Regression (nhóm) |

### 5.3 Mã hoá Định danh Quốc tế
- Sử dụng mã tiêu chuẩn **ISO 3166-1 alpha-3** (`Code`) để Tableau tự động nhận diện vai trò địa lý (Geographic Role: Country/Region) và vẽ bản đồ thế giới mà không xảy ra xung đột tên gọi.
- `OWID_WRL` = Tổng thế giới (World), dùng riêng cho các biểu đồ xu hướng toàn cầu.
- Calculated Field `[Is Country]` loại bỏ các thực thể vùng/châu lục khi xếp hạng quốc gia.

---

## 6. 10 Chỉ số Cốt lõi trong Fact Table

| # | Indicator (giá trị cột `Indicator`) | Đơn vị (cột `Unit`) | Nguồn Gốc OWID |
| :---: | :--- | :--- | :--- |
| 1 | `Population` | people | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) |
| 2 | `Population growth rate` | % | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) |
| 3 | `Total fertility rate` | children per woman | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) |
| 4 | `Median age` | years | [Median Age](https://ourworldindata.org/grapher/median-age) |
| 5 | `Life expectancy` | years | [Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) |
| 6 | `Older people (65+ years)` | people | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) |
| 7 | `Working-age adults (15-64 years)` | people | *(cùng nguồn #6)* |
| 8 | `Children (under-15s)` | people | *(cùng nguồn #6)* |
| 9 | `Share of population aged 65+` | % | Dẫn xuất từ #6 / #1 × 100 |
| 10 | `Old-age dependency ratio` | % | Dẫn xuất từ #6 / #7 × 100 |

---

*Tài liệu này phục vụ trích dẫn nguồn và phương pháp luận trong Báo cáo Đồ án Cuối kỳ. Phiên bản: 2026-09-26.*
