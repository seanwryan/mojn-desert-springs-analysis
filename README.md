Desert Springs Water‐Quality & Ecology Analysis
===============================================

**Overview**\
This project analyzes hydrological and ecological data from 250 desert springs monitored by the National Park Service's Mojave Desert Network. We process raw CSVs of water‐quality and site‐condition observations, generate cleaned tables, compute annual summaries and trend analyses, and produce static visualizations.

**Repository Structure**\
data/\
- Raw downloads from NPS (CSV)

output/\
- cleaned/  Intermediate "*_cleaned.csv" files\
- tables/  Final summary tables (annual water‐quality, trend results, ecology flags)\
- plots/  PNG figures illustrating key results

scripts/\
01_load_clean.py   Load raw CSVs and perform cleaning steps\
02_merge_observations.py Combine water‐quality & site metadata into one table\
03_summarize_trends.py Compute annual summaries and trend slopes for each spring\
04_ecology_summary.py Summarize ecological flags (vegetation, invasives, disturbance, wildlife, flow mods)\
05_visualize.py    Generate static plots (time‐series, distributions, bar charts)\
gather_schema.py  Helper to inspect cleaned schemas\
inspect_cleaned.py Quick checks on cleaned CSV outputs

requirements.txt\
- pandas\
- matplotlib

.gitignore\
- Excludes raw and cleaned data, Python cache, OS files

**Prerequisites**\
- Python 3.7 or higher\
- Install dependencies:\
- `pip install -r requirements.txt`

**Getting Started**

1.  Clone or download this repository.

2.  Place the raw NPS CSVs in the `data/` folder (as originally obtained from the IRMA portal).

3.  Run the cleaning script:\
    - `python scripts/01_load_clean.py`\
    - This produces cleaned CSVs under `output/cleaned/`.

4.  Merge observations and metadata:\
    - `python scripts/02_merge_observations.py`\
    - Produces `combined_observations.csv` in `output/tables/`.

5.  Summarize annual water‐quality and compute trends:\
    - `python scripts/03_summarize_trends.py`\
    - Outputs `summary_annual_water_quality.csv` and `trend_results.csv`.

6.  Summarize ecological flags by site:\
    - `python scripts/04_ecology_summary.py`\
    - Outputs `ecology_site_summary.csv`.

7.  Generate static visualizations:\
    - `python scripts/05_visualize.py`\
    - PNGs will appear in `output/plots/`.

**Key Outputs**\
- `output/tables/summary_annual_water_quality.csv` Annual means of conductivity, pH, temperature, dissolved oxygen per spring\
- `output/tables/trend_results.csv`       Linear trend slopes, significance (p‐value), and correlation for each parameter & spring\
- `output/tables/ecology_site_summary.csv` Binary flags indicating presence of vegetation, invasives, disturbance, wildlife, flow modifications\
- `output/plots/`                     Figures demonstrating temporal and spatial patterns

**Next Steps**\
- Map springs by chemistry extremes and ecology flags\
- Correlate water‐quality with ecological disturbances\
- Integrate climate data to explain interannual variability\
- Build simple predictive models of spring condition\
- Deploy an interactive dashboard for stakeholders

**Contact & License**\
Sean W. Ryan\

Licensed under the MIT License.
