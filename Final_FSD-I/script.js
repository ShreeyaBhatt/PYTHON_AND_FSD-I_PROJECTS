let expenses = JSON.parse(localStorage.getItem("expenses")) || [];
let debts = JSON.parse(localStorage.getItem("debts")) || [];

function saveData() {
    localStorage.setItem("expenses", JSON.stringify(expenses));
    localStorage.setItem("debts", JSON.stringify(debts));
}

function updateTotals() {
    let totalExpense = expenses.reduce((sum, item) => sum + Number(item.amount), 0);
    let totalDebt = debts.reduce((sum, item) => sum + Number(item.amount), 0);

    document.getElementById("totalExpense").innerText = "₹" + totalExpense;
    document.getElementById("totalDebt").innerText = "₹" + totalDebt;
}

function displayExpenses() {
    let table = document.getElementById("expenseTable");
    table.innerHTML = "";

    expenses.forEach((item) => {
        table.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>₹${item.amount}</td>
                <td>${item.date}</td>
                <td>${item.category ? item.category : "-"}</td>
            </tr>
        `;
    });

    updateTotals();
}

function displayDebts() {
    let table = document.getElementById("debtTable");
    table.innerHTML = "";

    debts.forEach((item) => {
        table.innerHTML += `
            <tr>
                <td>${item.person}</td>
                <td>₹${item.amount}</td>
                <td>${item.date ? item.date : "-"}</td>
                <td>${item.type ? item.type : "-"}</td>
            </tr>
        `;
    });

    updateTotals();
}


function addExpense() {
    let name = document.getElementById("expenseName").value;
    let amount = document.getElementById("expenseAmount").value;
    let date = document.getElementById("expenseDate").value;
    let category = document.getElementById("expenseCategory").value;

    if (!name || !amount || !date || !category) {
        alert("Please fill all fields");
        return;
    }

    expenses.push({ name, amount, date, category });
    saveData();
    displayExpenses();

    document.getElementById("expenseName").value = "";
    document.getElementById("expenseAmount").value = "";
    document.getElementById("expenseDate").value = "";
    document.getElementById("expenseCategory").value = "";
}

function addDebt() {
    let person = document.getElementById("debtPerson").value;
    let amount = document.getElementById("debtAmount").value;
    let date = document.getElementById("debtDate").value;
    let type = document.getElementById("debtType").value;

    if (!person || !amount || !date || !type) {
        alert("Please fill all fields");
        return;
    }

    debts.push({ person, amount, date, type });
    saveData();
    displayDebts();

    document.getElementById("debtPerson").value = "";
    document.getElementById("debtAmount").value = "";
    document.getElementById("debtDate").value = "";
    document.getElementById("debtType").value = "";
}


displayExpenses();
displayDebts();
