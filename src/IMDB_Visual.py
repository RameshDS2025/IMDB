import pandas as pd
import streamlit as st
import pymysql
import base64
import matplotlib.pyplot as plt

#To set the background image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Provide the path to the uploaded image
image_base64 = get_base64_of_bin_file("assets/Imdb_Image.png")


# CSS to set the background image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{image_base64}");
    background-size: cover;
}}
</style>
"""

# Inject the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Apply the CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Apply the custom CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

st.sidebar.image("assets/IMDB_Logo.png", width=150)

About_us=st.sidebar.button("About us", type="primary") #Set the about us page
if About_us:
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

Products=st.sidebar.button("Products", type="primary") #Product button
if Products:
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Products</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:24px;'>
                1. Interactive Movie Explorer App <br>
                2. Movie Analytics Dashboard <br>
                3. Movie Success Predictor <br>
                4. IMDb Companion Browser Exnsion <br>
                5. Movie Report Generator 
                </p>""", unsafe_allow_html=True)
    
Services=st.sidebar.button("Services", type="primary") #Services button
if Services:
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Services</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:24px;'>
                1. Filter by genre, year, rating and duration <br>
                2. Trends in genres over time <br>
                3. Collaborative filtering using IMDb ratings <br>
                4. Graph of rating trends across time <br>
                5. Genre preferences over time 
                </p>""", unsafe_allow_html=True)
    
Contact=st.sidebar.button("Contact", type="primary") #Contact button
if Contact:
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Contact</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:24px;'>
                0001 North Avenue, <br>
                Hollywood,  <br>
                USA - 10001.
                </p>""", unsafe_allow_html=True)

Privacy=st.sidebar.button("Privacy", type="primary") #Privacy button
if Privacy:
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Privacy</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:16px;'> 
                We respect your privacy and are committed to protecting your personal data. Any 
                information you provide to us via this website (such as your name, email, or 
                other details) will only be used to provide our We do not sell, rent, or 
                trade your personal information. By using our site, you agree to our privacy 
                practices outlined here.                
                </p>""", unsafe_allow_html=True)

Terms=st.sidebar.button("Terms & Conditions", type="primary") #T&C button
if Terms:
    st.markdown("<h3 style='color:#660d0d; font-weight:bold;'>Terms & conditions</h3>", unsafe_allow_html=True)
    st.markdown("""<p style='color:#4f0915; font-size:16px;'> 
                By accessing this website or using any of our services, you confirm that you are at 
                least 13 years old (or the applicable minimum age in your jurisdiction) and agree 
                to comply with these Terms. If you do not agree, please do not use the site.                
                </p>""", unsafe_allow_html=True)

#SQL server connection
mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="imdb"
)

mycursor= mydb.cursor()

# Selection box
main_selection = st.sidebar.selectbox(
    "Please select your main option:",
    ["-- Select --", "Search Options", "Plot with Details", "Filter Movies"]
)

#Options to select table
if main_selection == "Search Options":

    st.write("") #To clear the menu list that already appeared

    search_options = st.sidebar.selectbox(
        "Please select your option to search:",
        [
            "-- Select --",
            "Top 10 movies with highest ratings",
            "The top-rated movie for each genre",
            "The shortest and longest movies for each genre"
        ]
    )

    # Handle the search options logic
    if search_options == "Top 10 movies with highest ratings":
        mycursor.execute("""SELECT Title, Ratings, Votings, Genre 
                         FROM imdb_movies_list
                         ORDER BY Votings DESC, Ratings DESC LIMIT 10""")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=[i[0] for i in mycursor.description])
        df.index = df.index + 1  # Start index from 1 instead of 0
        df.index.name = 'S.No'  # Name the index column
        df.insert(0, 'S.No', df.index) # Insert the index as a new column at the start
        if 'Ratings' in df.columns:
            df['Ratings'] = df['Ratings'].round(1)
            styled_df = df.style.applymap(
                lambda x: "color: #4f0915; font-weight: bold;" if isinstance(x, (int, str, float)) else "font-weight: bold;"
            ).format({'Ratings': '{:.1f}'}).hide(axis="index")

        st.markdown(
            styled_df.to_html(),
            unsafe_allow_html=True
        )

    elif search_options == "The top-rated movie for each genre":
        mycursor.execute("""SELECT Title, Ratings, Genre
                         FROM imdb_movies_list i
                         WHERE Ratings = (
                         SELECT MAX(Ratings) 
                         FROM imdb_movies_list
                         WHERE Genre = i.Genre)
                         ORDER BY Ratings DESC""")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=[i[0] for i in mycursor.description])
        if 'Ratings' in df.columns:
            df['Ratings'] = df['Ratings'].round(1)
            df.index = df.index + 1
            df.index.name = 'S.No'  
            df.insert(0, 'S.No', df.index)
            styled_df = df.style.applymap(
                lambda x: "color: #4f0915; font-weight: bold; text-align: left;" if isinstance(x, (int, str, float)) else "font-weight: bold;"
            ).format({'Ratings': '{:.1f}'}).hide(axis="index")
        st.markdown(
            styled_df.to_html(),
            unsafe_allow_html=True)

    elif search_options == "The shortest and longest movies for each genre":
        mycursor.execute("""SELECT Title, Genre, Duration
                         FROM (Select Genre, Title, Duration,
                         ROW_NUMBER() OVER (PARTITION BY Genre, Duration ORDER BY Title) as rn
                         FROM imdb_movies_list m where Duration = (
                         SELECT MAX(Duration) FROM imdb_movies_list WHERE Genre = m.Genre)
                         OR Duration = (SELECT MIN(Duration) FROM imdb_movies_list WHERE Genre = m.Genre)
                         ) ranked where rn = 1 order by Genre, Duration DESC
                        """)
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=[i[0] for i in mycursor.description])
            # Create Longest and Shortest columns
        longest = df.groupby('Genre')['Duration'].transform('max')
        shortest = df.groupby('Genre')['Duration'].transform('min')

        # Add new columns
        df['Longest'] = df['Duration'].where(df['Duration'] == longest, "--")
        df['Shortest'] = df['Duration'].where(df['Duration'] == shortest, "--")

        # Drop the original Duration column
        df = df.drop(columns=['Duration'])
        df.index = df.index + 1
        df.index.name = 'S.No'  
        df.insert(0, 'S.No', df.index)
        
        styled_df = df.style.applymap(
                lambda x: "color: #4f0915; font-weight: bold;" if isinstance(x, (int, str, float)) else "font-weight: bold;"
            ).format().hide(axis="index")

        st.markdown(
            styled_df.to_html(),
            unsafe_allow_html=True)

elif main_selection == "Plot with Details":
    # Dropdown for plot-related options
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
        mycursor.execute("""SELECT Genre, COUNT(*) AS MovieCount
                            FROM imdb_movies_list
                            GROUP BY Genre
                            ORDER BY MovieCount DESC""")
        
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Genre', 'MovieCount'])
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df['Genre'], df['MovieCount'], color='blue')
        ax.set_xlabel('Genre')
        ax.set_ylabel('Number of Movies')
        ax.set_title('Count of Movies per Genre')
        plt.xticks(rotation=45)

        # Set transparency for the figure and axes background
        fig.patch.set_alpha(0.0)  
        ax.patch.set_alpha(0.0)   

        st.pyplot(fig)

    elif plot_options == "Horizontal bar chart of the average movie duration per genre":
        mycursor.execute("""select Genre, AVG(Duration) as AverageOfDuration
                        From imdb_movies_list
                        Group by Genre
                        Order by AverageOfDuration Desc""")
        
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns =['Genre','AverageOfDuration'])
        fig,ax=plt.subplots(figsize=(10,6))
        ax.barh(df['Genre'], df ['AverageOfDuration'], color='#420521')
        ax.set_xlabel('Average Of Duration (in minutes)')
        ax.set_ylabel('Genre')
        ax.set_title('Average Movie Duration as per the Genre')

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0) 

        st.pyplot(fig)

    elif plot_options == "Average voting counts across different genres":
        mycursor.execute("""select Genre, AVG(Votings) as AverageOfVotings
                        from imdb_movies_list
                        Group by Genre
                        Order by AverageOfVotings Desc""")
        
        results=mycursor.fetchall()
        df = pd.DataFrame(results, columns = ['Genre', 'AverageOfVotings'])
        fig,ax=plt.subplots(figsize=(10,6))
        ax.bar(df['Genre'], df['AverageOfVotings'], color='#0f0545')
        ax.set_xlabel("Average Votings counts")
        ax.set_ylabel("Genre")
        ax.set_title("Average voting counts per Genre")
        plt.xticks(rotation=45)

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)

    elif plot_options == "Histogram of movie ratings":
        mycursor.execute("""select Ratings
                        from imdb_movies_list
                        """)
        results=mycursor.fetchall()
        ratings=[row[0] for row in results]
        fig,ax= plt.subplots(figsize=(7,3))
        ax.hist(ratings, bins=25, color='orange', edgecolor='#03445c')
        ax.set_xlabel("Ratings")
        ax.set_ylabel("Frequency")
        ax.set_title("Movie Rating Frequency")

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)

    elif plot_options == "Pie chart of the highest total votings across the genre":
        mycursor.execute("""select Genre, SUM(Votings)
                            from imdb_movies_list
                            group by Genre
                            order by Votings desc""")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Genre', 'Votings'])
        
        total_votes = df['Votings'].sum()
        df['Percentage'] = (df['Votings'] / total_votes) * 100
        df = df.sort_values(by='Percentage', ascending=False)

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(
            df['Votings'],
            labels=None,  
            autopct='%1.1f%%', 
            startangle=140
        )
        
        ax.set_title("Highest total voting counts")
        
        ax.legend(
            wedges, df['Genre'],
            title="Genres",
            loc="upper right",
            bbox_to_anchor=(1, 0, 0.5, 1)
        )

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)

    elif plot_options == "Heatmap to compare average ratings across genre":
        mycursor.execute("""select Genre, AVG(Ratings) as AverageRatings
                        from imdb_movies_list
                        Group by Genre
                        Order by AverageRatings Desc""")
        
        results=mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Genre', 'AverageRatings'])
        fig, ax = plt.subplots(figsize=(10, 6))
        cax = ax.matshow(df['AverageRatings'].values.reshape(1, -1), cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_xticks(range(len(df['Genre'])))
        ax.set_xticklabels(df['Genre'], rotation=45)
        ax.set_yticks([])
        ax.set_title('Heatmap of Average Ratings per Genre')

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)

    elif plot_options == "Scatter plot of ratings vs voting counts":
        mycursor.execute("""select Ratings, Votings
                        from imdb_movies_list""")
        results=mycursor.fetchall()
        ratings=[rows [0] for rows in results]
        votings=[rows [1] for rows in results]
        fig,ax= plt.subplots(figsize=(10,6))
        ax.scatter(ratings, votings , color='#4a0980')
        ax.set_xlabel('Ratings')
        ax.set_ylabel('Votings')
        ax.set_title('Scatter plot of ratings vs voting counts')

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)

elif main_selection == "Filter Movies":
# Sidebar for filtering movies
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

    try:
        # Establish a connection to the database
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="imdb"
        )
        mycursor = mydb.cursor()

        # Fetch distinct genres from the database
        mycursor.execute("SELECT DISTINCT Genre FROM imdb_movies_list")
        genre_results = mycursor.fetchall()

        # Extract genre names into a list
        genre_options = ["All"] + [row[0] for row in genre_results]

        # Create a select box for genre selection
        selected_genre = st.sidebar.selectbox("Genre (optional)", genre_options)

        # Prepare the SQL query for filtering
        query = """
            SELECT Title, Ratings, Votings, Duration, Genre
            FROM imdb_movies_list
            WHERE Ratings BETWEEN %s AND %s
            AND Duration BETWEEN %s AND %s
            AND Votings BETWEEN %s AND %s
        """
        params = [min_rating, max_rating, min_duration, max_duration, min_votes, max_votes]

        # Add genre filter dynamically if provided
        if selected_genre != "All":
            query += " AND Genre = %s"
            params.append(selected_genre)

        # Execute the SQL query with the provided parameters
        mycursor.execute(query, params)
        results = mycursor.fetchall()  # Fetch all matching records

        # Convert the query results into a DataFrame
        columns = ['Title', 'Ratings', 'Votings', 'Duration', 'Genre']
        df = pd.DataFrame(results, columns=columns)

        if 'Ratings' in df.columns:
            df['Ratings'] = df['Ratings'].round(1)

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
            st.write("")  # Display a message if no results are found

    except Exception as e:
        # Handle any exceptions during database operations
        st.error(f"An error occurred: {e}")

    finally:
        # Ensure proper cleanup of database resources
        if 'mycursor' in locals():
            mycursor.close()  # Close the cursor
        if 'mydb' in locals() and mydb.open:
            mydb.close()  # Close the database connection