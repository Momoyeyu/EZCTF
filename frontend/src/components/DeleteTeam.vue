<template>
    <div id="deleteTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>解散战队</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <input v-model="password" placeholder="请输入密码" /><br><br>
      <button @click="delete_team()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { delete_Team } from '@/UserSystemApi/TeamApi';
  export default {
    data() {
      return {
        password: "",
      };
    },
    computed: {
    ...mapState(['teamname','isLeader','deleteTeam','manageTeam','userInfoButtonEnabled','err']),
    },
    methods: {
      ...mapMutations(['setTeamname','setIsLeader','setDeleteTeam','setManageTeam','setUserInfoButtonEnabled','setErr']),
      async delete_team() {
        try {
          const response = await delete_Team(this.password);
          console.log('解散战队响应:', response);
          if (response === 204) {
            alert("成功解散战队");
            this.setTeamname('');
            this.setIsLeader(false);
            localStorage.removeItem('teamname');
            localStorage.removeItem('isLeader');
            this.setDeleteTeam(false);
            this.setManageTeam(true);
            this.$router.push('/'); 
            this.setUserInfoButtonEnabled(true);
            this.setErr("");
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
        }
      },
      close() {
        this.setDeleteTeam(false);
        this.setManageTeam(true);
        this.setErr("");
      },
    },
  };
</script>
<style>
#deleteTeam {
    top: auto;
    left: auto;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 170px;
    background-color: #1e1e1e;
    justify-content: center;
    align-items: center;
    padding: 20px;
    border-style: solid;
    border-radius: 5px;
    border-color:white;
    border-width: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    color:white;
    z-index: 10;
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
 