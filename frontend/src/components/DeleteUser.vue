<template>
    <div id="deleteUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>账户注销</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <input v-model="password" placeholder="请输入密码" /><br><br>
      <button @click="delete_User()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { deleteUserInfo } from '@/UserSystemApi/UserApi';
  export default {
    data() {
      return {
        password: "",
      };
    },
    computed: {
    ...mapState(['username','teamname','score','isLeader','deleteUser','isLogin','setInfo','err','isHover','userInfoButtonEnabled']),
    },
    methods: {
      ...mapMutations(['setUsername','setTeamname','setIsLeader','setScore','setDeleteUser','setIsLogin','setSetInfo','setErr','setIsHover','setUserInfoButtonEnabled']),
      async delete_User() {
        try {
          const response = await deleteUserInfo(this.password);
          console.log('注销账户响应:', response);
          if (response===204) {
            alert("成功注销账号");
            this.setIsLogin(false);
            this.setUsername('');
            this.setTeamname('');
            this.setScore('');
            this.setIsLeader(false);
            this.setIsHover(false);
            localStorage.removeItem('isLogin');
            localStorage.removeItem('username');
            localStorage.removeItem('teamname');
            localStorage.removeItem('score');
            localStorage.removeItem('isLeader');
            this.setDeleteUser(false);
            this.setSetInfo(!this.$store.state.setInfo);
            this.setErr("");
            this.setUserInfoButtonEnabled(true);
          }
        } catch (error) {
          this.setErr("错误！");
        }
      },
      close() {
        this.setDeleteUser(false);
        this.setErr("");
        this.setSetInfo(true);
        this.setUserInfoButtonEnabled(true);
      },
    },
  };
</script>
<style>
#deleteUser {
    margin-top:-180px;
    margin-left:520px;
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
 