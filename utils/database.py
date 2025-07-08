import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

def get_session():
    """Get Snowflake session"""
    return get_active_session()

def authenticate_user(username, password):
    """Authenticate user against Snowflake database"""
    try:
        session = get_session()
        query = """
        SELECT * FROM HACKATON.USERS_DATA.USERS 
        WHERE USER_NAME = ? AND USER_PASSWORD = ?
        """
        result = session.sql(query, params=[username, password]).collect()
        
        if result:
            user_data = pd.DataFrame(result)
            return user_data.iloc[0]
        else:
            return None
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return None

def create_user(username, password, age, sex, weight, height, dietary_restrictions, dietary_goals):
    """Create a new user in the database"""
    try:
        session = get_session()
        insert_query = """
        INSERT INTO HACKATON.USERS_DATA.USERS 
        (USER_NAME, USER_PASSWORD, AGE, SEX, WEIGHT, HEIGHT, DIETARY_RESTRICTIONS, DIETARY_GOALS)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        session.sql(insert_query, params=[
            username, password, age, sex, weight, height, 
            dietary_restrictions, dietary_goals
        ]).collect()
        return True
    except Exception as e:
        st.error(f"Error creating account: {str(e)}")
        return False