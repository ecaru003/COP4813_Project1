#########################   Imports   ################################
import requests
import nltk
import streamlit as st
import main_functions
import pandas as pd
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#########################   Variables   ################################
apiKey=main_functions.read_from_file("JSON_Files/api_key.json")["my_key"]

urlTopBase="https://api.nytimes.com/svc/topstories/v2/"
urlTopEnd =".json?api-key=" + apiKey
#urlTop = urlTopBase + topic_choice + urlTopEnd

urlPopBase="https://api.nytimes.com/svc/mostpopular/v2/"
urlPopEnd=".json?api-key=" + apiKey
#urlPop= urlPopBase + form +"/" + days + urlPopEnd

topicsStr="arts,automobiles,books,business,fashion,food,health,home,insider,magazine,movies,nyregion,obituaries,opinion,politics,realestate,science,sports,sundayreview,technology,theater,t-magazine,travel,upshot,us,world"
topicsStr=topicsStr.split(",")
topics = [""]
for t in topicsStr:
    topics.append(t)

#########################   Methods   ################################
def get_json(request_url):
    request_response = requests.get(request_url).json()
    main_functions.save_to_file(request_response, "JSON_Files/response.json")

def get_abstracts():
    my_articles = main_functions.read_from_file("JSON_Files/response.json")
    all_abstracts = ""
    for a in my_articles["results"]:
        all_abstracts = all_abstracts + a["abstract"]
    return all_abstracts

def get_clean_words():
    abstracts = get_abstracts()
    all_words = word_tokenize(abstracts)

    words_no_punc = []
    for w in all_words:
        if w.isalpha():
            words_no_punc.append(w.lower())

    sw = stopwords.words("english")
    clean_words = []
    for m in words_no_punc:
        if m not in sw:
            clean_words.append(m)

    return clean_words



#########################   Page Design   ################################
st.title("Project 1")

st.text("Project: Project 1\n"
        "Author: Edrey Carulo\n"
        "Date: 10/03/2020")


st.header("Part A - Top Stories API")
st.subheader("I - Topic Selection")

user_name = st.text_input("Please enter your name:")

topic_choice = st.selectbox("Select a topic of interest:", topics)




if topic_choice != "":
    urlTop = urlTopBase + topic_choice + urlTopEnd         #Generates URL based on chosen word, unless invalid
    st.write("Hi {}, you selected {} as your topic.".format(user_name, topic_choice))

    get_json(urlTop)

    st.subheader("II - Frequency Distribution")
    freqdist_pie = st.checkbox("Click here to generate a frequency distribution as pie chart.")
    freqdist_bar = st.checkbox("Click here to generate a frequency distribution as bar chart.")
    if freqdist_pie or freqdist_bar:
        fdist = FreqDist(get_clean_words())
        most_common = fdist.most_common(10)

        mc_words = []  # labels
        mc_values = []  # sizes,
        for e in most_common:
            mc_words.append(e[0])
            mc_values.append(e[1])

        if freqdist_pie:
            plt.pie(mc_values,labels=mc_words, autopct='%1.1f%%', startangle=90)
            plt.axis("equal")
            st.pyplot(plt)

        if freqdist_bar:
            freq_data = pd.DataFrame(mc_values,index=mc_words)
            st.bar_chart(freq_data)


    st.subheader("III - Wordcloud")
    wCloud = st.checkbox("Click here to generate a wordcloud.")
    if wCloud:
        wordcloud = WordCloud().generate(get_abstracts())
        plt.figure(figsize=(20,20))
        plt.imshow(wordcloud)
        plt.axis("off")
        st.pyplot(plt)


st.header("Part B - Most Popular Articles")
st.subheader("Select if you want to see the most shared, emailed or viewed articles.")

popular_form = st.selectbox("Select your preferred set of articles.", ["","shared","emailed","viewed"])

popular_days = st.selectbox("Select the period of time (last days)", ["","1","7","30"])

if popular_form != "" and popular_days != "":
    urlPop = urlPopBase + popular_form +"/"+popular_days+urlPopEnd

    get_json(urlPop)

    wordcloud = WordCloud().generate(get_abstracts())
    plt.figure(figsize=(20, 20))
    plt.imshow(wordcloud)
    plt.axis("off")
    st.pyplot(plt)
