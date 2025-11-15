import streamlit as st
import pickle
import gzip
from typing import List

# --------------------------- Load Model Data ---------------------------
@st.cache_data
def load_data():
    # Load movies list (normal pickle file)
    with open("model/movie_list.pkl", "rb") as f:
        movies = pickle.load(f)

    # Load properly compressed similarity file
    with gzip.open("model/similarity_compressed.pkl.gz", "rb") as f:
        similarity = pickle.loads(f.read())   # <-- IMPORTANT fix

    return movies, similarity


movies, similarity = load_data()

# --------------------------- Page Config ---------------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# --------------------------- CSS ---------------------------
st.markdown(
    """
    <style>

    /* REMOVE STREAMLIT DEFAULT WHITE HEADER */
    header[data-testid="stHeader"] {
        opacity: 0 !important;
        height: 0px !important;
        display: none !important;
    }

    .stApp {
      background: linear-gradient(180deg, #0f1724 0%, #0b1220 40%, #07101a 100%);
      color: #e6eef8;
      font-family: 'Segoe UI', Roboto, Arial;
    }

    .main > div.block-container {
      padding-top: 2px !important;
      padding-left: 64px;
      padding-right: 64px;
    }

    #title {
      text-align: left;
      font-size: 44px;
      font-weight: 900;
      color: #00d2ff;
      text-shadow: 0 6px 20px rgba(0,210,255,0.06);
      margin-bottom: 6px;
    }

    #subtitle {
      color: #9fb8c9;
      margin-top: -6px;
      margin-bottom: 18px;
      font-weight: 600;
    }

    .select-label {
      color: #bcd6e6;
      font-weight: 700;
      margin-bottom: 6px;
      margin-left: 400px;
      font-size: 15px;
    }

    div[data-baseweb="select"] div {
        color: #ffffff !important;
    }

    div[data-baseweb="select"] {
      max-width: 420px !important;
      margin-left: auto;
      margin-right: auto;
      margin-bottom: 20px;
    }

    div[data-baseweb="select"] > div {
      height: 48px !important;
      border-radius: 12px !important;
      background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03)) !important;
      border: 1px solid rgba(255,255,255,0.06) !important;
      box-shadow: 0 8px 18px rgba(0,0,0,0.45);
      padding-left: 14px;
    }

    .cards-row {
      display: flex;
      justify-content: center;
      gap: 22px;
      flex-wrap: wrap;
      margin-top: 26px;
      margin-bottom: 26px;
    }

    .recommend-card {
      width: 220px;
      height: 140px;
      background: #D3D3D3;
      color: #0b1720;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 14px;
      text-align: center;
      font-weight: 700;
      font-size: 18px;
      box-shadow:
         0 6px 18px rgba(2,6,23,0.18),
         0 18px 40px rgba(2,6,23,0.12);
      transition: transform .22s ease, box-shadow .22s ease;
    }

    .recommend-card:hover {
      transform: translateY(-10px) scale(1.03);
      box-shadow:
         0 18px 40px rgba(2,6,23,0.30),
         0 30px 80px rgba(0,210,255,0.06);
    }

    .footer {
      margin-top: 44px;
      margin-bottom: 24px;
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border-radius: 14px;
      padding: 22px;
      border: 1px solid rgba(255,255,255,0.03);
      text-align: center;
      color: #cfe9ff;
      max-width: 960px;
      margin-left: auto;
      margin-right: auto;
      box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    }

    .footer a { color: #9fe8ff; text-decoration: none; font-weight: 700; }
    .footer a:hover { color: #58c2ff; }

    @media (max-width: 600px) {
        .main > div.block-container { padding-top: 4px !important; }
        .select-label {
            margin-left: 0 !important;
            text-align: center;
            display: block;
        }
        div[data-baseweb="select"] { max-width: 92% !important; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------- Header ---------------------------
st.markdown('<div id="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div id="subtitle">Instant recommendations — select any movie below</div>', unsafe_allow_html=True)

# --------------------------- Movie Select ---------------------------
st.markdown('<div class="select-label">🎞️ Choose a Movie</div>', unsafe_allow_html=True)

movie_list = movies['title'].values
selected_movie = st.selectbox("", movie_list, index=0, key="movie")

# --------------------------- Recommendation Logic ---------------------------
def recommend_titles(movie: str, topn: int = 5) -> List[str]:
    idx = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[idx])), key=lambda x: x[1], reverse=True)
    return [movies.iloc[pair[0]].title for pair in distances[1:topn+1]]

recs = recommend_titles(selected_movie, topn=5)
while len(recs) < 5:
    recs.append("—")

# --------------------------- Render Cards ---------------------------
cards_html = '<div class="cards-row">'
for title in recs:
    cards_html += f'<div class="recommend-card"><div class="title">{title}</div></div>'
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# --------------------------- Footer ---------------------------
st.markdown(
    """
    <div class="footer">
      <div style="font-weight:800; font-size:20px; margin-bottom:8px;">Contact & Social</div>
      <div>👤 <strong>Zuber Khan</strong></div>
      <div>📧 <a href="mailto:zuberkhan7301@gmail.com">zuberkhan7301@gmail.com</a> | 📱 +91 8979298864</div>
      <div style="margin-top:6px;">🔗 
        <a href="https://github.com/Zuber-123" target="_blank">GitHub</a> • 
        <a href="https://www.linkedin.com/in/zuber-khan7301" target="_blank">LinkedIn</a>
      </div>
      <div style="font-size:13px; margin-top:10px; color:#99cfe8;">Made with ❤️ using Streamlit</div>
    </div>
    """,
    unsafe_allow_html=True,
)
