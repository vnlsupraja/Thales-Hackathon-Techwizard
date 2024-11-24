import streamlit as st
from mongo import UserCredential
import genai_chatbot
import dashboard

def authenticate(username, password):
    cred_ob = UserCredential()
    actual_password = cred_ob.get_credential_by_username(username)
    if actual_password:
        if actual_password == password:
            return True
    return False

def add_background_image():
    """Add a background image to the login page using CSS and place the new image at the top left corner."""
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.wsj.net/im-821375?width=700&height=466");
            background-size: 50%; /* Reduce background image size to 50% */
            background-repeat: no-repeat; /* Ensure the image does not repeat */
            background-position: center; /* Center the background image */
        }
        .top-left-image {
            position: fixed;
            top: 0;
            left: 0;
            width: 150px;
            height: auto;
            z-index: 1; /* Ensure the image is on top of other elements */
        }
        .title {
            color: white;
        }
        /* Targeting the input fields */
        div[data-testid="stTextInput"] > div > input {
            color: green !important;
            background-color: lightyellow !important;
            border: 2px solid blue !important;
        }
        /* Targeting the labels */
        div[data-testid="stTextInput"] > label {
            color: white !important;
        }
        .success-message {
            color: green;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
 
def login_page():
    """Display the login page."""
    add_background_image()  # Call the function to add the background image
    st.markdown('<h1 class="title">Login Page</h1>', unsafe_allow_html=True)
   
    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
 
    # Button to trigger login
    login_button = st.button("Login")
 
    if login_button:
        if authenticate(username, password):
            st.session_state.logged_in = True  # Store the login state
            st.session_state.username = username  # Store the username
            st.success("Login Successful!")
            st.markdown('<p class="success-message">Login Successful!</p>', unsafe_allow_html=True)
            if "admin" in username.lower():
                st.session_state.page = "dashboard"  # Redirect admin to dashboard
            else:
                st.session_state.page = "chat"  # Redirect user to chat page
            st.rerun()  # Reload the app to trigger the appropriate page
        else:
            st.error("Invalid username or password.")


def home_page():
    """Display the home page after login."""
    st.title(f"Welcome, {st.session_state.username}!")
    st.write("This is the home page.")
    
    if st.button("Go to Dashboard"):
        st.session_state.page = "dashboard"  # Set the page state to 'dashboard'
        st.experimental_rerun()  # Reload the app to go to the dashboard



def main():
    """Main function that handles the routing."""
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        add_background_image()  # Add background image on login page
        login_page()  # Show the login page if not logged in
    elif 'page' not in st.session_state or st.session_state.page == "home":
        home_page()  # Show the home page if logged in
    elif st.session_state.page == "dashboard":
        dashboard.main()  # Show the dashboard if the user navigates there
    elif st.session_state.page == "chat":
        st.header(f"🌟 Welcome {st.session_state.username} 🌟")
        genai_chatbot.main_func()
          # Show the chat page if the user navigates there

if __name__ == "__main__":
    main()
