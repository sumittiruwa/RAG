import streamlit as st

st.set_page_config(layout="wide") # Set the layout to wide

#title of our app 
st.title("Ai blog")

#subheader
st.subheader("Generate your blog using AI") 

#siderbar
with st.sidebar:
    st.title("input your prompt here")
    st.subheader("enter the deatil here")
    
    
    # blog Title 
    blog_title = st.text_input("Enter your blog title")
    
    #keyoword
    keyword = st.text_input("Enter your keyword (comma-seperated)")
    
    
    # Number of Words
    num_words = st.slider("Select the number of words for your blog", min_value=100, max_value=2000, value=500, step=50)