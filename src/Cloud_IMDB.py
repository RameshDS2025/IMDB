import pandas as pd
import streamlit as st
import pymysql
import base64
import matplotlib.pyplot as plt
import os

import os

#To set the background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_asset_path(filename):
    # Construct absolute path to assets/<filename>
    # Script is in src/, assets/ is in ../assets/ relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, "assets", filename)

# Provide the path to the uploaded image
@st.cache_data
def load_bg():
    return get_base64_of_bin_file(get_asset_path("Imdb_Image.png"))

image_base64 = load_bg()

# CSS to set the background image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{image_base64}");
    background-size: cover;
}}
</style>
"""

def get_connection():
    return pymysql.connect(
        host=st.secrets["tidb"]["host"],
        port=st.secrets["tidb"]["port"],
        user=st.secrets["tidb"]["user"],
        password=st.secrets["tidb"]["password"],
        database="imdb",
        ssl={"ssl": True} 
    )

def run_query(query, params=None):
    try:
        with get_connection() as conn:
            return pd.read_sql(query, conn, params=params)
    except Exception:
        st.warning("📡 Database connection interrupted. Please refresh the page.")
        st.stop()

def rating_formatter(x):
    return str(int(x)) if x == int(x) else f"{x:.1f}"


# Inject the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

if "main_selection" not in st.session_state:
    st.session_state.main_selection = "-- Select --"

if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

st.sidebar.image(get_asset_path("IMDB_Logo.png"), width=150)

if st.sidebar.button("About us", type="primary"):
    st.session_state.active_page = "about"

if st.sidebar.button("Products", type="primary"):
    st.session_state.active_page = "products"

if st.sidebar.button("Services", type="primary"):
    st.session_state.active_page = "services"

if st.sidebar.button("Contact", type="primary"):
    st.session_state.active_page = "contact"

if st.sidebar.button("Privacy", type="primary"):
    st.session_state.active_page = "privacy"

if st.sidebar.button("Terms & Conditions", type="primary"):
    st.session_state.active_page = "terms"

if st.sidebar.button("Filter Options"):
    st.session_state.active_page = "home"

if st.session_state.active_page == "about":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>About Us</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:16px;'> 
                This project analyzes data from the IMDb movie database to uncover insights about films based " 
                on their genres, ratings, durations, and trends. Using tools like SQL, Python (Pandas,
                Matplotlib) and Streamlit, it allows users to interactively explore
                The lon gest and shortest movies in each genre
                Histograms of movie ratings to understand distribution
                Genre-wise statistics and visualizations
                Clean, styled tables with grouped headers for clarity
                The project aims to provide an intuitive interface for both data enthusiasts
                and film fans to explore patterns and make data-driven observations about movies.
                </p>""", unsafe_allow_html=True)

elif st.session_state.active_page == "products":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Products</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:24px;'>
                1. Interactive Movie Explorer App <br>
                2. Movie Analytics Dashboard <br>
                3. Movie Success Predictor <br>
                4. IMDb Companion Browser Exnsion <br>
                5. Movie Report Generator 
                </p>""", unsafe_allow_html=True)
    
elif st.session_state.active_page == "services":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Services</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:24px;'>
                1. Filter by genre, year, rating and duration <br>
                2. Trends in genres over time <br>
                3. Collaborative filtering using IMDb ratings <br>
                4. Graph of rating trends across time <br>
                5. Genre preferences over time 
                </p>""", unsafe_allow_html=True)
    
elif st.session_state.active_page == "contact":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Contact</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:24px;'>
                0001 North Avenue, <br>
                Hollywood,  <br>
                USA - 10001.
                </p>""", unsafe_allow_html=True)

elif st.session_state.active_page == "privacy":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Privacy</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:16px;'> 
                We respect your privacy and are committed to protecting your personal data. Any 
                information you provide to us via this website (such as your name, email, or 
                other details) will only be used to provide our We do not sell, rent, or 
                trade your personal information. By using our site, you agree to our privacy 
                practices outlined here.                
                </p>""", unsafe_allow_html=True)

elif st.session_state.active_page == "terms":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Terms & conditions</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:16px;'> 
                By accessing this website or using any of our services, you confirm that you are at 
                least 13 years old (or the applicable minimum age in your jurisdiction) and agree 
                to comply with these Terms. If you do not agree, please do not use the site.                
                </p>""", unsafe_allow_html=True)
    
elif st.session_state.active_page == "Filter Options":
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Filter Options</h3>", unsafe_allow_html=True)

st.markdown("""
<style>
table th {
    background-color: #0e1a87 !important;
    color: white !important;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- SEARCH OPTIONS --------------------

if st.session_state.active_page == "home" and "Filter Options":
    
    main_selection = st.sidebar.selectbox("Please select your main option:", 
                                        ["-- Select --", "Search Options", 
                                        "Plot with Details", "Filter Movies"],
                                        key="main_selection")
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
                df["Ratings"] = df["Ratings"].astype(float).round(2)

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
                    SELECT Title, Genre, Duration
                                FROM (Select Genre, Title, Duration,
                                ROW_NUMBER() OVER (PARTITION BY Genre, Duration ORDER BY Title) as rn
                                FROM imdb_movies_list m where Duration = (
                                SELECT MAX(Duration) FROM imdb_movies_list WHERE Genre = m.Genre)
                                OR Duration = (SELECT MIN(Duration) FROM imdb_movies_list WHERE Genre = m.Genre)
                                ) ranked where rn = 1 order by Genre, Duration DESC""")

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

                styled_df = (
                    df.style
                    .format({"Ratings": rating_formatter})
                    .set_properties(**{
                        "color": "#4f0915",
                        "font-weight": "bold"
                    })
                    .hide(axis="index")
                )

                st.markdown(
                    styled_df.to_html(),
                    unsafe_allow_html=True
                )
    elif main_selection == "Plot with Details":

            plot_options = st.sidebar.selectbox(
            "Please select your plot with details to view:",
            [
                "-- Select --",
                "Bar chart of the count of movies for each genre",
                "Horizontal bar chart of the average movie duration per genre",
                "Average voting counts across different genres",
                "Histogram of movie ratings",
                "Pie chart of the highest total votings across the genre",
                "Heatmap to compare average ratings across genre",
                "Scatter plot of ratings vs voting counts"
            ]
        )

            if plot_options == "Bar chart of the count of movies for each genre":
                df = run_query("""SELECT Genre, COUNT(*) AS MovieCount
                                FROM imdb_movies_list
                                GROUP BY Genre
                                ORDER BY MovieCount DESC""")

                fig, ax = plt.subplots(figsize=(9, 3))
                ax.bar(df['Genre'], df['MovieCount'], color='blue')
                ax.set_xlabel('Genre')
                ax.set_ylabel('Number of Movies')
                ax.set_title('Count of Movies per Genre')
                plt.xticks(rotation=45)

                # Set transparency for the figure and axes background
                fig.patch.set_alpha(0.0)  
                ax.patch.set_alpha(0.0)   

                st.pyplot(fig, use_container_width=False)

            elif plot_options == "Horizontal bar chart of the average movie duration per genre":
                df = run_query("""
                    SELECT Genre, AVG(Duration) AS AverageDuration
                    FROM imdb_movies_list
                    WHERE Duration IS NOT NULL
                    GROUP BY Genre
                    ORDER BY AverageDuration DESC
                """)

                fig,ax=plt.subplots(figsize=(7,3))
                ax.barh(df['Genre'], df ['AverageDuration'], color='#420521')
                ax.set_xlabel('Average Of Duration (in minutes)')
                ax.set_ylabel('Genre')
                ax.set_title('Average Movie Duration as per the Genre')

                fig.patch.set_alpha(0.0)
                ax.patch.set_alpha(0.0) 

                st.pyplot(fig, use_container_width=False)

            elif plot_options == "Average voting counts across different genres":
                df = run_query("""
                    SELECT Genre, AVG(Votings) AS AverageVotings
                    FROM imdb_movies_list
                    WHERE Votings IS NOT NULL
                    GROUP BY Genre
                    ORDER BY AverageVotings DESC
                """)

                fig,ax=plt.subplots(figsize=(9,3))
                ax.bar(df['Genre'], df['AverageVotings'], color='#0f0545')
                ax.set_xlabel("Average Votings counts")
                ax.set_ylabel("Genre")
                ax.set_title("Average voting counts per Genre")
                plt.xticks(rotation=45)

                fig.patch.set_alpha(0.0)
                ax.patch.set_alpha(0.0)

                st.pyplot(fig,use_container_width=False)

            elif plot_options == "Histogram of movie ratings":
                df = run_query("""
                    SELECT Ratings
                    FROM imdb_movies_list
                    WHERE Ratings IS NOT NULL
                """)
                fig, ax = plt.subplots(figsize=(9, 3))

                ax.hist(
                    df["Ratings"],     
                    bins=25,
                    edgecolor="#03445c"
                )

                ax.set_xlabel("Ratings")
                ax.set_ylabel("Frequency")
                ax.set_title("Movie Rating Frequency")

                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                st.pyplot(fig, use_container_width=False)

            elif plot_options == "Scatter plot of ratings vs voting counts":
                df = run_query("""
                    SELECT Ratings, Votings
                    FROM imdb_movies_list
                    WHERE Ratings IS NOT NULL
                    AND Votings IS NOT NULL
                """)

                fig, ax = plt.subplots(figsize=(9, 4))

                ax.scatter(
                    df["Ratings"],
                    df["Votings"],
                    alpha=0.6
                )

                ax.set_xlabel("Ratings")
                ax.set_ylabel("Voting Counts")
                ax.set_title("Scatter Plot of Ratings vs Voting Counts")

                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                st.pyplot(fig, use_container_width=False)



            elif plot_options == "Histogram of movie ratings":
                df = run_query("""
                    SELECT Ratings
                    FROM imdb_movies_list
                    WHERE Ratings IS NOT NULL
                """)

                fig, ax = plt.subplots(figsize=(7, 3))

                ax.hist(
                    df["Ratings"],
                    bins=25,
                    edgecolor="#03445c"
                )

                ax.set_xlabel("Ratings")
                ax.set_ylabel("Frequency")
                ax.set_title("Movie Rating Frequency")

                # Transparent background (same as scatter plot)
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                st.pyplot(fig)

            elif plot_options == "Pie chart of the highest total votings across the genre":
                df = run_query("""
                    SELECT Genre, SUM(Votings) AS Total_Votings
                    FROM imdb_movies_list
                    WHERE Votings IS NOT NULL
                    GROUP BY Genre
                    ORDER BY Total_Votings DESC
                """)

                # Optional: keep only top 8 genres to avoid clutter
                df = df.head(8)

                fig, ax = plt.subplots(figsize=(9, 3))

                wedges, texts, autotexts = ax.pie(
                    df["Total_Votings"],
                    autopct="%1.1f%%",
                    startangle=140,
                    wedgeprops={"edgecolor": "white"},
                    textprops={"fontsize": 4}
                )

                ax.set_title("Highest Total Voting Counts by Genre", fontsize=12)

                ax.legend(
                    wedges,
                    df["Genre"],
                    title="Genres",
                    loc="center left",
                    bbox_to_anchor=(1, 0.5),
                    fontsize = 6,
                    title_fontsize = 6
                )

                # Transparent background (same as your other plots)
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                st.pyplot(fig, use_container_width=False)

            elif plot_options == "Heatmap to compare average ratings across genre":
                df = run_query("""
                    SELECT Genre, AVG(Ratings) AS AverageRatings
                    FROM imdb_movies_list
                    WHERE Ratings IS NOT NULL
                    GROUP BY Genre
                    ORDER BY AverageRatings DESC
                """)

                fig, ax = plt.subplots(figsize=(10, 3))

                heatmap = ax.imshow(
                    df["AverageRatings"].values.reshape(1, -1),
                    cmap="coolwarm",
                    aspect="auto"
                )

                fig.colorbar(heatmap, ax=ax, fraction=0.03, pad=0.04)

                ax.set_xticks(range(len(df["Genre"])))
                ax.set_xticklabels(df["Genre"], rotation=45, ha="right")
                ax.set_yticks([])

                ax.set_title("Heatmap of Average Ratings Across Genres")

                # Transparent background (matches other plots)
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                st.pyplot(fig,use_container_width=False)

            elif plot_options == "Scatter plot of ratings vs voting counts":
                df = run_query("""
                    SELECT Ratings, Votings
                    FROM imdb_movies_list
                    WHERE Ratings IS NOT NULL
                    AND Votings IS NOT NULL
                """)

                fig, ax = plt.subplots(figsize=(10, 6))

                ax.scatter(
                    df["Ratings"],
                    df["Votings"],
                    alpha=0.6
                )

                ax.set_xlabel("Ratings")
                ax.set_ylabel("Votings")
                ax.set_title("Scatter Plot of Ratings vs Voting Counts")

                # Transparent background (consistent across all plots)
                fig.patch.set_alpha(0)
                ax.patch.set_alpha(0)

                st.pyplot(fig, use_container_width=False)

    elif main_selection == "Filter Movies":
        st.sidebar.header("Filter Movies")

        # Sidebar sliders and inputs with one decimal precision for applicable fields
        min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, step=0.1, format="%.1f")
        max_rating = st.sidebar.slider("Maximum Rating", 0.0, 10.0, 10.0, step=0.1, format="%.1f")

        # Duration typically doesn't require decimal precision; use integers
        min_duration = st.sidebar.slider("Minimum Duration (mins)", 0, 300, 90, step=1)
        max_duration = st.sidebar.slider("Maximum Duration (mins)", 0, 300, 180, step=1)

        # Votes are whole numbers; ensure no decimals
        min_votes = st.sidebar.number_input("Minimum Votes", min_value=0, value=1000, step=1)
        max_votes = st.sidebar.number_input("Maximum Votes", min_value=0, value=1000000, step=1)

        genres_df = run_query("SELECT DISTINCT Genre FROM imdb_movies_list ORDER BY Genre")
        genre_options = ["All"] + genres_df["Genre"].dropna().tolist()

        selected_genre = st.sidebar.multiselect(
            "Genre (optional)",
            genre_options,
            key="selected_genre"
        )

        query = """
            SELECT Title, Ratings, Votings, Duration, Genre
            FROM imdb_movies_list
            WHERE Ratings BETWEEN %s AND %s
            AND Duration BETWEEN %s AND %s
            AND Votings BETWEEN %s AND %s
        """
        params = [min_rating, max_rating, min_duration, max_duration, min_votes, max_votes]

        # ✅ Handle multiselect properly
        if selected_genre and "All" not in selected_genre:
            placeholders = ", ".join(["%s"] * len(selected_genre))
            query += f" AND Genre IN ({placeholders})"
            params.extend(selected_genre)


        # Execute the SQL query with the provided parameters
        df = run_query(query, params)

        # Convert the query results into a DataFrame
        columns = ['Title', 'Ratings', 'Votings', 'Duration', 'Genre']
        df = pd.DataFrame(df, columns=columns)

        if not df.empty and "Ratings" in df.columns:
            df["Ratings"] = df["Ratings"].round(1)

        # Display the filtered movies using Streamlit
        if not df.empty:

            styled_df = df.style.format({
                'Ratings': '{:.1f}'  # Ensures Ratings are displayed with 1 decimal place
            }).applymap(
                lambda x: "color: #4f0915; font-weight: bold;" if isinstance(x, (int, str, float)) else ""
            ).hide(axis="index")
            
            st.markdown(
                styled_df.to_html(),
                unsafe_allow_html=True)
                # st.dataframe(df, hide_index=True)  # Display the DataFrame as an interactive table
        else:
            st.markdown("""<div style="
                            text-align: center;
                            color: #4f0915;
                            font-size: 22px;
                            font-weight: bold;
                            font-style: italic;
                            margin-top: 80px;
                            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
                        ">
                            Select the proper range values to see results
                        </div>
                        """,
                        unsafe_allow_html=True)

