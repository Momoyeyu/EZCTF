import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Vuex from 'vuex';
import VueCookies from 'vue-cookies'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/index_icon/iconfont.css'
import axios from 'axios';

Vue.use(Vuex);
Vue.use(VueCookies)
Vue.use(ElementUI);
Vue.config.productionTip = false
axios.defaults.baseURL="http://localhost:8000"
const store = new Vuex.Store({
  state: {
    loginButtonEnabled: localStorage.getItem('LBE') === "false" ? false : true,
    userInfoButtonEnabled: localStorage.getItem('UBE') === "false" ? false : true,
    isHover: false,
    modifyUser: false,
    deleteUser: false,
    infoBoard: false,
    isLogin: localStorage.getItem('isLogin') || false, 
    setInfo: true,
    noTeam: false,
    createTeam: false,
    joinTeam: false,
    deleteTeam: false,
    changeTeamname: false,
    manageTeam: true,
    log: true,
    reg: false,
    FoPa: false,
    username: localStorage.getItem('username') || '', 
    score: localStorage.getItem('score') || '', 
    teamname: localStorage.getItem('teamname') || '', 
    isLeader: localStorage.getItem('isLeader') || false, 
    newLeader:'',
    changeLeader: false,
    kickMember: false,
    kMember:'',
    err: '',
    acceptInvite: false,
    inviter: '',
    inviteMember: false,
  },
  mutations: {
    setLoginButtonEnabled(state, value) {
      state.loginButtonEnabled = value;
    },
    setUserInfoButtonEnabled(state, value) {
      state.userInfoButtonEnabled = value;
    },
    setIsHover(state, value){
      state.isHover = value;
    },
    setUsername(state, value) {
      state.username = value;
    },
    setTeamname(state, value) {
      state.teamname = value;
    },
    setScore(state, value) {
      state.score = value;
    },
    setIsLeader(state, value) {
      state.isLeader = value;
    },
    setModifyUser(state, value) {
      state.modifyUser = value;
    },
    setDeleteUser(state, value) {
      state.deleteUser = value;
    },
    setInfoBoard(state, value) {
      state.infoBoard = value;
    },
    setIsLogin(state, value){
      state.isLogin = value;
    },
    setSetInfo(state, value){
      state.setInfo = value;
    },
    setNoTeam(state, value){
      state.noTeam =value;
    },
    setCreateTeam(state, value){
      state.createTeam =value;
    },
    setJoinTeam(state, value){
      state.joinTeam =value;
    },
    setDeleteTeam(state, value) {
      state.deleteTeam = value;
    },
    setChangeTeamname(state, value) {
      state.changeTeamname = value;
    },
    setManageTeam(state, value) {
      state.manageTeam = value;
    },
    setLog(state, value){
      state.log =value;
    },
    setReg(state, value){
      state.reg =value;
    },
    setFoPa(state, value){
      state.FoPa =value;
    },
    setNewLeader(state, value){
      state.newLeader =value;
    },
    setChangeLeader(state, value){
      state.changeLeader =value;
    },
    setKickMember(state, value){
      state.kickMember=value;
    },
    setKMember(state, value){
      state.kMember=value;
    },
    setErr(state, value){
      state.err =value;
    },
    setAcceptInvite(state, value){
      state.acceptInvite =value;
    },
    setInviter(state, value){
      state.inviter =value;
    },
    setInviteMember(state, value){
      state.inviteMember =value;
    },
  },
});

new Vue({
  router,
  render: h => h(App),
  store
}).$mount('#app')

