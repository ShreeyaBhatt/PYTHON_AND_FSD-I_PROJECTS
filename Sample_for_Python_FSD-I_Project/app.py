import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.title("💰 Expense Tracker")

FILE_NAME = "expenses.csv"

# ------------------ Page Navigation ------------------
page = st.selectbox("Select Page", ["Expense Tracker", "Visualizations"])

# ------------------ Load Data (Pandas only for CSV) ------------------
try:
    df = pd.read_csv(FILE_NAME)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

dates = df["Date"].tolist()
categories = df["Category"].tolist()
amounts = df["Amount"].tolist()
descriptions = df["Description"].tolist()

# ====================================================
# ================= PAGE 1 ===========================
# ====================================================
if page == "Expense Tracker":

    # -------- Sidebar: Add Expense --------
    st.sidebar.header("➕ Add Expense")

    expense_date = st.sidebar.date_input("Date", date.today())
    category = st.sidebar.selectbox(
        "Category",
        ["Food", "Transport", "Entertainment", "Utilities", "Other"]
    )
    amount = st.sidebar.number_input("Amount", min_value=0.0)
    description = st.sidebar.text_input("Description")

    if st.sidebar.button("Add Expense"):
        if amount <= 0:
            st.sidebar.error("Amount must be greater than zero")
        else:
            dates.append(str(expense_date))
            categories.append(category)
            amounts.append(amount)
            descriptions.append(description)

            new_df = pd.DataFrame({
                "Date": dates,
                "Category": categories,
                "Amount": amounts,
                "Description": descriptions
            })
            new_df.to_csv(FILE_NAME, index=False)
            st.sidebar.success("Expense Added Successfully!")

    # -------- Summary (Pure Python) --------
    st.subheader("📊 Summary")

    if len(amounts) > 0:
        total = 0
        for i in range(len(amounts)):
            total += amounts[i]

        average = total / len(amounts)

        st.write("**Total Spent:** ₹", total)
        st.write("**Average Expense:** ₹", round(average, 2))
    else:
        st.info("No expenses recorded yet.")

    # -------- Highest / Lowest Expense (Pure Python) --------
    st.subheader("🏆 Expense Highlights")

    if len(amounts) > 0:
        max_amount = amounts[0]
        min_amount = amounts[0]

        for i in range(len(amounts)):
            if amounts[i] > max_amount:
                max_amount = amounts[i]
            if amounts[i] < min_amount:
                min_amount = amounts[i]

        high_cat = ""
        low_cat = ""

        for i in range(len(amounts)):
            if amounts[i] == max_amount:
                high_cat = categories[i]
            if amounts[i] == min_amount:
                low_cat = categories[i]

        st.success(f"Highest Expense: ₹{max_amount} ({high_cat})")
        st.info(f"Lowest Expense: ₹{min_amount} ({low_cat})")
    else:
        st.warning("No expenses available.")

    # -------- Budget Progress Bar --------
    st.subheader("🎯 Monthly Budget Tracker")

    budget = st.number_input("Set Monthly Budget (₹)", min_value=0.0)

    if budget > 0 and len(amounts) > 0:
        spent = 0
        for i in range(len(amounts)):
            spent += amounts[i]

        percent = int((spent / budget) * 100)
        if percent > 100:
            percent = 100

        st.write(f"Spent ₹{spent} out of ₹{budget}")
        st.progress(percent)

    # -------- Expense Table --------
    st.subheader("📋 Expense History")
    st.dataframe(df)

# ====================================================
# ================= PAGE 2 ===========================
# ====================================================
if page == "Visualizations":

    st.header("📈 Expense Visualizations")

    if len(amounts) == 0:
        st.warning("No data available for visualization.")
    else:
        # -------- Monthly Expense Comparison (NO zip) --------
        st.subheader("📅 Monthly Expense Comparison")

        monthly_data = {}

        for i in range(len(dates)):
            month = dates[i][:7]   # YYYY-MM
            if month in monthly_data:
                monthly_data[month] += amounts[i]
            else:
                monthly_data[month] = amounts[i]

        months = []
        month_amounts = []

        for m in monthly_data:
            months.append(m)
            month_amounts.append(monthly_data[m])

        plt.figure(figsize=(6, 4))
        plt.bar(months, month_amounts)
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.title("Monthly Expenses")
        st.pyplot(plt)
        plt.clf()

        # -------- Category-wise Distribution (NO zip) --------
        st.subheader("🍰 Category-wise Distribution")

        category_data = {}

        for i in range(len(categories)):
            if categories[i] in category_data:
                category_data[categories[i]] += amounts[i]
            else:
                category_data[categories[i]] = amounts[i]

        labels = []
        values = []

        for c in category_data:
            labels.append(c)
            values.append(category_data[c])

        plt.figure(figsize=(5, 4))
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Expense Distribution by Category")
        st.pyplot(plt)
        plt.clf()
