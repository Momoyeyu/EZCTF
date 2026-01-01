<template>
    <div class="AcIn">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>邀请信息</h1>
          <p v-if="err" class="er">{{ err }}</p>
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
                  <td>{{ team.leader}}</td>
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
          <div id="btnSet">
            <button  @click="accept(team.inviter,true)" class="btn">接受</button> |
            <button  @click="accept(team.inviter,false)" class="btn">拒绝</button>
          </div>
    </div>
</template>
    
<script>
  import { mapState, mapMutations } from 'vuex';
  import { teamDetail,accept } from '@/UserSystemApi/TeamApi';
  import { profile } from '@/UserSystemApi/UserApi';
  export default {
    data() {
      return {
        team: {
          name: '',
          inviter: this.$store.state.inviter,
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
      ...mapState(['userInfoButtonEnabled','username','teamname','isLeader','inviter','acceptInvite','infoBoard','err']),
    },
    mounted() {
      this.profile(this.inviter);
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setIsMember','setInviter','setAcceptInvite','setInfoBoard','setErr']),
      close() {
        this.setInfoBoard(true);
        this.setAcceptInvite(false);
        this.setInviter("");
        this.setErr("");
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
      async accept(name,state) {
        try {
          const response = await accept(name,state);
          console.log('接受邀请响应', response);
          if(response.ret==='success'){
            alert(response.msg);
            this.setUserInfoButtonEnabled(true);
            this.setInviter("");
            this.setAcceptInvite(false);
            this.setInfoBoard(true);
            this.setErr("");
            this.setAcceptInvite(false);
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
        }
      },
      async profile(name) {
        try {
          const response = await profile(name);
          console.log('响应', response);
          if(response.ret==='success'){
            this.team.name=response.data.team;
            this.team_detail(this.team.name);
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
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
    
<style scoped>
.AcIn {
  width: 400px;
  height: 400px;
  position: absolute;
  top: 220px;
  left: 460px;
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

.btn{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 80px;
    height: 30px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn:hover{
    background-color: grey;
  }

  #btnSet{
    left:133px;
    bottom:20px;
    position: absolute;
  }

  .er{
    padding: 4px;
    color:red;
    font-size: small;
  }
</style>