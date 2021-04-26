import Vue from 'vue'
import VueRouter from 'vue-router'
import Events from '../views/Events.vue'
import Tickets from '../views/Tickets.vue'
import Create_event from '../views/Create_event.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: {name : 'Events'},
  },
  {
    path: '/events',
    name: 'Events',
    component: Events
  },
  {
    path: '/create-event',
    name: 'Create Event',
    component: Create_event
  },
  {
    path: '/tickets',
    name: 'Tickets',
    component: Tickets
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

