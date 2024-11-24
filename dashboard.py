import streamlit as st
import pandas as pd
import altair as alt
import json
import time
from utility import create_and_ingest_data, generate_random_date, send_mail
import config
from mongo import MongoMailManager
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def main():
    mongo_manager = MongoMailManager(config.MONGO_URI, config.DB_NAME, config.COLLECTION_NAME)
    retrieved_data = mongo_manager.retrieve_email_data()
    email_df = pd.DataFrame(retrieved_data)
    email_df['date'] = pd.to_datetime(email_df['date'])
    email_df.sort_values(by='date', ascending=False, inplace=True)
    email_df.reset_index(drop=True, inplace=True)

    st.title("📧 Enhanced Email Analysis Dashboard")
    st.sidebar.title("Filters")
    
    # Filter options
    sender_filter = st.sidebar.text_input("Search by Sender")
    date_range = st.sidebar.date_input("Date Range", [])
    st.sidebar.title("Refresh Mail Data")
    button_clicked = st.sidebar.button('Refresh Data')
    # Handle button click event
    if button_clicked:
        with st.spinner('Refreshing email data...'):
            mongo_manager = MongoMailManager(config.MONGO_URI, config.DB_NAME, config.COLLECTION_NAME)
            for i in range(5):
                try:
                    mail_data = create_and_ingest_data()
                    mail_data['date'] = generate_random_date()
                    if mail_data:
                        inserted_id = mongo_manager.save_email_data(mail_data)
                        print("Success")
                        time.sleep(3)
                    else:
                        print("Something wrong happen")
                except Exception as e:
                    print("Getting error", str(e))
        st.sidebar.success("Refreshed email data successfully!")


    st.sidebar.title("Enter Details to send mail")
    receiver_email = st.sidebar.text_input("Receiver's Email", "")
    subject = st.sidebar.text_input("Subject", "")
    body = st.sidebar.text_area("Email Body", "")
    button_clicked_2 = st.sidebar.button("Send Email")
    if button_clicked_2:
        if receiver_email and subject and body:
            send_mail(receiver_email, subject , body) 
            st.sidebar.success("Email  sent successfully!")
        else:
            st.sidebar.error("Please fill in all fields to submit the email details.")


    
    # Apply filters
    filtered_data = email_df
    if sender_filter:
        filtered_data = filtered_data[filtered_data['sender'].str.contains(sender_filter, case=False, na=False)]
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = filtered_data[(pd.to_datetime(filtered_data['date']) >= pd.Timestamp(start_date)) & 
                                      (pd.to_datetime(filtered_data['date']) <= pd.Timestamp(end_date))]
    
    # Display email details
    st.subheader("📋 Email Details")
    st.dataframe(filtered_data[['date', 'subject', 'sender', 'receiver', 'category', 'mail_body']])

    # Summary statistics
    st.subheader("📊 Summary Statistics")
    spam_count = filtered_data[filtered_data['category'] == 'spam'].shape[0]
    phishing_count = filtered_data[filtered_data['category'] == 'phishing'].shape[0]
    not_spam_count = filtered_data[filtered_data['category'] == 'normal'].shape[0]
    total_emails = filtered_data.shape[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Emails", total_emails)
    col2.metric("spam Emails", spam_count)
    col3.metric("Phishing Emails", phishing_count)
    col4.metric("Not spam Emails", not_spam_count)

    # Additional statistics
    st.subheader("📈 More Statistics")
    # Most common email subjects
    top_subjects = filtered_data['subject'].value_counts().head(10).reset_index()
    top_subjects.columns = ['Subject', 'Count']
    st.write("**Top 10 Most Common Subjects**")
    st.write(top_subjects)

    # Top 5 most frequent recipients
    top_recipients = filtered_data['receiver'].value_counts().head(5).reset_index()
    top_recipients.columns = ['Recipient', 'Count']
    st.write("**Top 5 Most Frequent Recipients**")
    st.write(top_recipients)

    # spam/Phishing vs Normal Emails Percentage
    classification_percentage = filtered_data['category'].value_counts(normalize=True).reset_index()
    classification_percentage.columns = ['Classification', 'Percentage']
    st.write("**spam/Phishing vs Normal Emails (%)**")
    st.write(classification_percentage)

    # Visualizations
    st.subheader("📈 Visualizations")

    # 1. spam/Phishing Distribution
    st.markdown("### Classification Distribution")
    classification_chart_data = filtered_data['category'].value_counts().reset_index()
    classification_chart_data.columns = ['Classification', 'Count']
    classification_chart = alt.Chart(classification_chart_data).mark_bar().encode(
        x='Classification',
        y='Count',
        color='Classification'
    )
    st.altair_chart(classification_chart, use_container_width=True)

    # 2. Emails Sent Over Time (Line Chart)
    st.markdown("### Emails Over Time")
    emails_over_time = filtered_data.groupby(filtered_data['date']).size().reset_index(name='Count')
    time_chart = alt.Chart(emails_over_time).mark_line(point=True).encode(
        x='date:T',
        y='Count',
        tooltip=['date', 'Count']
    )
    st.altair_chart(time_chart, use_container_width=True)

    # 3. Top 10 Senders by spam/Phishing Count (Bar Chart)
    st.markdown("### Top 10 Senders by spam/Phishing Emails")
    top_spam_senders = filtered_data[filtered_data['category'].isin(['spam', 'phishing'])]
    sender_spam_count = top_spam_senders['sender'].value_counts().head(10).reset_index()
    sender_spam_count.columns = ['Sender', 'spam Count']
    spam_sender_chart = alt.Chart(sender_spam_count).mark_bar().encode(
        x='spam Count',
        y=alt.Y('Sender', sort='-x'),
        color='spam Count'
    )
    st.altair_chart(spam_sender_chart, use_container_width=True)

    # 5. Category Distribution by Day of the Week (Bar Chart)
    st.markdown("### Category Distribution by Day of the Week")
    filtered_data['day_of_week'] = filtered_data['date'].dt.day_name()
    category_by_day = filtered_data.groupby(['day_of_week', 'category']).size().unstack().fillna(0).reset_index()
    day_category_chart = alt.Chart(category_by_day).mark_bar().encode(
        x='day_of_week',
        y='normal:Q',
        color='category:N',
        tooltip=['day_of_week', 'normal', 'spam', 'phishing']
    ).properties(width=600)
    st.altair_chart(day_category_chart, use_container_width=True)

    # 6. spam/Phishing Emails Over Time (Line Chart)
    st.markdown("### spam/Phishing Emails Over Time")
    spam_phishing_over_time = filtered_data[filtered_data['category'].isin(['spam', 'phishing'])]
    spam_phishing_time = spam_phishing_over_time.groupby(spam_phishing_over_time['date']).size().reset_index(name='Count')
    spam_phishing_time_chart = alt.Chart(spam_phishing_time).mark_line(point=True).encode(
        x='date:T',
        y='Count',
        color='category:N',
        tooltip=['date', 'Count']
    )
    st.altair_chart(spam_phishing_time_chart, use_container_width=True)

    # 7. Word Cloud of Email Subjects
    st.markdown("### Word Cloud of Email Subjects")
    all_subjects = ' '.join(filtered_data['subject'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_subjects)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

if __name__ == "__main__":
    main()
