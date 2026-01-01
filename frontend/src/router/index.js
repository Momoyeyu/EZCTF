import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Ranking from '../views/Ranking.vue'
import LoginSystem from '../views/LoginSystem.vue'
import TeamInfo from '../views/TeamInfo.vue'
import ManageTeam from '../views/ManageTeam.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Home',
    name: 'Home',
    component: Home
  },
  {
    path: '/Ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/Log',
    name: 'LoginSystem',
    component: LoginSystem,
  },
  {
    path: '/TeamInfo',
    name: 'TeamInfo',
    component: TeamInfo,
  },
  {
    path: '/ManageTeam',
    name: 'ManageTeam',
    component: ManageTeam,
  },
]

const router = new VueRouter({
  routes
})

export default router