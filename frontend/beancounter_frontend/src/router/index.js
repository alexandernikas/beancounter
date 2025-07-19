import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import ManageTeam from '../components/ManageTeam.vue';
import TransactionDetail from '../components/TransactionDetail.vue';
import ManageCoffeeMenu from '../components/ManageCoffeeMenu.vue'; 



const routes = [
  { path: '/home',
    name: 'Dashboard',
    component: Dashboard 
  },
  { path: '/manage-team',
    name: 'ManageTeam',
    component: ManageTeam 
  },
  {
    path: '/transaction/:transaction_id',
    name: 'TransactionDetail',
    component:TransactionDetail
  },
  {
    path: '/manage-coffee-menu',
    name: 'ManageCoffeeMenu',
    component: ManageCoffeeMenu
  }
    
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
