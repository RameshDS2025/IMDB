import pandas as pd
import streamlit as st
import pymysql
import base64
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(layout="wide", page_title="IMDb Analytics App")

# -------------------- BACKGROUND IMAGE --------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

@st.cache_data
def load_bg():
    return get_base64_of_bin_file("Imdb_Image.png")

image_base64 = load_bg()

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
    }}
    table th {{
        background-color: #0e1a87 !important;
        color: white !important;
        text-align: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- SAFE DB HELPERS --------------------
def get_connection():
    return pymysql.connect(
        host=st.secrets["tidb"]["host"],
        port=int(st.secrets["tidb"]["port"]),
        user=st.secrets["tidb"]["user"],
        password=st.secrets["tidb"]["password"],
        database="imdb",
        connect_timeout=10,
        read_timeout=30,
        autocommit=True
    )

def run_query(query, params=None):
    try:
        with get_connection() as conn:
            return pd.read_sql(query, conn, params=params)
    except Exception:
        st.warning("📡 Database connection interrupted. Please refresh the page.")
        st.stop()

# -------------------- SIDEBAR NAVIGATION --------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

st.sidebar.image("IMDB_Logo.png", width=150)

pages = [
    ("About us", "about"),
    ("Products", "products"),
    ("Services", "services"),
    ("Contact", "contact"),
    ("Privacy", "privacy"),
    ("Terms & Conditions", "terms"),
    ("Filter Options", "home"),
]

for label, key in pages:
    if st.sidebar.button(label, type="primary"):
        st.session_state.active_page = key

# -------------------- STATIC PAGES --------------------
def show_text(title, text, size=16):
    st.markdown(f"<h3 style='color:#660d0d'>{title}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#4f0915; font-size:{size}px;'>{text}</p>", unsafe_allow_html=True)

if st.session_state.active_page == "about":
    show_text(
        "About Us",
        "This project analyzes IMDb movie data to uncover insights across genres, ratings, durations, "
        "and voting trends using SQL, Python, and Streamlit."
    )

elif st.session_state.active_page == "products":
    show_text("Products", "1. Movie Explorer<br>2. Analytics Dashboard<br>3. Success Predictor", 22)

elif st.session_state.active_page == "services":
    show_text("Services", "Genre filters, trend analysis, visualizations, and insights", 22)

elif st.session_state.active_page == "contact":
    show_text("Contact", "Hollywood, USA", 22)

elif st.session_state.active_page == "privacy":
    show_text("Privacy", "We do not sell or misuse your personal data.")

elif st.session_state.active_page == "terms":
    show_text("Terms & Conditions", "You must be at least 13 years old to use this service.")

# -------------------- MAIN APP --------------------
if st.session_state.active_page == "home":

    main_selection = st.sidebar.selectbox(
        "Please select your main option:",
        ["-- Select --", "Search Options", "Plot with Details", "Filter Movies"]
    )

    # -------------------- SEARCH OPTIONS --------------------
    if main_selection == "Search Options":

        search_options = st.sidebar.selectbox(
            "Please select your option to search:",
            [
                "-- Select --",
                "Top 10 movies with highest ratings",
                "The top-rated movie for each genre",
                "The shortest and longest movies for each genre"
            ]
        )

        if search_options == "Top 10 movies with highest ratings":
            df = run_query("""
                SELECT Title, Ratings, Votings, Genre
                FROM imdb_movies_list
                ORDER BY Votings DESC, Ratings DESC
                LIMIT 10
            """)

        elif search_options == "The top-rated movie for each genre":
            df = run_query("""
                SELECT Title, Ratings, Genre
                FROM imdb_movies_list i
                WHERE (Genre, Ratings) IN (
                    SELECT Genre, MAX(Ratings)
                    FROM imdb_movies_list
                    GROUP BY Genre
                )
                ORDER BY Ratings DESC
            """)

        elif search_options == "The shortest and longest movies for each genre":
            df = run_query("""
                SELECT Genre, Title, Duration
                FROM imdb_movies_list
            """)

            longest = df.groupby("Genre")["Duration"].transform("max")
            shortest = df.groupby("Genre")["Duration"].transform("min")
            df["Longest"] = df["Duration"].where(df["Duration"] == longest, "--")
            df["Shortest"] = df["Duration"].where(df["Duration"] == shortest, "--")
            df = df.drop(columns="Duration")

        else:
            df = pd.DataFrame()

        if not df.empty:
            df.index += 1
            df.insert(0, "S.No", df.index)
            st.markdown(
                df.style.hide(axis="index").to_html(),
                unsafe_allow_html=True
            )

    # -------------------- PLOTS --------------------
    elif main_selection == "Plot with Details":

        plot_options = st.sidebar.selectbox(
            "Select plot:",
            [
                "-- Select --",
                "Bar chart of the count of movies for each genre",
                "Histogram of movie ratings",
                "Scatter plot of ratings vs voting counts"
            ]
        )

        if plot_options == "Bar chart of the count of movies for each genre":
            df = run_query("""
                SELECT Genre, COUNT(*) MovieCount
                FROM imdb_movies_list
                GROUP BY Genre
            """)

            fig, ax = plt.subplots()
            ax.bar(df["Genre"], df["MovieCount"])
            plt.xticks(rotation=45)
            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)
            st.pyplot(fig)

        elif plot_options == "Histogram of movie ratings":
            df = run_query("SELECT Ratings FROM imdb_movies_list")
            fig, ax = plt.subplots()
            ax.hist(df["Ratings"], bins=25)
            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)
            st.pyplot(fig)

        elif plot_options == "Scatter plot of ratings vs voting counts":
            df = run_query("SELECT Ratings, Votings FROM imdb_movies_list")
            fig, ax = plt.subplots()
            ax.scatter(df["Ratings"], df["Votings"])
            fig.patch.set_alpha(0)
            ax.patch.set_alpha(0)
            st.pyplot(fig)

    # -------------------- FILTER MOVIES --------------------
    elif main_selection == "Filter Movies":

        min_rating, max_rating = st.sidebar.slider("Rating", 0.0, 10.0, (5.0, 10.0))
        min_duration, max_duration = st.sidebar.slider("Duration", 0, 210, (90, 180))
        min_votes = st.sidebar.number_input("Min Votes", 0, 1_000_000, 1000)

        genres = run_query("SELECT DISTINCT Genre FROM imdb_movies_list")["Genre"].tolist()
        genre = st.sidebar.selectbox("Genre", ["All"] + genres)

        query = """
            SELECT Title, Ratings, Votings, Duration, Genre
            FROM imdb_movies_list
            WHERE Ratings BETWEEN %s AND %s
            AND Duration BETWEEN %s AND %s
            AND Votings >= %s
        """
        params = [min_rating, max_rating, min_duration, max_duration, min_votes]

        if genre != "All":
            query += " AND Genre = %s"
            params.append(genre)

        df = run_query(query, params)

        if not df.empty:
            st.markdown(
                df.style.hide(axis="index").to_html(),
                unsafe_allow_html=True
            )