<template>
    <div class="detail-container">
      <main class="main-content">
        <span class="exit-btn"
        @click="$router.push('/home')">✕</span>
        <h2>Coffee Menu</h2>
                <div class="mgmt-card relative">

          <!-- Content -->
          <div v-if="products">
            <!-- product table -->
            <div class="product-detail-list">
              <div class="table-container">
                <table class="product-table">
                  <thead>
                    <tr>
                      <th>Item</th>
                      <th>Menu Price</th>
                      <th>Update Date</th>
                    </tr>
                  </thead>
                  <tbody class="table-body-scroll">
                    <tr v-for="product in filteredProducts" :key="product.product_id">
                      <td>{{ product.product_name }}</td>
                      <td>{{ product.product_price }}</td>
                      <td>{{ product.update_date }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="sidebar-buttons">
                <input
      v-model="searchQuery"
      type="text"
      placeholder="Search menu..."
      class="search-box"
    />
            <button @click="updatePrices" class="style-btn">Update Prices</button>
            <p v-if="resultMessage">{{ resultMessage }}</p>

            <span class="suggestion-note">Prices retrieved from https://ventocoffee.com/ in compliance with user terms</span>

            </div>
            </div>
          </div>
  
          <div v-else>
            <p>Loading products...</p>
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
        products: [],
        resultMessage: '',
        searchQuery: ''
      };
    },
    computed: {
    filteredProducts() {
      return this.products.filter(product =>
        product.product_name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
    async created() {
      await this.fetchProducts();
    },
    methods: {
      async fetchProducts() {
        try {
          const res = await axios.get(`${process.env.VUE_APP_API_URL}/api/products/`);
          this.products = res.data;
          console.log("detail:", this.products);
        } catch (err) {
          console.error("Failed to fetch products:", err);
        }
      },
      async updatePrices() {
        console.log("Updating Prices");
        try {
          const response = await axios.post(`${process.env.VUE_APP_API_URL}/api/update_prices/`);
          const data = response.data;

          if (data.status === "success") {
            const updated = data.result.updated;
            const created = data.result.created;

            if (updated === 0 && created === 0) {
              alert('Prices are up to date');
            } else {
              alert(`Updated ${updated} item(s), created ${created} new item(s)`);
            }
            await this.fetchProducts();

          } else {
            this.resultMessage = `Error: ${data.message}`;
          }

        } catch (error) {
          console.error("Error updating prices:", error);
          alert('Failed to update prices');
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
      max-width: 700px;
      margin: 0 auto;
    }
    .product-detail-list {
      width: 100%;
  
    }
    .table-container {
    max-height: 400px;
    overflow-y: auto;
    border-radius: 8px;
    border: 1px solid #555;
    background-color: #4b4848;
  }
  
  .product-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #4b4848;
    table-layout: fixed;
  
  }
  
  .product-table th,
  .product-table td {
    padding: 12px;
    border-bottom: 1px solid #555;
    text-align: left;
    min-width: 100px;
  }
  
  .product-table thead th {
    position: sticky;
    top: 0;
    background-color: #2e2e2e;
    color: white;
    z-index: 1;
  }
  
  /* Zebra striping and hover effects */
  .product-table tbody tr:hover {
    background-color: #cfcfcf;
    color: black;
  }
  
  .product-table tbody tr:nth-child(even) {
    background-color: #717070;
  }
  
  .product-table tbody tr:nth-child(even):hover {
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
  .search-box {
  background-color: #545454;
    color: white;
    border: 1px solid #555;
    padding: 6px;
    border-radius: 4px;
}
  </style>