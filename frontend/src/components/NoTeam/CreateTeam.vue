<template>
    <div id="createTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>创建战队</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <form @submit.prevent="create_Team">
        <label for="teamname">战队名称:</label>
        <input type="text" id="teamname" v-model="team.team_name" required /><br><br>
        <label for="check">审核加入:</label>
        <input type="checkbox" id="check" v-model="team.check" /><br><br>
        <button type="submit">创建</button> |
        <button @click="Re()" id="R">返回</button>
      </form>
    </div>
</template>

<script>
import { createTeam } from '/src/UserSystemApi/TeamApi.js';
 import { mapState, mapMutations } from 'vuex';
 export default {
    data() {
      return {
        team: {
          team_name: '',
          leader_name: this.$store.state.username,
          check: false
        },
      };
    },
    computed: {
    ...mapState(['userInfoButtonEnabled','username','teamname','createTeam','noTeam','isLeader','err']),
    isValid(string) {
          const Regex = /^[a-zA-Z0-9_]+$/;
          return (string) => Regex.test(string);
    },
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setCreateTeam','setNoTeam','setIsLeader','setErr']),
      close() {
        this.setUserInfoButtonEnabled(true);
        this.setCreateTeam(false);
      },
      async create_Team() {
        try {
          if (!this.isValid(this.team.team_name)) {
              this.setErr("战队名只能包含数字、字母和下划线");
              return;
          }
          const response = await createTeam(this.team.leader_name, this.team.team_name, !this.team.check);
          if(response.ret='success'){
            alert(response.msg);
            console.log('创建战队响应', response);
            this.setTeamname(this.team.team_name);
            localStorage.setItem('teamname',response.data.team_name);
            this.setIsLeader(true);
            localStorage.setItem('isLeader',"true");
            this.setUserInfoButtonEnabled(true);
            this.setCreateTeam(false);
            this.setErr("");
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
        }
      }, 
      Re() {
        this.setCreateTeam(false);
        this.setNoTeam(true);
        this.setErr("");
      }
    },
  };
</script>

<style>
button{
  cursor: pointer;
}
#createTeam {
    margin-top:-220px;
    margin-left:470px;
    position: absolute;
    top: auto;
    left: auto;
    width: 350px;
    height: 220px;
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
#er{
    height: 8px;
    color:red;
    font-size: small;
}
</style>
  
