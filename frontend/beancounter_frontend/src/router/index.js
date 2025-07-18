import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import ManageTeam from '../components/ManageTeam.vue';

const routes = [
  { path: '/home',
    name: 'Dashboard',
    component: Dashboard },
  { path: '/manage-team',
    name: ManageTeam,
    component: ManageTeam }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
