# Population Trends Project Implementation Plan

## 1. Muc tieu

Phan tich xu huong dan so, toc do tang dan so va muc sinh theo quoc gia trong giai doan 1950-2026; so sanh du lieu uoc tinh voi du lieu du bao UN WPP medium scenario; xay dung bo du lieu san sang cho Tableau va mo hinh du bao dan so den nam 2050.

## 2. Pham vi va nguyen tac

- Du lieu OWID/UN WPP la nguon phan tich chinh.
- World Population Review chi dung de doi chieu cac gia tri 2024-2026.
- Khong ghi de hoac sua cac file trong `data/raw/`.
- Khong noi tiep estimate va projected ma khong co cot `DataStatus`.
- Khoa chinh logic cua fact table la `Entity`, `Code`, `Year`.
- Tat ca script co the chay lai tu dau.

## 3. Deliverables

### 3.1 Data processing

- `scripts/preprocess_population_data.py`
- `data/processed/population_fact_long.csv`
- `data/processed/population_fact_wide.csv`
- `data/processed/world_population_review_validation.csv`
- `data/processed/data_dictionary.csv`
- `data/processed/data_quality_report.json`

Fact table long co cac cot:

`Entity`, `Code`, `Year`, `Indicator`, `Value`, `Unit`, `DataStatus`, `Source`, `SourceUrl`.

### 3.2 EDA

- `scripts/run_eda.py`
- `reports/eda/01-global-population-trend.png`
- `reports/eda/02-top-populations.png`
- `reports/eda/03-growth-rate-distribution.png`
- `reports/eda/04-fertility-growth-scatter.png`
- `reports/eda/05-population-heatmap.png`
- `reports/eda/eda_summary.md`

### 3.3 Modeling

- `scripts/forecast_population.py`
- `data/processed/population_forecast_2050.csv`
- `reports/modeling/model_report.md`

Linear regression dung de du bao gia tri dan so. Logistic regression dung de phan loai nguy co suy giam dan so, khong dung de du bao truc tiep population.

### 3.4 Dashboard specification

- `docs/tableau-dashboard-spec.md`

Dashboard can co it nhat 8 loai bieu do, geographic map, bo loc nhieu cap, tooltip, drill-down va cross-filtering.

## 4. Pipeline

1. Doc va kiem tra schema raw.
2. Chuan hoa ten cot, kieu du lieu va gia tri rong.
3. Chuyen ba bang OWID/UN thanh long format.
4. Gan `DataStatus=estimate` cho cot historical va `DataStatus=projected` cho cot medium scenario.
5. Loai bo dong trung khoa va ghi so lieu vao quality report.
6. Doi chieu WPR voi population projected nam 2024-2026 va ghi sai lech.
7. Tao bang wide phuc vu Tableau.
8. Chay EDA truoc khi tao dashboard.
9. Huan luyen mo hinh tren du lieu historical, danh rieng cac nam projected khi danh gia.
10. Tao forecast den 2050 va tai vao Tableau.

## 5. Quality gates

- Dataset chinh co it nhat 5.000 dong.
- Co it nhat 3 bang processed co y nghia.
- `Year` la so nguyen, `Value` la so, khong co khoa trung.
- Moi indicator co don vi va DataStatus.
- Khong co missing trong cac cot khoa.
- Missing value trong cot chi tieu duoc bao cao, khong tu dong dien gia tri neu khong co co so.
- EDA co 3-5 bieu do va file tom tat.
- Mo hinh co train/test split theo thoi gian va metric phu hop.
- Dashboard co map va it nhat 8 loai chart.

## 6. Thu tu thuc thi

- [ ] Tao preprocessing pipeline va data dictionary.
- [ ] Chay preprocessing va vuot quality gates.
- [ ] Tao EDA va insight summary.
- [ ] Tao mo hinh du bao va danh gia.
- [ ] Tao dashboard specification va calculated fields.
- [ ] Nap cac file processed vao Tableau va kiem tra tuong tac.
- [ ] Cap nhat README va tai lieu nguon.