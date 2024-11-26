# Thales Secure Mail Analyzer
![photo png](https://github.com/user-attachments/assets/18b2788b-dff4-40da-8b5d-53e9c6addb9a)


**Thales Secure Mail Analyzer** is an advanced email security and management system designed to enhance organizational email safety. This project was developed for the **Thales GenTech India Hackathon** and aims to provide administrators with robust tools for managing email data while empowering end-users with AI-driven guidance to combat email threats.

---

## **Key Features**

### **User Authentication**
- **Secure Login System**: Integrated with MongoDB for credential validation.
- **Role-Based Access**:
  - **Admins**: Access an advanced dashboard for email management and analysis.
  - **Regular Users**: Redirected to an AI-powered chatbot for real-time assistance.

### **Admin Dashboard**
![Admin Dashboard_Email Refresh_ Dynamically updates the latest email data wi_20241126_090823_0000](https://github.com/user-attachments/assets/4f4008e1-e84a-43ca-8fcf-ebfac41150cd)

- **Email Refresh**: Dynamically updates the latest email data with one click.
- **Email Sending**: Compose and send security-related emails to users.
- **Data Display**: View detailed email data (sender, receiver, subject, date, category).
- **Filtering and Sorting**: Analyze emails by sender or date range.
- **Summary Statistics**:
  - Total emails processed.
  - Spam, phishing, and normal email counts.
  - Spam/phishing classification percentages.
- **Data Visualizations**:
  - Spam/Phishing email trends (line charts).
  - Top spam senders (bar charts).
  - Email subject patterns (word clouds).

### **AI-Powered Chatbot**
- **Thales Guardian Chatbot**:
  - Provides real-time guidance on identifying email threats.
  - Educates users on phishing and email safety best practices.
  - Features an engaging UI with glowing design effects.

---

## **Technical Stack**
- **Streamlit**: Interactive and user-friendly web interface.
- **MongoDB**: Database for storing user credentials and email data.
- **SMTP**: Automates email delivery directly from the dashboard.
- **Altair & WordCloud**: For generating dynamic data visualizations.
- **AI-Powered Chatbot**: Educates users and offers personalized responses.
- **Real-Time Data Ingestion**: Simulates email data for analysis and visualization.

---

## **Use Case and Impact**
- **For Admins**:
  - Analyze threats, refresh email data, and send security updates directly.
- **For Regular Users**:
  - AI-powered chatbot assistance for real-time email threat guidance.
- **Impact**:
  - Enhances email security operations.
  - Improves admin efficiency.
  - Empowers users to prevent email scams effectively.

---

## **Demo & Resources**
- **Video Playlist**: [Watch the video](https://m.youtube.com/playlist?list=PLfJhwbzVT0Tjenm6biEL89NnRevpeYm77)
- **Presentation**: [View presentation](https://he-s3.s3.amazonaws.com/media/sprint/thales-gentech-india-hackathon/team/2119330/28a989bthales_ppi_sub.pptx)
- **Demo App**: [Try the demo](https://techwizardthaleshackethon.streamlit.app/)
- **Repository**: [GitHub Repo](https://github.com/vnlsupraja/Thales-Hackathon-Techwizard)

## **Instructions for Testing**
1. Access the demo app using the credentials below:
   - **User Chatbot Access**:
     - Username: `thales_user1`
     - Password: `ThalesUserPass1`
   - **Admin Dashboard Access**:
     - Username: `thales_admin1`
     - Password: `ThalesAdminPass1`

2. Navigate through the chatbot or dashboard to explore functionality.
