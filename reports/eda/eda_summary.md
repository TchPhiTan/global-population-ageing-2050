# Báo cáo Phân tích Khám phá Dữ liệu (EDA): Biến động Dân số & Xu hướng Già hoá Toàn cầu đến năm 2050

## 1. Trụ cột 1: Biến động Quy mô & Tăng trưởng Dân số Toàn cầu (1950 – 2050)
* **Quy mô dân số mốc hiện tại (2026)**: Đạt xấp xỉ **8,300,678,396 người (~8.30 tỷ người)**.
* **Dự báo dân số đến năm 2050 (UN WPP Medium Scenario)**: Đạt xấp xỉ **9,664,378,585 người (~9.66 tỷ người)**.
* **Đỉnh tăng trưởng**: Tốc độ tăng trưởng hàng năm đạt đỉnh vào thập niên 1960 (~2.1%/năm) và liên tục giảm dần, dự kiến chỉ còn dưới 0.4%/năm vào năm 2050.
* **Phân hóa tăng trưởng năm 2026**:
  - Đã có **65 quốc gia/vùng lãnh thổ** ghi nhận mức tăng trưởng âm (suy giảm dân số), chủ yếu tập trung tại Đông Á (Hàn Quốc, Nhật Bản, Trung Quốc) và Đông/Nam Âu.
  - Còn **172 quốc gia/vùng lãnh thổ** duy trì tăng trưởng dương, dẫn đầu bởi các nước Châu Phi cận Sahara.
* **Top 10 quốc gia đông dân nhất 2026**: 
  1. Ấn Độ (1,476.6M) - chính thức vượt Trung Quốc
  2. Trung Quốc (1,412.9M)
  3. Hoa Kỳ (349.0M)
  4. Indonesia (287.9M)
  5. Pakistan (259.3M)

---

## 2. Trụ cột 2: Xu hướng Già hoá Dân số Toàn diện đến Năm 2050
* **Tỷ lệ người cao tuổi (65+ tuổi) tăng gấp 3 lần**:
  - Năm 1950: Chỉ chiếm **5.1%** dân số toàn cầu.
  - Năm 2026: Đã tăng lên **10.6%** (vượt ngưỡng xã hội già hóa 7%).
  - Đến năm 2050: Dự báo đạt **16.3%** dân số toàn cầu (chính thức bước vào ngưỡng Xã hội Già theo chuẩn LHQ >= 14%).
* **Tuổi trung vị toàn cầu (Median Age)**:
  - Năm 1950: **22.2 tuổi**.
  - Năm 2026: **31.1 tuổi**.
  - Năm 2050: **36.1 tuổi** (các khu vực như Châu Âu và Đông Á tuổi trung vị sẽ vượt ngưỡng 45-48 tuổi).
* **Tỷ số phụ thuộc người cao tuổi (Old-age Dependency Ratio)**:
  - Tăng từ **8.4%** (1950) lên **16.2%** (2026) và dự kiến đạt **25.8%** vào năm 2050.
  - Nghĩa là vào năm 2050, cứ khoảng 4 người trong độ tuổi lao động sẽ phải gánh hơn 1 người cao tuổi, tạo áp lực khổng lồ lên an sinh xã hội và y tế.
* **Làn sóng các Xã hội Siêu già (Super-aged Society - Tỷ lệ 65+ >= 20%)**:
  - Đến năm 2050, hơn **60 quốc gia** sẽ trở thành xã hội siêu già. Những nước đứng đầu bao gồm Hàn Quốc, Nhật Bản, Ý, Tây Ban Nha, Hồng Kông với tỷ lệ 65+ dự kiến vượt ngưỡng **35% - 40%**.

---

## 3. Danh mục 8 Biểu đồ EDA Đã Tạo
1. [`01-global-population-trend.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/01-global-population-trend.png): Xu hướng Quy mô Dân số Toàn cầu (1950 – 2050).
2. [`02-top-populations.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/02-top-populations.png): Top 10 Quốc gia Đông dân nhất Thế giới (Năm 2026).
3. [`03-growth-rate-distribution.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/03-growth-rate-distribution.png): Phân phối Tốc độ Tăng trưởng Quốc gia năm 2026.
4. [`04-fertility-growth-scatter.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/04-fertility-growth-scatter.png): Tương quan giữa Mức sinh (TFR) và Tốc độ Tăng trưởng.
5. [`05-population-heatmap.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/05-population-heatmap.png): Ma trận Quy mô Dân số Top 15 Quốc gia qua các Thập kỷ.
6. [`06-global-ageing-trend-2050.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/06-global-ageing-trend-2050.png): Chuyển dịch Cơ cấu 3 Khối Tuổi Toàn cầu (1950 – 2050).
7. [`07-median-age-by-continent.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/07-median-age-by-continent.png): Xu hướng Tăng trưởng Tuổi Trung vị theo Khu vực.
8. [`08-top-super-aged-societies-2050.png`](file:///Users/phitaan/Documents/WORKSPACE/TTDLTQ/PROJECT CUỐI KỲ - BASIC/reports/eda/08-top-super-aged-societies-2050.png): Top 10 Quốc gia có Tỷ lệ Dân số Già (65+) Cao nhất Thế giới năm 2050.
