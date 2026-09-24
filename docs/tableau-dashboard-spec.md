# Đặc tả Dashboard Tableau: Biến động Dân số & Xu hướng Già hoá Dân số Toàn cầu (1950 – 2050)

## 1. Tổng quan & Câu chuyện Dữ liệu (Data Story)

### 1.1 Mục tiêu Dashboard
Dashboard kết hợp hài hòa hai chủ đề cốt lõi:
1. **Biến động Dân số Toàn cầu**: Quy mô dân số, tốc độ tăng trưởng, mức sinh TFR qua 3 chương lịch sử - hiện tại - tương lai.
2. **Xu hướng Già hoá Dân số**: Tốc độ chuyển dịch cơ cấu tuổi, tuổi trung vị, tỷ số phụ thuộc và làn sóng các xã hội siêu già đến năm 2050.

| Chương | Thời kỳ | Câu chuyện chính |
| :---: | :--- | :--- |
| **Chương 1** | 1950 – 2023 | *"Thế kỷ bùng nổ dân số & Mở màn già hóa"* – Dân số tăng 3.3 lần, tuổi thọ tăng, mức sinh bắt đầu giảm |
| **Chương 2** | 2024 – 2026 | *"Bước ngoặt hiện tại"* – Ấn Độ vượt Trung Quốc, 65 quốc gia suy giảm, tỷ lệ 65+ vượt 10% |
| **Chương 3** | 2027 – 2050 | *"Tương lai phân hóa & Làn sóng Siêu già"* – Thế giới bước vào ngưỡng Xã hội Già (16.4%), >60 nước siêu già |

### 1.2 Thông điệp chính (Key Insights)
1. **8.3 tỷ người** (2026) → Dự kiến đạt đỉnh **~10.3 tỷ** vào năm 2084 rồi giảm dần.
2. **Ấn Độ** chính thức vượt **Trung Quốc** thành quốc gia đông dân nhất thế giới.
3. **65 quốc gia** đang trong chu kỳ suy giảm dân số tính đến năm 2026.
4. **130/237** quốc gia có tỷ suất sinh dưới mức thay thế (TFR < 2.1).
5. **Già hoá tăng tốc**: Tỷ lệ người cao tuổi (65+) tăng từ 5.0% (1950) lên 10.3% (2026) và đạt **16.4% vào năm 2050**.
6. **Tuổi trung vị toàn cầu**: Tăng từ 23.5 tuổi (1950) lên **36.2 tuổi (2050)** (Châu Âu và Đông Á vượt 45-48 tuổi).

---

## 2. Nguồn Dữ liệu & Cấu trúc

### 2.1 Bảng dữ liệu chính

| # | Tên file | Vai trò | Hàng | Cột chính |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `population_fact_long.csv` | Fact table chính (1950–2100) | **~352,000** | Entity, Code, Year, Indicator, Value, Unit, DataStatus |
| 2 | `population_fact_wide.csv` | Phiên bản wide cho phân tích | **~39,000** | Entity, Code, Year, Population, GrowthRate, TFR, MedianAge, Share65, DepRatio |
| 3 | `population_forecast_2050.csv` | Dự báo Linear Regression | **~24,000** | Entity, Code, Year, Population, Older_People_65plus, Share_65plus, DataStatus, Model |
| 4 | `country_risk_classification_2050.csv` | Phân loại rủi ro Logistic Regression | **237** | Entity, Code, Depopulation_Risk_Score, Super_Aged_Risk_Score, Super_Aged_Category |

---

## 3. Calculated Fields (Trường tính toán)

### 3.1 Danh sách Calculated Fields Cốt lõi

| # | Tên trường | Công thức Tableau | Mục đích |
| :---: | :--- | :--- | :--- |
| 1 | `[Is Country]` | *(Xem mục 2.3)* | Lọc quốc gia vs khu vực |
| 2 | `[Population (Millions)]` | `IF [Indicator] = "Population" THEN [Value] / 1000000 END` | Hiển thị dân số theo triệu người |
| 3 | `[Growth Rate (%)]` | `IF [Indicator] = "Population growth rate" THEN [Value] END` | Tốc độ tăng trưởng hàng năm |
| 4 | `[TFR]` | `IF [Indicator] = "Total fertility rate" THEN [Value] END` | Mức sinh (con/phụ nữ) |
| 5 | `[Median Age]` | `IF [Indicator] = "Median age" THEN [Value] END` | Tuổi trung vị |
| 6 | `[Share 65+ (%)]` | `IF [Indicator] = "Share of population aged 65+" THEN [Value] END` | Tỷ lệ người cao tuổi |
| 7 | `[Old-age Dependency Ratio]` | `IF [Indicator] = "Old-age dependency ratio" THEN [Value] END` | Tỷ số phụ thuộc người cao tuổi |
| 8 | `[Ageing Stage]` | `IF [Share 65+ (%)] >= 20 THEN "4. Xã hội Siêu già (>=20%)" ELSEIF [Share 65+ (%)] >= 14 THEN "3. Xã hội Già (14-20%)" ELSEIF [Share 65+ (%)] >= 7 THEN "2. Đang già hoá (7-14%)" ELSE "1. Dân số trẻ (<7%)" END` | Phân cấp già hoá chuẩn UN |
| 9 | `[Data Period]` | `IF [DataStatus] = "estimate" THEN "Lịch sử (Ước tính)" ELSEIF [DataStatus] = "projected" THEN "Dự phóng (UN WPP)" ELSE "Dự báo (Mô hình)" END` | Phân loại giai đoạn cho Legend |
| 10 | `[Below Replacement]` | `IF [TFR] < 2.1 THEN "Dưới mức thay thế" ELSE "Trên mức thay thế" END` | Phân loại TFR |
| 11 | `[Continent]` | *Left Join với `continent_mapping.csv` trên Code* | Nhóm 6 châu lục |

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

## 4. Thiết kế Dashboard – 4 Cụm Chuyên đề & 10 Loại Biểu đồ Khác biệt

Để đáp ứng hoàn hảo tiêu chuẩn **tối thiểu 8 loại biểu đồ khác nhau** (đạt 10 loại) và phục vụ kịch bản Storytelling khoa học, toàn bộ Dashboard được tổ chức thành **4 Cụm Chuyên đề (4 Analytical Clusters)**:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│  TIÊU ĐỀ: "BIẾN ĐỘNG DÂN SỐ TOÀN CẦU & XU HƯỚNG GIÀ HOÁ DÂN SỐ ĐẾN NĂM 2050"                    │
│  [Bộ lọc Toàn cục: Thực thể / Quốc gia (World / Vietnam / ...)] [Thanh trượt Năm: 1950 – 2050] │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│  THẺ KPI CHÍNH (4 Cards Đồng bộ theo Quốc gia & Năm):                                            │
│  [1. Quy mô Dân số]      [2. Tốc độ Tăng trưởng (%)]   [3. Tỷ lệ Người già 65+ (%)]   [4. Mức sinh TFR]  │
├────────────────────────────────────────────────┬────────────────────────────────────────────────┤
│  CỤM 1: QUY MÔ & PHÂN BỐ KHÔNG GIAN            │  CỤM 2: TIẾN TRÌNH & ĐỔI NGÔI LỊCH SỬ          │
│  - Chart 1: Filled Map (Bản đồ Địa lý Thế giới)│  - Chart 4: Area + Line Chart (Xu hướng 1950-50│
│  - Chart 2: Treemap (Cây Tỷ trọng Dân số)      │  - Chart 5: Bump Chart (Hoán đổi Thứ hạng)     │
│  - Chart 3: Horizontal Bar (Top 10 Dân số)     │                                                │
├────────────────────────────────────────────────┼────────────────────────────────────────────────┤
│  CỤM 3: NGUYÊN NHÂN & PHÂN HÓA TĂNG TRƯỞNG     │  CỤM 4: CƠ CẤU TUỔI & DỰ BÁO GIÀ HÓA 2050      │
│  - Chart 6: Histogram (Phân phối Tăng trưởng)  │  - Chart 8: 100% Stacked Area (3 Khối Tuổi)    │
│  - Chart 7: Scatter Plot (Mức sinh TFR vs Grow)│  - Chart 9: Heatmap (Ma trận Già hóa Thập kỷ)  │
│                                                │  - Chart 10: Dual-Axis Line (So sánh ML vs UN) │
└────────────────────────────────────────────────┴────────────────────────────────────────────────┘
```

---

### 🏛️ CỤM 1: QUY MÔ & PHÂN BỐ KHÔNG GIAN (Scale & Spatial Distribution)
* **Giá trị đặc trưng**: Độ lớn quy mô dân số và sự tập trung địa lý (Châu Á chiếm gần 60%, Top 10 quốc gia chiếm >55% dân số toàn cầu).

#### Chart 1: Bản đồ Địa lý – Dân số theo Quốc gia (Filled Map)
* **Loại biểu đồ**: Filled Map (Bản đồ địa lý thế giới Choropleth).
* **Fields**: Geographic dimension `[Code]` / `[Entity]`, Color: `SUM([Population (Millions)])`.
* **Màu sắc**: Sequential Palette (Xanh nhạt $\rightarrow$ Xanh navy sẫm).
* **Tính năng Drill-down**: Click vào bất kỳ quốc gia nào (ví dụ Việt Nam) $\rightarrow$ Tự động lọc tất cả biểu đồ còn lại trong Dashboard.

#### Chart 2: Phân bổ Tỷ trọng Dân số (Treemap)
* **Loại biểu đồ**: Treemap (Biểu đồ diện tích hình chữ nhật lồng ghép).
* **Fields**: Dimension `[Entity]`, Size: `SUM([Population (Millions)])`, Color: `[Continent]`.
* **Ý nghĩa**: Diện tích ô thể hiện trực quan đóng góp của quốc gia vào dân số thế giới (Ấn Độ & Trung Quốc chiếm >35%).

#### Chart 3: Top 10 Quốc gia Đông dân nhất (Horizontal Bar Chart)
* **Loại biểu đồ**: Horizontal Bar Chart (Thanh ngang xếp hạng).
* **Fields**: Rows `[Entity]` (Top 10 by Population), Columns `SUM([Population (Millions)])`.
* **Màu sắc**: Màu nhấn `#2b5c8f`. Highlight riêng Ấn Độ (`#E94560`) và Trung Quốc (`#F5A623`).

---

### ⏳ CỤM 2: TIẾN TRÌNH & ĐỔI NGÔI LỊCH SỬ (Temporal Dynamics & Milestone Shifting)
* **Giá trị đặc trưng**: Thế kỷ bùng nổ dân số (tăng 3.3 lần từ 1950) nhưng đà tăng đang giảm dần về bão hòa; các cuộc đổi ngôi vị thế quyền lực nhân khẩu học.

#### Chart 4: Xu hướng Quy mô Dân số Toàn cầu 1950 – 2050 (Area + Line Chart)
* **Loại biểu đồ**: Area Chart kết hợp Line.
* **Fields**: Trục X `[Year]` (1950 – 2050), Trục Y `SUM([Population (Billions)])`.
* **Màu sắc**: Phân tách 2 vùng: Lịch sử (`estimate`, màu xanh teal `#4ECDC4`) và Dự phóng (`projected`, màu cam `#FF6B6B`).
* **Vạch chuẩn**: Vạch đứng mốc hiện tại năm 2026 (8.3 tỷ người) và chú thích đỉnh dân số ~10.3 tỷ vào năm 2084.

#### Chart 5: Hoán đổi Thứ hạng Dân số theo Thời gian (Bump Chart)
* **Loại biểu đồ**: Bump Chart (Line chart xếp hạng thứ bậc).
* **Fields**: Trục X `[Year]` (1950, 1970, 1990, 2010, 2026, 2040, 2050), Trục Y `RANK(SUM([Population]))` (đảo ngược trục: hạng 1 ở trên cùng).
* **Ý nghĩa**: Đường thứ hạng của Ấn Độ chính thức cắt lên trên Trung Quốc tại mốc 2023–2026; Nigeria vượt Mỹ tiến lên top 3 trước năm 2050.

---

### ⚖️ CỤM 3: NGUYÊN NHÂN & PHÂN HÓA TĂNG TRƯỞNG (Demographic Drivers & Divergence)
* **Giá trị đặc trưng**: Tính phân cực (65 nước suy giảm vs 172 nước tăng) và mối quan hệ nhân quả gốc rễ từ mức sinh giảm sâu dưới ngưỡng thay thế ($TFR < 2.1$).

#### Chart 6: Phân phối Tốc độ Tăng trưởng Dân số (Histogram)
* **Loại biểu đồ**: Histogram (Tần số theo các bin 0.25%).
* **Fields**: Trục X `[Growth Rate (%)]`, Trục Y `COUNT([Entity])`.
* **Reference Line**: Vạch đỏ tại `0%` (Zero-growth threshold) tách biệt 65 nước thu hẹp dân số bên trái và 172 nước tăng trưởng bên phải.

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
  - Trẻ em (0–14 tuổi): Xanh lá `#76c893` (thu hẹp từ 38% xuống 21%).
  - Độ tuổi lao động (15–64 tuổi): Xanh navy `#1e6091` (đạt đỉnh bão hòa rồi giảm dần).
  - Người cao tuổi (65+ tuổi): Đỏ đậm `#d00000` (phình to gấp hơn 3 lần từ 5.0% lên 16.4%).

#### Chart 9: Ma trận Tỷ lệ Già hóa & Tuổi Trung vị theo Thập kỷ (Heatmap / Highlight Table)
* **Loại biểu đồ**: Heatmap (Bảng nhiệt ma trận).
* **Fields**: Hàng `[Entity]` (Top 15 quốc gia), Cột `[Year]` (1970, 1990, 2010, 2026, 2040, 2050), Color & Label: `[Share 65+ (%)]` hoặc `[Median Age]`.
* **Ý nghĩa**: Màu sắc chuyển từ vàng nhạt sang đỏ sẫm thể hiện tốc độ già hóa dựng đứng của các nước Đông Á và Châu Âu.

#### Chart 10: SO SÁNH DỰ BÁO GIÀ HÓA: MÔ HÌNH HỌC MÁY (ML) VS KỊCH BẢN CHUẨN LIÊN HỢP QUỐC (UN WPP)
* **Mục đích**: **Đối chiếu trực tiếp kết quả mô hình Machine Learning tự xây dựng (Linear Regression) với số liệu dự báo mẫu của UN WPP Medium Scenario** trong giai đoạn 2027 – 2050.
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
    * Mô hình Linear Regression ngoại suy tuyến tính dựa trên quán tính gia tốc của chuỗi dữ liệu 30 năm gần nhất (1996–2026).
    * Kịch bản chuẩn UN WPP sử dụng mô hình thành phần Cohort-Component vi mô kết hợp bảng sống (Life Tables) và giả định mức sinh hồi phục nhẹ sau năm 2040.
    * Do đó, ở các quốc gia có mức sinh giảm cực sốc (như Hàn Quốc, Trung Quốc), UN WPP dự báo tỷ lệ già hóa tăng nhanh hơn trong khi Linear Regression có xu hướng thận trọng hơn một chút.
* **Trình diễn Tương tác khi Filter**:
  - Khi xem Toàn cầu (`World`): Cả UN WPP và Mô hình ML cùng chỉ ra năm 2050 tỷ lệ người già đạt **~16.4%** (chính thức bước vào ngưỡng Xã hội Già).
  - Khi chọn `Vietnam`: Cả hai nguồn đều dự phóng Việt Nam sẽ cán mốc **20.5% – 21.1%** người cao tuổi vào năm 2050, xác nhận Việt Nam sẽ chính thức trở thành **Xã hội Siêu già** trước năm 2050.

---

### BẢNG TỔNG HỢP KIỂM TRA 10 LOẠI BIỂU ĐỒ TRÊN DASHBOARD

| STT | Tên Biểu đồ | Loại Biểu đồ trong Tableau | Cụm Chuyên đề | Giá trị Phân tích Cốt lõi |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Bản đồ Dân số Thế giới | **Filled Map** (Choropleth) | Cụm 1: Quy mô & Phân bố | Mật độ phân bố địa lý toàn cầu |
| **2** | Cây Tỷ trọng Dân số | **Treemap** (Rectangles) | Cụm 1: Quy mô & Phân bố | Đóng góp tỷ trọng của từng quốc gia |
| **3** | Top 10 Nước Đông dân | **Horizontal Bar Chart** | Cụm 1: Quy mô & Phân bố | Xếp hạng quy mô tuyệt đối |
| **4** | Xu hướng Dân số 1950–50 | **Area + Line Chart** | Cụm 2: Tiến trình Lịch sử | Đỉnh tăng trưởng và bão hòa |
| **5** | Đổi ngôi Thứ hạng Dân số | **Bump Chart** (Rank Line) | Cụm 2: Tiến trình Lịch sử | Ấn Độ vượt TQ, Nigeria vượt Mỹ |
| **6** | Phân phối Tốc độ Tăng | **Histogram** (Bins) | Cụm 3: Nguyên nhân Suy giảm| 65 nước âm vs 172 nước dương |
| **7** | Mức sinh TFR vs Tăng trưởng | **Scatter Plot** (Bubbles) | Cụm 3: Nguyên nhân Suy giảm| 4 góc phần tư & ngưỡng TFR 2.1 |
| **8** | Chuyển dịch 3 Khối Tuổi | **100% Stacked Area Chart** | Cụm 4: Già hóa & Dự báo ML | Thu hẹp trẻ em, phình to người già |
| **9** | Ma trận Già hóa Thập kỷ | **Heatmap / Highlight Table** | Cụm 4: Già hóa & Dự báo ML | Làn sóng chuyển màu cảnh báo |
| **10**| **So sánh Dự báo ML vs UN**| **Dual-Axis Line Chart** | Cụm 4: Già hóa & Dự báo ML | **Đối chiếu Mô hình ML với Chuẩn LHQ** |

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

## 7. KPI Cards (Thẻ Chỉ số Chính Động theo Quốc gia & Năm)

4 Thẻ KPI được thiết kế **hoàn toàn tương tác (Dynamic Interaction)**. Khi người dùng thay đổi bộ lọc `[Entity]` (mặc định là `World`, hoặc chọn `Vietnam`) và thanh trượt `[Year]` (ví dụ `2026` hoặc `2020`), toàn bộ 4 thẻ KPI sẽ tức thời tính toán lại theo đúng quốc gia và năm đã chọn:

| # | Thẻ KPI | Công thức Calculated Field trên Tableau | Ví dụ: World (2026) | Ví dụ: Vietnam (2020) | Định dạng hiển thị (Format) |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **KPI 1** | 🌍 **Quy mô Dân số** | `SUM(IF [Indicator] = "Population" THEN [Value] END)` | **8.30 Tỷ** | **97.47 Triệu** | Number (Custom): Đơn vị Triệu / Tỷ |
| **KPI 2** | 📈 **Tốc độ Tăng trưởng** | `AVG(IF [Indicator] = "Population growth rate" THEN [Value] END) / 100` | **+0.88%** | **+0.92%** | Percentage (2 chữ số thập phân) |
| **KPI 3** | 👵 **Tỷ lệ Người già 65+** | `AVG(IF [Indicator] = "Share of population aged 65+" THEN [Value] END) / 100` | **10.32%**<br>*(Đang già hoá)* | **8.84%**<br>*(Đang già hoá)* | Percentage kèm subtitle phân loại `[Ageing Stage]` |
| **KPI 4** | 👶 **Mức sinh (TFR)** | `AVG(IF [Indicator] = "Total fertility rate" THEN [Value] END)` | **2.14** | **1.94**<br>*(Dưới thay thế)* | Number (Decimal, 2 số) kèm `[Below Replacement]` |

**Thiết kế Thẻ KPI trên Tableau**:
- Tạo 4 worksheet con độc lập: `KPI-01-Population`, `KPI-02-Growth`, `KPI-03-Share65`, `KPI-04-TFR`.
- Kéo Calculated Field tương ứng vào thẻ **Text** trên Marks Card.
- Định dạng Text: Giá trị chính cỡ chữ 28pt Bold, màu trắng `#FFFFFF`; Phụ đề bên dưới 10pt `#8B8B9E`.
- Tô màu nền thẻ trên Dashboard: Container màu `#16213E`, bo góc nhẹ, viền trái 4px màu Accent (`#4ECDC4` cho Dân số, `#2196F3` cho Tăng trưởng, `#E94560` cho Già hóa, `#F5A623` cho Mức sinh).

---

## 8. Story Points (Tableau Storyboard Kể chuyện Dữ liệu)

Tạo Tableau Story với 5 Story Points nối tiếp nhau theo tiến trình logic:

### Story Point 1: "Bức tranh Tổng quan & Quy mô Địa lý" (Cụm 1)
- **Worksheets ghép**: KPI Cards + `01-GeoMap` + `02-Treemap` + `03-TopPopulations`.
- **Thông điệp (Caption)**: *"Dân số thế giới đã vượt 8.3 tỷ người vào năm 2026, với hơn 55% dân số tập trung tại Top 10 quốc gia, dẫn đầu bởi Ấn Độ và Trung Quốc."*

### Story Point 2: "Tiến trình Lịch sử & Đổi ngôi Quyền lực" (Cụm 2)
- **Worksheets ghép**: `04-GlobalTrend` (Area + Line) + `05-RankBumpChart`.
- **Thông điệp (Caption)**: *"Thế kỷ bùng nổ dân số đang dần khép lại. Dấu mốc lịch sử 2023–2026 chứng kiến Ấn Độ chính thức soán ngôi Trung Quốc; đến 2050, Nigeria sẽ vượt Mỹ để lọt vào Top 3 thế giới."*

### Story Point 3: "Nguyên nhân Gốc rễ: Mức sinh Suy giảm & Phân hóa Toàn cầu" (Cụm 3)
- **Worksheets ghép**: `06-GrowthHistogram` + `07-FertilityGrowthQuadrant`.
- **Thông điệp (Caption)**: *"Phân cực nhân khẩu học: 65 quốc gia đã bước vào chu kỳ suy giảm dân số. Hơn 55% các nước có mức sinh rơi xuống dưới ngưỡng thay thế (TFR < 2.1), đẩy thế giới vào bẫy già hóa."*

### Story Point 4: "Làn sóng Già hóa & Xã hội Siêu già 2050" (Cụm 4)
- **Worksheets ghép**: `08-AgeBracketsTransition` + `09-AgeingDecadeMatrix`.
- **Thông điệp (Caption)**: *"Đến năm 2050, tỷ lệ người cao tuổi (65+) sẽ tăng gấp 3 lần so với năm 1950, chiếm 16.4% dân số toàn cầu. Hơn 60 quốc gia (bao gồm Việt Nam, Nhật Bản, Hàn Quốc, Đức) sẽ chính thức trở thành Xã hội Siêu già."*

### Story Point 5: "Dự phóng Tương lai: So sánh Mô hình Học máy (ML) & Chuẩn Liên Hợp Quốc (UN)" (Cụm 4)
- **Worksheets ghép**: `10-ForecastComparisonMLvsUN`.
- **Thông điệp (Caption)**: *"Mô hình Linear Regression của nhóm bám sát kịch bản chuẩn của UN WPP với độ lệch MAE < 0.8% về tỷ lệ người già, đồng thuận khẳng định tốc độ già hóa của Việt Nam thuộc nhóm nhanh nhất thế giới."*

---

## 9. Hướng dẫn Triển khai Từng Bước trên Tableau (Step-by-Step Implementation Guide)

### Bước 1: Làm mới & Chuẩn hóa Nguồn Dữ liệu (Data Source Setup)
1. Mở Tableau Desktop / Tableau Public và mở tệp [`TTDLTQ FINAL.twb`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT%20CU%E1%BB%90I%20K%E1%BB%B2%20-%20BASIC/TTDLTQ%20FINAL.twb).
2. Vào thẻ **Data** trên menu $\rightarrow$ Bấm chuột phải vào `population_fact_long` $\rightarrow$ Chọn **Refresh** (hoặc bấm `F5`).
   > **Lưu ý**: Dữ liệu hiện tại đã được loại bỏ hoàn toàn 2 cột tĩnh thừa (`Source` và `SourceUrl`), chỉ còn đúng 7 cột chuẩn: `Entity`, `Code`, `Year`, `Indicator`, `Value`, `Unit`, `DataStatus`. Kích thước tệp đã giảm xuống còn 23MB giúp Tableau tải và tính toán cực nhanh.
3. Kiểm tra kiểu dữ liệu của các cột:
   - `Code`: Bấm vào biểu tượng kiểu dữ liệu $\rightarrow$ Chọn **Geographic Role** $\rightarrow$ **Country/Region**.
   - `Year`: Đảm bảo là **Number (Whole)** hoặc Date/Year.
   - `Value`: **Number (Decimal)**.
   - `Indicator`, `DataStatus`, `Unit`, `Entity`: **String**.
4. Nạp thêm nguồn phụ `data/processed/population_forecast_2050.csv`:
   - Data $\rightarrow$ New Data Source $\rightarrow$ Text File $\rightarrow$ Chọn `population_forecast_2050.csv` (dùng riêng cho Chart 10).

---

### Bước 2: Tạo Trọn bộ Calculated Fields (Sẵn sàng Copy-Paste)
Vào Data Pane $\rightarrow$ Bấm mũi tên cạnh Search $\rightarrow$ **Create Calculated Field**:

```tableau
// 1. [Population (Millions)]
IF [Indicator] = "Population" THEN [Value] / 1000000 END

// 2. [Population (Billions)]
IF [Indicator] = "Population" THEN [Value] / 1000000000 END

// 3. [Growth Rate (%)]
IF [Indicator] = "Population growth rate" THEN [Value] END

// 4. [TFR]
IF [Indicator] = "Total fertility rate" THEN [Value] END

// 5. [Median Age]
IF [Indicator] = "Median age" THEN [Value] END

// 6. [Share 65+ (%)]
IF [Indicator] = "Share of population aged 65+" THEN [Value] END

// 7. [Old-age Dependency Ratio]
IF [Indicator] = "Old-age dependency ratio" THEN [Value] END

// 8. [Ageing Stage] - Phân cấp Già hoá chuẩn Liên Hợp Quốc
IF [Share 65+ (%)] >= 20 THEN "4. Siêu già (>=20%)"
ELSEIF [Share 65+ (%)] >= 14 THEN "3. Xã hội già (14-20%)"
ELSEIF [Share 65+ (%)] >= 7 THEN "2. Đang già hoá (7-14%)"
ELSE "1. Dân số trẻ (<7%)"
END

// 9. [Below Replacement] - Phân loại Mức sinh
IF [TFR] < 2.1 THEN "Dưới mức thay thế (<2.1)"
ELSE "Trên mức thay thế (>=2.1)"
END

// 10. [Is Country] - Lọc bỏ các thực thể vùng/châu lục để tránh trùng lắp khi xếp hạng
NOT ISNULL([Code]) AND [Code] != "OWID_WRL" AND [Code] != ""

// 11. [Data Period] - Phân tách giai đoạn hiển thị
IF [DataStatus] = "estimate" THEN "1. Lịch sử (1950-2023)"
ELSEIF [DataStatus] = "projected" THEN "2. Dự phóng UN (2024-2100)"
ELSE "3. Dự báo ML (2027-2050)"
END
```

---

### Bước 3: Thao tác Kéo Thả Chi tiết cho Từng Sheet (10 Biểu đồ Khác biệt)

#### 🏛️ CỤM 1: QUY MÔ & PHÂN BỐ KHÔNG GIAN
1. **Sheet 1: `01-GeoMap` (Filled Map - Bản đồ Địa lý)**:
   - Thẻ Marks: Chọn **Map**.
   - Kéo `[Code]` vào **Detail**.
   - Kéo `[Population (Millions)]` vào **Color** (chọn bảng màu Palette: *Blues* hoặc *Teal*).
   - Thẻ Filters: Kéo `[Is Country]` $\rightarrow$ Chọn `True`; Kéo `[Indicator]` $\rightarrow$ Chọn `"Population"`.
   - Cài đặt Tooltip: Kéo `[Entity]`, `[Population (Millions)]`, `[Year]` vào Tooltip.

2. **Sheet 2: `02-Treemap` (Cây Tỷ trọng Dân số)**:
   - Thẻ Marks: Chọn **Square**.
   - Kéo `[Entity]` vào **Detail** và **Label**.
   - Kéo `[Population (Millions)]` vào **Size**.
   - Kéo `[Continent]` (hoặc `[Entity]`) vào **Color**.
   - Thẻ Filters: `[Is Country]` = `True`, `[Indicator]` = `"Population"`.

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
   - Reference Line: Nhấp chuột phải trục X $\rightarrow$ Add Reference Line $\rightarrow$ Chọn giá trị cố định `Year = 2026` với nhãn *"Hiện tại (2026: 8.3 Tỷ)"*.

5. **Sheet 5: `05-RankBumpChart` (Bump Chart - Hoán đổi Thứ hạng Top Quốc gia)**:
   - Thẻ Filters: Chọn Top 7 quốc gia lớn nhất (Ấn Độ, Trung Quốc, Mỹ, Nigeria, Indonesia, Pakistan, Brazil).
   - Columns: Kéo `[Year]` (chọn các mốc 1950, 1970, 1990, 2010, 2026, 2040, 2050).
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
   - Reference Line: Nhấp chuột phải vào trục X $\rightarrow$ Add Reference Line $\rightarrow$ Hằng số `0.0` (Vạch đỏ nét đứt) đánh dấu ngưỡng tăng trưởng bằng 0: Bên trái là 65 nước suy giảm dân số, bên phải là các nước tăng trưởng.

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
   - Thẻ Filters: Kéo `[Indicator]` $\rightarrow$ Chỉ chọn 3 chỉ số:
     * `Children (under-15s)`
     * `Working-age adults (15-64 years)`
     * `Older people (65+ years)`
   - Columns: Kéo `[Year]` (1950 – 2050).
   - Rows: Kéo `SUM([Value])` $\rightarrow$ Nhấp chuột phải $\rightarrow$ **Quick Table Calculation** $\rightarrow$ **Percent of Total** $\rightarrow$ Compute Using **Table (Down)**.
   - Thẻ Marks: Chọn **Area**. Kéo `[Indicator]` vào **Color**:
     * Trẻ em: Xanh lá `#76C893`.
     * Lao động: Xanh navy `#1E6091`.
     * Người già 65+: Đỏ đậm `#D00000`.

9. **Sheet 9: `09-AgeingDecadeMatrix` (Heatmap / Highlight Table - Ma trận Già hóa)**:
   - Thẻ Filters: Lọc Top 15 quốc gia già hoá tiêu biểu (Nhật, Hàn, Ý, Đức, Việt Nam, Trung Quốc, Mỹ,...).
   - Rows: Kéo `[Entity]`.
   - Columns: Kéo `[Year]` (chọn Discrete các mốc: 1970, 1990, 2010, 2026, 2040, 2050).
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
4. **Cài đặt Bộ lọc Toàn cục (Global Filters)**:
   - Bấm vào Sheet Bản đồ $\rightarrow$ Bật bộ lọc `[Entity]` và `[Year]`.
   - Nhấp vào mũi tên trên menu bộ lọc $\rightarrow$ **Apply to Worksheets** $\rightarrow$ Chọn **"Selected Worksheets..."** $\rightarrow$ Tích chọn **TẤT CẢ** các Sheet trong Dashboard (kể cả 4 Thẻ KPI).
   - **Kết quả tương tác**:
     * Mặc định chọn `World` $\rightarrow$ Thẻ KPI và biểu đồ thể hiện số liệu Toàn cầu 8.3 tỷ người năm 2026.
     * Khi người dùng chọn `Vietnam` và kéo thanh trượt về `2020` $\rightarrow$ Toàn bộ 4 thẻ KPI và các biểu đồ tự động chuyển đổi thành 97.47 triệu dân, tăng trưởng 0.92%, mức sinh 1.94 con và tỷ lệ người già 8.84%!
5. **Cài đặt Dashboard Filter Action (Click-to-Filter)**:
   - Trên thanh menu: Dashboard $\rightarrow$ **Actions...** $\rightarrow$ **Add Action** $\rightarrow$ **Filter**.
   - Source Sheets: Chọn `01-GeoMap`, `02-Treemap`, `03-TopPopulations`.
   - Run action on: **Select**.
   - Target Sheets: Tích chọn tất cả các Sheet còn lại trên Dashboard.
   - Clearing the selection will: **Show all values** (hoặc chuyển về World).
6. **Thêm Chú thích Nguồn Dữ liệu ở Chân trang (Footer Note)**:
   - Kéo một Text Box nhỏ ở góc dưới Dashboard (font 9pt, màu `#8B8B9E`):
     * *"Nguồn dữ liệu: Liên Hợp Quốc UN World Population Prospects (2024 Revision) via Our World in Data & World Population Review. Mô hình dự báo: Linear Regression & Logistic Regression (2027–2050)."*
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

*Tài liệu này được tạo tự động bởi pipeline phân tích dân số. Phiên bản: 2026-09-22.*
