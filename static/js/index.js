// 格式化货币金额
function formatCurrency(amount) {
  return new Intl.NumberFormat("en-AU", {
    style: "currency",
    currency: "AUD",
  }).format(amount);
}

// 格式化百分比变化
function formatPercentageChange(change) {
  const sign = change >= 0 ? "+" : "";
  return `${sign}${change.toFixed(1)}%`;
}

// 更新财务概览卡片
function updateFinancialOverview(data) {
  // 更新收入卡片
  document.getElementById("monthly-income-amount").textContent = formatCurrency(
    data.income.amount
  );

  const incomeChange = document.getElementById("monthly-income-change");
  const incomeArrow = data.income.change >= 0 ? "fa-arrow-up" : "fa-arrow-down";
  const incomeColor =
    data.income.change >= 0 ? "text-green-500" : "text-red-500";
  incomeChange.innerHTML = `
    <span class="${incomeColor} font-medium">
      <i class="fas ${incomeArrow} mr-1"></i>
      ${formatPercentageChange(data.income.change)}
    </span>
    <br>
    <span class="text-gray-500">Compared to last month</span>
  `;

  // 更新支出卡片
  document.getElementById("monthly-expenses-amount").textContent =
    formatCurrency(data.expenses.amount);

  const expensesChange = document.getElementById("monthly-expenses-change");
  const expensesArrow =
    data.expenses.change <= 0 ? "fa-arrow-down" : "fa-arrow-up";
  const expensesColor =
    data.expenses.change >= 0 ? "text-green-500" : "text-red-500";
  expensesChange.innerHTML = `
    <span class="${expensesColor} font-medium">
      <i class="fas ${expensesArrow} mr-1"></i>
      ${formatPercentageChange(data.expenses.change)}
    </span>
    <br>
    <span class="text-gray-500">Compared to last month</span>
  `;

  // 更新余额卡片
  document.getElementById("monthly-balance-amount").textContent =
    formatCurrency(data.balance.amount);

  const balanceChange = document.getElementById("monthly-balance-change");
  const balanceArrow =
    data.balance.change >= 0 ? "fa-arrow-up" : "fa-arrow-down";
  const balanceColor =
    data.balance.change >= 0 ? "text-green-500" : "text-red-500";
  balanceChange.innerHTML = `
    <span class="${balanceColor} font-medium">
      <i class="fas ${balanceArrow} mr-1"></i>
      ${formatPercentageChange(data.balance.change)}
    </span>
    <br>
    <span class="text-gray-500">Compared to last month</span>
  `;
}

// 获取财务概览数据
function fetchFinancialOverview() {
  console.log("正在获取财务概览数据...");
  fetch("/api/financial-overview")
    .then((response) => {
      console.log("API响应状态:", response.status);
      return response.json();
    })
    .then((data) => {
      console.log("接收到的数据:", data);
      updateFinancialOverview(data);
      updateRecentTransactions(data.recent_transactions);
    })
    .catch((error) => {
      console.error("Error fetching financial overview:", error);
    });
}

// 更新最近交易记录
function updateRecentTransactions(transactions) {
  const transactionsTable = document.getElementById(
    "recent-transactions-table"
  );
  if (!transactionsTable) {
    console.error("Cannot find recent-transactions-table element");
    return;
  }

  // 清空现有内容
  transactionsTable.innerHTML = "";

  // 限制显示前5条记录
  const displayTransactions = transactions.slice(0, 10);

  // 为每条交易记录创建表格行
  displayTransactions.forEach((transaction) => {
    // 根据交易类型和分类选择适当的图标和背景色
    let iconClass, bgColor;

    if (transaction.type === "income") {
      if (transaction.category === "Salary") {
        iconClass = "fa-money-bill-wave text-blue-500";
        bgColor = "bg-blue-100";
      } else if (transaction.category === "Bonus") {
        iconClass = "fa-gift text-indigo-500";
        bgColor = "bg-indigo-100";
      } else if (transaction.category === "Investment") {
        iconClass = "fa-chart-line text-green-500";
        bgColor = "bg-green-100";
      } else {
        iconClass = "fa-wallet text-purple-500";
        bgColor = "bg-purple-100";
      }
    } else {
      // expense
      if (transaction.category === "Dining") {
        iconClass = "fa-utensils text-red-500";
        bgColor = "bg-red-100";
      } else if (transaction.category === "Shopping") {
        iconClass = "fa-shopping-bag text-purple-500";
        bgColor = "bg-purple-100";
      } else if (transaction.category === "Transportation") {
        iconClass = "fa-subway text-yellow-500";
        bgColor = "bg-yellow-100";
      } else if (transaction.category === "Housing") {
        iconClass = "fa-home text-green-500";
        bgColor = "bg-green-100";
      } else {
        iconClass = "fa-tag text-gray-500";
        bgColor = "bg-gray-100";
      }
    }

    // 金额格式和样式
    const amountPrefix = transaction.type === "income" ? "+" : "-";
    const amountColor =
      transaction.type === "income" ? "text-green-600" : "text-red-600";

    // 创建表格行
    const row = document.createElement("tr");
    row.innerHTML = `
      <td class="px-6 py-4 whitespace-nowrap">
        <div class="flex items-center">
          <div class="${bgColor} p-2 rounded-lg mr-3">
            <i class="fas ${iconClass}"></i>
          </div>
          <span class="text-gray-700">${transaction.category}</span>
        </div>
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-gray-700">${
        transaction.description || ""
      }</td>
      <td class="px-6 py-4 whitespace-nowrap text-gray-500">${
        transaction.date
      }</td>
      <td class="px-6 py-4 whitespace-nowrap font-medium ${amountColor}">
        ${amountPrefix}$${formatCurrency(transaction.amount).substring(1)}
      </td>
    `;

    transactionsTable.appendChild(row);
  });
}

// 页面加载时获取数据
document.addEventListener("DOMContentLoaded", fetchFinancialOverview);
// 每5分钟更新一次数据
setInterval(fetchFinancialOverview, 5 * 60 * 1000);
