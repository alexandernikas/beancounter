<template>
    <div class="detail-container">

        <main class="main-content">
          <span class="exit-btn" @click="$router.push('/home')" > ✕ </span>

            <h2>Manage Team Members</h2>
 
    <div class="mgmt-card">  
      <table class="employee-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Order</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in employees" :key="emp.id">
            <td><input v-model="emp.employee_name" /></td>
            <td>
                <select v-model="emp.product" class="style-dropdown">
                <option v-for="product in products" :key="product.product_id" :value="product.product_id">
                    {{ product.product_name }}
                </option>
                </select>
            </td>
            <td>
                <button class="remove-btn" @click="deleteEmployee(emp.employee_id)">−</button>

            </td>
          </tr>
        </tbody>
      </table>
      <div class="sidebar-buttons">
      <button class = "style-btn" @click="addNewEmployee">Add Employee</button>
      <button class = "style-btn" @click="saveChanges">Save Changes</button>

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
      employees: [],
      products: [],
    };
  },
  async created() {
    await this.fetchEmployees();
    await this.fetchProducts();
  },
  methods: {
    async fetchEmployees() {
      const res = await axios.get('http://localhost:8000/api/employees/');
      this.employees = res.data;
    },
    async fetchProducts() {
      const res = await axios.get('http://localhost:8000/api/products/');
      this.products = res.data;
    },
    async deleteEmployee(employeeId) {
      if (employeeId === null) {
        this.employees = this.employees.filter(emp => emp.employee_id !== employeeId);

      } else {
      axios.post('http://localhost:8000/api/delete_employee/', {
        employee_id: employeeId
      })
      .then(response => {
        console.log('Employee marked as inactive:', response.data);
        //  hide the employee from the UI once removed
        this.employees = this.employees.filter(emp => emp.employee_id !== employeeId);
      })
      .catch(error => {
        console.error('Error deleting employee:', error.response ? error.response.data : error.message);
      })};
    },
    async addNewEmployee() {
        const newEmp = {
            employee_id: null,
            product_name: '',
            employee_name: '',
            update_date:'',
            is_absent: false,
            product: null,
            is_new: true
        };
  this.employees.push(newEmp);
    },
    async saveChanges() {

        try {
            const res = await axios.post('http://localhost:8000/api/save_bulk_employees/', {
            employees: this.employees
            });
            alert('Changes saved');
            this.$router.push('/home'); // redirect to home page

            await this.fetchEmployees(); // refresh after save
        } catch (err) {
            console.error('Error saving changes:', err);
            alert('Failed to save changes.');
        }
  },
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
.employee-table {
  margin: 0 auto;
  margin-bottom:10px;
}

.employee-table input {
    background-color: #545454;
    color: white;
    border: 1px solid #555;
    padding: 6px;
  }
  .employee-table td {
  padding-right:20px;
  padding-bottom:7px;
  border-top: 1px solid rgb(176, 176, 176);
  padding-top:7px;
}


.employee-table td button {
  color: red; /* or any color you want */
  background: rgba(255, 0, 0, 0.093);
  border: none;
  cursor: pointer;
  font-size: 1.2em;
  border-radius: 100%;;
}
  .mgmt-card {
  background-color: #3b3b3b;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

  .main-content {
    flex: 1;
    padding: 20px;
    max-width: 500px;
    margin: 0 auto;

  }
  .remove-btn {
  background-color: transparent;
  border: 2px solid red;
  color:white;
  font-weight: bold;
  font-size: 1.2em;
  width: 32px;
  height: 32px;
  line-height: 1;
  text-align: center;
  cursor: pointer;
  padding: 0;
}

.remove-btn:hover {
  background-color: red;
  color: white;
}


</style>