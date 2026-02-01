// TEMPORARY FRONTEND LOGIC
// DELETE / REPLACE during Python backend integration

let expenses = [];
let streak = 0;
let streakDoneToday = false;

// ADD EXPENSE
// function addExpense(){
//     let date = document.getElementById("dateInput").value;
//     let amount = document.getElementById("amountInput").value;
//     let category = document.getElementById("categoryInput").value;

//     if(date === "" || amount === ""){
//         alert("Please fill all fields");
//         return;
//     }

//     expenses.push({
//         date,
//         category,
//         amount: Number(amount)
//     });

//     render(expenses);
//     completeStreak();

//     document.getElementById("dateInput").value = "";
//     document.getElementById("amountInput").value = "";
// }

// RENDER
function render(list){
    let table = document.getElementById("expenseTable");
    table.innerHTML = "";

    let total = 0;

    list.forEach(e => {
        total += e.amount;
        table.innerHTML += `
            <tr>
                <td>${e.date}</td>
                <td>${e.category}</td>
                <td>${e.amount}</td>
            </tr>
        `;
    });

    document.querySelector(".expense-header span").innerText = `Total: ₹${total}`;
    document.querySelectorAll(".card h3")[0].innerText = `₹${total}`;
    document.querySelectorAll(".card h3")[1].innerText = `₹${total}`;
}

// SEARCH
document.getElementById("searchInput").addEventListener("input", function(){
    let key = this.value.toLowerCase();
    let filtered = expenses.filter(e =>
        e.date.includes(key) || e.category.toLowerCase().includes(key)
    );
    render(filtered);
});

// STREAK SYSTEM
function completeStreak(){
    if(!streakDoneToday){
        streak++;
        streakDoneToday = true;
        document.getElementById("streakCount").innerText = streak;
        alert("🔥 Daily Streak Updated!");
    }
}

function markNoSpendDay(){
    completeStreak();
    alert("✅ No-Spend Day Marked!");
}

// LOGOUT
document.querySelector(".logout").addEventListener("click", function(){
    window.location.href = "index.html";
});
