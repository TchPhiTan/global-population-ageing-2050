# Kế hoạch Phân công Nhiệm vụ & Hướng dẫn Viết Báo cáo Đồ án
## Đề tài: Biến động Dân số & Xu hướng Già hoá Dân số Toàn cầu (1950 – 2050)

> **Cập nhật**: 2026-09-28 | **Môn học**: Trực quan hóa Dữ liệu / Phân tích Dữ liệu  
> **Cơ sở dữ liệu chính**: `data/processed/population_fact_wide.csv` | **Nguồn phụ ML**: `data/processed/population_forecast_2050.csv`  
> **Kiến trúc sản phẩm**: 2-Tab Dashboard lồng trong Tableau Storyboard (10 Biểu đồ + 4 Thẻ KPI)

---

## 1. Cơ cấu Phân công Nhiệm vụ Tổng quát (Nhóm 3 Người)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                CƠ CẤU PHÂN CÔNG NHIỆM VỤ NHÓM 3 NGƯỜI                            │
├───────────────────────────────┬──────────────────────────────────┬───────────────────────────────┤
│ THÀNH VIÊN 1 (TEAM LEADER)    │ THÀNH VIÊN 2 (MEMBER A)          │ THÀNH VIÊN 3 (MEMBER B)       │
├───────────────────────────────┼──────────────────────────────────┼───────────────────────────────┤
│ • 4 Thẻ KPI Cards toàn cục    │ • CỤM 2: Tiến trình Lịch sử      │ • CỤM 4: Cơ cấu Tuổi & ML     │
│ • CỤM 1: Quy mô & Địa lý      │   - Chart 4: Area Trend (Xu hướng)│  - Chart 8: 100% Stacked Area │
│   - Chart 1: Filled Map       │   - Chart 5: Bump Chart (Thứ hạng)│  - Chart 9: Heatmap Già hóa   │
│   - Chart 2: Animated Scatter │ • CỤM 3: Nguyên nhân & Mức sinh  │  - Chart 10: Line ML vs UN    │
│   - Chart 3: Top 10 Bar Chart │   - Chart 6: Histogram Tăng trưởng│ • Viết báo cáo Cụm 4          │
│ • Ghép Dashboard 1, 2 & Story │   - Chart 7: Scatter 4 Góc phần tư│ • Đánh giá đối chiếu mô hình  │
│ • Viết Tổng quan & Kết luận   │ • Viết báo cáo Cụm 2 & Cụm 3     │   Machine Learning            │
└───────────────────────────────┴──────────────────────────────────┴───────────────────────────────┘
```

---

## 2. Phần Phân công Chi tiết cho THÀNH VIÊN 2 (MEMBER A)
> **Phạm vi phụ trách**: Cụm 2 (Tiến trình & Đổi ngôi) + Cụm 3 (Nguyên nhân & Phân hóa Tăng trưởng)  
> **Số lượng biểu đồ**: 4 Worksheets (`04-GlobalTrend`, `05-RankBumpChart`, `06-GrowthHistogram`, `07-FertilityGrowthQuadrant`)  
> **File dữ liệu sử dụng**: `data/processed/population_fact_wide.csv`

---

### 🏛️ CỤM 2: TIẾN TRÌNH & ĐỔI NGÔI LỊCH SỬ

#### Chart 4: Xu hướng Dân số Toàn cầu 1950–2050 (`04-GlobalTrend`)
* **Loại biểu đồ**: Area + Line Chart (Miền diện tích kết hợp đường thẳng).
* **Cấu hình trên Tableau**:
  - `Columns`: Kéo `[Year]` (Continuous, dải 1950 – 2050).
  - `Rows`: Kéo `SUM([Population (Billions)])` (hoặc tạo Calculated Field `[Population] / 1000000000`).
  - `Marks Card`: Chọn **Area**.
  - `Color`: Kéo trường `[Data Period]` vào Color:
    + Vùng Lịch sử (1950–2023): Tô màu Xanh ngọc `#4ECDC4`.
    + Vùng Dự phóng (2024–2050): Tô màu Cam san hô `#FF6B6B`.
  - `Reference Line`: Kẻ đường dọc tại trục X `Year = 2023`, nhãn: *"Hiện tại (2023: 8.09 Tỷ)"*, nét đứt xám.
  - `Filters`: Kéo `[Entity]` $\rightarrow$ Chọn `World`.
* **Khai thác Insight & Số liệu trọng tâm**:
  - Tốc độ bùng nổ: Dân số thế giới tăng gấp 3.2 lần trong hơn 70 năm (từ 2.5 tỷ năm 1950 lên 8.09 tỷ năm 2023).
  - Xu thế uốn cong: Sau năm 2023, đà tăng trưởng chậm dần và tiến tới trạng thái ổn định ~9.66 tỷ người vào năm 2050 trước khi đạt đỉnh ~10.3 tỷ vào thập niên 2080.
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Biểu đồ miền diện tích (Area Chart) minh họa rõ nét tiến trình chuyển đổi giữa hai giai đoạn: Lịch sử và Dự phóng. Giai đoạn 1950–2023 được đặc trưng bởi độ dốc dựng đứng của cuộc bùng nổ dân số thế kỷ 20, đưa quy mô nhân loại từ 2.5 tỷ lên vượt mốc 8.09 tỷ người vào năm 2023. Ở giai đoạn dự phóng (2024–2050), đường cong tăng trưởng bắt đầu bão hòa rõ rệt, hướng tới mốc 9.66 tỷ người vào năm 2050, phản ánh tác động trễ của xu thế giảm mức sinh trên diện rộng."*

---

#### Chart 5: Hoán đổi Thứ hạng Top 7 Quốc gia Đông dân (`05-RankBumpChart`)
* **Loại biểu đồ**: Bump Chart (Line Chart theo dõi thứ bậc xếp hạng).
* **Cấu hình trên Tableau**:
  - `Filters`: 
    + Kéo `[Entity]` $\rightarrow$ Lọc đúng Top 7 quốc gia lớn: *India, China, United States, Nigeria, Indonesia, Pakistan, Brazil*.
    + Kéo `[Year]` $\rightarrow$ Chọn Discrete các mốc chính: *1950, 1970, 1990, 2010, 2023, 2040, 2050*.
  - `Columns`: Kéo `[Year]` (Discrete).
  - `Rows`: Kéo `SUM([Population])` $\rightarrow$ Nhấp chuột phải $\rightarrow$ **Quick Table Calculation** $\rightarrow$ **Rank**.
  - `Compute Using`: Chuột phải lại vào viên thuốc Rank $\rightarrow$ **Compute Using** $\rightarrow$ Chọn **`[Entity]`**.
  - **Đảo ngược trục Y (Cực kỳ quan trọng)**: Chuột phải trục Y $\rightarrow$ **Edit Axis** $\rightarrow$ Tích chọn **`Reversed`** (để Hạng 1 nằm ở đỉnh trên cùng).
  - `Marks Card`: Chọn **Line**. Kéo `[Entity]` vào thẻ **Color** và thẻ **Label**.
* **Khai thác Insight & Số liệu trọng tâm**:
  - Giao điểm lịch sử năm 2023: Ấn Độ chính thức vượt Trung Quốc giành vị trí số 1.
  - Ngôi sao mới nổi: Nigeria từ vị trí số 6 (năm 1950) sẽ chính thức vượt qua Hoa Kỳ để lọt vào Top 3 thế giới trước năm 2050.
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Biểu đồ Bump Chart phác họa trực quan sự tái định hình trật tự địa chính trị - nhân khẩu học toàn cầu qua một thế kỷ. Điểm nhấn lớn nhất là giao điểm lịch sử vào năm 2023 khi Ấn Độ chính thức vượt qua Trung Quốc để giữ vị thế quốc gia đông dân nhất thế giới. Đáng chú ý, nhờ mức sinh duy trì ở mức cao, Nigeria được dự báo sẽ vượt qua Hoa Kỳ vào thập niên 2040 để vươn lên vị trí thứ 3 toàn cầu, biến Châu Phi thành tâm điểm gia tăng quy mô dân số mới."*

---

### ⚖️ CỤM 3: NGUYÊN NHÂN & PHÂN HÓA TĂNG TRƯỞNG

#### Chart 6: Phân phối Tốc độ Tăng trưởng Dân số (`06-GrowthHistogram`)
* **Loại biểu đồ**: Histogram (Tần số phân phối theo các khoảng bin 0.25%).
* **Cấu hình trên Tableau**:
  - Tạo Bin: Trong Data Pane, chuột phải `[Population growth rate]` $\rightarrow$ Create $\rightarrow$ **Bins...** $\rightarrow$ Nhập Size of bins = `0.25`.
  - `Columns`: Kéo trường `[Population growth rate (bin)]`.
  - `Rows`: Kéo `COUNTD([Entity])`.
  - `Marks Card`: Chọn **Bar**.
  - `Reference Line`: Chuột phải trục X $\rightarrow$ Add Reference Line $\rightarrow$ Chọn hằng số `0.0%` (Vạch đỏ nét đứt).
  - `Filters`: `[Year] = 2023`, `[Is Country] = True`.
* **Khai thác Insight & Số liệu trọng tâm**:
  - Sự phân cực nhị phân: Bên trái vạch 0% là **54 quốc gia** có mức tăng trưởng âm (đang suy giảm dân số); Bên phải là **183 quốc gia** vẫn đang tăng trưởng dương.
  - Phân bổ lệch phải: Đa số các quốc gia tập trung trong dải tăng trưởng khiêm tốn 0.5% – 1.5%/năm.
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Biểu đồ tần số phân phối (Histogram) vạch trần nghịch lý phân cực sâu sắc của bức tranh dân số năm 2023. Mặc dù tổng thể nhân loại vẫn tăng thêm ~70 triệu người/năm, nhưng đã có tới 54 quốc gia và vùng lãnh thổ chính thức rơi vào chu kỳ tăng trưởng âm (<0%), tập trung chủ yếu tại Đông Á và Châu Âu. Sự phân hóa này khẳng định tăng trưởng dân số toàn cầu không còn mang tính đồng nhất mà đang co cụm cục bộ."*

---

#### Chart 7: Ma trận 4 Góc phần tư TFR vs Tốc độ Tăng trưởng (`07-FertilityGrowthQuadrant`)
* **Loại biểu đồ**: 4-Quadrant Scatter Plot (Phân tán bong bóng chia 4 góc phần tư).
* **Cấu hình trên Tableau**:
  - `Columns`: `AVG([Total fertility rate])` (Trục X: Mức sinh con/phụ nữ).
  - `Rows`: `AVG([Population growth rate])` (Trục Y: Tốc độ tăng trưởng hàng năm %).
  - `Marks Card`: Chọn **Circle**. Kéo `[Entity]` vào **Detail**, kéo `SUM([Population (Millions)])` vào **Size**.
  - `Color`: Kéo `[Below Replacement]` (Màu Xanh nếu TFR >= 2.1; Màu Cam nếu TFR < 2.1).
  - `Reference Lines`:
    + Đường dọc trục X: Hằng số $TFR = 2.1$ (Ngưỡng sinh thay thế).
    + Đường ngang trục Y: Hằng số $Growth = 0.0\%$ (Ngưỡng suy giảm dân số).
  - `Filters`: `[Year] = 2023` (hoặc mốc gần nhất có đủ 2 chỉ số), `[Is Country] = True`.
* **Khai thác Insight 4 Góc phần tư**:
  1. *Góc trên bên phải (TFR > 2.1, Growth > 0%)*: Bùng nổ dân số (Châu Phi cận Sahara).
  2. *Góc trên bên trái (TFR < 2.1, Growth > 0%)*: Vùng chuyển đổi (Việt Nam, Ấn Độ - TFR đã dưới 2.1 nhưng dân số vẫn tăng nhẹ nhờ quán tính cơ cấu tuổi trẻ).
  3. *Góc dưới bên trái (TFR < 2.1, Growth < 0%)*: **Bẫy suy giảm dân số** (Hàn Quốc, Nhật Bản, Trung Quốc, Ý).
  4. *Góc dưới bên phải*: Vùng bất thường (hiếm gặp).
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Ma trận phân tán 4 góc phần tư chứng minh mối liên hệ nhân quả gốc rễ giữa mức sinh suy giảm và nguy cơ suy thoái quy mô dân số. Góc dưới bên trái đại diện cho 'bẫy suy giảm' nơi các quốc gia có TFR thấp kỷ lục (Hàn Quốc 0.72, Singapore 0.97) đang gánh chịu tỷ lệ tăng trưởng âm sâu sắc. Đáng lưu ý, Việt Nam đang nằm ở góc trên bên trái — giai đoạn chuyển tiếp then chốt khi mức sinh đã giảm xuống 1.91 con/phụ nữ nhưng dân số vẫn tăng nhẹ nhờ quán tính thế hệ trước, cảnh báo dư địa vàng sắp khép lại trong 10-15 năm tới."*

---

## 3. Phần Phân công Chi tiết cho THÀNH VIÊN 3 (MEMBER B)
> **Phạm vi phụ trách**: Cụm 4 (Cơ cấu Tuổi, Ma trận Già hóa & Đối chiếu Mô hình ML)  
> **Số lượng biểu đồ**: 3 Worksheets (`08-AgeBracketsTransition`, `09-AgeingDecadeMatrix`, `10-ForecastComparisonMLvsUN`)  
> **File dữ liệu sử dụng**: `data/processed/population_fact_wide.csv` và **`data/processed/population_forecast_2050.csv`**

---

### 👵 CỤM 4: CƠ CẤU TUỔI & DỰ BÁO GIÀ HÓA ĐẾN 2050

#### Chart 8: Chuyển dịch 3 Khối Tuổi 1950–2050 (`08-AgeBracketsTransition`)
* **Loại biểu đồ**: 100% Stacked Area Chart (Miền diện tích xếp chồng 100%).
* **Cấu hình trên Tableau**:
  - `Columns`: Kéo `[Year]` (Continuous, 1950 – 2050).
  - `Rows`: Kéo trường **`Measure Values`**.
  - `Marks Card`: Chọn **Area**.
  - `Filters`:
    + Kéo `Measure Names` vào Filters $\rightarrow$ Chỉ chọn đúng 3 trường:
      * `Children (under-15s)`
      * `Working-age adults (15-64 years)`
      * `Older people (65+ years)`
    + Kéo `[Entity]` $\rightarrow$ Mặc định chọn `World`.
  - `Color`: Kéo `Measure Names` vào Color $\rightarrow$ Gán màu:
    + Trẻ em (`Children`): Xanh lá tươi `#76C893`.
    + Lao động (`Working-age`): Xanh Navy `#1E6091`.
    + Người cao tuổi (`Older people 65+`): Đỏ đậm `#D00000`.
  - **Tính phần trăm 100%**: Chuột phải vào `Measure Values` trên Rows $\rightarrow$ **Quick Table Calculation** $\rightarrow$ **Percent of Total** $\rightarrow$ **Compute Using: Table (Down)**.
* **Khai thác Insight & Số liệu trọng tâm**:
  - Người già phình to: Tỷ lệ 65+ tăng gấp hơn 3 lần, từ 5.1% (1950) lên 16.3% (2050).
  - Trẻ em thu hẹp: Tỷ lệ 0–14 tuổi giảm gần một nửa, từ 35% xuống 20%.
  - Bão hòa lao động: Khối tuổi 15–64 đạt đỉnh cực đại về tỷ trọng trong giai đoạn 2010–2020 rồi bước vào giai đoạn co hẹp vĩnh viễn.
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Biểu đồ miền xếp chồng 100% tái hiện sống động sự đảo chiều cấu trúc tuổi của nhân loại qua một thế kỷ. Trong khi khối người trong độ tuổi lao động (15–64 tuổi) đạt đỉnh bão hòa rồi suy giảm dần, thì tỷ lệ trẻ em (dưới 15 tuổi) sụt giảm mạnh mẽ từ 35% xuống chỉ còn 20% vào năm 2050. Ngược lại, nhóm người cao tuổi (65+) tăng tốc gấp hơn 3 lần, chiếm tới 16.3% dân số toàn cầu vào giữa thế kỷ, báo hiệu sự kết thúc của thời kỳ 'Cơ cấu Dân số Vàng' trên diện rộng."*

---

#### Chart 9: Ma trận Tỷ lệ Già hóa theo Thập kỷ Top 15 Quốc gia (`09-AgeingDecadeMatrix`)
* **Loại biểu đồ**: Heatmap / Highlight Table (Bảng nhiệt ma trận).
* **Cấu hình trên Tableau**:
  - `Rows`: Kéo `[Entity]` (Lọc Top 15 quốc gia già hoá tiêu biểu: *Japan, South Korea, Italy, Germany, Vietnam, China, United States, France, Spain...*).
  - `Columns`: Kéo `[Year]` (chọn Discrete các mốc thập kỷ: *1970, 1990, 2010, 2023, 2040, 2050*).
  - `Marks Card`: Chọn **Square**.
  - `Color` & `Label`: Kéo trường `AVG([Share of population aged 65+])`.
  - `Edit Colors`: Chọn Palette *Red-Yellow-Green Diverging* $\rightarrow$ Tích chọn **Reversed** (để tỷ lệ người già cao tô màu đỏ sẫm báo động).
* **Khai thác Insight & Số liệu trọng tâm**:
  - Siêu già hóa Đông Á: Hàn Quốc và Nhật Bản có tỷ lệ 65+ dự kiến vượt 36% – 40% vào năm 2050 (cứ 5 người thì có 2 người già).
  - Tốc độ phi mã của Việt Nam: Năm 1990 chỉ có 4.8% (Dân số trẻ), đến năm 2023 đạt 8.62% (Đang già hóa), và vọt lên 19.99% (~20.0%) vào năm 2050 (Chính thức trở thành Xã hội Siêu già). Tốc độ già hóa của Việt Nam thuộc nhóm nhanh nhất thế giới.
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Ma trận bảng nhiệt Heatmap phơi bày sự chênh lệch rõ rệt về vận tốc già hóa giữa các nền kinh tế. Nếu như các nước Châu Âu (Đức, Ý) mất từ 60 đến 80 năm để chuyển dịch từ xã hội già hóa sang xã hội già, thì các quốc gia Đông Á và Việt Nam chỉ mất từ 20 đến 25 năm. Sắc đỏ sẫm cảnh báo phủ kín toàn bộ nhóm Top 15 quốc gia vào năm 2050, xác nhận làn sóng 'Siêu già hóa' sẽ là thách thức an sinh và y tế lớn nhất của nửa sau thế kỷ 21."*

---

#### Chart 10: Đối chiếu Dự báo Học máy (ML) vs Kịch bản Chuẩn Liên Hợp Quốc (`10-ForecastComparisonMLvsUN`)
* **Loại biểu đồ**: Dual-Axis Line Chart (Biểu đồ đường đối chiếu sai số).
* **Nguồn dữ liệu**: **⭐ `population_forecast_2050.csv`** (Chứa sẵn cột `Model`).
* **Cấu hình trên Tableau**:
  - `Columns`: Kéo `[Year]` (Continuous, dải 2000 – 2050).
  - `Rows`: Kéo `AVG([Share_65plus])`.
  - `Marks Card`: Chọn **Line**.
  - `Color`: Kéo trường `[Model]`:
    + `un_wpp_medium`: Màu Xanh Navy `#0F3460` (Kịch bản chuẩn Liên Hợp Quốc UN WPP).
    + `linear_regression`: Màu Cam `#F5A623` (Mô hình Học máy do nhóm tự xây dựng).
  - `Reference Line`: Thêm đường tham chiếu ngang tại `Y = 20.0%` đánh dấu *"Ngưỡng Xã hội Siêu già (Super-Aged Society)"*.
  - `Filters`: Kéo `[Entity]` $\rightarrow$ Mặc định `World`, có thể chọn xem riêng `Vietnam`.
* **Khai thác Insight & Số liệu trọng tâm**:
  - Độ chính xác thực nghiệm: Mô hình Linear Regression của nhóm bám sát kịch bản UN WPP với sai số trung bình tuyệt đối $MAE < 0.8\%$ trên quy mô toàn cầu.
  - Dự báo trường hợp Việt Nam: Cả UN WPP (20.0%) và Mô hình ML (20.8%) đều đồng thuận khẳng định Việt Nam sẽ bước qua ngưỡng Xã hội Siêu già (~20%) vào năm 2050.
* **Đoạn văn mẫu đưa vào Báo cáo**:
  > *"Biểu đồ đường đối chiếu thực nghiệm chứng minh độ tương thích cao giữa Mô hình Học máy (Linear Regression) do nhóm xây dựng và Kịch bản Chuẩn UN WPP Medium Scenario giai đoạn 2024–2050. Sai số tuyệt đối trung bình (MAE) ghi nhận ở mức dưới 0.8% trên quy mô toàn cầu. Đặc biệt đối với trường hợp Việt Nam, cả hai mô hình đều hội tụ tại kết luận: Tỷ lệ người cao tuổi 65+ sẽ chính thức chạm ngưỡng 20% vào năm 2050, khẳng định độ tin cậy và giá trị dự báo thực tiễn của pipeline Machine Learning trong bài toán nhân khẩu học."*

---

## 4. Phần Nhiệm vụ của THÀNH VIÊN 1 (TEAM LEADER - BẠN)
1. **Phụ trách Cụm 1**:
   - `01-GeoMap`: Bản đồ phân bố quy mô dân số (tích hợp Viz in Tooltip `Tooltip-CountryTrend`).
   - `02-DemographicTransition`: Animated Scatter Plot theo phong cách Hans Rosling (Tuổi thọ vs Mức sinh, có Pages Animation).
   - `03-TopPopulations`: Horizontal Bar Chart Top 10 nước đông dân nhất.
2. **Phụ trách 4 Thẻ KPI Cards toàn cục**:
   - `KPI-01-Population` (Quy mô dân số - Tỷ/Triệu).
   - `KPI-02-Growth` (Tốc độ tăng trưởng % - So với mốc 0%).
   - `KPI-03-Share65` (Tỷ lệ người già 65% - Phân loại theo ngưỡng UN).
   - `KPI-04-TFR` (Mức sinh - So với ngưỡng thay thế 2.1 con/phụ nữ).
3. **Tích hợp Dashboard & Tableau Story**:
   - Nhận 7 worksheets từ Bạn A và Bạn B.
   - Lắp ráp thành **Dashboard 1** (Quy mô & Lịch sử) và **Dashboard 2** (Phân hóa & Già hóa ML).
   - Cài đặt Dashboard Actions (Filter cho Nhóm A, Highlight cho Nhóm B).
   - Đóng gói 2 Story Points hoàn chỉnh với Executive Captions.
4. **Chắp bút Báo cáo Tổng thể**: Viết Lời mở đầu, Phương pháp thu thập dữ liệu (OWID + WPR), và Kết luận kiến nghị chính sách.

---

## 5. Bảng Tra cứu Màu sắc (Design Tokens) để Nhóm Dùng Thống Nhất

| Vai trò thiết kế | Mã màu Hex | Tên gọi | Dùng cho |
| :--- | :---: | :--- | :--- |
| **Canvas Background** | `#1A1A2E` | Deep Navy | Màu nền của Dashboard |
| **Card Container** | `#16213E` | Midnight Blue | Nền của các thẻ KPI và biểu đồ |
| **Primary Accent (Già hóa/Cảnh báo)** | `#E94560` | Crimson Red | Người già 65+, Nước suy giảm dân số |
| **Secondary Accent (Trẻ em/Lịch sử)** | `#4ECDC4` | Mint Teal | Trẻ em <15 tuổi, Giai đoạn lịch sử, Tăng trưởng dương |
| **Third Accent (Lao động/Dự phóng)** | `#1E6091` | Deep Blue | Khối tuổi lao động 15–64, Kịch bản chuẩn UN |
| **Fourth Accent (ML Forecast/Fertility)** | `#F5A623` | Amber Gold | Đường dự báo Machine Learning, Mức sinh TFR |
| **Text Tiêu đề** | `#EAEAEA` | Light Gray | Tiêu đề và số KPI chính (Font: Arial / Roboto Bold) |
| **Text Phụ đề** | `#8B8B9E` | Muted Gray | Nhãn chú thích, đơn vị |
