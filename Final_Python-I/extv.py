import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# App title
st.title("Expense Tracker and Visualisation")

# File names
EXPENSE_FILE = "expenses.csv"
DEBT_FILE = "debts.csv"

# Page navigation
page = st.selectbox(
    "Select Page",
    ["Expense Tracker", "Debt Tracker", "Visualisations"]
)

# Load expense data
try:
    exp_df = pd.read_csv(EXPENSE_FILE)
except FileNotFoundError:
    exp_df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

exp_dates = exp_df["Date"].tolist()
exp_categories = exp_df["Category"].tolist()
exp_amounts = exp_df["Amount"].tolist()
exp_descriptions = exp_df["Description"].tolist()

indices = list(range(len(exp_dates)))

def get_expense_date(i):
    return exp_dates[i]

sorted_indices = sorted(indices, key=get_expense_date)

exp_dates = [exp_dates[i] for i in sorted_indices]
exp_categories = [exp_categories[i] for i in sorted_indices]
exp_amounts = [exp_amounts[i] for i in sorted_indices]
exp_descriptions = [exp_descriptions[i] for i in sorted_indices]

exp_df = pd.DataFrame({
    "Date": exp_dates,
    "Category": exp_categories,
    "Amount": exp_amounts,
    "Description": exp_descriptions
})

# Load debt data
try:
    debt_df = pd.read_csv(DEBT_FILE)
except FileNotFoundError:
    debt_df = pd.DataFrame(
        columns=["Date", "Person", "Amount", "Type", "Note", "Status"]
    )

debt_dates = debt_df["Date"].tolist()
debt_people = debt_df["Person"].tolist()
debt_amounts = debt_df["Amount"].tolist()
debt_types = debt_df["Type"].tolist()
debt_notes = debt_df["Note"].tolist()
debt_status = debt_df["Status"].tolist()

indices_d = list(range(len(debt_dates)))

def get_debt_date(i):
    return debt_dates[i]

sorted_indices_d = sorted(indices_d, key=get_debt_date)

debt_dates = [debt_dates[i] for i in sorted_indices_d]
debt_people = [debt_people[i] for i in sorted_indices_d]
debt_amounts = [debt_amounts[i] for i in sorted_indices_d]
debt_types = [debt_types[i] for i in sorted_indices_d]
debt_notes = [debt_notes[i] for i in sorted_indices_d]
debt_status = [debt_status[i] for i in sorted_indices_d]

debt_df = pd.DataFrame({
    "Date": debt_dates,
    "Person": debt_people,
    "Amount": debt_amounts,
    "Type": debt_types,
    "Note": debt_notes,
    "Status": debt_status
})

# Expense tracker page
if page == "Expense Tracker":
    st.sidebar.header("Add Expense")

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
            exp_dates.append(str(expense_date))
            exp_categories.append(category)
            exp_amounts.append(amount)
            exp_descriptions.append(description)

            pd.DataFrame({
                "Date": exp_dates,
                "Category": exp_categories,
                "Amount": exp_amounts,
                "Description": exp_descriptions
            }).to_csv(EXPENSE_FILE, index=False)

            st.sidebar.success("Expense added successfully")

    st.subheader("Summary")

    total = 0
    for a in exp_amounts:
        total += a

    if len(exp_amounts) > 0:
        st.write("Total spent: ₹", total)
        st.write("Average expense: ₹", round(total / len(exp_amounts), 2))
    else:
        st.info("No expenses recorded yet")

    st.subheader("Monthly budget")

    budget = st.number_input("Set monthly budget", min_value=0.0, value=5000.0)
    current_month = str(date.today())[:7]
    monthly_total = 0

    for i in range(len(exp_dates)):
        if exp_dates[i][:7] == current_month:
            monthly_total += exp_amounts[i]

    if budget > 0:
        st.write(f"Spent this month: ₹{monthly_total}")
        st.progress(min(monthly_total / budget, 1.0))

    st.download_button(
        "Download Expenses CSV",
        exp_df.to_csv(index=False),
        "expenses.csv",
        "text/csv"
    )

    st.dataframe(exp_df)

# Debt tracker page
if page == "Debt Tracker":
    st.sidebar.header("Add Debt")

    debt_date = st.sidebar.date_input("Date", date.today())
    person = st.sidebar.text_input("Person name")
    debt_amount = st.sidebar.number_input("Amount", min_value=0.0)
    debt_type = st.sidebar.selectbox("Type", ["I Owe", "Owed To Me"])
    note = st.sidebar.text_input("Note")

    if st.sidebar.button("Add Debt"):
        if debt_amount <= 0 or person == "":
            st.sidebar.error("Enter valid details")
        else:
            debt_dates.append(str(debt_date))
            debt_people.append(person)
            debt_amounts.append(debt_amount)
            debt_types.append(debt_type)
            debt_notes.append(note)
            debt_status.append("Unpaid")

            pd.DataFrame({
                "Date": debt_dates,
                "Person": debt_people,
                "Amount": debt_amounts,
                "Type": debt_types,
                "Note": debt_notes,
                "Status": debt_status
            }).to_csv(DEBT_FILE, index=False)

            st.sidebar.success("Debt added successfully")

    st.subheader("Debt summary")

    owe = 0
    get = 0

    for i in range(len(debt_amounts)):
        if debt_status[i] == "Unpaid":
            if debt_types[i] == "I Owe":
                owe += debt_amounts[i]
            else:
                get += debt_amounts[i]

    st.error(f"You owe: ₹{owe}")
    st.success(f"Owed to you: ₹{get}")
    st.info(f"Net balance: ₹{get - owe}")

    st.subheader("Mark debt as paid")

    unpaid = []

    for i in range(len(debt_people)):
        if debt_status[i] == "Unpaid":
            unpaid.append(f"{i} - {debt_people[i]} ₹{debt_amounts[i]}")

    if len(unpaid) == 0:
        st.success("All debts cleared")
    else:
        selected = st.selectbox("Select debt", unpaid)

        if st.button("Mark as paid"):
            idx = int(selected.split(" - ")[0])
            debt_status[idx] = "Paid"

            pd.DataFrame({
                "Date": debt_dates,
                "Person": debt_people,
                "Amount": debt_amounts,
                "Type": debt_types,
                "Note": debt_notes,
                "Status": debt_status
            }).to_csv(DEBT_FILE, index=False)

            st.success("Debt marked as paid")

    st.download_button(
        "Download Debts CSV",
        debt_df.to_csv(index=False),
        "debts.csv",
        "text/csv"
    )

    st.dataframe(debt_df)

# Visualisation page
if page == "Visualisations":
    st.header("Expense Visualisations")

    if len(exp_amounts) == 0:
        st.warning("No data available")
    else:
        plt.figure(figsize=(6, 4))
        plt.hist(exp_amounts, bins=10, label="Expenses")
        plt.legend()
        st.pyplot(plt)
        plt.clf()

        monthly_data = {}
        names = {"01":"January","02":"February","03":"March","04":"April",
                 "05":"May","06":"June","07":"July","08":"August",
                 "09":"September","10":"October","11":"November","12":"December"}

        for i in range(len(exp_dates)):
            m = names[exp_dates[i][5:7]]
            monthly_data[m] = monthly_data.get(m, 0) + exp_amounts[i]

        plt.figure(figsize=(6, 4))
        plt.plot(list(monthly_data.keys()), list(monthly_data.values()), marker="o")
        st.pyplot(plt)
        plt.clf()

        category_data = {}

        for i in range(len(exp_categories)):
            category_data[exp_categories[i]] = category_data.get(
                exp_categories[i], 0
            ) + exp_amounts[i]

        plt.figure(figsize=(5, 4))
        plt.pie(
            category_data.values(),
            labels=category_data.keys(),
            explode=[0.05]*len(category_data),
            autopct="%1.1f%%"
        )
        st.pyplot(plt)
        plt.clf()
