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
