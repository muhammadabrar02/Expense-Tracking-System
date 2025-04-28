import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# --- Load or Create Data ---
def load_data():
    if os.path.exists("expenses.csv"):
        df = pd.read_csv("expenses.csv")
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    return df

def save_data(df):
    df.to_csv("expenses.csv", index=False)

# --- Sidebar: Navigation ---
st.sidebar.title("Expense Tracker")
menu = st.sidebar.radio("Menu", ["Add Expense", "View Expenses", "Analyze"])

# --- Main Title ---
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>💸 Personal Expense Tracker</h1>", unsafe_allow_html=True)

# --- Load Existing Data ---
df = load_data()

# --- Add Expense ---
if menu == "Add Expense":
    st.subheader("Add a New Expense")
    with st.form(key="expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Entertainment", "Transportation", "Other"])
        with col2:
            date = st.date_input("Date", datetime.now())
            description = st.text_input("Description")

        submit_button = st.form_submit_button(label="Add Expense")

    if submit_button:
         new_expense = {"Date": date, "Category": category, "Amount": amount, "Description": description}
         df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
         save_data(df)
         st.success("Expense added successfully!")


# --- View Expenses ---
elif menu == "View Expenses":
    st.subheader("All Expenses")
    st.dataframe(df)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='expenses.csv',
        mime='text/csv',
    )

# --- Analyze Expenses ---
elif menu == "Analyze":
    st.subheader("Expense Analysis")
    
    if df.empty:
        st.warning("No expenses to analyze.")
    else:
        # Total Spent
        total_spent = df["Amount"].sum()
        st.metric("Total Spent", f"${total_spent:.2f}")

        # Expenses by Category
        category_sum = df.groupby("Category")["Amount"].sum().reset_index()

        fig_pie = px.pie(category_sum, names="Category", values="Amount", title="Expenses by Category")
        st.plotly_chart(fig_pie, use_container_width=True)

        fig_bar = px.bar(category_sum, x="Category", y="Amount", title="Expenses by Category (Bar)")
        st.plotly_chart(fig_bar, use_container_width=True)

