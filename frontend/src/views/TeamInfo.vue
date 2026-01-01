<template>
  <div id="bkg">
    <div id="teaminfo">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>战队信息</h1>
          <p>战队名称:{{ team.name }}&nbsp;&nbsp;&nbsp;成员数:{{team.membernum}}/{{ team.maxnum }}</p>
          <p>战队总积分:{{ team.team_score }}</p>
          <div class="scrollable-table-container">
            <table class="two-column-table">
              <thead>
                <tr>
                  <th>队长</th>
                  <th>积分</th>
                </tr>
                <tr>
                  <td>{{team.leader}}</td>
                  <td>{{ team.leader_score }}</td>
                </tr>
                <tr>
                <th>成员</th>
                <th>积分</th>
              </tr>
              </thead>
              <tbody>
                <tr v-for="member in members" :key="member.username" v-if="checkLeader(member.username)">
                <td>{{ member.username }}</td>
                <td>{{ member.score }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        <button id="Ret" @click="quit()">退出战队</button>
    </div>
  </div> 
</template>
    
<script>
  import { mapState, mapMutations } from 'vuex';
  import { teamDetail,quitTeam } from '@/UserSystemApi/TeamApi';
  export default {
    data() {
      return {
        team: {
          member_name: this.$store.state.username,
          name: this.$store.state.teamname,
          leader: '',
          leader_score: '',
          membernum: '',
          maxnum:'10',
          team_score: ''
        },
        members: [
        { username: '', score: "" },
      ],
      };
    },
    computed: {
      ...mapState(['userInfoButtonEnabled','username','teamname','isLeader',]),
    },
    mounted() {
      this.team_detail(this.team.name);
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setIsLeader',]),
      close() {
        this.setUserInfoButtonEnabled(true);
        localStorage.setItem('UBE',true);
        this.$router.push('/');
      },
      async team_detail(name) {
        try {
          const response = await teamDetail(name);
          console.log('获取用户列表响应', response);
          if(response.ret==='success'){
            this.members=response.data.members;
            this.team.membernum=response.data.team_member;
            this.team.leader=response.data.leader;
            this.team.leader_score=response.data.leader_score;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
      },
      async quit() {
        try {
          const response = await quitTeam();
          console.log('退出战队响应', response);
          if(response.ret==='success'){
            alert(response.msg);
            this.setTeamname('');
            this.setIsLeader(false);
            this.setUserInfoButtonEnabled(true);
            localStorage.setItem('UBE',true);
            localStorage.removeItem('teamname');
            localStorage.removeItem('isLeader');
            this.$router.push("/");
            console.log(response.data);
          }
        } catch (error) {
          console.log(error.response.data.msg);
        }
      },
      checkLeader(name){
        if(name==this.team.leader){
          return false;
        }
        return true;
      },
    },
  };
</script>
    
<style>
#teaminfo {
  width: 600px;
  height: 400px;
  position: absolute;
  top: auto;
  left: auto;
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

.two-column-table {
  margin-left: 30%;
  width: 40%;
  table-layout: fixed;
}

.two-column-table th,
.two-column-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.two-column-table th:first-child,
.two-column-table td:first-child {
  text-align: center;
}

#Ret{
  left:287px;
  bottom:20px;
  position: absolute;
}

#bkg{
height:87vh;
background-image:url("../assets/背景.png");
background-size:cover;
}

  </style>