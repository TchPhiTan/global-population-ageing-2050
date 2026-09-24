# Tóm tắt Khám phá Dữ liệu Dân số Toàn diện (EDA đến năm 2026)

## 1. Xu hướng Dân số Toàn cầu tại Mốc 2026
- **Dân số thế giới năm hiện tại (2026)**: Đạt xấp xỉ **8,300,678,396 người** (~8.30 tỷ người).
- **Dự báo đạt đỉnh (LHQ medium scenario)**: Dân số toàn cầu dự kiến tiếp tục tăng và đạt đỉnh vào năm **2084** ở mức **10,289,315,239 người** (~10.29 tỷ người).
- **Phân tách số liệu**: Giai đoạn 1950 - 2023 phản ánh số liệu ước tính lịch sử (`estimate`), từ 2024 - 2026 trở đi phản ánh số liệu cập nhật hiện tại theo kịch bản chuẩn của UN WPP và đối chiếu kiểm chứng chéo WPR.

## 2. Top 10 Quốc gia Đông dân nhất Thế giới (Năm 2026)
| Thứ hạng | Quốc gia | Dân số năm 2026 (người) | Quy mô (triệu người) |
| :---: | :--- | :---: | :---: |
| 1 | India | 1,476,625,571 | 1,476.6M |
| 2 | China | 1,412,914,090 | 1,412.9M |
| 3 | United States | 349,035,484 | 349.0M |
| 4 | Indonesia | 287,886,782 | 287.9M |
| 5 | Pakistan | 259,299,792 | 259.3M |
| 6 | Nigeria | 242,431,835 | 242.4M |
| 7 | Brazil | 213,562,666 | 213.6M |
| 8 | Bangladesh | 177,818,039 | 177.8M |
| 9 | Russia | 143,394,457 | 143.4M |
| 10 | Ethiopia | 138,902,185 | 138.9M |

## 3. Động lực Tăng trưởng & Xu hướng Phân hóa Dân số năm 2026
- **Năm phân tích**: 2026 trên 237 quốc gia và vùng lãnh thổ.
- **Biên độ tăng trưởng**: Thấp nhất -4.16% đến Cao nhất 3.28%.
- **Quốc gia suy giảm dân số (tăng trưởng âm)**: Đến năm 2026, đã có **65** quốc gia/vùng lãnh thổ ghi nhận tỷ lệ tăng trưởng âm (tăng từ 54 quốc gia năm 2023), phản ánh rõ làn sóng suy giảm dân số mở rộng tại Đông Á và Châu Âu.
- **Quốc gia tiếp tục tăng trưởng**: Còn **172** quốc gia/vùng lãnh thổ duy trì tốc độ dương, dẫn đầu bởi các nước Châu Phi cận Sahara.

## 4. Tác động của Mức sinh (TFR 2023) đối với Tăng trưởng Dân số năm 2026
- Đánh giá trên **237** quốc gia/vùng lãnh thổ có đầy đủ dữ liệu.
- **Dưới mức sinh thay thế (TFR < 2.1)**: **130** trên 237 quốc gia (54.9%) có mức sinh không đạt ngưỡng thay thế, dẫn tới nguy cơ suy giảm dân số kéo dài sau năm 2026.
- **Tương quan nhân quả**: Các quốc gia có TFR < 1.5 (như Hàn Quốc, Nhật Bản, một số nước Nam Âu) đều rơi sâu vào vùng tăng trưởng âm trong năm 2026.

## 5. Kiểm chứng Chéo Dữ liệu Thực tế Hiện tại (UN WPP vs World Population Review 2024 - 2026)
- **Tỷ lệ khớp thực thể**: **705 / 705 bản ghi (100.0%)** khớp hoàn hảo giữa UN WPP và WPR sau khi chuẩn hóa bảng ánh xạ định danh quốc tế (Alias Mapping).
- **Mức độ tương đồng về quy mô**: Sai lệch tương đối trung bình < 0.05% trên các quốc gia chủ chốt (Ấn Độ, Trung Quốc, Mỹ, Indonesia, Việt Nam đạt độ khớp gần như tuyệt đối).
- **Ý nghĩa**: Xác thực rằng các dự phóng giai đoạn 2024 - 2026 của UN WPP Medium Scenario hoàn toàn trùng khớp với dữ liệu thống kê cập nhật của World Population Review, tạo nền tảng vững chắc cho mô hình hóa.

## 6. Định hướng cho Bước Tiếp theo (Modeling & Dashboard Tableau)
1. **Mô hình Dự báo Dân số (2026 - 2050)**: Sử dụng Hồi quy Tuyến tính / Xu hướng Thời gian (Linear Regression / Time Series Trend) huấn luyện trên dữ liệu 1950 - 2023 và kiểm định trên giai đoạn 2024 - 2026 trước khi dự phóng đến năm 2050.
2. **Mô hình Phân loại Nguy cơ Suy giảm Dân số (Depopulation Risk)**: Ứng dụng Logistic Regression để phân loại xác suất một quốc gia bước vào chu kỳ suy giảm dân số kéo dài dựa trên TFR < 2.1 và đà tăng trưởng âm năm 2026.
3. **Dashboard Tableau**: Tích hợp fact table kết hợp với kết quả dự báo 2050, thiết kế phân lớp Country vs Region linh hoạt.
