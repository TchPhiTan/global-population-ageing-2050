# Đặc tả Dashboard Tableau: Xu hướng Dân số Toàn cầu (1950 – 2050)

## 1. Tổng quan & Câu chuyện Dữ liệu (Data Story)

### 1.1 Mục tiêu Dashboard
Dashboard kể câu chuyện về **sự chuyển đổi nhân khẩu học toàn cầu** qua 3 chương chính:

| Chương | Thời kỳ | Câu chuyện chính |
| :---: | :--- | :--- |
| **Chương 1** | 1950 – 2023 | *"Thế kỷ bùng nổ dân số"* – Dân số tăng gấp 4 lần trong vòng một thế kỷ |
| **Chương 2** | 2024 – 2026 | *"Bước ngoặt hiện tại"* – Ấn Độ vượt Trung Quốc, 65 quốc gia đã suy giảm |
| **Chương 3** | 2027 – 2050 | *"Tương lai phân hóa"* – Châu Phi bùng nổ, Đông Á & Châu Âu thu hẹp |

### 1.2 Thông điệp chính (Key Insights)

> *"Dân số toàn cầu không còn tăng theo hàm mũ – tốc độ tăng trưởng đã đạt đỉnh vào thập niên 1960 và liên tục giảm kể từ đó."*
> — Lấy cảm hứng từ Our World in Data

1. **8.3 tỷ người** (2026) → Dự kiến đạt đỉnh **~10.3 tỷ** vào năm 2084 rồi giảm dần
2. **Ấn Độ** chính thức vượt **Trung Quốc** thành quốc gia đông dân nhất thế giới
3. **65 quốc gia** đang trong chu kỳ suy giảm dân số tính đến năm 2026 (tăng từ 54 quốc gia năm 2023)
4. **130/237** quốc gia (54.9%) có tỷ suất sinh dưới mức thay thế (TFR < 2.1)
5. **Châu Phi cận Sahara** là động lực tăng trưởng duy nhất còn mạnh, trong khi Đông Á và Châu Âu thu hẹp

### 1.3 Đối tượng sử dụng
- Giảng viên và sinh viên môn Thống kê / Dân số học
- Nhà hoạch định chính sách (tham khảo)
- Bất kỳ ai quan tâm đến xu hướng dân số toàn cầu

---

## 2. Nguồn Dữ liệu & Cấu trúc

### 2.1 Bảng dữ liệu chính

| # | Tên file | Vai trò | Hàng | Cột chính |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `population_fact_long.csv` | Fact table chính (1950–2100) | ~154,000 | Entity, Code, Year, Indicator, Value, Unit, DataStatus |
| 2 | `population_fact_wide.csv` | Phiên bản wide cho heatmap | ~14,500 | Entity, Code, Year, Population, GrowthRate, TFR, DataStatus |
| 3 | `population_forecast_2050.csv` | Dự báo Linear Regression | ~24,000 | Entity, Code, Year, Population, DataStatus, Model |

### 2.2 Kết nối trong Tableau
- **Kết nối chính**: Drag `population_fact_long.csv` làm nguồn primary.
- **Blend/Join**: Left join `population_forecast_2050.csv` trên khóa `(Entity, Code, Year)` để có cột `Model` và giá trị `forecast`.
- **Pivot**: Nếu dùng `population_fact_wide.csv`, không cần pivot – đã sẵn các cột chỉ tiêu riêng.

### 2.3 Phân loại Entity (Country vs Region)
Sử dụng **Calculated Field** để phân biệt quốc gia khỏi nhóm tổng hợp khu vực:

```
// [Is Country]
IF LEN([Code]) = 3
   AND UPPER([Code]) = [Code]
   AND NOT STARTSWITH([Code], "OWID_")
   AND NOT STARTSWITH([Code], "UN_")
   AND [Code] != ""
THEN "Country"
ELSEIF [Code] = "OWID_KOS" THEN "Country"  // Kosovo ngoại lệ
ELSE "Region/Aggregate"
END
```

---

## 3. Calculated Fields (Trường tính toán)

### 3.1 Danh sách Calculated Fields

| # | Tên trường | Công thức Tableau | Mục đích |
| :---: | :--- | :--- | :--- |
| 1 | `[Is Country]` | *(Xem mục 2.3 ở trên)* | Lọc quốc gia vs khu vực |
| 2 | `[Population (Millions)]` | `IF [Indicator] = "Population" THEN [Value] / 1000000 END` | Hiển thị dân số theo đơn vị triệu |
| 3 | `[Population (Billions)]` | `IF [Indicator] = "Population" THEN [Value] / 1000000000 END` | Hiển thị dân số theo đơn vị tỷ |
| 4 | `[Growth Rate (%)]` | `IF [Indicator] = "Population growth rate" THEN [Value] END` | Trích tốc độ tăng trưởng |
| 5 | `[TFR]` | `IF [Indicator] = "Total fertility rate" THEN [Value] END` | Trích tỷ suất sinh |
| 6 | `[Data Period]` | `IF [DataStatus] = "estimate" THEN "Lịch sử (Ước tính)" ELSEIF [DataStatus] = "projected" THEN "Dự phóng (UN WPP)" ELSE "Dự báo (Mô hình)" END` | Phân loại giai đoạn cho legend |
| 7 | `[Below Replacement]` | `IF [TFR] < 2.1 THEN "Dưới mức thay thế" ELSE "Trên mức thay thế" END` | Phân loại TFR cho màu sắc |
| 8 | `[Growth Category]` | `IF [Growth Rate (%)] < -1 THEN "Suy giảm mạnh" ELSEIF [Growth Rate (%)] < 0 THEN "Suy giảm nhẹ" ELSEIF [Growth Rate (%)] < 1 THEN "Tăng trưởng thấp" ELSEIF [Growth Rate (%)] < 2 THEN "Tăng trưởng vừa" ELSE "Tăng trưởng cao" END` | Phân nhóm tăng trưởng |
| 9 | `[Continent]` | *Dùng Group hoặc Calculated Field dựa trên Code (xem 3.2)* | Nhóm theo châu lục |
| 10 | `[Population Rank]` | `RANK(SUM([Population (Millions)]))` | Xếp hạng cho top N |
| 11 | `[Reference TFR = 2.1]` | `2.1` | Đường tham chiếu mức sinh thay thế |
| 12 | `[Reference Growth = 0]` | `0` | Đường tham chiếu zero growth |
| 13 | `[Year Label]` | `STR([Year])` | Nhãn năm dạng text |
| 14 | `[Decade]` | `INT([Year] / 10) * 10` | Nhóm theo thập kỷ |

### 3.2 Phân nhóm Châu lục (Continent Grouping)

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

## 4. Thiết kế Dashboard – 10 Loại Biểu đồ

### Tổng quan Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: "Xu hướng Dân số Toàn cầu 1950 – 2050"                │
│  [Bộ lọc: Năm] [Bộ lọc: Châu lục] [Bộ lọc: DataStatus]       │
├──────────────────────────┬──────────────────────────────────────┤
│  KPI Cards (4 thẻ)       │  Chart 1: Global Population Trend   │
│  - Dân số 2026           │  (Area Chart / Line Chart)          │
│  - Tốc độ tăng trưởng   │                                      │
│  - Quốc gia suy giảm    │                                      │
│  - TFR trung bình        │                                      │
├──────────────────────────┼──────────────────────────────────────┤
│  Chart 2: Geographic Map │  Chart 3: Top 15 Bar Chart          │
│  (Filled Map / Symbol)   │  (Horizontal Bar)                   │
│                          │                                      │
├──────────────────────────┼──────────────────────────────────────┤
│  Chart 4: Growth Rate    │  Chart 5: TFR vs Growth Scatter     │
│  Distribution (Histogram)│  (Scatter Plot)                     │
├──────────────────────────┼──────────────────────────────────────┤
│  Chart 6: Population     │  Chart 7: Treemap                   │
│  Heatmap                 │  (Phân bổ dân số theo quốc gia)     │
├──────────────────────────┼──────────────────────────────────────┤
│  Chart 8: Bump Chart     │  Chart 9: Pie/Donut Chart           │
│  (Thay đổi xếp hạng)    │  (Phân bổ theo châu lục)            │
├──────────────────────────┴──────────────────────────────────────┤
│  Chart 10: Forecast Comparison (Dual-axis / Combined)          │
│  Đường dự báo LR vs UN WPP cho top 5 quốc gia                 │
├─────────────────────────────────────────────────────────────────┤
│  FOOTER: Nguồn dữ liệu, ghi chú phương pháp                   │
└─────────────────────────────────────────────────────────────────┘
```

---

### Chart 1: Xu hướng Dân số Toàn cầu (Area Chart + Line)
**Mục đích**: Kể chương 1 – "Thế kỷ bùng nổ dân số" → đạt đỉnh → suy giảm

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Area Chart kết hợp Line |
| **Trục X** | `[Year]` (1950 – 2100) |
| **Trục Y** | `SUM([Population (Billions)])` |
| **Màu sắc** | `[Data Period]`: Xanh dương (Lịch sử), Cam (Dự phóng UN), Đỏ nhạt (Dự báo) |
| **Filter** | `Entity = "World"` |
| **Reference Line** | Đường ngang tại Y = 8.3 (mốc 2026), đường dọc tại X = 2026 |
| **Annotation** | "Đạt đỉnh ~10.3 tỷ người vào 2084" tại điểm peak |
| **Tooltip** | "Năm: {Year} | Dân số: {Population (Billions):,.2f} tỷ | Trạng thái: {Data Period}" |

**Câu chuyện**: *"Từ 2.5 tỷ người (1950) đến 8.3 tỷ (2026) – dân số tăng hơn 3 lần. Nhưng tốc độ đang chậm lại, và LHQ dự kiến đỉnh vào 2084."*

---

### Chart 2: Bản đồ Địa lý – Dân số Theo Quốc gia (Filled Map)
**Mục đích**: Trực quan hóa quy mô dân số trên bản đồ thế giới

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Filled Map (Geographic Map) |
| **Geographic Role** | Gán `[Code]` → Country/Region (ISO-3) |
| **Màu sắc** | `SUM([Population (Millions)])` – Sequential palette (trắng → xanh đậm) |
| **Kích thước** | Không áp dụng (filled map) |
| **Filter** | `[Is Country] = "Country"`, `[Indicator] = "Population"`, Year slider |
| **Tooltip** | "{Entity}: {Population (Millions):,.1f} triệu người | Tăng trưởng: {Growth Rate (%):,.2f}% | TFR: {TFR:,.2f}" |
| **Drill-down** | Click vào quốc gia → Filter tất cả các chart khác theo quốc gia đó |

**Biến thể phụ**: Tạo thêm Symbol Map (bong bóng) với kích thước = Population để so sánh trực quan giữa Ấn Độ và Trung Quốc.

---

### Chart 3: Top 15 Quốc gia Đông dân nhất (Horizontal Bar Chart)
**Mục đích**: Kể chương 2 – "Ấn Độ vượt Trung Quốc"

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Horizontal Bar Chart (thanh ngang) |
| **Trục Y** | `[Entity]` – sắp xếp giảm dần theo Population |
| **Trục X** | `SUM([Population (Millions)])` |
| **Màu sắc** | `[Growth Category]` hoặc gradient theo dân số |
| **Filter** | `[Is Country] = "Country"`, Top N = 15 by Population, Year = 2026 |
| **Label** | Hiển thị giá trị dân số (triệu) trên mỗi thanh |
| **Highlight** | India và China có màu đặc biệt (đỏ/cam) |
| **Tooltip** | "{Entity}: {Population (Millions):,.1f}M | Xếp hạng: #{Population Rank}" |

**Câu chuyện**: *"Năm 2026, India (1,477M) đã chính thức vượt China (1,413M) – khoảng cách ~64 triệu người và ngày càng mở rộng."*

---

### Chart 4: Phân phối Tốc độ Tăng trưởng (Histogram)
**Mục đích**: Cho thấy bức tranh toàn cầu – phần lớn quốc gia đang chậm lại

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Histogram (Bin) |
| **Trục X** | `[Growth Rate (%)]` – tạo bin với kích thước 0.25% |
| **Trục Y** | `COUNT([Entity])` – số quốc gia rơi vào mỗi bin |
| **Màu sắc** | Gradient: Đỏ (âm) → Xám (gần 0) → Xanh lá (dương) |
| **Filter** | `[Is Country] = "Country"`, Year = 2026 |
| **Reference Line** | Đường dọc tại X = 0 (zero growth) với label "Ngưỡng suy giảm" |
| **Reference Line** | Đường dọc tại X = giá trị trung vị (median) |
| **Annotation** | "65 quốc gia có tăng trưởng âm" với mũi tên chỉ vùng bên trái 0 |

---

### Chart 5: Tương quan TFR và Tốc độ Tăng trưởng (Scatter Plot)
**Mục đích**: Giải thích mối quan hệ nhân quả – mức sinh thấp → suy giảm dân số

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Scatter Plot (Biểu đồ phân tán) |
| **Trục X** | `AVG([TFR])` (dữ liệu TFR 2023) |
| **Trục Y** | `AVG([Growth Rate (%)])` (dữ liệu Growth 2026) |
| **Kích thước bóng** | `SUM([Population (Millions)])` – bong bóng lớn = dân số đông |
| **Màu sắc** | `[Continent]` hoặc `[Below Replacement]` |
| **Filter** | `[Is Country] = "Country"` |
| **Reference Lines** | Ngang: Y = 0 (zero growth) | Dọc: X = 2.1 (replacement level) |
| **Label** | Hiển thị tên cho top 10 quốc gia đông dân nhất |
| **Quadrant Annotation** | 4 góc phần tư: "Tăng trưởng bền vững", "Bonus nhân khẩu", "Bẫy suy giảm", "Chuyển đổi" |
| **Trend Line** | Linear trend line với R² hiển thị |
| **Tooltip** | "{Entity} | TFR: {TFR:,.2f} | Growth: {Growth Rate (%):,.2f}% | Pop: {Population (Millions):,.1f}M" |

**Câu chuyện**: *"130 quốc gia (54.9%) rơi vào vùng 'TFR dưới mức thay thế' – hầu hết ở Đông Á và Châu Âu. Mối tương quan giữa mức sinh thấp và tăng trưởng âm rất rõ ràng."*

---

### Chart 6: Bản đồ Nhiệt Dân số (Heatmap)
**Mục đích**: Trực quan hóa sự thay đổi dân số qua thời gian cho top quốc gia

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Heatmap (Text Table với Color) |
| **Hàng** | `[Entity]` – Top 15 quốc gia đông dân nhất |
| **Cột** | `[Year]` – Chọn các mốc: 1950, 1970, 1990, 2000, 2010, 2020, 2026, 2030, 2040, 2050 |
| **Màu sắc** | `SUM([Population (Millions)])` – Sequential palette (vàng nhạt → đỏ đậm) |
| **Label** | `SUM([Population (Millions)])` format "###M" |
| **Sort** | Sắp xếp theo dân số năm 2026 giảm dần |
| **Tooltip** | "{Entity} ({Year}): {Population (Millions):,.1f} triệu người" |

---

### Chart 7: Treemap – Phân bổ Dân số Toàn cầu
**Mục đích**: Trực quan hóa tỷ trọng dân số từng quốc gia trong tổng thể

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Treemap |
| **Dimension** | `[Entity]` |
| **Kích thước ô** | `SUM([Population (Millions)])` |
| **Màu sắc** | `[Continent]` hoặc `[Growth Category]` |
| **Label** | `[Entity]` + `SUM([Population (Millions)])` format "###M" |
| **Filter** | `[Is Country] = "Country"`, Year = 2026, Top 30 by Population |
| **Tooltip** | "{Entity}: {Population (Millions):,.1f}M | Tỷ trọng: {SUM(Population (Millions))/TOTAL(SUM(Population (Millions)))*100:,.1f}%" |

**Câu chuyện**: *"India và China chiếm hơn 35% dân số toàn cầu. Top 10 quốc gia chiếm hơn 55% tổng dân số thế giới."*

---

### Chart 8: Bump Chart – Thay đổi Xếp hạng Dân số theo Thời gian
**Mục đích**: Kể câu chuyện "ai vượt ai" qua các thập kỷ

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Bump Chart (Line chart + Rank) |
| **Trục X** | `[Year]` – các mốc thập kỷ: 1950, 1960, ..., 2020, 2026, 2030, 2040, 2050 |
| **Trục Y** | `RANK(SUM([Population (Millions)]))` – đảo ngược (1 ở trên) |
| **Màu sắc / Đường** | `[Entity]` – mỗi quốc gia một đường |
| **Filter** | `[Is Country] = "Country"`, Top 10 by Population at Year 2026 |
| **Marks** | Circle + Line, kích thước circle to hơn tại mốc hiện tại 2026 |
| **Label** | Tên quốc gia tại điểm đầu (1950) và điểm cuối (2050) |
| **Highlight** | India (đỏ), China (vàng), Nigeria (xanh lá) |

**Câu chuyện**: *"India vượt China vào khoảng 2023. Nigeria dự kiến vươn lên vị trí thứ 3 vào 2050, vượt Mỹ."*

**Cách tạo trong Tableau**:
1. Tạo Calculated Field: `[Pop Rank] = RANK(SUM([Value]), 'desc')` (Table Calculation, compute using Entity)
2. Đặt `[Year]` lên Columns, `[Pop Rank]` lên Rows (đảo trục)
3. Đặt `[Entity]` lên Color và Detail
4. Sử dụng Line + Circle marks

---

### Chart 9: Biểu đồ Tròn/Donut – Phân bổ Dân số theo Châu lục
**Mục đích**: Cho thấy Châu Á chiếm đa số, Châu Phi đang tăng mạnh

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Donut Chart (Pie Chart biến thể) |
| **Dimension** | `[Continent]` |
| **Measure** | `SUM([Population (Billions)])` |
| **Màu sắc** | `[Continent]` – palette tùy chỉnh |
| **Label** | Tên châu lục + Phần trăm |
| **Filter** | `[Is Country] = "Country"`, Year = 2026 |
| **Tooltip** | "{Continent}: {Population (Billions):,.2f} tỷ ({Percent of Total:,.1f}%)" |

**Biến thể**: Tạo 2 donut cạnh nhau (2026 vs 2050) để so sánh sự chuyển dịch tỷ trọng.

**Cách tạo Donut trong Tableau**:
1. Tạo Pie Chart bình thường
2. Thêm 1 Dual Axis với vòng tròn trắng nhỏ hơn ở giữa
3. Đặt số liệu tổng (8.3 tỷ) ở trung tâm

---

### Chart 10: So sánh Dự báo – Thực tế vs Mô hình (Dual-Axis Line)
**Mục đích**: Kể chương 3 – "Tương lai phân hóa"

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Loại biểu đồ** | Dual-Axis Line Chart / Combined Chart |
| **Nguồn dữ liệu** | `population_forecast_2050.csv` |
| **Trục X** | `[Year]` (1950 – 2050) |
| **Trục Y** | `SUM([Population])` / 1,000,000 (triệu) |
| **Đường 1** | `Model = "actual_or_un_wpp"` – Đường liền (xanh dương) |
| **Đường 2** | `Model = "linear_regression"` – Đường đứt đoạn (cam) |
| **Filter** | Chọn Top 5 quốc gia: India, China, USA, Indonesia, Nigeria |
| **Trellis / Small Multiples** | Mỗi quốc gia 1 panel nhỏ |
| **Reference Band** | Vùng 2024–2026 tô màu nhạt (giai đoạn xác thực) |
| **Tooltip** | "{Entity} ({Year}) | UN WPP: {Actual}M | Linear Reg: {Forecast}M | Chênh lệch: {Delta}M" |

**Câu chuyện**: *"Mô hình hồi quy tuyến tính (R² = 0.9956) bám sát xu hướng LHQ cho giai đoạn 2016–2023. Tuy nhiên, với các quốc gia chuyển đổi nhân khẩu nhanh như Trung Quốc, mô hình tuyến tính có thể đánh giá thấp tốc độ suy giảm."*

---

## 5. Bộ lọc & Tương tác (Filters & Interactivity)

### 5.1 Bộ lọc chính (Dashboard-level)

| # | Tên bộ lọc | Loại | Mặc định | Áp dụng cho |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Năm (Year)** | Slider (range) | 1950 – 2050 | Tất cả worksheet |
| 2 | **Châu lục (Continent)** | Multi-select dropdown | Tất cả | Tất cả worksheet (trừ Global Trend) |
| 3 | **Trạng thái dữ liệu (DataStatus)** | Multi-select checkbox | Tất cả | Tất cả worksheet |
| 4 | **Quốc gia (Entity)** | Search & select | Không chọn | Chart cụ thể |
| 5 | **Loại thực thể (Is Country)** | Single select | "Country" | Tất cả worksheet |

### 5.2 Tương tác nâng cao

| Tính năng | Mô tả | Cách cài đặt |
| :--- | :--- | :--- |
| **Cross-filtering** | Click vào quốc gia trên Map → filter tất cả chart khác | Dashboard Action → Filter |
| **Highlight** | Hover trên 1 quốc gia → highlight đường/điểm tương ứng trên chart khác | Dashboard Action → Highlight |
| **Drill-down** | Click Châu lục trên Donut → hiển thị chi tiết quốc gia trong châu lục | Set Action hoặc Filter Action với detail sheet |
| **Tooltip Action** | Hover trên Map → hiển thị mini line chart trong tooltip | Viz in Tooltip |
| **Parameter** | Cho phép người dùng chọn năm mục tiêu (2026, 2030, 2040, 2050) | Parameter + Calculated Field |
| **URL Action** | Click vào quốc gia → mở trang Our World in Data tương ứng | Dashboard Action → URL: `https://ourworldindata.org/grapher/population?country=<Code>` |

### 5.3 Viz in Tooltip (Biểu đồ mini trong Tooltip)
Tạo worksheet phụ `[Tooltip - Population Trend Mini]`:
- Line chart nhỏ (300×200 px)
- X = Year (1950–2050), Y = Population (Millions)
- Filter theo Entity từ worksheet chính
- Nhúng vào tooltip bằng: `Insert` → `Sheets` → `[Tooltip - Population Trend Mini]`

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

## 7. KPI Cards (Thẻ Chỉ số Chính)

Tạo 4 KPI Cards ở đầu Dashboard:

| # | Tên KPI | Giá trị (Year = 2026) | Calculated Field |
| :---: | :--- | :--- | :--- |
| 1 | 🌍 Dân số Toàn cầu | 8.30 tỷ | `SUM([Population (Billions)])` filter Entity = "World" |
| 2 | 📈 Tốc độ Tăng trưởng TB | 0.88% | `AVG([Growth Rate (%)])` filter Is Country |
| 3 | 📉 Quốc gia Suy giảm | 65 | `COUNTD(IF [Growth Rate (%)] < 0 THEN [Entity] END)` |
| 4 | 👶 TFR Trung vị Toàn cầu | 2.14 | `MEDIAN([TFR])` |

**Thiết kế KPI Card**:
- Nền: `#16213E` với viền trái 4px màu accent
- Giá trị chính: Font 36pt Bold, màu trắng
- Label phụ: Font 10pt, màu `#8B8B9E`
- Icon: Emoji hoặc icon font

---

## 8. Story Points (Tableau Story)

Tạo Tableau Story với 5 Story Points kể câu chuyện tuần tự:

### Story Point 1: "Bức tranh Tổng quan"
- Dashboard: KPI Cards + Global Trend + Map
- Caption: *"Dân số thế giới đã vượt 8.3 tỷ người vào năm 2026, nhưng tốc độ tăng trưởng đang chậm lại đáng kể so với đỉnh điểm thập niên 1960."*

### Story Point 2: "Những Gã Khổng lồ"
- Dashboard: Top 15 Bar Chart + Bump Chart
- Caption: *"India chính thức vượt China vào 2023. Nigeria được dự báo sẽ vươn lên vị trí thứ 3 vào 2050."*

### Story Point 3: "Làn sóng Suy giảm"
- Dashboard: Growth Distribution + Scatter TFR vs Growth
- Caption: *"65 quốc gia đang trong chu kỳ suy giảm dân số. 130/237 quốc gia có mức sinh dưới ngưỡng thay thế (TFR < 2.1)."*

### Story Point 4: "Bản đồ Phân hóa"
- Dashboard: Map (màu = Growth Rate) + Heatmap + Treemap
- Caption: *"Châu Phi cận Sahara tiếp tục bùng nổ dân số trong khi Đông Á và Châu Âu thu hẹp – thế giới đang phân hóa sâu sắc."*

### Story Point 5: "Nhìn về Tương lai 2050"
- Dashboard: Forecast Comparison + Donut 2026 vs 2050
- Caption: *"Mô hình dự báo cho thấy sự chuyển dịch trọng tâm dân số từ Châu Á sang Châu Phi sẽ định hình lại trật tự kinh tế – xã hội toàn cầu."*

---

## 9. Hướng dẫn Triển khai từng Bước

### Bước 1: Chuẩn bị Dữ liệu
1. Mở Tableau Desktop → Connect → Text file
2. Nạp `data/processed/population_fact_long.csv`
3. Nạp `data/processed/population_forecast_2050.csv` (New Data Source hoặc Join)
4. Kiểm tra data type: `Year` = Number (Whole), `Value` = Number (Decimal), `Code` = String

### Bước 2: Tạo Calculated Fields
1. Tạo tất cả Calculated Fields từ Mục 3
2. Kiểm tra `[Is Country]` filter hoạt động đúng (237 quốc gia)
3. Tạo `[Continent]` Group hoặc tải `continent_mapping.csv`

### Bước 3: Tạo Individual Worksheets
1. Tạo 10 worksheet theo đặc tả ở Mục 4
2. Đặt tên worksheet có tiền tố số thứ tự: `01-GlobalTrend`, `02-GeoMap`, ...
3. Thiết lập tooltip với Viz in Tooltip cho Map

### Bước 4: Ghép Dashboard
1. Tạo Dashboard mới → kích thước 1920 × 1080 (hoặc Automatic)
2. Kéo thả các worksheet theo layout ở Mục 4
3. Thêm Filter Actions, Highlight Actions
4. Thêm KPI Cards (dùng worksheet riêng cho mỗi KPI)
5. Thêm Header text box và Footer

### Bước 5: Tạo Story
1. Tạo Tableau Story với 5 Story Points
2. Thêm caption cho mỗi Story Point
3. Thiết lập Navigator style

### Bước 6: Kiểm tra & Xuất bản
1. Kiểm tra cross-filtering hoạt động giữa Map ↔ Bar ↔ Scatter
2. Kiểm tra tooltip hiển thị đúng giá trị
3. Kiểm tra bộ lọc Year slider hoạt động trơn tru
4. Export dưới dạng `.twbx` (Packaged Workbook)
5. Hoặc publish lên Tableau Public

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

*Tài liệu này được tạo tự động bởi pipeline phân tích dân số. Phiên bản: 2026-09-22.*
