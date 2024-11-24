import streamlit as st
from config import USER_PROMPT
from PIL import Image, ImageEnhance
from utility import get_response_from_gemini
import base64

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

def main_func():
    st.title("Thales Guardian: Protecting You from Email Scams 💬")
    # Display chat history 
    if "messages" not in st.session_state: 
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message (message ["role"]): 
            st.markdown(message["content"])

    if prompt_from_user := st.chat_input("Ask Something"):

        st.session_state.messages.append({'role': 'user', "content": prompt_from_user})
        with st.chat_message("user"):
            st.markdown(prompt_from_user)
        prompt = USER_PROMPT.format(prompt_from_user)
        response = get_response_from_gemini(prompt)

        st.session_state.messages.append({'role': 'assistant', "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    
        # Insert custom CSS for glowing effect
        st.markdown(
            """
            <style>
            .cover-glow {
                width: 100%;
                height: 100vh;
                padding: 3px;
                box-shadow: 
                    0 0 5px #330000,
                    0 0 10px #660000,
                    0 0 15px #990000,
                    0 0 20px #CC0000,
                    0 0 25px #FF0000,
                    0 0 30px #FF3333,
                    0 0 35px #FF6666;
                position: relative;
                z-index: -1;
                border-radius: 45px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        img_path = r"images\back3.jpg"
        img_base64 = img_to_base64(img_path)
        if img_base64:
            st.sidebar.markdown(
                f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
                unsafe_allow_html=True,
            )


# if __name__ == "__main__":
#     main()