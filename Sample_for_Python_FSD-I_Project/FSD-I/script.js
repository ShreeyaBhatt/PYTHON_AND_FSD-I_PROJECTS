let expenses = JSON.parse(localStorage.getItem("expenses")) || [];

function addExpense() {
    let date = document.getElementById("date").value;
    let category = document.getElementById("category").value;
    let amount = Number(document.getElementById("amount").value);
    let description = document.getElementById("description").value;

    if (date === "" || amount <= 0) {
        alert("Enter valid details");
        return;
    }

    let expense = {
        date: date,
        category: category,
        amount: amount,
        description: description
    };

    expenses.push(expense);
    localStorage.setItem("expenses", JSON.stringify(expenses));

    displayExpenses();
}

function displayExpenses() {
    let tableBody = document.getElementById("expenseTable");
    tableBody.innerHTML = "";

    let total = 0;

    for (let i = 0; i < expenses.length; i++) {
        total += expenses[i].amount;

        let row = document.createElement("tr");

        let cell1 = document.createElement("td");
        cell1.innerText = expenses[i].date;

        let cell2 = document.createElement("td");
        cell2.innerText = expenses[i].category;

        let cell3 = document.createElement("td");
        cell3.innerText = expenses[i].amount;

        let cell4 = document.createElement("td");
        cell4.innerText = expenses[i].description;

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);

        tableBody.appendChild(row);
    }

    let average = expenses.length > 0 ? total / expenses.length : 0;

    document.getElementById("total").innerText =
        "Total Spent: ₹ " + total;

    document.getElementById("average").innerText =
        "Average Expense: ₹ " + average.toFixed(2);
}

displayExpenses();
