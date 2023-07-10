import streamlit as st
import requests
from streamlit_option_menu import option_menu

def streamlit_app():
    with st.sidebar:
        selected = option_menu("Main Menu", ["Introduction", 'Predict', 'Searching'], 
            icons=['house', 'gear'], menu_icon="cast", default_index=0)

    if selected == "Introduction":
        st.title("Introduction")
    if selected == "Predict":
        st.title("Predict caption")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            response = requests.post("http://localhost:81/predict/", files={"file": uploaded_file})
            output = response.json()
            
        if st.button("GET CAPTION HERE"):
                st.write("Prediction:")
                st.image(output["image_path"])
                st.write("Caption:", output["caption"])

    if selected == "Searching":
        st.title("Searching some products")
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            response = requests.post("http://localhost:81/search/", files={"file": uploaded_file})
            output = response.json()

        if st.button("GET SOME RELATED PRODUCT HERE"):
                st.write("Searching result:")
                st.image(output["image_path"])
                results = output["result"][1]
                st.write("Here are some results")
                for result in results:
                    st.write(result)

if __name__ == "__main__":
    streamlit_app()
