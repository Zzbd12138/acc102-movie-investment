"""
Movie Investment Analysis Dashboard
A Streamlit app for analyzing movie investment returns
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Movie Investment Analyzer",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 Movie Investment Analysis Dashboard")
st.markdown("""
    <style>
    .big-font { font-size:20px !important; }
    </style>
    """, unsafe_allow_html=True)
st.markdown("### Helping investors make data-driven decisions about movie investments")

# Sidebar filters
st.sidebar.header("🔍 Filter Movies")

# Load data function with caching
@st.cache_data
def load_and_clean_data():
    """Load and clean the TMDB movie dataset"""
    df = pd.read_csv('tmdb_5000_movies.csv')
    
    # Data cleaning
    df_clean = df.dropna(subset=['budget', 'revenue', 'vote_average'])
    df_clean = df_clean[(df_clean['budget'] > 0) & (df_clean['revenue'] > 0)]
    
    # Calculate ROI
    df_clean['roi'] = (df_clean['revenue'] - df_clean['budget']) / df_clean['budget']
    
    # Extract year
    df_clean['release_year'] = pd.to_datetime(df_clean['release_date'], errors='coerce').dt.year
    df_clean = df_clean.dropna(subset=['release_year'])
    df_clean['release_year'] = df_clean['release_year'].astype(int)
    
    # Extract main genre
    def extract_main_genre(genres_str):
        try:
            genres_list = ast.literal_eval(genres_str)
            if genres_list:
                return genres_list[0]['name']
            return 'Unknown'
        except:
            return 'Unknown'
    
    df_clean['main_genre'] = df_clean['genres'].apply(extract_main_genre)
    
    return df_clean

# Load the data
df = load_and_clean_data()

# Sidebar filters
all_genres = ['All'] + sorted(df['main_genre'].unique().tolist())
selected_genre = st.sidebar.selectbox("Movie Genre", all_genres)

min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
year_range = st.sidebar.slider("Release Year", min_year, max_year, (2000, max_year))

min_roi = float(df['roi'].min())
max_roi = float(df['roi'].max())
roi_range = st.sidebar.slider("Minimum ROI", min_roi, max_roi, (min_roi, max_roi))

# Apply filters
filtered_df = df[
    (df['release_year'].between(year_range[0], year_range[1])) &
    (df['roi'].between(roi_range[0], roi_range[1]))
]

if selected_genre != 'All':
    filtered_df = filtered_df[filtered_df['main_genre'] == selected_genre]

# Display current filter status
st.info(f"Showing {len(filtered_df)} movies based on your filters")

# Row 1: Key metrics (KPI cards)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Movies", len(filtered_df))

with col2:
    avg_roi = filtered_df['roi'].mean()
    st.metric("Average ROI", f"{avg_roi:.1%}")

with col3:
    success_rate = (filtered_df['roi'] > 0).mean()
    st.metric("Success Rate (ROI>0)", f"{success_rate:.1%}")

with col4:
    if len(filtered_df) > 0:
        best_movie = filtered_df.loc[filtered_df['roi'].idxmax(), 'title']
        st.metric("Best Movie", best_movie[:20])
    else:
        st.metric("Best Movie", "N/A")

# Row 2: Chart 1 - ROI by Genre
st.subheader("📊 Average ROI by Movie Genre")
col1, col2 = st.columns(2)

with col1:
    genre_roi = filtered_df.groupby('main_genre')['roi'].mean().sort_values(ascending=False).head(10)
    
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    bars = ax1.barh(range(len(genre_roi)), genre_roi.values, color='steelblue')
    ax1.set_yticks(range(len(genre_roi)))
    ax1.set_yticklabels(genre_roi.index)
    ax1.set_xlabel('Average ROI')
    ax1.set_title('Top 10 Genres by ROI')
    ax1.invert_yaxis()
    
    for i, v in enumerate(genre_roi.values):
        ax1.text(v + 0.02, i, f'{v:.1%}', va='center')
    
    st.pyplot(fig1)
    plt.close(fig1)

# Row 2: Chart 2 - Budget vs Revenue
with col2:
    sample_df = filtered_df.sample(min(500, len(filtered_df)))
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    scatter = ax2.scatter(sample_df['budget'], sample_df['revenue'], 
                          c=sample_df['vote_average'], cmap='viridis', 
                          alpha=0.6, s=50)
    plt.colorbar(scatter, ax=ax2, label='Rating')
    ax2.set_xlabel('Budget (USD)')
    ax2.set_ylabel('Revenue (USD)')
    ax2.set_title('Budget vs Revenue')
    
    max_val = max(sample_df['budget'].max(), sample_df['revenue'].max())
    ax2.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Break-even')
    ax2.legend()
    
    st.pyplot(fig2)
    plt.close(fig2)

# Row 3: Chart 3 - ROI Trend Over Years
st.subheader("📈 ROI Trend Over Time")

yearly_roi = filtered_df.groupby('release_year')['roi'].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(yearly_roi['release_year'], yearly_roi['roi'], marker='o', linewidth=2, markersize=4)
ax3.set_xlabel('Release Year')
ax3.set_ylabel('Average ROI')
ax3.set_title('Movie Investment ROI Trend')
ax3.grid(True, alpha=0.3)
ax3.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Break-even')
ax3.legend()

st.pyplot(fig3)
plt.close(fig3)

# Row 4: Chart 4 - Rating vs ROI
st.subheader("⭐ Do Higher Ratings Mean Higher Returns?")

fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.scatter(filtered_df['vote_average'], filtered_df['roi'], alpha=0.3, s=30)

# Add trend line
z = np.polyfit(filtered_df['vote_average'], filtered_df['roi'], 1)
p = np.poly1d(z)
ax4.plot(sorted(filtered_df['vote_average']), 
         p(sorted(filtered_df['vote_average'])), 
         "r-", linewidth=2, label=f'Trend (slope={z[0]:.3f})')

ax4.set_xlabel('Average Rating')
ax4.set_ylabel('ROI')
ax4.set_title('Rating vs ROI Relationship')
ax4.legend()
ax4.grid(True, alpha=0.3)

st.pyplot(fig4)
plt.close(fig4)

# Row 5: Top movies table
st.subheader("🏆 Top Performing Movies")
top_movies = filtered_df.nlargest(20, 'roi')[['title', 'release_year', 'main_genre', 'budget', 'revenue', 'roi', 'vote_average']]
top_movies['roi'] = top_movies['roi'].apply(lambda x: f"{x:.1%}")
top_movies['budget'] = top_movies['budget'].apply(lambda x: f"${x:,.0f}")
top_movies['revenue'] = top_movies['revenue'].apply(lambda x: f"${x:,.0f}")

st.dataframe(top_movies, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Data Source: TMDB 5000 Movie Dataset (Kaggle) | 🛠️ Built with Streamlit")