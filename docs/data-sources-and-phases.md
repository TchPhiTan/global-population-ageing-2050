# Tài liệu Nguồn Dữ liệu & Phương pháp Luận (Data Sources & Methodology)

Tài liệu này lưu trữ đầy đủ đường dẫn nguồn gốc (URLs), đơn vị phát hành, phương pháp thu thập và mô tả chi tiết của từng chỉ số phục vụ cho việc trích dẫn trong Báo cáo Đồ án Cuối kỳ.

---

## 1. Nguồn Dữ liệu Chính: UN World Population Prospects (Biên tập bởi Our World in Data)

Tất cả các chuỗi dữ liệu lịch sử (1950 – 2023) và dự phóng kịch bản trung bình (2024 – 2100) đều được thu thập từ Ban Dân số Liên Hợp Quốc (**United Nations Population Division - UN WPP 2024 Revision**) thông qua hệ thống phân phối của **Our World in Data (OWID)**.

| STT | Chỉ số (Indicator) | Đơn vị (Unit) | Chu kỳ | Đường dẫn Nguồn gốc (Source URL) | Ghi chú Phương pháp |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **1** | **Quy mô Dân số**<br>`Population` | người | 1950–2100 | [OWID: Population with UN Projections](https://ourworldindata.org/grapher/population-with-un-projections) | Đo lường vào ngày 1/7 hàng năm theo biên giới hiện đại. Giai đoạn 2024–2100 theo UN Medium Scenario. |
| **2** | **Tốc độ Tăng trưởng Dân số**<br>`Population growth rate` | % | 1950–2100 | [OWID: Population Growth Rates](https://ourworldindata.org/grapher/population-growth-rates) | Tỷ lệ gia tăng hàng năm kết hợp giữa mức tăng tự nhiên (sinh - tử) và di cư ròng. |
| **3** | **Mức sinh Tổng cộng (TFR)**<br>`Total fertility rate` | con / phụ nữ | 1950–2023 | [OWID: Children Born per Woman](https://ourworldindata.org/grapher/children-born-per-woman) | Số con trung bình một phụ nữ sẽ sinh trong độ tuổi sinh đẻ. Ngưỡng thay thế chuẩn là 2.1. |
| **4** | **Tuổi Trung vị**<br>`Median age` | tuổi (năm) | 1950–2100 | [OWID: Median Age](https://ourworldindata.org/grapher/median-age) | Tuổi chia đôi dân số thành hai nửa bằng nhau. Thước đo tổng hợp trực quan nhất về già hóa. |
| **5** | **Tuổi thọ Trung bình khi sinh**<br>`Life expectancy` | tuổi (năm) | 1950–2023 | [OWID: Life Expectancy](https://ourworldindata.org/grapher/life-expectancy) | Số năm trung bình một đứa trẻ sơ sinh kỳ vọng sống nếu mức tử vong theo tuổi giữ nguyên. |
| **6** | **Cơ cấu 3 Nhóm Tuổi**<br>`Older (65+)`, `Working (15-64)`, `Children (<15)` | người | 1950–2100 | [OWID: Age Groups with Projections](https://ourworldindata.org/grapher/population-young-working-elderly-with-projections) | Phân tách chuẩn mực của LHQ thành 3 khối: Dưới 15 tuổi, Độ tuổi lao động (15–64), và Người cao tuổi (65+). |
| **7** | **Tỷ lệ Người cao tuổi 65+**<br>`Share of population aged 65+` | % | 1950–2100 | [OWID: Age Structure](https://ourworldindata.org/age-structure) | Chỉ số dẫn xuất: $\frac{\text{Older (65+)}}{\text{Total Population}} \times 100$. Chuẩn LHQ: $\ge 7\%$ (Đang già hóa), $\ge 14\%$ (Già), $\ge 20\%$ (Siêu già). |
| **8** | **Tỷ số Phụ thuộc Người già**<br>`Old-age dependency ratio` | % | 1950–2100 | [OWID: Dependency Ratios](https://ourworldindata.org/grapher/age-dependency-ratio-projected-to-2100) | Chỉ số dẫn xuất: $\frac{\text{Older (65+)}}{\text{Working-age (15-64)}} \times 100$. Đo lường gánh nặng an sinh xã hội trên 100 lao động. |

---

## 2. Nguồn Kiểm chứng Chéo Độc lập: World Population Review (WPR)

* **Tên tệp thô**: `data/raw/world-population-review-2024-2026.csv`
* **Nhà cung cấp**: [World Population Review (Live Population Clock)](https://worldpopulationreview.com/)
* **Khung thời gian**: 2024 – 2026
* **Mục đích sử dụng**: Làm nguồn độc lập đối chiếu, kiểm chứng chéo (Cross-validation) với số liệu dự báo giai đoạn hiện tại (2024–2026) của UN WPP Medium Scenario.
* **Kết quả đối chiếu**: 100% bản ghi (705/705 dòng) khớp hoàn hảo sau khi chuẩn hóa Alias Mapping quốc tế. Độ lệch tương đối giữa hai nguồn trên các quốc gia lớn nhỏ hơn **0.05%**, khẳng định độ tin cậy tuyệt đối của dữ liệu.

---

## 3. Quy chuẩn Thiết kế Dữ liệu trong Tableau (Data Design Principles)

1. **Tối ưu hóa Hiệu năng & Dung lượng**:
   - Trường URL tĩnh lặp lại (`SourceUrl`) đã được lược bỏ khỏi Fact Table để giảm 50% kích thước tệp (từ 55MB xuống 29MB), giúp Tableau nạp dữ liệu nhanh tức thì.
   - Toàn bộ nguồn gốc, đường dẫn và tài liệu tham khảo được quy chuẩn hóa trong file Markdown này và mục Giới thiệu (About/Methodology) trong Báo cáo Đồ án.
2. **Phân tách Rạch ròi Trạng thái Dữ liệu (`DataStatus`)**:
   - `estimate`: Dữ liệu điều tra thống kê lịch sử (1950 – 2023).
   - `projected`: Dữ liệu viễn cảnh tương lai theo Kịch bản Chuẩn của Liên Hợp Quốc UN WPP (2024 – 2100).
   - `forecast`: Dữ liệu dự báo do Mô hình Machine Learning (Linear Regression) của nhóm tự xây dựng (2027 – 2050).
3. **Mã hóa Định danh Quốc tế**:
   - Sử dụng mã tiêu chuẩn **ISO 3166-1 alpha-3** (`Code`) để Tableau tự động nhận diện vai trò địa lý (Geographic Role: Country/Region) và vẽ bản đồ thế giới mà không xảy ra xung đột tên gọi.
