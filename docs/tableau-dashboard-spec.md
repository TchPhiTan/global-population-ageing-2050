# TÀI LIỆU ĐẶC TẢ KỸ THUẬT TABLEAU DASHBOARD (TABLEAU DASHBOARD SPECIFICATION)
## DỰ ÁN: PHÂN TÍCH & TRỰC QUAN HÓA DÂN SỐ & GIÀ HÓA TOÀN CẦU (1950 – 2050)

---

## 1. TỔNG QUAN HỆ THỐNG & NGUỒN DỮ LIỆU

### 1.1. Nguồn dữ liệu cốt lõi
* **File dữ liệu chính:** `data/processed/population_fact_wide.csv`
* **Quy mô:** 27,880 dòng dữ liệu chuẩn hóa, giai đoạn 1950 – 2050.
* **Các trường dữ liệu quan trọng:**
  * `Entity`: Tên quốc gia, châu lục hoặc thế giới (`World`).
  * `Code`: Mã định danh ISO-3 (hoặc mã vùng).
  * `Continent`: Châu lục chuẩn tiếng Anh (`Africa`, `Asia`, `Europe`, `North America`, `Oceania`, `South America`).
  * `Region_Type`: Phân loại cấp bậc (`Quốc Gia`, `Châu Lục`, `Thế Giới`, `Vùng & Khối Thu Nhập (Others)`).
  * `Year`: Năm thống kê (1950 đến 2050).
  * `DataStatus`: Trạng thái số liệu (`estimate`: số liệu lịch sử 1950–2021; `projected`: dự phóng UN WPP 2022–2050).
  * `Population`: Dân số tuyệt đối (người).
  * Các chỉ số nhân khẩu học: `Growth rate`, `Total fertility rate (TFR)`, `Life expectancy`, `Median age`, `Share of population aged 65+`, `Old-age dependency ratio`...

### 1.2. Kiến trúc 4 Dashboard Chuyên đề
Hệ thống báo cáo được thiết kế tối giản, hiện đại và tập trung theo 4 Dashboard:
* **Dashboard 1: Tổng quan Dân số Thế giới (1950 – 2050)** *(Hiện tại đang hoàn thiện)*
  * Tương tác đa chiều qua 3 cấp bậc: Toàn cầu (`World`), Châu lục (`Continent`), Quốc gia (`Country`).
  * Gồm: Hệ thống Thẻ KPI, Bản đồ phân dải dân số (kèm Viz-in-Tooltip Sparkline), Bảng xếp hạng Top 10 linh hoạt, Biểu đồ diện tích Lịch sử vs Dự phóng.
* **Dashboard 2: Nguyên nhân & Khủng hoảng Già hóa Dân số** *(Chờ ý tưởng chi tiết từ người dùng)*.
* **Dashboard 3: Chuyển dịch Cấu trúc Tuổi & Lao động**.
* **Dashboard 4: Dự báo Mô hình Máy học (ML) vs Chuẩn Liên Hợp Quốc 2050**.

---

## 2. HỆ THỐNG THAM SỐ ĐIỀU HÀNH TOÀN CỤC (GLOBAL PARAMETERS)

Bộ 4 tham số này điều khiển đồng bộ toàn bộ logic lọc, đổi màu, zoom bản đồ, và tiêu đề trên toàn bộ các biểu đồ:

| Tên Parameter | Data Type | Kiểu giá trị / Danh sách lựa chọn | Mục đích sử dụng |
| :--- | :--- | :--- | :--- |
| **`p_Year`** | Integer | Range: `1950` đến `2050`, Step = `1` | Trục thời gian điều khiển mốc năm trên toàn Dashboard. |
| **`p_Level`** | String | List: `World`, `Continent`, `Country` | Chuyển đổi góc nhìn phân tích (Toàn cầu / Châu lục / Quốc gia). |
| **`p_Chau_Luc`**| String | List: `Africa`, `Asia`, `Europe`, `North America`, `Oceania`, `South America` | Lọc dữ liệu khi `p_Level` = "Continent". |
| **`p_Quoc_Gia`**| String | List các quốc gia lấy từ `Entity` (`Region_Type = "Quốc Gia"`) | Lọc tiêu điểm quốc gia khi `p_Level` = "Country". |

---

## 3. DANH MỤC CALCULATED FIELDS TINH GỌN (CHỈ GIỮ CÁC TRƯỜNG ĐANG DÙNG)

> **Nguyên tắc:** Loại bỏ toàn bộ các trường rác/thừa thãi. Chỉ giữ đúng các trường phục vụ trực tiếp cho các biểu đồ và KPI.

### 3.1. Nhóm nhận diện & Phân loại
* **`Is Country`**
  ```tableau
  [Region_Type] = "Quốc Gia"
  ```
* **`Population Bin`** *(Phân 6 dải quy mô dân số chuẩn quốc tế)*
  ```tableau
  IF [Population] >= 1000000000 THEN "6. Trên 1 tỷ"
  ELSEIF [Population] >= 300000000 THEN "5. 300 triệu - 1 tỷ"
  ELSEIF [Population] >= 100000000 THEN "4. 100 - 300 triệu"
  ELSEIF [Population] >= 30000000 THEN "3. 30 - 100 triệu"
  ELSEIF [Population] >= 10000000 THEN "2. 10 - 30 triệu"
  ELSE "1. Dưới 10 triệu"
  END
  ```

### 3.2. Nhóm phục vụ Bản đồ (`W1A-Map`)
* **`Map Zoom Filter`** *(Tự động thu phóng bản đồ theo góc nhìn parameter)*
  ```tableau
  IF [p_Level] = "World" THEN TRUE
  ELSEIF [p_Level] = "Continent" THEN [Continent] = [p_Chau_Luc]
  ELSE [Entity] = [p_Quoc_Gia]
  END
  ```
* **`Tooltip Mode Context`** *(Dòng tiêu đề ngữ cảnh trong Tooltip)*
  ```tableau
  IF [p_Level] = "World" THEN "🌐 Góc nhìn: Toàn cầu (Bản đồ phân dải dân số)"
  ELSEIF [p_Level] = "Continent" THEN "🧭 Góc nhìn: Châu lục " + [p_Chau_Luc]
  ELSE "📍 Góc nhìn: Tiêu điểm quốc gia " + [p_Quoc_Gia]
  END
  ```

### 3.3. Nhóm phục vụ Bảng xếp hạng Top 10 (`W1B-Top10`)
* **`Top10 Scope Filter`** *(Bộ lọc Context chuẩn bị dữ liệu đầu vào)*
  ```tableau
  [Is Country] AND [Year] = [p_Year] AND (
      [p_Level] = "World" 
      OR [p_Level] = "Country"
      OR ([p_Level] = "Continent" AND [Continent] = [p_Chau_Luc])
  )
  ```
* **`Rank Pop`** *(Thứ hạng dân số)*
  ```tableau
  RANK(SUM([Population]))
  ```
* **`Top10 Display Filter`** *(Lọc hiển thị: World -> Top 10; Continent -> Top 10; Country -> Đúng 1 quốc gia đó)*
  ```tableau
  IF [p_Level] = "World" THEN
      [Rank Pop] <= 10
  ELSEIF [p_Level] = "Continent" THEN
      [Rank Pop] <= 10
  ELSE
      ATTR([Entity]) = [p_Quoc_Gia]
  END
  ```
  *(Lưu ý: Compute Using theo `Entity` hoặc `Table (down)`)*.
* **`Top10 Bar Color`** *(Tô màu phân biệt thanh được chọn)*
  ```tableau
  IF [p_Level] = "Country" THEN "Quốc gia chọn"
  ELSE "Bảng xếp hạng"
  END
  ```
* **`Top10 Dynamic Title`** *(Tiêu đề sheet tự biến đổi)*
  ```tableau
  IF [p_Level] = "World" THEN "Top 10 Quốc gia Đông dân nhất Thế giới - Năm " + STR([p_Year])
  ELSEIF [p_Level] = "Continent" THEN "Top 10 Đông dân nhất Châu " + [p_Chau_Luc] + " - Năm " + STR([p_Year])
  ELSE "Quy mô Dân số Quốc gia: " + [p_Quoc_Gia] + " - Năm " + STR([p_Year])
  END
  ```

### 3.4. Nhóm phục vụ Biểu đồ Xu hướng Lịch sử vs Dự phóng (`W1C-TrendArea`)
* **`Trend Dynamic Filter`** *(Chống Double-Counting 55-65 tỷ người, chỉ lấy đúng 1 thực thể)*
  ```tableau
  IF [p_Level] = "World" THEN [Entity] = "World"
  ELSEIF [p_Level] = "Continent" THEN [Entity] = [p_Chau_Luc]
  ELSE [Entity] = [p_Quoc_Gia]
  END
  ```

---

## 4. CHI TIẾT CÁC SHEET THÀNH PHẦN (DASHBOARD 1)

### 4.1. Sheet 1: `W1A-Map` (Choropleth Map - Bản đồ Phân dải Dân số)
* **Loại biểu đồ:** Filled Map (Bản đồ địa lý tô màu theo dải dân số).
* **Cấu hình thẻ Marks:**
  * Loại: **Map**.
  * Color: `Population Bin` (Bảng màu 6 nấc từ nhạt đến đậm dần: Xanh mint $\rightarrow$ Xanh ngọc $\rightarrow$ Xanh dương $\rightarrow$ Xanh navy sẫm).
  * Detail: `Entity`, `Continent`, `p_Year`, `p_Level`, `Tooltip Mode Context`.
* **Bộ lọc (Filters):**
  * `[Is Country]` = `True`.
  * `[Year] = [p_Year]` = `True`.
  * `[Map Zoom Filter]` = `True` (Chuột phải chọn **Add to Context** để hỗ trợ zoom mượt mà).
* **Định dạng Tooltip Minimalism (Có tích hợp Viz-in-Tooltip):**
  ```text
  <Tooltip Mode Context>
  ────────────────────────────────────────────────
  <Entity> (<Continent>)

  Năm thống kê: <p_Year>
  Dân số: <SUM(Population)> người
  Quy mô: <Population Bin>

  Xu hướng dân số (1950 – 2050)
  <Sheet name="Tooltip-PopTrend" maxwidth="290" maxheight="100" filter="<Entity>">
  ```

### 4.2. Sheet Phụ: `Tooltip-PopTrend` (Mini Sparkline trong Tooltip)
* **Loại biểu đồ:** Dual-Axis Line + Circle (Trục kép).
* **Columns:** `Year` (Continuous 1950 – 2050).
* **Rows (Trục 1):** `SUM(Population)` $\rightarrow$ Mark: **Line** (Color: `DataStatus` - Xanh ngọc lịch sử, Cam dự phóng; nét mảnh).
* **Rows (Trục 2):** `IF [Year] = [p_Year] THEN [Population] END` $\rightarrow$ Mark: **Circle** (Màu cam/đỏ nổi bật, mốc năm hiện tại).
* **Format Minimalism:** Ẩn toàn bộ Header trục Y, xóa sạch Gridlines, bỏ viền, thiết lập `Entire View`.

### 4.3. Sheet 2: `W1B-Top10` (Horizontal Bar Chart - Bảng xếp hạng linh hoạt)
* **Loại biểu đồ:** Horizontal Bar Chart (Thanh ngang nằm ngang).
* **Rows:** `Entity` (Chuột phải Sort by Field: `Population`, Descending).
* **Columns:** `SUM(Population)`.
* **Color:** `Top10 Bar Color` (`Quốc gia chọn`: Đỏ cam `#EF4444`; `Bảng xếp hạng`: Xanh Navy `#2B5C8F`).
* **Labels:** Bật nhãn số ở cuối mỗi thanh (`SUM(Population)`), font chữ 9pt Semi-Bold.
* **Bộ lọc (Filters):**
  * `[Top10 Scope Filter]` = `True` (Thêm vào **Context**).
  * `[Top10 Display Filter]` = `True` (Compute Using: `Entity`).
* **Format Minimalism:** Ẩn Header trục X dưới đáy, tắt Gridlines, tiêu đề chèn `<Top10 Dynamic Title>`.
* **Tooltip:**
  ```text
  XẾP HẠNG & QUY MÔ DÂN SỐ • NĂM <p_Year>
  ────────────────────────────────────────
  <Entity> (<ATTR(Continent)>)

  🏆 Vị thế: Hạng <Rank Pop>
  👥 Dân số: <SUM(Population)> Người
  ```

### 4.4. Sheet 3: `W1C-TrendArea` (Area + Line Chart - Xu hướng Lịch sử vs Dự phóng)
* **Loại biểu đồ:** Dual-Axis Area + Line (Diện tích mờ kết hợp đường viền sắc nét).
* **Columns:** `Year` (Continuous 1950 – 2050).
* **Rows (Trục 1):** `SUM(Population)` $\rightarrow$ Mark: **Area**, Color: `DataStatus` (Opacity 40-50%).
* **Rows (Trục 2):** `SUM(Population)` $\rightarrow$ Mark: **Line**, Color: `DataStatus` (Opacity 100%, nét mảnh).
  * Đồng bộ trục (Synchronize Axis) và ẩn trục phụ bên phải.
* **Bảng màu:**
  * `estimate` (Lịch sử): Xanh Teal thanh lịch `#0D9488`.
  * `projected` (Dự phóng): Cam san hô `#F97316`.
* **Vạch chuẩn tương tác (Reference Line):**
  * Thêm Reference Line trên trục X: Giá trị gắn với Parameter `p_Year`, nét đứt màu xám `#64748B`.
* **Bộ lọc (Filters):**
  * `[Trend Dynamic Filter]` = `True`.
* **Format Minimalism:** Tắt Gridlines, giữ trục số chính, định dạng nhãn theo Tỷ/Triệu người.

---

## 5. THIẾT KẾ BỐ CỤC LẮP GHÉP DASHBOARD 1 (LAYOUT & CONTAINERS)

### 5.1. Kích thước & Cấu trúc tổng thể
* **Kích thước Dashboard:** Cố định `1440 x 900 px` (chuẩn Desktop hiện đại) hoặc `1366 x 768 px`.
* **Màu nền toàn bộ:** Trắng ngà nhạt `#F8FAFC` tạo cảm giác sang trọng, các khung chứa biểu đồ nền trắng tinh `#FFFFFF` bo góc nhẹ hoặc có viền mờ `#E2E8F0`.

### 5.2. Sơ đồ Wireframe Bố cục Dashboard 1

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [HEADER]: TỔNG QUAN DÂN SỐ THẾ GIỚI (1950 – 2050)                                       │
│ [CONTROLS]: 📅 p_Year (Slider) | 🌐 p_Level (Dropdown) | 🧭 p_Chau_Luc | 📍 p_Quoc_Gia   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ [KPI CONTAINER - 4 THẺ CHỈ SỐ]:                                                         │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌─────────────────────┐ │
│ │ 👥 TỔNG DÂN SỐ   │ │ 🏆 VỊ THẾ TOÀN CẦU│ │ 📈 TỐC ĐỘ TĂNG   │ │ 👵 TỶ LỆ 65+ TUỔI   │ │
│ │ 8.09 Tỷ người    │ │ Hạng 1 Toàn cầu  │ │ +0.88% / năm     │ │ 10.0% dân số        │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ └─────────────────────┘ │
├───────────────────────────────────────────┬────────────────────────────────────────────┤
│ [CỘT TRÁI - 55% BỀ NGANG]:                │ [CỘT PHẢI - 45% BỀ NGANG]:                 │
│                                           │ (Vertical Container chứa 2 biểu đồ)        │
│ SHEET: W1A-Map                            ├────────────────────────────────────────────┤
│ * Bản đồ địa lý phân dải 6 nhóm dân số    │ SHEET: W1B-Top10                           │
│ * Zoom động theo World / Continent / Ctry │ * Top 10 Đông dân nhất                     │
│ * Tooltip chứa Mini Sparkline lịch sử     │ * Highlight nước chọn khi ở mode Country   │
│                                           ├────────────────────────────────────────────┤
│                                           │ SHEET: W1C-TrendArea                       │
│                                           │ * Biểu đồ diện tích Lịch sử vs Dự phóng    │
│                                           │ * Vạch đứt mốc năm trượt theo p_Year       │
└───────────────────────────────────────────┴────────────────────────────────────────────┘
```

---

## 6. SẴN SÀNG CHO DASHBOARD 2
Toàn bộ thông số, logic tính toán và thiết kế của **Dashboard 1** đã được khóa chuẩn xác trong tài liệu này. 

Hệ thống đã sẵn sàng để lắp ghép Dashboard 1 và đón nhận toàn bộ ý tưởng cấu trúc, chủ đề từ người dùng cho **Dashboard 2**!
