import streamlit as st

# Set up the main layout
st.set_page_config(page_title="dashboard2", layout="wide")

# Display buttons in a row
#col1, col2, col3, col4, col5 = st.columns(5)
#with col1:
 #   if st.button("Home"):
#      pass
#with col2:
 #   if st.button("Jobs"):
  #      pass
#with col3:
 #   if st.button("Explore"):
  #      pass
#with col4:
 #   if st.button("Connect"):
  #      pass
#with col5:
 #   if st.button("Pages"):
  #      pass

# Sidebar with user profile and navigation menu
with st.sidebar:
    st.image("C:/Users/hp/Desktop/project/Jobs LLM scrapper/images/6130408.png", width=170)
    st.title("Hey, Mr. User User 👋")
    st.subheader("Navigate your jobs here 🔎👇")
    # st.write("User- Online")

#other buttons for sidebar options
    if st.sidebar.button("BOOKMARKED"):
        st.write("You have not shown interest in any jobs")
    if st.sidebar.button("APPLIED"):
        st.write("You have not applied for any jobs yet")
    if st.sidebar.button("INTERVIEWING"):
        st.write("You have not been shortlisted for any interview yet")
    if st.sidebar.button("NEGOTIATING"):
        st.write("You have not been selected for any job yet")
    if st.sidebar.button("ACCEPTED"):
        st.write("You have not accepted any job yet")


# Main content area with Dashboard statistics
st.subheader("Dashboard")
col1, col3, col2, col4 = st.columns(4)

# Function to display metric with image
def display_metric_with_image(column, title, value, image_path):
    with column:
        st.metric(label=title, value=value)
        st.image(image_path, width=100)

# Display metrics with images
display_metric_with_image(col1, "📌 Bookmarked", "08", "C:/Users/hp/Desktop/project/Jobs LLM scrapper/images/9135326.png")
display_metric_with_image(col3, "📋 Applications", "1.7k", "C:/Users/hp/Desktop/project/Jobs LLM scrapper/images/6904024.png")
display_metric_with_image(col2, "✨ Shortlisted", "03", "C:/Users/hp/Desktop/project/Jobs LLM scrapper/images/6130061.png")
display_metric_with_image(col4, "💵 Accepted", "04", "C:/Users/hp/Desktop/project/Jobs LLM scrapper/images/7090895.png")

st.subheader("My Jobs")
# List different job positions
st.write("Document Writer")
st.write("Product Designer")
