<template>
  <div class="detail-container">
    <main class="main-content">
      <span class="exit-btn"
      @click="$router.push('/home')">✕</span>
      <h2>Order Details</h2>

      <!-- Card Wrapper -->
      <div class="mgmt-card relative">
        <!-- Exit Button -->


        <!-- Content -->
        <div v-if="transactionDetail && transactionDetail.length">
          <!-- Transaction Table -->
          <div class="transaction-detail-list">
            <div class="table-container">
              <table class="transaction-table">
                <thead>
                  <tr>
                    <th>Purchaser</th>
                    <th>Recipient</th>
                    <th>Order</th>
                    <th>Price</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody class="table-body-scroll">
                  <tr v-for="detail in transactionDetail" :key="detail.transaction_detail_id">
                    <td>{{ detail.purchaser_name }}</td>
                    <td>{{ detail.debtor_name }}</td>
                    <td>{{ detail.product_name }}</td>
                    <td>${{ detail.product_price }}</td>
                    <td>{{ detail.transaction_date }}</td>
                  </tr>
                </tbody>
              </table>


            </div>
            <div class="sidebar-buttons">
            <button
                @click="rollbackTransaction"
                class="style-btn">🗑️ Delete Transaction
              </button>
            </div>
          </div>
        </div>

        <div v-else>
          <p>Loading transaction...</p>
        </div>
      </div>
    </main>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      transactionDetail: [],
    };
  },
  async created() {
    await this.fetchTransactionDetail();
  },
  methods: {
    async fetchTransactionDetail() {
      const transaction_id = this.$route.params.transaction_id;
      try {
        const res = await axios.get(`http://localhost:8000/api/details/${transaction_id}/`);
        this.transactionDetail = res.data;
        console.log("detail:", this.transactionDetail);
      } catch (err) {
        console.error("Failed to fetch transaction detail:", err);
      }
    },
    async rollbackTransaction() {
      const transaction_id = this.$route.params.transaction_id;
      try {
        axios.post(`http://localhost:8000/api/rollback_transaction/${transaction_id}/`)
          .then(response => {
            console.log('Transaction rolled back:', response.data);
            this.$router.push('/home'); // redirect after rollback
          })
          .catch(error => {
            console.error('Error rolling back transaction:', error);
          });
      } catch (error) {
        console.error("Error in rollbackTransaction:", error);
      }
    }


  }
};
</script>

<style scoped>
.detail-container {
    display: flex;
    min-height: 50vh;
    color: white;
    justify-content:center;
    align-items: center;
    
}
.mgmt-card {
  background-color: #3b3b3b;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
}

  .main-content {
    flex: 1;
    padding: 20px;
    max-width: 1000px;
    margin: 0 auto;
  }
  .transaction-detail-list {
    width: 100%;

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
</style>