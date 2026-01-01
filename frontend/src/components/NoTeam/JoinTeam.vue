<template>
    <div id="jointeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>加入战队</h1>
      <label for="search">搜索战队: </label>
      <input id="search" v-model="searchQuery" placeholder="请输入战队名称" @input="filter()"/><br><br>
      <div class="scrollable-table-container">
        <table class="three-column-table">
          <thead>
            <tr>
            <th>战队名称</th>
            <th>队长</th>
            <th>积分</th>
            <th>人数</th>
            <th>操作</th>
            </tr>
            </thead>
            <tbody>
              <tr v-for="team in filteredTeams" :key="team.team_name">
              <td>{{ team.team_name }}</td>
              <td>{{ team.leader_name }}</td>
              <td>{{ team.team_points }}</td>
              <td>{{ team.team_member }}/{{ maxnum }}</td>
              <td>
                <button @click="jointeam(team.team_name)" v-if="team.allow_join">加入</button>
                <button @click="jointeam(team.team_name)" v-if="!team.allow_join">申请</button>
              </td>
              </tr>
          </tbody>
        </table>
      </div><br><br>
      <button class="Return" @click="Re()">返回</button>
    </div>
  </template>
  
  <script>
  import { searchTeam,joinTeam } from '/src/UserSystemApi/TeamApi.js';
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        name: this.$store.state.username,
        searchQuery: "",
        teams: [
          {
            team_name:"",
            leader_name: "",
            leader_email: "",
            team_points:"",
            team_member:"",
            allow_join: "",
          }
        ],
        maxnum: 10,
      };
    },
    computed: {
      filteredTeams() {
        if(this.searchQuery!=''){
          const query = this.searchQuery.toLowerCase();
          return this.teams.filter((team) => team.team_name.toLowerCase().includes(query));
        }
        else{
          return this.teams;
        }
      },
      ...mapState(['userInfoButtonEnabled','username','teamname','joinTeam','noTeam']),
    },
    mounted() {
      this.searchTeams("");
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setJoinTeam','setNoTeam']),
      close() {
        this.setUserInfoButtonEnabled(true);
        this.setJoinTeam(false);
      },
      Re() {
        this.setJoinTeam(false);
        this.setNoTeam(true);
      },
      async jointeam(teamname) {
        try {
          const response = await joinTeam(teamname);
          if (response.ret === 'success') {
            alert(response.msg);
            console.log('发送申请响应:', response.msg);
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('网络请求失败:', error);
        }
      },
      async searchTeams(name) {
        try {
          const response = await searchTeam(name);
          console.log('搜索战队响应', response);
          if(response.ret==='success'){
            this.teams=response.data.team_list;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
      },
    },
  };
  </script>

<style>
button{
  cursor: pointer;
}
#jointeam {
    margin-top:-260px;
    margin-left:350px;
    position: absolute;
    top: auto;
    left: auto;
    width: 600px;
    height: 360px;
    justify-content: center;
    align-items: center;
    background-color: #1e1e1e;
    padding: 20px;
    border-style: solid;
    border-radius: 5px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
}

.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}

.scrollable-table-container {
  max-height: 300px; 
  overflow-y: auto; 
}

.three-column-table {
  width: 100%;
}

.three-column-table th,
.three-column-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.three-column-table th:first-child,
.three-column-table td:first-child {
  text-align: center;
}

.Return{
  left:300px;
  bottom:20px;
  position: absolute;
}
</style>
  