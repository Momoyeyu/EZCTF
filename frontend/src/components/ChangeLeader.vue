<template>
    <div id="changeleader">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>权限转让</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <p>是否将队长转让给{{ newLeader }}?</p><br>
      <button @click="change_leader()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { changeTeamLeader } from '@/UserSystemApi/TeamApi';
  export default {
    computed: {
    ...mapState(['changeLeader','manageTeam','newLeader','err','isLeader','userInfoButtonEnabled']),
    },
    methods: {
      ...mapMutations(['setChangeLeader','setManageTeam','setNewLeader','setErr','setIsLeader','setUserInfoButtonEnabled']),
      async change_leader() {
        try {
          const response = await changeTeamLeader(this.$store.state.newLeader);
          console.log('解散战队响应:', response);
          if (response.ret === "success") {
            alert("队长权限转让成功");
            this.setIsLeader(false);
            localStorage.removeItem('isLeader');
            this.setChangeLeader(false);
            this.setNewLeader("");
            this.setManageTeam(true);
            this.$router.push('/'); 
            this.setUserInfoButtonEnabled(true);
            localStorage.setItem('UBE',true);
            this.setErr("");
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
        }
      },
      close() {
        this.setChangeLeader(false);
        this.setNewLeader("");
        this.setManageTeam(true);
        this.setErr("");
      },
    },
  };
</script>
<style>
#changeleader {
    top: auto;
    left: auto;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 200px;
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
 