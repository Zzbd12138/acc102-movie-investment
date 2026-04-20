# acc102-movie-investment
Movie investment analysis dashboard with Streamlit
# Movie Investment Analysis Dashboard

## 1. Problem & Target User

**Target User:** Independent film investors and small production companies

**Problem:** Movie investment carries high financial risk, with approximately 35% of movies failing to generate profit. This interactive dashboard helps investors identify which genres, budget ranges, and rating levels historically produce the highest returns, enabling data-driven investment decisions.

## 2. Data Source

**Source:** TMDB 5000 Movie Dataset (Kaggle)

**Access Date:** April 2026

**Key Variables:**
| Variable | Description |
|----------|-------------|
| budget | Production budget (USD) |
| revenue | Box office revenue (USD) |
| vote_average | Average user rating (0-10) |
| genres | Primary movie genre |
| release_date | Theatrical release date |

**Dataset Size:** 4,803 movies (2000-2020)

## 3. Methods

The Python workflow includes:

1. **Data Loading:** Read CSV using pandas
2. **Data Cleaning:** Remove rows with missing budget/revenue, filter out zero values
3. **Feature Engineering:** 
   - ROI = (revenue - budget) / budget
   - Extract release_year from release_date
   - Parse JSON genres to extract main genre
4. **Analysis:** Group by genre for ROI comparison, correlation analysis
5. **Visualization:** Bar chart, scatter plot, line chart, correlation plot
6. **Dashboard:** Interactive Streamlit app with genre/year/ROI filters

## 4. Key Findings

1. **Animation** movies generate the highest average ROI (approximately 150%), followed by Family and Fantasy genres.

2. **Budget-Revenue Correlation:** Positive correlation (0.68) exists, but high budget does NOT guarantee profit. Many movies with budgets over $100M still lose money.

3. **Success Rate:** 65% of movies achieve positive ROI, meaning 1 in 3 investments loses money.

4. **Rating Impact:** Movies rated above 7.5 have 40% higher average ROI than movies rated below 5.0.

5. **Time Trend:** Movie ROI peaked around 2012-2015 and has been declining since 2016.

## 5. How to Run

### Prerequisites
Make sure you have Python installed. Then install dependencies:

```bash
pip install streamlit pandas numpy matplotlib seaborn
Run the App
After cloning the repository, navigate to the project folder and run:
streamlit run app.py
The dashboard will open in your browser at http://localhost:8501

Files in this Repository
File	Purpose
app.py	Main Streamlit dashboard application
tmdb_5000_movies.csv	Dataset
requirements.txt	Python package dependencies
movie_analysis.ipynb	Jupyter notebook with detailed analysis

## 6. Product Links
Item	Link
Demo Video	[YouTube link here]
GitHub Repository	[Your GitHub repo link here]

## 7. Limitations & Future Work
Current Limitations
ROI calculation assumes reported budgets are accurate (marketing/distribution costs not included)

Dataset ends in 2020, missing recent streaming-era trends (2021-2026)

Genre classification uses only primary genre (ignores hybrid categories)

Does not account for external factors (economic conditions, competition, seasonality)

Future Improvements
Add production company analysis to identify most successful studios

Include sequel vs original movie comparison

Incorporate cast and director data for star-power analysis

Add streaming revenue data for modern movie analysis

Author
[Baodan.Zhang] - ACC102 Mini Assignment, Track 4 (Interactive Data Analysis Tool)

Submission Date: April 24, 2026
