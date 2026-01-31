// Page switching
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    document.getElementById(pageId).classList.remove('hidden');
}

// Expense data (temporary – frontend only)
let expenses = [];
let debts = [];

function addExpense() {
    let date = document.getElementById("expDate").value;
    let category = document.getElementById("expCategory").value;
    let amount = document.getElementById("expAmount").value;
    let desc = document.getElementById("expDesc").value;

    if (amount <= 0 || date === "") {
        alert("Enter valid expense");
        return;
    }

    expenses.push({ date, category, amount, desc });
    renderExpenses();
}

function renderExpenses() {
    let table = document.getElementById("expenseTable");

    table.innerHTML = `
        <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Amount</th>
            <th>Description</th>
        </tr>
    `;

    expenses.forEach(e => {
        let row = table.insertRow();
        row.insertCell(0).innerText = e.date;
        row.insertCell(1).innerText = e.category;
        row.insertCell(2).innerText = e.amount;
        row.insertCell(3).innerText = e.desc;
    });
}

function addDebt() {
    let date = document.getElementById("debtDate").value;
    let person = document.getElementById("person").value;
    let amount = document.getElementById("debtAmount").value;
    let type = document.getElementById("debtType").value;

    if (amount <= 0 || person === "") {
        alert("Enter valid debt");
        return;
    }

    debts.push({ date, person, amount, type });
    renderDebts();
}

function renderDebts() {
    let list = document.getElementById("debtList");
    list.innerHTML = "";

    debts.forEach(d => {
        let li = document.createElement("li");
        li.innerText = `${d.date} - ${d.person} - ₹${d.amount} (${d.type})`;
        list.appendChild(li);
    });
}