import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.title("💰 Expense Tracker and Visualisation")

EXPENSE_FILE = "expenses.csv"
DEBT_FILE = "debts.csv"

# ------------------ Page Navigation ------------------
page = st.selectbox(
    "Select Page",
    ["Expense Tracker", "Debt Tracker", "Visualisations"]
)

# ------------------ Load Expense Data ------------------
try:
    exp_df = pd.read_csv(EXPENSE_FILE)
except FileNotFoundError:
    exp_df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

exp_dates = exp_df["Date"].tolist()
exp_categories = exp_df["Category"].tolist()
exp_amounts = exp_df["Amount"].tolist()
exp_descriptions = exp_df["Description"].tolist()

# -------- SORT EXPENSE DATA BY DATE USING sorted() WITHOUT zip() --------
indices = list(range(len(exp_dates)))
sorted_indices = sorted(indices, key=lambda x: exp_dates[x])

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

# ------------------ Load Debt Data ------------------
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

# -------- SORT DEBT DATA BY DATE USING sorted() WITHOUT zip() --------
indices_d = list(range(len(debt_dates)))
sorted_indices_d = sorted(indices_d, key=lambda x: debt_dates[x])

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

# ====================================================
# ================= EXPENSE PAGE =====================
# ====================================================
if page == "Expense Tracker":

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
            exp_dates.append(str(expense_date))
            exp_categories.append(category)
            exp_amounts.append(amount)
            exp_descriptions.append(description)

            new_df = pd.DataFrame({
                "Date": exp_dates,
                "Category": exp_categories,
                "Amount": exp_amounts,
                "Description": exp_descriptions
            })
            new_df.to_csv(EXPENSE_FILE, index=False)
            st.sidebar.success("Expense Added Successfully!")

    st.subheader("📊 Summary")

    if len(exp_amounts) > 0:
        total = 0
        for a in exp_amounts:
            total += a

        st.write("**Total Spent:** ₹", total)
        st.write("**Average Expense:** ₹", round(total / len(exp_amounts), 2))
    else:
        st.info("No expenses recorded yet.")

    # ---------------- MONTHLY BUDGET PROGRESS ----------------
    st.subheader("🎯 Monthly Budget Progress")

    # User selects month
    month_input = st.date_input("Choose Month for Budget", date.today())
    selected_month = str(month_input)[:7]  # YYYY-MM

    budget = st.number_input("Set Monthly Budget (₹)", min_value=0.0)

    if budget > 0:
        monthly_total = 0

        for i in range(len(exp_dates)):
            if exp_dates[i][:7] == selected_month:
                monthly_total += exp_amounts[i]

        st.write(f"Spent in {selected_month}: ₹{monthly_total}")
        progress = int((monthly_total / budget) * 100)
        if progress > 100:
            progress = 100

        st.progress(progress)

    st.subheader("📋 Expense History (Oldest → Newest)")
    st.dataframe(exp_df)

# ====================================================
# ================= DEBT PAGE ========================
# ====================================================
if page == "Debt Tracker":

    st.sidebar.header("➕ Add Debt")

    debt_date = st.sidebar.date_input("Date", date.today())
    person = st.sidebar.text_input("Person Name")
    debt_amount = st.sidebar.number_input("Amount", min_value=0.0)
    debt_type = st.sidebar.selectbox(
        "Type",
        ["I Owe", "Owed To Me"]
    )
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

            new_debt_df = pd.DataFrame({
                "Date": debt_dates,
                "Person": debt_people,
                "Amount": debt_amounts,
                "Type": debt_types,
                "Note": debt_notes,
                "Status": debt_status
            })
            new_debt_df.to_csv(DEBT_FILE, index=False)
            st.sidebar.success("Debt Added Successfully!")

    st.subheader("📊 Debt Summary (Unpaid Only)")

    total_owe = 0
    total_get = 0

    for i in range(len(debt_amounts)):
        if debt_status[i] == "Unpaid":
            if debt_types[i] == "I Owe":
                total_owe += debt_amounts[i]
            else:
                total_get += debt_amounts[i]

    st.error(f"💸 You Owe: ₹{total_owe}")
    st.success(f"💰 Owed To You: ₹{total_get}")
    st.info(f"📌 Net Balance: ₹{total_get - total_owe}")

    st.subheader("✅ Mark Debt as Paid")

    unpaid = []

    for i in range(len(debt_people)):
        if debt_status[i] == "Unpaid":
            unpaid.append(f"{i} - {debt_people[i]} ₹{debt_amounts[i]}")

    if len(unpaid) == 0:
        st.success("All debts cleared 🎉")
    else:
        selected = st.selectbox("Select Debt", unpaid)

        if st.button("Mark as Paid"):
            idx = int(selected.split(" - ")[0])
            debt_status[idx] = "Paid"

            updated_df = pd.DataFrame({
                "Date": debt_dates,
                "Person": debt_people,
                "Amount": debt_amounts,
                "Type": debt_types,
                "Note": debt_notes,
                "Status": debt_status
            })
            updated_df.to_csv(DEBT_FILE, index=False)

            st.success("Debt marked as Paid ✅")

    st.subheader("📋 Debt History")
    st.dataframe(debt_df)

# ====================================================
# ================= Visualisation PAGE ===============
# ====================================================
if page == "Visualisations":

    st.header("📈 Expense Visualisations")

    if len(exp_amounts) == 0:
        st.warning("No data available.")
    else:
        # -------- DAILY HISTOGRAM --------
        st.subheader("📊 Daily Expense Distribution (Histogram)")

        plt.figure(figsize=(6, 4))
        plt.hist(exp_amounts, bins=10)
        plt.xlabel("Expense Amount")
        plt.ylabel("Frequency")
        plt.title("Daily Expense Histogram")
        st.pyplot(plt)
        plt.clf()

        # -------- MONTHLY LINE GRAPH --------
        st.subheader("📈 Monthly Expense Trend")

        monthly_data = {}

        for i in range(len(exp_dates)):
            month = exp_dates[i][:7]
            if month in monthly_data:
                monthly_data[month] += exp_amounts[i]
            else:
                monthly_data[month] = exp_amounts[i]

        months = []
        totals = []

        for m in monthly_data:
            months.append(m)
            totals.append(monthly_data[m])

        plt.figure(figsize=(6, 4))
        plt.plot(months, totals, marker="o")
        plt.xlabel("Month")
        plt.ylabel("Total Spent")
        plt.title("Monthly Expense Line Graph")
        st.pyplot(plt)
        plt.clf()

        # -------- CATEGORY PIE CHART --------
        st.subheader("🥧 Category-wise Expense Distribution")

        category_data = {}

        for i in range(len(exp_categories)):
            if exp_categories[i] in category_data:
                category_data[exp_categories[i]] += exp_amounts[i]
            else:
                category_data[exp_categories[i]] = exp_amounts[i]

        labels = []
        values = []

        for c in category_data:
            labels.append(c)
            values.append(category_data[c])

        plt.figure(figsize=(5, 4))
        plt.pie(values, labels=labels, autopct="%1.1f%%")
        plt.title("Expenses by Category")
        st.pyplot(plt)
        plt.clf()
