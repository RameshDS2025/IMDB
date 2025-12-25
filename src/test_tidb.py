import streamlit as st
import pymysql
import os

def test_connection():
    print("Testing connection to TiDB Cloud...")
    
    # Check if secrets file is accessible/loaded
    if "tidb" not in st.secrets:
        print("Error: 'tidb' section not found in .streamlit/secrets.toml")
        print("Please ensure your secrets.toml has the following structure:")
        print("""
[tidb]
host = "..."
port = 4000
user = "..."
password = "..."
        """)
        return

    try:
        # Construct path to SSL cert
        # Construct path to SSL cert
        # Relative to this script, assets are in ../assets
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        ssl_ca = os.path.join(project_root, 'assets', 'isrgrootx1.pem')
        
        if not os.path.exists(ssl_ca):
            print(f"Warning: SSL certificate not found at {ssl_ca}")
            print("Attempting connection without specific SSL CA (using system defaults or None)...")
            ssl_config = {"ssl": True}
        else:
            print(f"Using SSL certificate: {ssl_ca}")
            ssl_config = {"ssl": {"ca": ssl_ca}}

        conn = pymysql.connect(
            host=st.secrets["tidb"]["host"],
            port=st.secrets["tidb"]["port"],
            user=st.secrets["tidb"]["user"],
            password=st.secrets["tidb"]["password"],
            database="imdb",
            **ssl_config
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            print(f"Connection Successful! Test Query Result: {result}")
        
        conn.close()
        
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()
