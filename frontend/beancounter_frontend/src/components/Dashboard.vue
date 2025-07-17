<template>
    <div class="dashboard-container">
        <aside class="sidebar">
  <div class="sidebar-header">
    <h2>☕ Bean Counter</h2>
  </div>
  <div class="coffee-run-card">
    <h3>Enter Coffee Run</h3>
    <div class="form-group">
      <label for="purchaser">Purchaser:</label>
      <select id="purchaser" v-model="selectedPurchaser" class="purchaser-dropdown">
        <option value="">Select purchaser...</option>
        <option v-for="employee in employeeOrders" :key="employee.id" :value="employee.employee_name">
          {{ employee.employee_name }}
        </option>
      </select>
    </div>
    <div class="sidebar-buttons">
      <button class="sidebar-btn">Submit</button>
    </div>
  </div>
  <div class="team-coffee-order">
    <table class="employee-orders">
      <thead>
        <tr>
          <th>Name</th>
          <th>Order</th>
          <th>Out of Office?</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in employeeOrders" :key="employee.id">
          <td>{{ employee.employee_name }}</td>
          <td>{{ employee.product_name }}</td>
          <td class="ooo">
            <label>
      <input
        type="checkbox"
        v-model="employee.is_absent"
        :true-value="true"
        :false-value="false"
      />
    </label>
  </td>
        </tr>
      </tbody>
    </table>
    <div class="sidebar-buttons">
      <button class="sidebar-btn">Manage Coffee Menu</button>
      <button class="sidebar-btn">Manage Team Members</button>
    </div>
  </div>

</aside>

  
      <!-- Main Content -->
      <main class="main-content">
        <!-- Suggested Buyer Card -->
        <div class="suggested-buyer-card">
          <h1 v-if="suggestedBuyer">☕ Next Coffee Run - {{ suggestedBuyer }} ☕</h1>
          <p v-else>Loading...</p>
          <span class="suggestion-note">Based on purchase history</span>

        </div>
  
        <!-- Transaction Table -->
        <div class="transaction-list">
          <h2 class="table-banner">Previous Coffee Runs</h2>
          <table class="transaction-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Purchaser</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="txn in transactions" :key="txn.id">
                <td>{{ txn.transaction_date }}</td>
                <td>{{ txn.purchaser_name }}</td>
                <td>${{ txn.transaction_amount }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        transactions: [],
        suggestedBuyer: null,
        employeeOrders: [],
      };
    },
    methods: {    
        // methods go here
    },
    created() {
        axios.get('http://localhost:8000/api/summaries/')
        .then(response => {
          this.transactions = response.data;        })
        .catch(error => {
          console.error("Error fetching transactions:", error);
        });
        // Fetch suggested buyer
        axios.get('http://localhost:8000/api/suggest_buyer/')
        .then(response => {
            this.suggestedBuyer = response.data.name;
        })
      .catch(error => {
        console.error("Error fetching suggested buyer:", error);
      });
    // Fetch team orders
        axios.get('http://localhost:8000/api/employees/')
        .then(response => {
            this.employeeOrders = response.data;
        })
        .catch(error => {
            console.error("Error fetching employee orders:", error);
        });
        },
  };
  </script>
  
  <style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #1e1e1e;
  color: white;
}
/* sidebar styling */
.sidebar {
  width: 375px;
  background-color: #2c2c2c;
  padding: 0;
  border-right: 1px solid #444;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  background-color:  #717070;
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #444;
}
.team-coffee-order {
  background-color:  #393939;
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #444;
  border-radius: 10px;
  margin: 11px;
  text-align:left;

}
.employee-orders td {
text-align:left;
padding-right:10px;
padding-left:10px;
}

.employee-orders td {
text-align:left;
padding-right:5px;
padding-left:10px;
border-top: 1px solid white;

}

.employee-orders td:nth-child(1),
.employee-orders td:nth-child(2) {
  border-right: 1px solid white;
}
.employee-orders th:nth-child(1),
.employee-orders th:nth-child(2) {
  padding-right:10px;
padding-left:10px;
}

.employee-orders td:last-child {
  text-align: center;
  /* padding-left:5px; */
}
.employee-orders th:last-child {
  padding-left:3px;
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.4em;
  color: #fff; 
}

.sidebar h2 {
  /* margin-bottom: 20px; */
  font-size: 1.4em;
}

.coffee-run-card {
  background-color: #393939;
  padding: 20px;
  border-radius: 10px;
  margin: 10px;
}

.coffee-run-card h3 {
  margin: 0 0 15px 0;
  font-size: 1.2em;
  color: #fff;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #ddd;
  font-size: 0.9em;
}

.purchaser-dropdown {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #666;
  border-radius: 6px;
  background-color: #4b4848;
  color: white;
  font-size: 0.9em;
}

.purchaser-dropdown:focus {
  outline: none;
  border-color: #888;
  background-color: #5a5757;
}


/* main content */
.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.suggested-buyer-card {
  background-color: #3b3b3b;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.suggestion-note {
  font-size: 0.9em;
  color: #aaa;
  font-style: italic;
}

.sidebar-buttons {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.sidebar-btn {
  background-color: #4b4848;
  color: white;
  border: 1px solid #666;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9em;
  transition: background-color 0.2s;
}

.sidebar-btn:hover {
  background-color: #5a5757;
}

.sidebar-btn:active {
  background-color: #3a3a3a;
}
/* transaction table */
.transaction-list {
  width: 100%;
}
.table-banner {
    text-align:left;
}
.transaction-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #4b4848;
  border-radius: 8px;
  overflow: hidden;
  text-align: left;
}

.transaction-table th,
.transaction-table td {
  padding: 12px;
}

.transaction-table tr:hover {
  background-color: #cfcfcf;
  color: black;
}

.transaction-table th {
  background-color: #2e2e2e;
  color: white;
}

.transaction-table tr:nth-child(even) {
  background-color: #717070;
}

.transaction-table tr:nth-child(even):hover {
  background-color: #cfcfcf;
  color: black;
}

.coffee-icon {
  height: 20px;
  vertical-align: middle;
  margin: 0 5px;
}

  </style>