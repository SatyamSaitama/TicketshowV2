import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SearchView from '../views/SearchView.vue'
import loginView from '../views/loginView.vue'
import AdminLoginView from '../views/AdminLoginView.vue'
import BookingView from '../views/BookingView.vue'
import testView from '../views/testView.vue'
import PaymentView from '../views/PaymentView.vue'
import OrderView from '../views/OrderView.vue'
// Method to check if the user is authenticated
import SignupView from '../views/SignupView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import VenuesView from '../views/VenuesView.vue'
import ShowManager from '../views/ShowManager.vue'
import UserSignup from '../views/UserSignup.vue'
import AnalyticsView from '../views/AnalyticsView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  
  {
    path: '/search',
    name: 'SearchView',
    component: SearchView
  },
  {
    path: '/login',
    name: 'loginView',
    component: loginView
  },
  {
    path: '/admin_login',
    name: 'AdminLoginView',
    component: AdminLoginView
  },
  {
    path: '/test',
    name: 'testView',
    component: testView
  },
  {
    path: '/book',
    name: 'BookingView',
    component: BookingView
  },
  {
    path: '/payment',
    name: 'PaymentView',
    component: PaymentView
  },
  {
    path: '/order',
    name: 'OrderView',
    component: OrderView
  },
  {path:"/admin_signup",
  name : 'SingnupView',
  component : SignupView
},
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/venues',
    name: 'VenuesView',
    component: VenuesView,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('token') == null || localStorage.getItem('role') != 'admin')  {
        next('/admin_login')
      } else {
        next()
      }
    } 
  }
  ,
  {
    path: '/shows',
    name: 'ShowManager',
    component: ShowManager,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('token') == null || localStorage.getItem('role') != 'admin') {
        next('/admin_login')
      } else {
        next()
      }
    }
  },
  {
    path : '/signup',
    name : 'UserSignup',
    component : UserSignup
  },
  {
    path: '/analytics',
    name: 'AnalyticsView',
    component: AnalyticsView,}


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
