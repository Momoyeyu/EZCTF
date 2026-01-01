<template>
    <div class="invitemember">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>发送邀请</h1><br>
      <label for="search">邀请对象: </label>
      <input id="search" v-model="username" placeholder="请输入邀请对象"/><br><br><br>
      <button class="btn" @click="invite(username)">邀请</button> |
      <button class="btn" @click="Re()">返回</button>
    </div>
  </template>
  
  <script>
  import { Invite } from '/src/UserSystemApi/TeamApi.js';
  import { mapState, mapMutations } from 'vuex';
  export default {
    data() {
      return {
        username: "",
      };
    },
    computed: {
      ...mapState(['inviteMember','manageTeam','teamname']),
    },
    methods: {
      ...mapMutations(['setInviteMember','setManageTeam','setTeamname']),
      close() {
        this.setInviteMember(false);
        this.setManageTeam(true);
      },
      Re() {
        this.setInviteMember(false);
        this.setManageTeam(true);
      },
      async invite(name) {
        try {
          const response = await Invite(name);
          console.log('搜索战队响应', response);
          if(response.ret==='success'){
            alert(response.msg);
            this.username='';
            console.log(response.data);
            window.location.reload();  
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('错误:', error);
        }
      },
    },
  };
  </script>

<style scoped>
button{
  cursor: pointer;
}
.invitemember {
    position: absolute;
    top: auto;
    left: auto;
    width: 300px;
    height: 200px;
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

.btn{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 60px;
    height: 30px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn:hover{
    background-color: grey;
  }
</style>
  