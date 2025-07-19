<template>
    <div class="dashboard-container">
      <Sidebar 
        :employee-orders="employeeOrders"
        :suggestedPurchaser="suggestedBuyer"

        @submission-complete="reloadDashboardData"
      />
      
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
        <h2 class="table-banner">Previous Coffee Runs  <input
      v-model="searchQuery"
      type="text"
      placeholder="Search coffee runs..."
      class="search-box"
    /></h2>
      
        <div class="table-container">
            <table class="transaction-table">
            <thead>
                <tr>
                <th>Date</th>
                <th>Purchaser</th>
                <th>Amount</th>
                </tr>
            </thead>
            <tbody class="table-body-scroll">
                <tr v-for="txn in filteredTransactions" :key="txn.transaction_id" @click="goToTransaction(txn.transaction_id)">
                <td>{{ txn.transaction_date }}</td>
                <td>{{ txn.purchaser_name }}</td>
                <td>${{ txn.transaction_amount }}</td>
                </tr>
            </tbody>
            </table>
        </div>
        </div>

        
      </main>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Sidebar from './Sidebar.vue';
  
  export default {
    name: 'Dashboard',
    components: {
      Sidebar
    },
    data() {
      return {
        transactions: [],
        suggestedBuyer: null,
        employeeOrders: [],
        searchQuery:''
      };
    },
    computed: {
    filteredTransactions() {
      return this.transactions.filter(transaction =>
        transaction.purchaser_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
    methods: {
      async fetchTransactions() {
        try {
          const response = await axios.get('http://localhost:8000/api/summaries/');
          this.transactions = response.data;
          console.log('fetched transactions', this.transactions);

        } catch (error) {
          console.error("Error fetching transactions:", error);
        }
      },
  
      async fetchSuggestedBuyer() {
        try {
          const response = await axios.get('http://localhost:8000/api/suggest_buyer/');
          this.suggestedBuyer = response.data.name;
        } catch (error) {
          console.error("Error fetching suggested buyer:", error);
        }
      },
  
      async fetchEmployeeOrders() {
        try {
          const response = await axios.get('http://localhost:8000/api/employees/');
          this.employeeOrders = response.data;
        } catch (error) {
          console.error("Error fetching employee orders:", error);
        }
      },
  
      async reloadDashboardData() {
        await this.fetchTransactions(); 
        await this.fetchSuggestedBuyer();  
      },
        goToTransaction(transaction_id) {
            this.$router.push({ name: 'TransactionDetail', params: { transaction_id } });
        }
    },
  
    async created() {
      await this.fetchTransactions();
      await this.fetchSuggestedBuyer();
      await this.fetchEmployeeOrders();
    }
  };
  </script>
  
  
  <style scoped>
  .dashboard-container {
    display: flex;
    min-height: 100vh;
    background-color: #1e1e1e;
    color: white;
  }
  
  /* Main content */
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

  
  /* Transaction table */
  .transaction-list {
    width: 100%;
  }
  
  .table-banner {
    text-align: left;
    margin-bottom: 10px;
  }
  
  .table-container {
  max-height: 400px;
  overflow-y: auto;
  border-radius: 8px;
  border: 1px solid #555;
  background-color: #4b4848;
}

.transaction-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #4b4848;
  table-layout: fixed;
}

.transaction-table th,
.transaction-table td {
  padding: 12px;
  border-bottom: 1px solid #555;
  text-align: left;
  min-width: 100px;
}

.transaction-table thead th {
  position: sticky;
  top: 0;
  background-color: #2e2e2e;
  color: white;
  z-index: 1;
}

/* Zebra striping and hover effects */
.transaction-table tbody tr:hover {
  background-color: #cfcfcf;
  color: black;
}

.transaction-table tbody tr:nth-child(even) {
  background-color: #717070;
}

.transaction-table tbody tr:nth-child(even):hover {
  background-color: #cfcfcf;
  color: black;
}

/* Scrollbar styling */
.table-container::-webkit-scrollbar {
  width: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #919191;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #4f698a;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
    background: #465d7a;
}

  
  .coffee-icon {
    height: 20px;
    vertical-align: middle;
    margin: 0 5px;
  }

  .search-box {
  background-color: #545454;
    color: white;
    border: 1px solid #555;
    padding: 6px;
    margin-left:20px;
    border-radius: 4px;
}
  </style>