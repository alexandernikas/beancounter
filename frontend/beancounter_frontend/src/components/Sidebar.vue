<template>
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>
          Bean Counter
          <!-- <img src="/coffee-beans.png" alt="Coffee Beans" class="coffee-beans-icon"> -->
        </h1>
      </div>
      
      <div class="coffee-run-card">
        <h3>Enter Coffee Run</h3>
        <div class="form-group">
          <label for="purchaser">Purchaser:</label>
          <select id="purchaser" v-model="selectedPurchaser" class="style-dropdown">
            <option value="">Select purchaser...</option>
            <option v-for="employee in employeeOrders" :key="employee.employee_id" :value="employee.employee_id">
              {{ employee.employee_name }}
            </option>
          </select>
        </div>
        <div class="sidebar-buttons">
          <button class="style-btn" @click="submitAll">Submit</button>
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
          <button class="style-btn" @click="$router.push('/manage-coffee-menu')">Manage Coffee Menu</button>
          <button class="style-btn" @click="$router.push('/manage-team')">Manage Team Members</button>
        </div>
      </div>
    </aside>
  </template>
  
  <script>
  export default {
    name: 'Sidebar',
    props: {
      employeeOrders: {
        type: Array,
        required: true
      },
      
    },
    data() {
      return {
        selectedPurchaser: ''
      };
    },
    methods: {
      async submitAbsences() {
        const absentIds = this.employeeOrders
            .filter(emp => emp.is_absent)
            .map(emp => emp.employee_id);
            console.log('Submitting absences:', absentIds);

        try {
            const response = await fetch('http://localhost:8000/api/update_absences/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ absent_employee_ids: absentIds }),
    
            });
            if (!response.ok) throw new Error('Failed to update absences');

            // alert('Employee absences updated');
        } catch (error) {
            console.error(error);
            alert('Malformed request: failed to update employee absences');
        }
        },
        async submitTransaction() {
            console.log("orders:", this.employeeOrders); 
         // filter absent employees
        const presentEmployees = this.employeeOrders.filter(emp => !emp.is_absent);

        // set purchaser
        const purchaserId = this.selectedPurchaser;
        if (!purchaserId) {
            alert('No available purchaser');
            return;
        }

        // build purchases list
        const purchases = presentEmployees.map(emp => ({
            debtor_id: emp.employee_id,
            product_id: emp.product
        }));

        const payload = {
            purchaser_id: purchaserId,
            purchases: purchases
        };
        console.log(payload);

        try {
            const response = await fetch('http://localhost:8000/api/create_transaction/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
            });

    if (!response.ok) throw new Error('Failed to post transaction');

    alert('Coffee transaction submitted successfully');
  } catch (error) {
    console.error(error);
    alert('Error submitting transaction');
  }
},
// absence updates and transaction submission are chained together to account for team absences
async submitAll() {
  try {
    await this.submitAbsences();  // wait until absences are updated
    await this.submitTransaction();  // then post the transaction
    this.$emit('submission-complete'); // let dashboard know submission is complete
  } catch (error) {
    console.error('Error during submission:', error);
    alert('Failed to complete submission.');
  }
},

    }
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 450px;
    background-color: #2c2c2c;
    padding: 0;
    border-right: 1px solid #444;
    display: flex;
    flex-direction: column;
  }
  
  .sidebar-header {
    background-color: #717070;
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #444;
  }
  
  .sidebar-header h1 {
    margin: 0;
    font-size: 2.4em;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }
    
  .team-coffee-order {
    background-color: #393939;
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #444;
    border-radius: 10px;
    margin: 11px;
    text-align: left;
  }
  
  .employee-orders td {
    text-align: left;
    padding-right: 5px;
    padding-left: 10px;
    border-top: 1px solid white;
  }
  
  .employee-orders td:nth-child(1),
  .employee-orders td:nth-child(2) {
    border-right: 1px solid white;
  }
  
  .employee-orders th:nth-child(1),
  .employee-orders th:nth-child(2) {
    padding-right: 10px;
    padding-left: 10px;
  }
  
  .employee-orders td:last-child {
    text-align: center;
  }
  
  .employee-orders th:last-child {
    padding-left: 3px;
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
  

  
  </style>