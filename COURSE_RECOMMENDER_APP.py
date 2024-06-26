# importing libraries

import streamlit as st
import streamlit.components.v1 as stc

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel

# load our dataset
def load_data(course_recommender):
    df = pd.read_csv(course_recommender)
    return df

# Fxn
# Vectorize + Cosine Similarity Matrix

def vectorize_text_to_cosine_mat(course_recommender):
    count_vect = CountVectorizer()
    cv_mat = count_vect.fit_transform(course_recommender)
    # Get the cosine
    cosine_sim_mat = cosine_similarity(cv_mat)
    return cosine_sim_mat

#  Recommendation system
@st.cache_data
def get_recommendation(title,cosine_sim_mat,df,num_of_rec=5):
    # indices of the course
    course_indices = pd.Series(df.index,index=df['course_title']).drop_duplicates()
    # index of course
    idx = course_indices[title]

#look into the cosine matrix for that index
    sim_scores = list(enumerate(cosine_sim_mat[idx]))
    sim_scores = sorted(sim_scores,key=lambda x:x[1],reverse=True)
    selected_course_indices = [i[0] for i in sim_scores[1:]]
    selected_course_scores = [i[0] for i in sim_scores[1:]]

    # get the dataframe & title
    result_df = df.iloc[selected_course_indices]
    result_df['similarity_score'] = selected_course_scores
    final_recommended_courses = result_df[['course_title','similarity_score','url','price','num_subscribers']]
    return final_recommended_courses

# Search for course
@st.cache_data
def search_term_if_not_found(term,df):
    result_df = df[df["course_title"].str.contains(term)]
    return result_df
# CSS Style
RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #a8f0c6;
  border-left: 5px solid #6c6c6c;">
<h4>{}</h4>
<p style="color:blue;"><span style="color:black;">📈Score::</span>{}</p>
<p style="color:blue;"><span style="color:black;">🔗</span><a href="{}",target="_blank">Link</a></p>
<p style="color:blue;"><span style="color:black;">💲Price:</span>{}</p>
<p style="color:blue;"><span style="color:black;">🧑‍🎓👨🏽‍🎓 Students:</span>{}</p>

</div>
"""
def main():
    st.title("COURSE RECOMMENDATION APP")

    menu = ["Home","Recommend","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    df = load_data("C:\MOD_14_WEB_APPLICATION\course_recommender/udemy_course_data.csv")

    if choice == "Home":
        st.subheader("Home")
        st.dataframe(df.head(10))

    elif choice == "Recommend":
       st.subheader("Recommend Courses")
       cosine_sim_mat = vectorize_text_to_cosine_mat(df['course_title'])
       search_term = st.text_input("Search")
       num_of_rec = st.sidebar.number_input("Number",4,30,7)
       if st.button("Recommend"):
           if search_term is not None:
               try:
                   results = get_recommendation(search_term, cosine_sim_mat, df, num_of_rec)


                   for row in results.iterrows():
                       rec_title = row[1][0]
                       rec_score = row[1][1]
                       rec_url = row[1][2]
                       rec_price = row[1][3]
                       rec_num_sub = row[1][4]

                       # st.write("Title",rec_title)
                       stc.html(RESULT_TEMP.format(rec_title, rec_score, rec_url, rec_price, rec_num_sub), height=350)
               except:
                   results = "Not Found"
                   st.warning(results)
                   st.info("Suggested Options include")
                   results_df = search_term_if_not_found(search_term,df)
                   st.dataframe(results_df)

               # st.write(results)

               # how to maximize your profits options trading
    else:
        st.subheader("About")
        st.text("Built with Streamlit & Pandas")


if __name__ == "__main__":
    main()
