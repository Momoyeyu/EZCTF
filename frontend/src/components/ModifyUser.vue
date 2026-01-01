<template>
    <div id="modifyUser">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>修改信息</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <input v-model="newUsername" placeholder="请输入新用户名" /><br><br>
      <input v-model="password" placeholder="请输入密码" /><br><br>
      <button @click="modify_User()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { modifyUserInfo } from '@/UserSystemApi/UserApi';
  export default {
    data() {
      return {
        user_name:this.$store.state.username,
        newUsername: "",
        password: "",
      };
    },
    computed: {
    ...mapState(['username','teamname','modifyUser','err','setInfo','userInfoButtonEnabled']),
    isValid(string) {
          const Regex = /^[a-zA-Z0-9_]+$/;
          return (string) => Regex.test(string);
    },
    },
    methods: {
      ...mapMutations(['setUsername','setTeamname','setModifyUser','setErr','setSetInfo','setUserInfoButtonEnabled']),
      async modify_User() {
        try {
          if (!this.isValid(this.newUsername)) {
              this.setErr("用户名只能包含数字、字母和下划线");
              return;
          }
          const response = await modifyUserInfo(this.user_name, this.newUsername,this.password);
          console.log('修改信息响应:', response);
          if (response.ret === 'success') {
            alert(response.msg);
            this.setModifyUser(false);
            this.setUsername(response.data.new_username);
            localStorage.setItem('username', response.data.new_username);
            this.setErr("");
            this.setSetInfo(true);
            this.setUserInfoButtonEnabled(true);
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
          console.error('错误:', error);
        }
      },
      close() {
        this.setModifyUser(false);
        this.setErr("");
        this.setSetInfo(true);
        this.setUserInfoButtonEnabled(true);
      },
    },
  };
</script>
<style>
#modifyUser {
    margin-top:-200px;
    margin-left:520px;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 220px;
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
    padding: 4px;
    color:red;
    font-size: small;
}
</style>
 