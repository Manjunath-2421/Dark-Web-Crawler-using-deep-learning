import streamlit as st
import os 
import utils
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-container {
        max-width: 800px;
        padding: 30px;
        margin: auto;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 36px;
        color: #333;
        text-align: center;
        margin-bottom: 30px;
    }
    .paragraph {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .input-section {
        margin-bottom: 20px;
    }
    .button-crawl {
        padding: 10px 20px;
        font-size: 18px;
        font-weight: bold;
        color: #fff;
        background-color: #5bc0de;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .result-section {
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to display classification results with bar chart
def display_classification_results(df):
    st.success('Classification Results')
    st.write(df)
    st.bar_chart(df.set_index('label'))

# Function to plot a pie chart for the label with the highest score
def plot_pie_chart(df):
    max_label = df.loc[df['score'].idxmax(), 'label']
    max_score = df.loc[df['score'].idxmax(), 'score']
    other_score = df['score'].sum() - max_score
    labels = [max_label, 'Other Labels']
    sizes = [max_score, other_score]
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Highest Scoring Label')
    st.pyplot()

# Main function
def main():
    st.title('🕵️‍♂️ Dark Web Crawler')
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    st.markdown('<p class="paragraph">Explore the Dark Web</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    link = st.text_input('🔗 Paste web link here')
    btn = st.button('Crawl')
    st.markdown('</div>', unsafe_allow_html=True)

    text_file_path = os.path.join('./data', 'data.txt')

    if link and btn:
        op = utils.fetch_text_from_url(link)
        print(op)

        if os.path.exists(text_file_path):
            with open(text_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                text = text.strip()

            results = utils.classify_text(text)
            df = pd.DataFrame(results[0])
            df = df.sort_values('score', ascending=True) 
            
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            # Display classification results with bar chart
            display_classification_results(df)
            
            # Plot a pie chart for the label with the highest score
            plot_pie_chart(df)
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__=='__main__':
    main()
