# Đặc tả Dashboard Tableau: Biến động Dân số & Xu hướng Già hoá Dân số Toàn cầu (1950 – 2050)

> **Cập nhật lần cuối**: 2026-09-26 | **Phiên bản**: v2.0 | **Workbook**: `TTDLTQ FINAL.twb`

## 1. Tổng quan & Câu chuyện Dữ liệu (Data Story)

### 1.1 Mục tiêu Dashboard
Dashboard kết hợp hài hòa hai chủ đề cốt lõi:
1. **Biến động Dân số Toàn cầu**: Quy mô dân số, tốc độ tăng trưởng, mức sinh TFR qua 3 chương lịch sử - hiện tại - tương lai.
2. **Xu hướng Già hoá Dân số**: Tốc độ chuyển dịch cơ cấu tuổi, tuổi trung vị, tỷ số phụ thuộc và làn sóng các xã hội siêu già đến năm 2050.

| Chương | Thời kỳ | Câu chuyện chính |
| :---: | :--- | :--- |
| **Chương 1** | 1950 – 2023 | *"Thế kỷ bùng nổ dân số & Mở màn già hóa"* – Dân số tăng 3.2 lần (từ 2.5 tỷ lên 8.09 tỷ), tuổi thọ tăng, mức sinh bắt đầu giảm |
| **Chương 2** | 2023 | *"Bước ngoặt hiện tại"* – Dân số vượt 8.09 tỷ, Ấn Độ chính thức vượt Trung Quốc, 54 quốc gia suy giảm, tỷ lệ 65+ chạm 10% |
| **Chương 3** | 2024 – 2050 | *"Tương lai phân hóa & Làn sóng Siêu già"* – Thế giới bước vào ngưỡng Xã hội Già (16.3%), >60 nước siêu già |

### 1.2 Thông điệp chính (Key Insights)
1. **8.09 tỷ người** (2023) → Dự kiến đạt đỉnh **~10.3 tỷ** vào năm 2084 rồi giảm dần.
2. **Ấn Độ** chính thức vượt **Trung Quốc** thành quốc gia đông dân nhất thế giới (2023).
3. **54 quốc gia** đang trong chu kỳ suy giảm dân số tính đến năm 2023.
4. **130/237** quốc gia có tỷ suất sinh dưới mức thay thế (TFR < 2.1).
5. **Già hoá tăng tốc**: Tỷ lệ người cao tuổi (65+) tăng từ 5.1% (1950) lên 10.0% (2023) và đạt **16.3% vào năm 2050**.
6. **Tuổi trung vị toàn cầu**: Tăng từ 22.2 tuổi (1950) lên **30.4 tuổi (2023)** và **36.1 tuổi (2050)** (Châu Âu và Đông Á vượt 45-48 tuổi).

### 1.3 Ánh xạ Chi tiết: Chart Tableau ↔ Nguồn Our World in Data

Bảng dưới đây liệt kê cụ thể **mỗi chart trên Tableau Dashboard** tham khảo chart nào trên Our World in Data, sử dụng chỉ số và bảng dữ liệu gì:

| Chart # | Tên Chart | Loại Biểu đồ | Chart/Bài viết OWID Tham khảo | Chỉ số (Indicator) | File Dữ liệu Tableau |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | Bản đồ Dân số | Filled Map | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | `Population` | `population_fact_wide.csv` |
| **2** | Chuyển đổi Nhân khẩu học | Animated Scatter Plot | [Life Expectancy vs Fertility](https://ourworldindata.org/grapher/fertility-rate-vs-life-expectancy) *(Gapminder / Hans Rosling style)* | `Life expectancy` (X) + `TFR` (Y) + `Population` (Size) | `population_fact_wide.csv` |
| **3** | Top 10 Đông dân | Horizontal Bar | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) → Tab Table | `Population` | `population_fact_wide.csv` |
| **4** | Xu hướng 1950–2050 | Area + Line | [World Population over Time](https://ourworldindata.org/grapher/population-with-un-projections?tab=chart&time=1950..2100&country=~OWID_WRL) | `Population` | `population_fact_wide.csv` |
| **5** | Đổi ngôi Thứ hạng | Bump Chart | [Population Growth](https://ourworldindata.org/population-growth) *(bài viết rank qua thời gian)* | `Population` (Rank) | `population_fact_wide.csv` |
| **6** | Phân phối Tăng trưởng | Histogram | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) → Distribution | `Population growth rate` | `population_fact_wide.csv` |
| **7** | TFR vs Tăng trưởng | Scatter Plot | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) + [Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | `TFR` (X) + `Growth Rate` (Y) + `Population` (Size) | `population_fact_wide.csv` |
| **8** | 3 Khối Tuổi | 100% Stacked Area | [Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) → Relative | `Children <15`, `Working 15-64`, `Older 65+` | `population_fact_wide.csv` |
| **9** | Ma trận Già hoá | Heatmap | [Age Structure](https://ourworldindata.org/age-structure) + [Median Age](https://ourworldindata.org/grapher/median-age) | `Share 65+` hoặc `Median Age` | `population_fact_wide.csv` |
| **10** | ML vs UN WPP | Dual-Axis Line | *(Biểu đồ riêng – đối chiếu kết quả ML với UN WPP)* | `Share_65plus`, `Population` | `population_forecast_2050.csv` + `model_vs_un_wpp_comparison_2050.csv` |
| **KPI 1** | Quy mô Dân số | KPI Card | [Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | `Population` | `population_fact_wide.csv` |
| **KPI 2** | Tốc độ Tăng trưởng | KPI Card | [Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | `Population growth rate` | `population_fact_wide.csv` |
| **KPI 3** | Tỷ lệ Người già 65+ | KPI Card | [Age Structure](https://ourworldindata.org/age-structure) | `Share of population aged 65+` | `population_fact_wide.csv` |
| **KPI 4** | Mức sinh TFR | KPI Card | [Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) | `Total fertility rate` | `population_fact_wide.csv` |

> **Cách sử dụng bảng này**: Khi cần truy xuất hoặc trích dẫn nguồn cho bất kỳ chart nào trong Dashboard, tra cứu cột "Chart/Bài viết OWID Tham khảo" để lấy URL gốc và phương pháp luận.

---

## 2. Nguồn Dữ liệu & Cấu trúc

### 2.1 Bảng dữ liệu chính

| # | Tên file | Vai trò | Hàng | Cột chính | Dùng cho |
| :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | **`population_fact_wide.csv`** | **⭐ Data source chính cho cả 5 Dashboard** (1950–2050) | **27,880** | Entity, Code, Continent, Region_Type, Year, Population, GrowthRate, NaturalGrowthRate, TFR, MedianAge, LifeExpectancy, Births, Deaths, Share65, DepRatio, PotentialSupportRatio, GDP_per_capita | **Dashboard 1–5 (Bản đồ, Top 10, Dual-Axis, Scatter, Ma trận)** |
| 2 | **`population_by_5yr_age_group.csv`** | Tháp tuổi chi tiết theo nhóm 5 tuổi (1950–2050) | **407,190** | Entity, Code, Continent, Region_Type, Year, Age_Group, Age_Order, Population | **Dashboard 2 (Population Pyramid)** |
| 3 | **`ageing_transition_speed.csv`** | Đo lường số năm chuyển dịch già hóa 7% → 14% → 20% | **256** | Entity, Code, Continent, Year_Reached_7_Pct, Year_Reached_14_Pct, Year_Reached_20_Pct, Years_From_7_To_14, Years_From_14_To_20 | **Dashboard 4 (Dumbbell Chart)** |
| 4 | **`country_risk_classification_2050.csv`** | Phân loại rủi ro Logistic Regression (Suy giảm & Siêu già) | **237** | Entity, Code, Depopulation_Risk_Score, Depopulation_Category, Super_Aged_Risk_Score, Super_Aged_Category | **Dashboard 5 (Bản đồ phân loại rủi ro ML)** |
| 5 | **`population_forecast_2050.csv`** | Dự báo ML Linear Regression vs UN WPP (2024–2050) | **30,336** | Entity, Code, Year, Population, Older_People_65plus, Share_65plus, DataStatus, Model | **Dashboard 5 (Đối chiếu ML vs UN)** |
| 6 | `population_fact_long.csv` | File gốc định dạng long dùng cho pipeline Python | **359,833** | Entity, Code, Year, Indicator, Value, Unit, DataStatus | Dùng cho ETL / Machine Learning |

> **⚠️ Điểm nâng cấp vượt trội của bộ dữ liệu mới**:
> - Trường `[Region_Type]` và `[Continent]` đã được **tích hợp sẵn trực tiếp vào từng dòng**, người dùng Tableau không cần làm Data Blending hay viết hàm IF phức tạp để phân loại cấp bậc World / Continent / Country / Others.
> - Bổ sung các thước đo sinh tử mới từ UN WPP/OWID: `[Natural population growth rate]`, `[Births]`, `[Deaths]`, `[GDP per capita]`, `[Potential support ratio]`.

---

## 3. Calculated Fields (Trường tính toán)

### 3.1 Danh sách Calculated Fields Cốt lõi

> **Lưu ý**: Vì data source chính là file **`population_fact_wide.csv`** (mỗi dòng đã có sẵn các cột riêng), nên các Calculated Field đơn giản hơn (không cần `IF [Indicator] = ...`).

| # | Tên trường | Công thức Tableau (file wide) | Mục đích |
| :---: | :--- | :--- | :--- |
| 1 | `[Is Country]` | *(Xem mục 2.3)* | Lọc quốc gia vs khu vực |
| 2 | `[Population (Millions)]` | `[Population] / 1000000` | Hiển thị dân số theo triệu người |
| 3 | `[Population (Billions)]` | `[Population] / 1000000000` | Hiển thị dân số theo tỷ người |
| 4 | `[Growth Rate (%)]` | `[Population growth rate]` *(cột có sẵn)* | Tốc độ tăng trưởng hàng năm |
| 5 | `[TFR]` | `[Total fertility rate]` *(cột có sẵn)* | Mức sinh (con/phụ nữ) |
| 6 | `[LE]` | `[Life expectancy]` *(cột có sẵn)* | Tuổi thọ trung bình |
| 7 | `[Median Age]` | `[Median age]` *(cột có sẵn)* | Tuổi trung vị |
| 8 | `[Share 65+ (%)]` | `[Share of population aged 65+]` *(cột có sẵn)* | Tỷ lệ người cao tuổi |
| 9 | `[Old-age Dependency Ratio]` | `[Old-age dependency ratio]` *(cột có sẵn)* | Tỷ số phụ thuộc người cao tuổi |
| 10 | `[Ageing Stage]` | `IF [Share 65+ (%)] >= 20 THEN "4. Xã hội Siêu già (>=20%)" ELSEIF [Share 65+ (%)] >= 14 THEN "3. Xã hội Già (14-20%)" ELSEIF [Share 65+ (%)] >= 7 THEN "2. Đang già hoá (7-14%)" ELSE "1. Dân số trẻ (<7%)" END` | Phân cấp già hoá chuẩn UN |
| 11 | `[Data Period]` | `IF [DataStatus] = "estimate" THEN "Lịch sử (Ước tính)" ELSEIF [DataStatus] = "projected" THEN "Dự phóng (UN WPP)" ELSE "Dự báo (Mô hình)" END` | Phân loại giai đoạn cho Legend |
| 12 | `[Below Replacement]` | `IF [TFR] < 2.1 THEN "Dưới mức thay thế" ELSE "Trên mức thay thế" END` | Phân loại TFR |
| 13 | `[Continent]` | *Left Join với `continent_mapping.csv` trên Code* | Nhóm 6 châu lục |
| 14 | `[TFR Display]` | `IF [Year] <= 2023 THEN [Total fertility rate] ELSE { FIXED [Entity]: MAX(IF [Year] = 2023 THEN [Total fertility rate] END) } END` | TFR fallback cho KPI4 khi Year > 2023 |
| 15 | `[TFR Label]` | `IF [Year] <= 2023 THEN STR(ROUND([TFR], 2)) + " con/phụ nữ" ELSE STR(ROUND([TFR Display], 2)) + " (2023*)" END` | Nhãn KPI4 có chú thích khi dùng data cũ |
| 16 | `[LE Display]` | `IF [Year] <= 2023 THEN [Life expectancy] ELSE { FIXED [Entity]: MAX(IF [Year] = 2023 THEN [Life expectancy] END) } END` | Tuổi thọ fallback khi Year > 2023 |
| 17 | `[Share of World Pop (%)]` | `SUM([Population]) / SUM({ FIXED [Year]: SUM(IF [Entity] = "World" THEN [Population] END) }) * 100` | **LOD**: Tỷ trọng dân số so với toàn cầu |
| 18 | `[Ageing Diff from World (%)]` | `[Share of population aged 65+] - { FIXED [Year]: AVG(IF [Entity] = "World" THEN [Share of population aged 65+] END) }` | **LOD**: Độ lệch già hóa so với mức trung bình thế giới |

### 3.2 Các Biểu thức LOD Nâng cao (Level of Detail Expressions - FIXED)

> **💡 Điểm nhấn kỹ thuật nâng cao**: Trong Tableau, LOD cho phép tính toán các chỉ số vĩ mô (toàn cầu, châu lục) độc lập với bộ lọc trên màn hình, giúp thẻ KPI và các phân tích tương quan không bị gãy dữ liệu:
> 1. **LOD Fallback (`[TFR Display]`, `[LE Display]`)**: Dùng `{ FIXED [Entity]: MAX(...) }` để tự động lấy giá trị thực tế mới nhất (2023) khi người dùng kéo thanh trượt năm lên 2024–2050 (thay vì dùng Table Calculation `WINDOW_MAX` dễ bị lỗi `Null` trên thẻ KPI).
> 2. **LOD Tỷ trọng Thế giới (`[Share of World Pop (%)]`)**: Tính tỷ lệ % dân số của một quốc gia trên tổng dân số toàn cầu tại năm được chọn.
> 3. **LOD Độ lệch Già hóa (`[Ageing Diff from World (%)]`)**: Đánh giá một quốc gia đang già nhanh hơn hay chậm hơn mức trung bình toàn cầu bao nhiêu điểm phần trăm.

### 3.3 Phân cấp Địa lý & Drill-down (Geographic Hierarchy)

Tạo **Hierarchy** trong Tableau để hỗ trợ tính năng **Drill-down** tự nhiên:
1. Nhấp chuột phải vào trường `[Continent]` $\rightarrow$ **Hierarchy** $\rightarrow$ **Create Hierarchy...** $\rightarrow$ Đặt tên: `Địa lý (Geographic)`.
2. Kéo trường `[Entity]` và trường `[Code]` thả vào bên trong Hierarchy vừa tạo theo thứ tự phân cấp:
   `[Continent]` (Châu lục) $\rightarrow$ `[Entity]` (Quốc gia/Vùng) $\rightarrow$ `[Code]` (Mã ISO-3).
3. **Hiệu ứng Drill-down**: Khi kéo trường `[Continent]` vào bất kỳ biểu đồ nào, người dùng có thể bấm vào biểu tượng dấu cộng **`[+]`** trên tiêu đề để mở rộng từ 6 Châu lục xuống chi tiết 237 Quốc gia.

Tạo **Group** trong Tableau bằng cách:
1. Right-click cột `Entity` → Create → Group
2. Hoặc dùng Calculated Field dựa trên ISO Code:

```
// [Continent] - Gán dựa trên mã ISO-3
CASE LEFT([Code], 2)
  // Châu Á
  WHEN "AF" THEN "Châu Á"  // Afghanistan
  WHEN "CN" THEN "Châu Á"  // China
  WHEN "IN" THEN "Châu Á"  // India
  // ... (nên dùng Group thủ công hoặc reference table cho đầy đủ)
  ELSE "Khác"
END
```

> **Khuyến nghị**: Tạo file CSV bổ sung `continent_mapping.csv` với 2 cột `Code, Continent` rồi Left Join vào fact table trong Tableau.

---

## 4. Kiến trúc Triển khai: 2-Tab Dashboard lồng trong Tableau Story (Phương án B)

Để tối ưu hóa trải nghiệm thị giác (UI/UX), tránh quá tải thông tin mà vẫn đáp ứng hoàn hảo tiêu chí **đủ 10 loại biểu đồ khác biệt**, đồ án được triển khai theo **Phương án B: Chia thành 2 Dashboards chuyên đề (mỗi Dashboard đúng 5 biểu đồ + Thẻ KPI) và kết nối qua Tableau Story**:

```
                                ┌────────────────────────────────────────────────────────┐
                                │             TABLEAU STORY (BỘ TRUYỆN DỮ LIỆU)          │
                                │  [Story 1: Quy mô & Tiến trình]  [Story 2: Già hóa & ML 2050]   │
                                └───────────────────────────┬────────────────────────────┘
                                                            │
                 ┌──────────────────────────────────────────┴──────────────────────────────────────────┐
                 ▼                                                                                     ▼
┌─────────────────────────────────────────────────────────────────┐   ┌─────────────────────────────────────────────────────────────────┐
│ DASHBOARD 1: QUY MÔ & CHUYỂN DỊCH NHÂN KHẨU HỌC LỊCH SỬ         │   │ DASHBOARD 2: NGUYÊN NHÂN, KHỦNG HOẢNG GIÀ HÓA & DỰ BÁO ML 2050  │
│ [Bộ lọc Toàn cục: Entity (World) | Year (2023)]                 │   │ [Bộ lọc Toàn cục: Entity (World) | Year (2023)]                 │
├─────────────────────────────────────────────────────────────────┤   ├─────────────────────────────────────────────────────────────────┤
│ 4 Thẻ KPI: [Dân số]  [Tăng trưởng %]  [Tỷ lệ 65+]  [Mức sinh TFR]│   │ 4 Thẻ KPI: [Tỷ lệ 65+]  [Tuổi trung vị]  [Phụ thuộc già]  [TFR] │
├────────────────────────────────┬────────────────────────────────┤   ├────────────────────────────────┬────────────────────────────────┤
│ Chart 1: Filled Map (Bản đồ)   │ Chart 4: Area + Line (Xu hướng)│   │ Chart 6: Histogram (Phân phối) │ Chart 8: 100% Stacked Area     │
│ (Tích hợp Viz in Tooltip)      │ (Phân tách Lịch sử vs Dự phóng)│   │ (54 nước âm vs 183 nước dương) │ (3 Khối tuổi: Trẻ, Lao động, 65│
├────────────────────────────────┼────────────────────────────────┤   ├────────────────────────────────┼────────────────────────────────┤
│ Chart 2: Animated Scatter Plot │ Chart 5: Bump Chart            │   │ Chart 7: 4-Quadrant Scatter    │ Chart 9: Heatmap Ma trận Già   │
│ (Hans Rosling: Tuổi thọ vs TFR)│ (Đổi ngôi thứ hạng Top 7 nước) │   │ (TFR vs Tốc độ Tăng trưởng)    │ (Top 15 nước qua các thập kỷ)  │
├────────────────────────────────┴────────────────────────────────┤   ├────────────────────────────────┴────────────────────────────────┤
│ Chart 3: Horizontal Bar Chart (Top 10 Đông dân nhất)            │   │ Chart 10: Dual-Axis Line (So sánh Mô hình ML vs Chuẩn UN WPP)   │
└─────────────────────────────────────────────────────────────────┘   └─────────────────────────────────────────────────────────────────┘
```

---

### 🏛️ CỤM 1: QUY MÔ & PHÂN BỐ KHÔNG GIAN (Scale & Spatial Distribution)
* **Giá trị đặc trưng**: Độ lớn quy mô dân số và sự tập trung địa lý (Châu Á chiếm gần 60%, Top 10 quốc gia chiếm >55% dân số toàn cầu).

#### Chart 1: Bản đồ Địa lý – Dân số theo Quốc gia (Filled Map)
* **Loại biểu đồ**: Filled Map (Bản đồ địa lý thế giới Choropleth).
* **Fields**: Geographic dimension `[Code]` / `[Entity]`, Color: `SUM([Population (Millions)])`.
* **Màu sắc**: Sequential Palette (Xanh nhạt $\rightarrow$ Xanh navy sẫm).
* **Tính năng Drill-down**: Click vào bất kỳ quốc gia nào (ví dụ Việt Nam) $\rightarrow$ Tự động lọc tất cả biểu đồ còn lại trong Dashboard.

#### Chart 2: Chuyển đổi Nhân khẩu học – Tuổi thọ vs Mức sinh (Animated Scatter Plot)
* **Loại biểu đồ**: Animated Scatter Plot (Biểu đồ phân tán bong bóng có Animation theo thời gian – phong cách Hans Rosling / Gapminder).
* **Tham khảo OWID**: [Life Expectancy vs Fertility Rate](https://ourworldindata.org/grapher/fertility-rate-vs-life-expectancy)
* **Fields**:
  - Trục X: `[Life expectancy]` (Tuổi thọ trung bình – Continuous).
  - Trục Y: `[TFR]` (Tổng tỷ suất sinh – Continuous).
  - Size: `SUM([Population (Millions)])` (Kích thước bong bóng theo quy mô dân số).
  - Color: `[Continent]` (Phân nhóm theo châu lục).
  - Pages: `[Year]` (Trục animation cho phép bấm Play chạy từ 1950 → 2023).
  - Label: `[Entity]` (Chỉ hiện cho các mark đang được chọn).
  - Tooltip: `[Entity]`, `[Year]`, `[Life expectancy]`, `[TFR]`, `[Population (Millions)]`.
* **Reference Lines**:
  - Vạch ngang tại $TFR = 2.1$ (Ngưỡng sinh thay thế – dưới ngưỡng này dân số sẽ thu hẹp về dài hạn).
  - Vạch dọc tại $LE = 70$ tuổi (Ngưỡng tuổi thọ cao theo phân loại WHO).
* **Filters**: `[Is Country]` = `True` (chỉ quốc gia, bỏ khu vực); `[Year]` range 1950–2023 (data `Life expectancy` và `TFR` chỉ có đến 2023).
* **Ý nghĩa – Câu chuyện Chuyển đổi Nhân khẩu học (Demographic Transition)**:
  - **Năm 1950**: Gần như tất cả các nước co cụm ở **góc trái-trên** (tuổi thọ thấp ~45, sinh nhiều ~5–7 con) → *"Sinh nhiều, chết sớm"*.
  - **Chạy animation theo thập kỷ**: Các nước từ từ di chuyển sang **góc phải-dưới** (tuổi thọ tăng >70, mức sinh giảm <2.1) → *"Sinh ít, sống lâu"* = **Gốc rễ của Già hóa dân số**.
  - **Năm 2023**: Châu Phi (vùng lớn nhất còn lại ở góc trái-trên), Đông Á dẫn đầu đường chuyển đổi (TFR <1.2, LE >80 tuổi), ASEAN (Việt Nam) ở vùng chuyển tiếp.
  - Chart này giải đáp câu hỏi: *"Tại sao thế giới già đi?"* — Vì sự kết hợp đồng thời của tuổi thọ tăng + mức sinh giảm.
* **Indicators được khai thác**: ✅ `Life expectancy` (chưa dùng ở chart nào khác) + ✅ `TFR` (góc nhìn mới so với Chart 7) + ✅ `Population` (Size) + ✅ `Continent` (Color). Tổng cộng khai thác **3 indicators** trong đó 1 indicator hoàn toàn mới (`Life expectancy`).

#### Chart 3: Top 10 Quốc gia Đông dân nhất (Horizontal Bar Chart)
* **Loại biểu đồ**: Horizontal Bar Chart (Thanh ngang xếp hạng).
* **Fields**: Rows `[Entity]` (Top 10 by Population), Columns `SUM([Population (Millions)])`.
* **Màu sắc**: Màu nhấn `#2b5c8f`. Highlight riêng Ấn Độ (`#E94560`) và Trung Quốc (`#F5A623`).

---

### ⏳ CỤM 2: TIẾN TRÌNH & ĐỔI NGÔI LỊCH SỬ (Temporal Dynamics & Milestone Shifting)
* **Giá trị đặc trưng**: Thế kỷ bùng nổ dân số (tăng 3.2 lần từ 1950) nhưng đà tăng đang giảm dần về bão hòa; các cuộc đổi ngôi vị thế quyền lực nhân khẩu học.

#### Chart 4: Xu hướng Quy mô Dân số Toàn cầu 1950 – 2050 (Area + Line Chart)
* **Loại biểu đồ**: Area Chart kết hợp Line.
* **Fields**: Trục X `[Year]` (1950 – 2050), Trục Y `SUM([Population (Billions)])`.
* **Màu sắc**: Phân tách 2 vùng: Lịch sử (`estimate`, màu xanh teal `#4ECDC4`) và Dự phóng (`projected`, màu cam `#FF6B6B`).
* **Vạch chuẩn**: Vạch đứng mốc hiện tại năm 2023 (8.09 tỷ người) và chú thích đỉnh dân số ~10.3 tỷ vào năm 2084.

#### Chart 5: Hoán đổi Thứ hạng Dân số theo Thời gian (Bump Chart)
* **Loại biểu đồ**: Bump Chart (Line chart xếp hạng thứ bậc).
* **Fields**: Trục X `[Year]` (1950, 1970, 1990, 2010, 2023, 2040, 2050), Trục Y `RANK(SUM([Population]))` (đảo ngược trục: hạng 1 ở trên cùng).
* **Ý nghĩa**: Đường thứ hạng của Ấn Độ chính thức cắt lên trên Trung Quốc tại mốc 2023; Nigeria vượt Mỹ tiến lên top 3 trước năm 2050.

---

### ⚖️ CỤM 3: NGUYÊN NHÂN & PHÂN HÓA TĂNG TRƯỞNG (Demographic Drivers & Divergence)
* **Giá trị đặc trưng**: Tính phân cực (54 nước suy giảm vs 183 nước tăng) và mối quan hệ nhân quả gốc rễ từ mức sinh giảm sâu dưới ngưỡng thay thế ($TFR < 2.1$).

#### Chart 6: Phân phối Tốc độ Tăng trưởng Dân số (Histogram)
* **Loại biểu đồ**: Histogram (Tần số theo các bin 0.25%).
* **Fields**: Trục X `[Growth Rate (%)]`, Trục Y `COUNT([Entity])`.
* **Reference Line**: Vạch đỏ tại `0%` (Zero-growth threshold) tách biệt 54 nước thu hẹp dân số bên trái và 183 nước tăng trưởng bên phải.

#### Chart 7: Tương quan Mức sinh và Tốc độ Tăng trưởng (Scatter Plot - 4 Góc phần tư)
* **Loại biểu đồ**: Scatter Plot (Phân tán bong bóng có kích thước theo quy mô dân số).
* **Fields**: Trục X `[TFR]` (Mức sinh con/phụ nữ), Trục Y `[Growth Rate (%)]`, Bubble Size: `SUM([Population])`.
* **Đường tham chiếu**: Vạch dọc tại $TFR = 2.1$ (Mức sinh thay thế) và vạch ngang tại $Growth = 0\%$.
* **4 Góc phần tư**:
  1. *Góc trên bên phải*: Tăng trưởng cao & Mức sinh cao (Châu Phi cận Sahara).
  2. *Góc trên bên trái*: Vùng chuyển đổi (Việt Nam, Ấn Độ - TFR đã dưới 2.1 nhưng vẫn tăng nhẹ nhờ quán tính tuổi trẻ).
  3. *Góc dưới bên trái*: Bẫy suy giảm (Đông Á: Hàn Quốc, Nhật Bản, Trung Quốc; Nam/Đông Âu).
  4. *Góc dưới bên phải*: Bất thường / di cư.

---

### 👵 CỤM 4: CƠ CẤU TUỔI & DỰ BÁO GIÀ HOÁ ĐẾN 2050 (Ageing Transition & Predictive ML)
* **Giá trị đặc trưng**: Trọng tâm cốt lõi của đề tài – Sự già đi của dân số thế giới, tỷ lệ 65+ tăng gấp 3 lần và so sánh đối chiếu giữa Mô hình Học máy tự xây dựng với Kịch bản Chuẩn Liên Hợp Quốc.

#### Chart 8: Chuyển dịch Cơ cấu 3 Nhóm Tuổi 1950 – 2050 (100% Stacked Area Chart)
* **Loại biểu đồ**: 100% Stacked Area Chart (Miền xếp chồng 100%).
* **Fields**: Trục X `[Year]`, Trục Y `% of Total Population`.
* **3 Lớp màu sắc**:
  - Trẻ em (0–14 tuổi): Xanh lá `#76c893` (thu hẹp từ 35% xuống 20%).
  - Độ tuổi lao động (15–64 tuổi): Xanh navy `#1e6091` (đạt đỉnh bão hòa rồi giảm dần).
  - Người cao tuổi (65+ tuổi): Đỏ đậm `#d00000` (phình to gấp hơn 3 lần từ 5.1% lên 16.3%).

#### Chart 9: Ma trận Tỷ lệ Già hóa & Tuổi Trung vị theo Thập kỷ (Heatmap / Highlight Table)
* **Loại biểu đồ**: Heatmap (Bảng nhiệt ma trận).
* **Fields**: Hàng `[Entity]` (Top 15 quốc gia), Cột `[Year]` (1970, 1990, 2010, 2023, 2040, 2050), Color & Label: `[Share 65+ (%)]` hoặc `[Median Age]`.
* **Ý nghĩa**: Màu sắc chuyển từ vàng nhạt sang đỏ sẫm thể hiện tốc độ già hóa dựng đứng của các nước Đông Á và Châu Âu.

#### Chart 10: SO SÁNH DỰ BÁO GIÀ HÓA: MÔ HÌNH HỌC MÁY (ML) VS KỊCH BẢN CHUẨN LIÊN HỢP QUỐC (UN WPP)
* **Mục đích**: **Đối chiếu trực tiếp kết quả mô hình Machine Learning tự xây dựng (Linear Regression) với số liệu dự báo mẫu của UN WPP Medium Scenario** trong giai đoạn 2024 – 2050.
* **Loại biểu đồ**: Dual-Axis Line Chart kết hợp Difference Indicator (Đường trục kép có so sánh sai số).
* **Nguồn dữ liệu**:
  - Bảng 1: [`data/processed/population_forecast_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_forecast_2050.csv) (Chứa cả 2 đường `Model = "un_wpp_medium"` và `Model = "linear_regression"`).
  - Bảng 2: [`data/processed/model_vs_un_wpp_comparison_2050.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/model_vs_un_wpp_comparison_2050.csv) (Chứa sẵn các cột chênh lệch định lượng `Share65_Diff` và `Population_Diff_Pct`).
* **Cấu hình trên Tableau**:
  1. Trục X: `[Year]` (1950 – 2050).
  2. Trục Y chính: `AVG([Share_65plus])` (hoặc `SUM([Population]) / 1,000,000`).
  3. Kéo trường `[Model]` vào thẻ **Color**:
     - Đường nét liền màu xanh `#0F3460`: `Model = "un_wpp_medium"` (Kịch bản chuẩn Liên Hợp Quốc).
     - Đường nét đứt màu cam `#F5A623`: `Model = "linear_regression"` (Mô hình Học máy tự xây dựng).
  4. Trục Y phụ (hoặc Tooltip / Sub-bar): Thể hiện độ lệch chênh lệch `[Share65_Diff] = [Share65_ML] - [Share65_UN]` (%).
  5. Vạch tham chiếu: Đường ngang tại `Y = 20%` đánh dấu ngưỡng **Xã hội Siêu già (Super-Aged Society)**.
* **Nội dung Phân tích So sánh & Đánh giá (Evaluation & Insights)**:
  - **Mức độ tương đồng**: Trên phạm vi toàn cầu và các quốc gia có đà tăng trưởng ổn định (như Mỹ, Ấn Độ, Việt Nam), mô hình ML bám sát UN WPP với độ lệch $MAE < 0.8\%$ về tỷ lệ người cao tuổi.
  - **Khác biệt phương pháp luận**:
    * Mô hình Linear Regression ngoại suy tuyến tính dựa trên quán tính gia tốc của chuỗi dữ liệu 30 năm gần nhất (1994–2023).
    * Kịch bản chuẩn UN WPP sử dụng mô hình thành phần Cohort-Component vi mô kết hợp bảng sống (Life Tables) và giả định mức sinh hồi phục nhẹ sau năm 2040.
    * Do đó, ở các quốc gia có mức sinh giảm cực sốc (như Hàn Quốc, Trung Quốc), UN WPP dự báo tỷ lệ già hóa tăng nhanh hơn trong khi Linear Regression có xu hướng thận trọng hơn một chút.
* **Trình diễn Tương tác khi Filter**:
  - Khi xem Toàn cầu (`World`): Cả UN WPP và Mô hình ML cùng chỉ ra năm 2050 tỷ lệ người già đạt **~16.3%** (chính thức bước vào ngưỡng Xã hội Già).
  - Khi chọn `Vietnam`: Cả hai nguồn đều dự phóng Việt Nam sẽ cán mốc **~20.0% – 20.8%** người cao tuổi vào năm 2050, xác nhận Việt Nam sẽ chạm ngưỡng **Xã hội Siêu già** vào năm 2050.

---

### BẢNG TỔNG HỢP KIỂM TRA 10 LOẠI BIỂU ĐỒ TRÊN DASHBOARD

| STT | Tên Biểu đồ | Loại Biểu đồ trong Tableau | Cụm Chuyên đề | Giá trị Phân tích Cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Bản đồ Dân số Thế giới | **Filled Map** (Choropleth) | Cụm 1: Quy mô & Phân bố | Mật độ phân bố địa lý toàn cầu |
| **2** | Chuyển đổi Nhân khẩu học (LE vs TFR) | **Animated Scatter Plot** (Bubbles + Pages) | Cụm 1: Quy mô & Phân bố | Gốc rễ già hóa: Tuổi thọ tăng + Mức sinh giảm |
| **3** | Top 10 Nước Đông dân | **Horizontal Bar Chart** | Cụm 1: Quy mô & Phân bố | Xếp hạng quy mô tuyệt đối |
| **4** | Xu hướng Dân số 1950–50 | **Area + Line Chart** | Cụm 2: Tiến trình Lịch sử | Đỉnh tăng trưởng và bão hòa |
| **5** | Đổi ngôi Thứ hạng Dân số | **Bump Chart** (Rank Line) | Cụm 2: Tiến trình Lịch sử | Ấn Độ vượt TQ, Nigeria vượt Mỹ |
| **6** | Phân phối Tốc độ Tăng | **Histogram** (Bins) | Cụm 3: Nguyên nhân Suy giảm| 54 nước âm vs 183 nước dương |
| **7** | Mức sinh TFR vs Tăng trưởng | **Scatter Plot** (Bubbles) | Cụm 3: Nguyên nhân Suy giảm| 4 góc phần tư & ngưỡng TFR 2.1 |
| **8** | Chuyển dịch 3 Khối Tuổi | **100% Stacked Area Chart** | Cụm 4: Già hóa & Dự báo ML | Thu hẹp trẻ em, phình to người già |
| **9** | Ma trận Già hóa Thập kỷ | **Heatmap / Highlight Table** | Cụm 4: Già hóa & Dự báo ML | Làn sóng chuyển màu cảnh báo |
| **10**| **So sánh Dự báo ML vs UN**| **Dual-Axis Line Chart** | Cụm 4: Già hóa & Dự báo ML | **Đối chiếu Mô hình ML với Chuẩn LHQ** |

## 5. Bộ lọc & Tương tác (Filters & Interactivity)

### 5.1 Phân loại 3 Nhóm Phản ứng với Bộ lọc

Do đặc thù dữ liệu (một số indicators chỉ có đến 2023, một số chart cần hiện nhiều quốc gia cùng lúc), 10 charts được chia thành **3 nhóm phản ứng khác nhau** với bộ lọc toàn cục:

| Nhóm | Charts | Year filter | Entity filter | Lý do |
| :---: | :--- | :--- | :--- | :--- |
| **A – Đồng bộ 100%** | Chart 1 (Map), 4 (Trend), 8 (Stacked Area), 10 (ML vs UN), KPI 1-3 | ✅ Áp dụng | ✅ Áp dụng (Filter) | Data đầy đủ 1950–2100, hiện 1 entity |
| **B – Chỉ Highlight** | Chart 2 (LE vs TFR), 6 (Histogram), 7 (TFR vs GR) | ❌ Không áp dụng | ✅ Áp dụng (Highlight, không Filter) | Cần hiện nhiều nước cùng lúc; TFR/LE chỉ đến 2023 |
| **C – Độc lập** | Chart 3 (Top 10), 5 (Bump), 9 (Heatmap), KPI 4 (TFR) | ❌ Không áp dụng | ❌ Bộ lọc riêng | Danh sách nước cố định; Year ở mốc thập kỷ cố định |

### 5.2 Bộ lọc chính (Dashboard-level)

| # | Tên bộ lọc | Loại | Mặc định | Apply to Worksheets |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Năm (Year)** | Slider (single year) | 2023 | **Nhóm A only**: `01-GeoMap`, `04-GlobalTrend`, `06-GrowthHistogram`, `08-AgeBrackets`, `10-ForecastML`, `KPI-01`, `KPI-02`, `KPI-03` |
| 2 | **Quốc gia (Entity)** | Search & multi-select | World | **Nhóm A only**: `01-GeoMap`, `04-GlobalTrend`, `08-AgeBrackets`, `10-ForecastML`, `KPI-01` ~ `KPI-04` |
| 3 | **Châu lục (Continent)** | Multi-select dropdown | Tất cả | Nhóm A + B (trừ Chart 4 Global Trend) |
| 4 | **Loại thực thể (Is Country)** | Single select | "Country" | Tất cả worksheet |

### 5.3 Dashboard Actions (Tương tác nâng cao)

| # | Loại Action | Source | Target | Run on | Mô tả |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | **Filter** | `01-GeoMap`, `03-TopPopulations` | **Nhóm A**: Chart 4, 8, 10, KPI 1-4 | Select | Click quốc gia trên Map/Bar → lọc toàn bộ Nhóm A |
| 2 | **Highlight** | `01-GeoMap`, `03-TopPopulations` | **Nhóm B**: Chart 2, 6, 7 | Select | Click quốc gia → highlight sáng trên Scatter/Histogram, các nước khác mờ nhạt |
| 3 | **URL** | `01-GeoMap` | External | Select | Mở `https://ourworldindata.org/grapher/population?country=<Code>` |
| 4 | **Tooltip (Viz in Tooltip)** | `01-GeoMap` | `Tooltip-PopTrendMini` | Hover | Hiện mini line chart dân số trong tooltip |

> **Tại sao Nhóm B dùng Highlight thay vì Filter?**
> - Chart 2 (LE vs TFR Scatter) cần hiện **nhiều nước cùng lúc** để so sánh. Nếu filter chỉ còn 1 nước → chỉ thấy 1 bong bóng duy nhất → mất ý nghĩa.
> - Chart 6 (Histogram) cần phân phối của **tất cả nước** → filter 1 nước = 1 bin duy nhất.
> - Chart 7 (TFR vs Growth) tương tự Chart 2.
> - **Highlight Action** giải quyết bằng cách: vẫn hiện tất cả, nhưng quốc gia được chọn sẽ **sáng rõ**, các nước khác **mờ 30%**.

### 5.4 Xử lý KPI 4 (TFR) khi Year > 2023

Do `Total fertility rate` chỉ có data đến 2023, khi Year filter chọn 2040/2050 thì KPI 4 sẽ trống. Giải pháp:

```
// Calculated Field: [TFR Display]
IF [Year] <= 2023 THEN 
    [Total fertility rate]
ELSE 
    { FIXED [Entity]: MAX(IF [Year] = 2023 THEN [Total fertility rate] END) }
END

// Calculated Field: [TFR Label]  
IF [Year] <= 2023 THEN 
    STR(ROUND([Total fertility rate], 2)) + " con/phụ nữ"
ELSE
    STR(ROUND([TFR Display], 2)) + " con/phụ nữ (2023*)"
END
```

→ KPI 4 sẽ hiện giá trị TFR cuối cùng có data (năm 2023) kèm dấu `*` để người dùng biết đây là data lịch sử.

### 5.5 Hướng dẫn Cài đặt Viz in Tooltip (Biểu đồ con nhúng trong Tooltip)

Viz in Tooltip giúp nâng cấp trải nghiệm người dùng: Khi hover vào bất kỳ quốc gia nào trên **Bản đồ (`01-GeoMap`)** hoặc **Bong bóng (`02-DemographicTransition`)**, thay vì chỉ hiện con số khô khan, một **biểu đồ Sparkline thu nhỏ** sẽ hiện ra trực tiếp:

1. **Tạo Worksheet con `Tooltip-CountryTrend`**:
   - Columns: Kéo `[Year]` (Continuous, 1950 – 2050).
   - Rows: Kéo `SUM([Population (Millions)])`.
   - Thẻ Marks: Chọn **Area** (Tô màu xanh `#4ECDC4`, độ mờ Opacity = 60%).
   - Định dạng: Ẩn Header trục X và trục Y để biểu đồ gọn gàng, kích thước thiết kế chuẩn 300 × 160 px.
2. **Nhúng vào Sheet Bản đồ (`01-GeoMap`) và Scatter Plot (`02-DemographicTransition`)**:
   - Mở Sheet `01-GeoMap` $\rightarrow$ Bấm nút **Tooltip** trên thẻ Marks Card.
   - Bấm vào menu **Insert** ở góc trên bên phải hộp thoại Tooltip $\rightarrow$ Chọn **Sheets** $\rightarrow$ `Tooltip-CountryTrend`.
   - Cú pháp Tableau tự sinh:
     ```tableau
     <Sheet name="Tooltip-CountryTrend" maxwidth="320" maxheight="160" filter="<All Fields>">
     ```
   - Định dạng văn bản Tooltip đi kèm:
     ```text
     Quốc gia: <Entity> (<Code>) | Năm: <Year>
     Quy mô Dân số: <SUM(Population (Millions))> Triệu người
     Xu hướng Dân số 1950 – 2050:
     <Sheet name="Tooltip-CountryTrend" maxwidth="320" maxheight="160" filter="<All Fields>">
     ```

### 5.6 Hướng dẫn Cài đặt Drill-down Địa lý (Geographic Drill-down)

Có 2 phương thức Drill-down chuyên nghiệp được triển khai:
1. **Drill-down bằng Hierarchy (Thao tác trục [+] và [-])**:
   - Sau khi tạo Hierarchy `Địa lý (Geographic)` gồm `[Continent] -> [Entity] -> [Code]` (xem mục 3.3).
   - Kéo trường `[Continent]` vào Rows trên Chart 3 (Bar Chart) hoặc Chart 9 (Heatmap).
   - Người xem chỉ cần bấm vào nút **`[+]`** trên nhãn trục để tự động bung từ cấp Châu lục xuống danh sách Quốc gia.
2. **Drill-down tương tác qua Dashboard Action (Click-to-Drill)**:
   - Trên Dashboard 1: Bấm chọn một quốc gia trên Bản đồ $\rightarrow$ Tự động lọc toàn bộ các biểu đồ Trend (Chart 4), Tháp tuổi (Chart 8) và Thẻ KPI theo đúng quốc gia đó.
   - Bấm ra vùng trống ngoài bản đồ $\rightarrow$ Tự động hoàn lại góc nhìn Toàn cầu (`World`).

---

## 6. Thiết kế Giao diện & Bảng Màu

### 6.1 Bảng Màu Chính

| Vai trò | Mã màu | Tên |
| :--- | :--- | :--- |
| Background chính | `#1A1A2E` | Dark Navy |
| Background phụ | `#16213E` | Deep Blue |
| Text chính | `#EAEAEA` | Light Gray |
| Text phụ | `#8B8B9E` | Muted Gray |
| Accent 1 (highlight) | `#E94560` | Coral Red |
| Accent 2 (positive) | `#0F3460` | Royal Blue |
| Accent 3 (forecast) | `#F5A623` | Amber |
| Estimate data | `#4ECDC4` | Teal |
| Projected data | `#FF6B6B` | Salmon |
| Forecast data | `#F5A623` | Amber |

### 6.2 Bảng Màu theo Châu lục

| Châu lục | Mã màu |
| :--- | :--- |
| Châu Á | `#2196F3` (Blue) |
| Châu Phi | `#4CAF50` (Green) |
| Châu Âu | `#9C27B0` (Purple) |
| Bắc Mỹ | `#FF9800` (Orange) |
| Nam Mỹ | `#F44336` (Red) |
| Châu Đại Dương | `#00BCD4` (Cyan) |

### 6.3 Typography
- **Tiêu đề Dashboard**: Roboto Bold 24pt, màu `#EAEAEA`
- **Tiêu đề Chart**: Roboto Medium 14pt, màu `#EAEAEA`
- **Label**: Roboto Regular 10pt, màu `#8B8B9E`
- **Tooltip**: Roboto Regular 11pt

### 6.4 Layout Dimensions
- **Dashboard kích thước**: Fixed size 1920 × 1080 px (Full HD) hoặc Automatic
- **Padding giữa các chart**: 10px
- **Header height**: 80px
- **Filter bar height**: 50px
- **Footer height**: 40px

---

## 7. KPI Cards (Thẻ Chỉ số Chính Động theo Quốc gia & Năm)

4 Thẻ KPI được thiết kế **hoàn toàn tương tác (Dynamic Interaction)**. Khi người dùng thay đổi bộ lọc `[Entity]` (mặc định là `World`, hoặc chọn `Vietnam`) và thanh trượt `[Year]` (ví dụ `2023` hoặc `2020`), toàn bộ 4 thẻ KPI sẽ tức thời tính toán lại theo đúng quốc gia và năm đã chọn:

| # | Thẻ KPI | Công thức Calculated Field trên Tableau (file wide) | Ví dụ: World (2023) | Ví dụ: Vietnam (2020) | Định dạng hiển thị (Format) |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **KPI 1** | 🌍 **Quy mô Dân số** | `SUM([Population])` | **8.09 Tỷ** | **97.47 Triệu** | Number (Custom): Đơn vị Triệu / Tỷ |
| **KPI 2** | 📈 **Tốc độ Tăng trưởng** | `AVG([Population growth rate]) / 100` | **+0.87%** | **+0.92%** | Percentage (2 chữ số thập phân) |
| **KPI 3** | 👵 **Tỷ lệ Người già 65+** | `AVG([Share of population aged 65+]) / 100` | **9.99%**<br>*(Đang già hoá)* | **8.84%**<br>*(Đang già hoá)* | Percentage kèm subtitle phân loại `[Ageing Stage]` |
| **KPI 4** | 👶 **Mức sinh (TFR)** | `AVG([TFR Display])` | **2.25** | **1.94**<br>*(Dưới thay thế)* | Number (Decimal, 2 số) kèm nhãn `[TFR Label]` |

**Thiết kế Thẻ KPI trên Tableau**:
- Tạo 4 worksheet con độc lập: `KPI-01-Population`, `KPI-02-Growth`, `KPI-03-Share65`, `KPI-04-TFR`.
- Kéo Calculated Field tương ứng vào thẻ **Text** trên Marks Card.
- Định dạng Text: Giá trị chính cỡ chữ 28pt Bold, màu trắng `#FFFFFF`; Phụ đề bên dưới 10pt `#8B8B9E`.
- Tô màu nền thẻ trên Dashboard: Container màu `#16213E`, bo góc nhẹ, viền trái 4px màu Accent (`#4ECDC4` cho Dân số, `#2196F3` cho Tăng trưởng, `#E94560` cho Già hóa, `#F5A623` cho Mức sinh).

---

## 8. Story Points (Tableau Storyboard Kể chuyện Dữ liệu)

Tạo Tableau Story với 5 Story Points nối tiếp nhau theo tiến trình logic:

### Story Point 1: "Bức tranh Tổng quan & Quy mô Địa lý" (Cụm 1)
- **Worksheets ghép**: KPI Cards + `01-GeoMap` + `02-DemographicTransition` + `03-TopPopulations`.
- **Thông điệp (Caption)**: *"Dân số thế giới đạt 8.09 tỷ người vào năm 2023, với hơn 55% tập trung tại Top 10 quốc gia. Quá trình Chuyển đổi Nhân khẩu học cho thấy toàn cầu đang dịch chuyển từ 'sinh nhiều, chết sớm' sang 'sinh ít, sống lâu' — gốc rễ của làn sóng già hóa."*

### Story Point 2: "Tiến trình Lịch sử & Đổi ngôi Quyền lực" (Cụm 2)
- **Worksheets ghép**: `04-GlobalTrend` (Area + Line) + `05-RankBumpChart`.
- **Thông điệp (Caption)**: *"Thế kỷ bùng nổ dân số đang dần khép lại. Dấu mốc lịch sử năm 2023 chứng kiến Ấn Độ chính thức soán ngôi Trung Quốc; đến 2050, Nigeria sẽ vượt Mỹ để lọt vào Top 3 thế giới."*

### Story Point 3: "Nguyên nhân Gốc rễ: Mức sinh Suy giảm & Phân hóa Toàn cầu" (Cụm 3)
- **Worksheets ghép**: `06-GrowthHistogram` + `07-FertilityGrowthQuadrant`.
- **Thông điệp (Caption)**: *"Phân cực nhân khẩu học: 54 quốc gia đã bước vào chu kỳ suy giảm dân số tính đến năm 2023. Hơn 55% các nước có mức sinh rơi xuống dưới ngưỡng thay thế (TFR < 2.1), đẩy thế giới vào bẫy già hóa."*

### Story Point 4: "Làn sóng Già hóa & Xã hội Siêu già 2050" (Cụm 4)
- **Worksheets ghép**: `08-AgeBracketsTransition` + `09-AgeingDecadeMatrix`.
- **Thông điệp (Caption)**: *"Đến năm 2050, tỷ lệ người cao tuổi (65+) sẽ tăng gấp 3 lần so với năm 1950, chiếm 16.3% dân số toàn cầu. Hơn 60 quốc gia (bao gồm Việt Nam, Nhật Bản, Hàn Quốc, Đức) sẽ chính thức trở thành Xã hội Siêu già."*

### Story Point 5: "Dự phóng Tương lai: So sánh Mô hình Học máy (ML) & Chuẩn Liên Hợp Quốc (UN)" (Cụm 4)
- **Worksheets ghép**: `10-ForecastComparisonMLvsUN`.
- **Thông điệp (Caption)**: *"Mô hình Linear Regression của nhóm bám sát kịch bản chuẩn của UN WPP giai đoạn 2024–2050 với độ lệch MAE < 0.8% về tỷ lệ người già, đồng thuận khẳng định tốc độ già hóa của Việt Nam thuộc nhóm nhanh nhất thế giới."*

---

## 9. Hướng dẫn Triển khai Từng Bước trên Tableau (Step-by-Step Implementation Guide)

### Bước 1: Làm mới & Chuẩn hóa Nguồn Dữ liệu (Data Source Setup)
1. Mở Tableau Desktop / Tableau Public và kết nối tệp [`data/processed/population_fact_wide.csv`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/data/processed/population_fact_wide.csv).
2. Vào thẻ **Data** trên menu $\rightarrow$ Bấm chuột phải vào `population_fact_wide` $\rightarrow$ Chọn **Refresh** (hoặc bấm `F5`).
   > **Lưu ý**: Dữ liệu file Wide có 39,478 dòng và 14 cột được gom nhóm theo Entity - Year, bao gồm đầy đủ tất cả chỉ số (Population, TFR, Life expectancy, Median age, Age groups, 65+...). Giúp Tableau tải nhẹ (~3.9MB), tính toán cực nhanh và đồng bộ bộ lọc tự động 100%.
3. Kiểm tra kiểu dữ liệu của các cột:
   - `Code`: Bấm vào biểu tượng kiểu dữ liệu $\rightarrow$ Chọn **Geographic Role** $\rightarrow$ **Country/Region**.
   - `Year`: Đảm bảo là **Number (Whole)** hoặc Date/Year.
   - `Population`, `Older people (65+ years)`, `Working-age adults (15-64 years)`, `Children (under-15s)`: **Number (Whole)**.
   - `Population growth rate`, `Total fertility rate`, `Life expectancy`, `Median age`, `Share of population aged 65+`, `Old-age dependency ratio`: **Number (Decimal)**.
   - `Entity`, `DataStatus`: **String**.
4. Nạp thêm nguồn phụ `data/processed/population_forecast_2050.csv`:
   - Data $\rightarrow$ New Data Source $\rightarrow$ Text File $\rightarrow$ Chọn `population_forecast_2050.csv` (dùng riêng cho Chart 10).

---

### Bước 2: Tạo Trọn bộ Calculated Fields (Sẵn sàng Copy-Paste)
Vào Data Pane $\rightarrow$ Bấm mũi tên cạnh Search $\rightarrow$ **Create Calculated Field**:

```tableau
// 1. [Population (Millions)]
[Population] / 1000000

// 2. [Population (Billions)]
[Population] / 1000000000

// 3. [Growth Rate (%)]
[Population growth rate]

// 4. [TFR]
[Total fertility rate]

// 5. [LE]
[Life expectancy]

// 6. [Median Age]
[Median age]

// 7. [Share 65+ (%)]
[Share of population aged 65+]

// 8. [Old-age Dependency Ratio]
[Old-age dependency ratio]

// 9. [Ageing Stage] - Phân cấp Già hoá chuẩn Liên Hợp Quốc
IF [Share 65+ (%)] >= 20 THEN "4. Siêu già (>=20%)"
ELSEIF [Share 65+ (%)] >= 14 THEN "3. Xã hội già (14-20%)"
ELSEIF [Share 65+ (%)] >= 7 THEN "2. Đang già hoá (7-14%)"
ELSE "1. Dân số trẻ (<7%)"
END

// 10. [Below Replacement] - Phân loại Mức sinh
IF [TFR] < 2.1 THEN "Dưới mức thay thế (<2.1)"
ELSE "Trên mức thay thế (>=2.1)"
END

// 11. [Is Country] - Lọc bỏ các thực thể vùng/châu lục để tránh trùng lắp khi xếp hạng
NOT ISNULL([Code]) AND [Code] != "OWID_WRL" AND [Code] != ""

// 12. [Data Period] - Phân tách giai đoạn hiển thị
IF [DataStatus] = "estimate" THEN "1. Lịch sử (1950-2023)"
ELSEIF [DataStatus] = "projected" THEN "2. Dự phóng UN (2024-2100)"
ELSE "3. Dự báo ML (2027-2050)"
END

// 13. [TFR Display] - Fallback cho KPI4 khi Year > 2023
IF [Year] <= 2023 THEN [Total fertility rate]
ELSE { FIXED [Entity]: MAX(IF [Year] = 2023 THEN [Total fertility rate] END) }
END

// 14. [TFR Label] - Nhãn hiển thị cho KPI4 kèm chú thích nếu dùng dữ liệu cố định 2023
IF [Year] <= 2023 THEN STR(ROUND([TFR], 2)) + " con/phụ nữ"
ELSE STR(ROUND([TFR Display], 2)) + " con/phụ nữ (2023*)"
END
```

---

### Bước 3: Thao tác Kéo Thả Chi tiết cho Từng Sheet (10 Biểu đồ Khác biệt)

#### 🏛️ CỤM 1: QUY MÔ & PHÂN BỐ KHÔNG GIAN
1. **Sheet 1: `01-GeoMap` (Filled Map - Bản đồ Địa lý)**:
   - Thẻ Marks: Chọn **Map**.
   - Kéo `[Code]` vào **Detail**.
   - Kéo `[Population (Millions)]` vào **Color** (chọn bảng màu Palette: *Blues* hoặc *Teal*).
   - Thẻ Filters: Kéo `[Is Country]` $\rightarrow$ Chọn `True`.
   - Cài đặt Tooltip: Kéo `[Entity]`, `[Population (Millions)]`, `[Year]` vào Tooltip.

2. **Sheet 2: `02-DemographicTransition` (Animated Scatter Plot – Tuổi thọ vs Mức sinh)**:
   - Thẻ Marks: Chọn **Circle**.
   - Columns: Kéo `[Life expectancy]` (hoặc `[LE]`) $\rightarrow$ Chọn Continuous.
   - Rows: Kéo `[Total fertility rate]` (hoặc `[TFR]`) $\rightarrow$ Chọn Continuous.
   - Kéo `SUM([Population (Millions)])` vào **Size** (chỉnh kích thước bong bóng phù hợp).
   - Kéo `[Continent]` vào **Color** (hoặc tạo bảng màu tùy chỉnh cho 6 châu lục).
   - Kéo `[Entity]` vào **Detail**.
   - Kéo `[Entity]` vào **Label** $\rightarrow$ Click Label $\rightarrow$ Chọn **"Selected"** ở mục *Marks to Label* (chỉ hiện nhãn khi hover/click).
   - **Animation (Pages Shelf)**: Kéo `[Year]` vào **Pages** shelf $\rightarrow$ Tableau tự tạo thanh điều khiển Play/Pause.
     * Cài đặt: Bấm nút History trên thanh Pages $\rightarrow$ Tích chọn **Show trails** để thấy vết di chuyển của mỗi quốc gia qua thời gian.
   - Thẻ Filters: `[Is Country]` = `True`; `[Year]` range 1950–2023.
   - **Reference Lines** (Tab Analytics $\rightarrow$ Kéo Reference Line):
     * Vạch ngang Y = `2.1` (Ngưỡng sinh thay thế) — nhãn: *"TFR = 2.1 (Mức thay thế)"*, nét đứt đỏ.
     * Vạch dọc X = `70` (Ngưỡng tuổi thọ cao) — nhãn: *"LE = 70 (Tuổi thọ cao)"*, nét đứt xanh.
   - **Tooltip**: Chỉnh nội dung Tooltip hiển thị `Entity`, `Year`, `Life Expectancy`, `TFR`, `Population`.

3. **Sheet 3: `03-TopPopulations` (Horizontal Bar Chart - Top 10 Quốc gia)**:
   - Rows: Kéo `[Entity]`.
   - Columns: Kéo `SUM([Population (Millions)])`.
   - Lọc Top 10: Nhấp chuột phải vào `[Entity]` trên Rows $\rightarrow$ Filter $\rightarrow$ Tab **Top** $\rightarrow$ Chọn *By field: Top 10 by SUM([Population (Millions)])*.
   - Sắp xếp: Bấm biểu tượng Sort Descending trên thanh công cụ để đưa nước đông nhất lên đầu.
   - Color: Tô màu nhấn `#2B5C8F`, gắn nhãn giá trị ở cuối mỗi thanh ngang.

---

#### ⏳ CỤM 2: TIẾN TRÌNH & ĐỔI NGÔI LỊCH SỬ
4. **Sheet 4: `04-GlobalTrend` (Area + Line Chart - Xu hướng Quy mô 1950–2050)**:
   - Columns: Kéo `[Year]` (Continuous - Màu xanh lá cây, dải 1950–2050).
   - Rows: Kéo `SUM([Population (Billions)])`.
   - Thẻ Marks: Chọn **Area**.
   - Kéo `[Data Period]` vào **Color** để phân tách vùng *Lịch sử (1950–2023)* màu Teal `#4ECDC4` và vùng *Dự phóng (2024–2050)* màu Cam `#FF6B6B`.
   - Reference Line: Nhấp chuột phải trục X $\rightarrow$ Add Reference Line $\rightarrow$ Chọn giá trị cố định `Year = 2023` với nhãn *"Hiện tại (2023: 8.09 Tỷ)"*.

5. **Sheet 5: `05-RankBumpChart` (Bump Chart - Hoán đổi Thứ hạng Top Quốc gia)**:
   - Thẻ Filters: Chọn Top 7 quốc gia lớn nhất (Ấn Độ, Trung Quốc, Mỹ, Nigeria, Indonesia, Pakistan, Brazil).
   - Columns: Kéo `[Year]` (chọn các mốc 1950, 1970, 1990, 2010, 2023, 2040, 2050).
   - Rows: Kéo `SUM([Population])` $\rightarrow$ Nhấp chuột phải $\rightarrow$ **Quick Table Calculation** $\rightarrow$ **Rank**.
   - Nhấp chuột phải lại vào viên thuốc Rank $\rightarrow$ **Compute Using** $\rightarrow$ Chọn `[Entity]`.
   - Đảo trục Rank: Nhấp chuột phải trục Y $\rightarrow$ Edit Axis $\rightarrow$ Tích chọn **Reversed** (để Hạng 1 nằm ở trên đỉnh).
   - Marks: Chọn **Line**, kéo `[Entity]` vào **Color** và **Label**.

---

#### ⚖️ CỤM 3: NGUYÊN NHÂN & PHÂN HÓA TĂNG TRƯỞNG
6. **Sheet 6: `06-GrowthHistogram` (Histogram - Phân phối Tốc độ Tăng trưởng)**:
   - Tạo Bin: Trong Data Pane, nhấp chuột phải vào `[Growth Rate (%)]` $\rightarrow$ Create $\rightarrow$ **Bins...** $\rightarrow$ Đặt Size of bins = `0.25`.
   - Columns: Kéo viên thuốc `[Growth Rate (%) (bin)]` vừa tạo.
   - Rows: Kéo `COUNTD([Entity])`.
   - Thẻ Marks: Chọn **Bar**.
   - Reference Line: Nhấp chuột phải vào trục X $\rightarrow$ Add Reference Line $\rightarrow$ Hằng số `0.0` (Vạch đỏ nét đứt) đánh dấu ngưỡng tăng trưởng bằng 0: Bên trái là 54 nước suy giảm dân số, bên phải là các nước tăng trưởng.

7. **Sheet 7: `07-FertilityGrowthQuadrant` (Scatter Plot - Ma trận 4 Góc Phần tư)**:
   - Columns: Kéo `AVG([TFR])` (Trục X: Mức sinh).
   - Rows: Kéo `AVG([Growth Rate (%)])` (Trục Y: Tốc độ tăng trưởng).
   - Thẻ Marks: Chọn **Circle**. Kéo `[Entity]` vào **Detail**, kéo `SUM([Population (Millions)])` vào **Size**.
   - Kéo `[Below Replacement]` vào **Color**.
   - Tạo 2 Đường Tham chiếu (Reference Lines):
     * Trục X: Đường đứng tại $TFR = 2.1$ (Ngưỡng sinh thay thế).
     * Trục Y: Đường ngang tại $Growth = 0.0\%$ (Ngưỡng suy giảm dân số).

---

#### 👵 CỤM 4: CƠ CẤU TUỔI & DỰ BÁO GIÀ HOÁ 2050
8. **Sheet 8: `08-AgeBracketsTransition` (100% Stacked Area Chart - Chuyển dịch 3 Khối Tuổi)**:
   - Columns: Kéo `[Year]` (Continuous, 1950 – 2050).
   - Rows: Kéo `Measure Values`.
   - Thẻ Marks: Chọn **Area**.
   - Thẻ Filters: Kéo `Measure Names` vào Filters $\rightarrow$ Chỉ chọn 3 trường:
     * `Children (under-15s)`
     * `Working-age adults (15-64 years)`
     * `Older people (65+ years)`
   - Kéo `Measure Names` vào **Color**:
     * Trẻ em (`Children (under-15s)`): Xanh lá `#76C893`.
     * Lao động (`Working-age adults (15-64 years)`): Xanh navy `#1E6091`.
     * Người già 65+ (`Older people (65+ years)`): Đỏ đậm `#D00000`.
   - Đổi sang tỷ lệ 100%: Nhấp chuột phải vào `Measure Values` trên Rows $\rightarrow$ **Quick Table Calculation** $\rightarrow$ **Percent of Total** $\rightarrow$ Compute Using **Table (Down)**.
   - Thẻ Filters: Kéo `[Entity]` $\rightarrow$ Mặc định chọn `World`.

9. **Sheet 9: `09-AgeingDecadeMatrix` (Heatmap / Highlight Table - Ma trận Già hóa)**:
   - Thẻ Filters: Lọc Top 15 quốc gia già hoá tiêu biểu (Nhật, Hàn, Ý, Đức, Việt Nam, Trung Quốc, Mỹ,...).
   - Rows: Kéo `[Entity]`.
   - Columns: Kéo `[Year]` (chọn Discrete các mốc: 1970, 1990, 2010, 2023, 2040, 2050).
   - Thẻ Marks: Chọn **Square**.
   - Kéo `AVG([Share 65+ (%)])` vào **Color** và vào **Label**.
   - Edit Colors: Chọn Palette *Red-Yellow-Green Diverging* (Đảo ngược để giá trị cao tỷ lệ già hóa tô màu đỏ sẫm cảnh báo).

10. **Sheet 10: `10-ForecastComparisonMLvsUN` (Dual-Axis Line - Đối chiếu Mô hình ML vs Kịch bản Chuẩn UN)**:
    - Chuyển sang nguồn dữ liệu: `population_forecast_2050.csv`.
    - Columns: Kéo `[Year]` (dải 2000 – 2050).
    - Rows: Kéo `AVG([Share_65plus])`.
    - Thẻ Marks: Chọn **Line**.
    - Kéo `[Model]` vào **Color**:
      * `un_wpp_medium`: Màu Xanh Navy `#0F3460` (Kịch bản Chuẩn của Liên Hợp Quốc).
      * `linear_regression`: Màu Cam `#F5A623` (Mô hình Machine Learning do nhóm xây dựng).
    - Reference Line: Thêm đường ngang tại `Y = 20%` đánh dấu ngưỡng **Xã hội Siêu già (Super-Aged Society)**.
    - Insight hiển thị: So sánh trực tiếp độ lệch giữa mô hình của nhóm và UN (toàn cầu lệch <0.8%, khẳng định độ tin cậy của thuật toán).

---

### Bước 4: Ghép Dashboard & Cấu hình Tương tác Toàn cục (Global Filter & Actions)
1. **Tạo Dashboard mới**:
   - Size: Chọn **Fixed Size** $\rightarrow$ **1920 × 1080 (Full HD)**.
   - Đặt nền Dashboard màu tối sang trọng: `#1A1A2E`.
2. **Bố trí Khung Header & 4 KPI Cards**:
   - Kéo Text Box tiêu đề: *"PHÂN TÍCH BIẾN ĐỘNG DÂN SỐ TOÀN CẦU & XU HƯỚNG GIÀ HOÁ DÂN SỐ ĐẾN NĂM 2050"*.
   - Kéo 1 Horizontal Container đặt 4 thẻ KPI (`KPI-01`, `KPI-02`, `KPI-03`, `KPI-04`) nằm ngang trên cùng.
3. **Bố trí 4 Cụm Chuyên đề**:
   - Kéo các Horizontal / Vertical Container xếp thành 4 ô lưới trực quan tương ứng với 4 Cụm chuyên đề (như khung Wireframe mục 4).
4. **Cài đặt Bộ lọc Toàn cục (Global Filters) — Theo Chiến lược 3 Nhóm (Xem Mục 5.1)**:
   - Bấm vào Sheet Bản đồ $\rightarrow$ Bật bộ lọc `[Entity]` và `[Year]`.
   - **Year filter** $\rightarrow$ **Apply to Worksheets** $\rightarrow$ **Selected Worksheets...** $\rightarrow$ Chỉ tích chọn **Nhóm A**:
     * ✅ `01-GeoMap`, `04-GlobalTrend`, `06-GrowthHistogram`, `08-AgeBracketsTransition`, `10-ForecastComparisonMLvsUN`, `KPI-01`, `KPI-02`, `KPI-03`.
     * ❌ **KHÔNG tích**: `02-DemographicTransition` (dùng Pages shelf riêng), `05-RankBumpChart` (mốc thập kỷ cố định), `07-FertilityGrowthQuadrant` (TFR chỉ đến 2023), `09-AgeingDecadeMatrix` (mốc thập kỷ cố định), `KPI-04-TFR` (dùng `[TFR Display]` có fallback riêng).
   - **Entity filter** $\rightarrow$ **Apply to Worksheets** $\rightarrow$ **Selected Worksheets...** $\rightarrow$ Chỉ tích chọn **Nhóm A**:
     * ✅ `01-GeoMap`, `04-GlobalTrend`, `08-AgeBracketsTransition`, `10-ForecastComparisonMLvsUN`, `KPI-01` ~ `KPI-04`.
     * ❌ **KHÔNG tích**: `02-DemographicTransition`, `06-GrowthHistogram`, `07-FertilityGrowthQuadrant` (Nhóm B dùng Highlight), `03-TopPopulations`, `05-RankBumpChart`, `09-AgeingDecadeMatrix` (Nhóm C độc lập).
   - **Kết quả tương tác**:
     * Mặc định chọn `World` năm `2023` $\rightarrow$ Nhóm A hiện số liệu toàn cầu 8.09 tỷ người. Nhóm B hiện tất cả nước với World được highlight.
     * Khi chọn `Vietnam` năm `2020` $\rightarrow$ Nhóm A chuyển sang Vietnam (97.47M, GR 0.92%, Share65 8.84%). Nhóm B highlight Vietnam trên nền các nước khác mờ. Nhóm C giữ nguyên.
5. **Cài đặt Dashboard Actions — Filter & Highlight (Xem Mục 5.3)**:
   - **Action 1 — Filter Action (Click-to-Filter cho Nhóm A)**:
     * Dashboard $\rightarrow$ Actions $\rightarrow$ Add Action $\rightarrow$ **Filter**.
     * Source Sheets: `01-GeoMap`, `03-TopPopulations`.
     * Target Sheets: **Nhóm A** — `04-GlobalTrend`, `08-AgeBracketsTransition`, `10-ForecastComparisonMLvsUN`, `KPI-01` ~ `KPI-04`.
     * Run action on: **Select**.
     * Clearing the selection will: **Show all values**.
   - **Action 2 — Highlight Action (Click-to-Highlight cho Nhóm B)**:
     * Dashboard $\rightarrow$ Actions $\rightarrow$ Add Action $\rightarrow$ **Highlight**.
     * Source Sheets: `01-GeoMap`, `03-TopPopulations`.
     * Target Sheets: **Nhóm B** — `02-DemographicTransition`, `06-GrowthHistogram`, `07-FertilityGrowthQuadrant`.
     * Run action on: **Select**.
     * Clearing the selection will: **Show all highlights**.
   - **Action 3 — URL Action**:
     * Source Sheets: `01-GeoMap`.
     * URL: `https://ourworldindata.org/grapher/population?country=<Code>`.
6. **Thêm Chú thích Nguồn Dữ liệu ở Chân trang (Footer Note)**:
   - Kéo một Text Box nhỏ ở góc dưới Dashboard (font 9pt, màu `#8B8B9E`):
     * *"Nguồn dữ liệu: Liên Hợp Quốc UN World Population Prospects (2024 Revision) via Our World in Data & World Population Review. Mô hình dự báo: Linear Regression & Logistic Regression (2024–2050)."*
   - Cách làm này đáp ứng 100% tiêu chuẩn báo cáo khoa học mà không làm nặng Fact Table trong cơ sở dữ liệu.

---

## 10. Checklist Kiểm tra Chất lượng (Quality Checklist)

| # | Tiêu chí | Yêu cầu | ✅/❌ |
| :---: | :--- | :--- | :---: |
| 1 | Số loại biểu đồ | ≥ 8 loại khác nhau | ☐ |
| 2 | Geographic Map | Có bản đồ thế giới | ☐ |
| 3 | Bộ lọc | ≥ 3 bộ lọc interactive | ☐ |
| 4 | Tooltip | Mọi chart đều có tooltip chi tiết | ☐ |
| 5 | Drill-down | Click trên Map → filter chart khác | ☐ |
| 6 | Cross-filtering | Tương tác giữa ít nhất 3 chart | ☐ |
| 7 | Calculated Fields | ≥ 10 trường tính toán | ☐ |
| 8 | Reference Lines | Ít nhất 2 chart có reference lines | ☐ |
| 9 | Data Period | Phân biệt rõ estimate/projected/forecast | ☐ |
| 10 | Story Points | ≥ 3 story points với caption | ☐ |
| 11 | KPI Cards | ≥ 3 thẻ chỉ số chính | ☐ |
| 12 | Responsiveness | Dashboard hiển thị đúng trên 1920×1080 | ☐ |
| 13 | Annotations | Ít nhất 2 annotation giải thích insight | ☐ |
| 14 | Color Palette | Bảng màu nhất quán, phân biệt rõ ràng | ☐ |
| 15 | Viz in Tooltip | Ít nhất 1 chart có mini viz trong tooltip | ☐ |

---

## 11. Tham khảo & Cảm hứng Thiết kế

- **Our World in Data** – [Population Growth](https://ourworldindata.org/population-growth): Cách kể chuyện bằng dữ liệu, phân chia thời kỳ estimate vs projection, sử dụng annotation giải thích insight.
- **DataReportal** – [Digital 2026: Global Population Trends](https://datareportal.com/reports/digital-2026-global-population-trends): Cách trình bày KPI cards, bảng màu tối (dark mode), typography hiện đại.
- **UN World Population Prospects**: Nguồn dữ liệu gốc, phương pháp medium scenario.

---

*Tài liệu này được tạo tự động bởi pipeline phân tích dân số. Phiên bản: 2026-09-26.*

---

## PHỤ LỤC: Tóm tắt Nhanh Cách Làm Dashboard trên Tableau

### A. Quy trình Tổng quát (5 Bước)

```text
1. Nạp dữ liệu  →  2. Tạo Calculated Fields  →  3. Dựng 10 Sheet  →  4. Ghép Dashboard  →  5. Cấu hình Story
     ↓                      ↓                         ↓                     ↓                     ↓
  Refresh CSV          Copy-paste 11            Kéo thả theo          Global Filter        5 Story Points
  + Set Code           công thức từ              hướng dẫn            + Click-to-Filter     + Caption
  = Geographic          mục 3.1                 Bước 3 ở trên         + Highlight Action
```

### B. Checklist File Cần Nạp vào Tableau

| # | File | Cách nạp | Ghi chú |
| :---: | :--- | :--- | :--- |
| 1 | `population_fact_wide.csv` | **⭐ Data Source chính duy nhất** (Text file) | Set `Code` = Geographic Role: Country/Region |
| 2 | `continent_mapping.csv` | Left Join vào bảng 1 trên cột `Code` | Thêm chiều Continent |
| 3 | `population_forecast_2050.csv` | Data Source riêng (cho Chart 10) | Chứa 2 Model: `un_wpp_medium` + `linear_regression` |
| 4 | `model_vs_un_wpp_comparison_2050.csv` | *(Tuỳ chọn)* Blend hoặc Join cho Tooltip Chart 10 | Chứa sẵn cột `Share65_Diff`, `Population_Diff_Pct` |

### C. Bảng Tham khảo Nhanh: Chart → Marks Type → Trục

| Chart # | Marks Type | Rows | Columns | Color | Size | Detail | Pages (Animation) |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | Map | *(auto)* | *(auto)* | SUM(Population M) | – | Code | – |
| 2 | Circle | Total fertility rate | Life expectancy | Continent | SUM(Population M) | Entity | Year |
| 3 | Bar | Entity | SUM(Population M) | #2B5C8F | – | – | – |
| 4 | Area | SUM(Population B) | Year | Data Period | – | – | – |
| 5 | Line | RANK(Population) | Year | Entity | – | – | – |
| 6 | Bar | COUNTD(Entity) | Growth Rate (bin) | – | – | – | – |
| 7 | Circle | Growth Rate (%) | Total fertility rate | Below Replacement | SUM(Population M) | Entity | – |
| 8 | Area | Measure Values (% Total) | Year | Measure Names | – | – | – |
| 9 | Square | Entity | Year (discrete) | AVG(Share 65+) | – | – | – |
| 10 | Line | AVG(Share_65plus) | Year | Model | – | – | – |
