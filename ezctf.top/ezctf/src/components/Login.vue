<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <div slot="header" class="clearfix">
        <span class="auth-title">用户登录</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="close">
          <i class="el-icon-close"></i>
        </el-button>
      </div>
      
      <el-alert
        v-if="err"
        :title="err"
        type="error"
        show-icon
        @close="setErr('')"
        style="margin-bottom: 20px;">
      </el-alert>

      <el-form :model="loginInfo" @submit.native.prevent="loginUser">
        <el-form-item label="用户名/邮箱">
          <el-input v-model="loginInfo.usernameOrEmail" placeholder="请输入用户名或邮箱" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="loginInfo.password" type="password" placeholder="请输入密码" prefix-icon="el-icon-lock" show-password></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" native-type="submit" class="full-width-btn" :loading="loading">登录</el-button>
        </el-form-item>
        
        <div class="auth-links">
          <el-button type="text" @click="FoP">忘记密码?</el-button>
          <el-button type="text" @click="Reg">注册新账号</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { login, user_profile } from '../UserSystemApi/UserApi.js';
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'Login',
  data() {
    return {
      loginInfo: {
        usernameOrEmail: '',
        password: '',
      },
      loading: false,
    };
  },
  computed: {
    ...mapState(['err']),
  },
  methods: {
    ...mapMutations([
      'setLoginButtonEnabled',
      'setUsername',
      'setIsLogin',
      'setLog',
      'setReg',
      'setFoPa',
      'setTeamname',
      'setScore',
      'setIsLeader',
      'setErr'
    ]),
    close() {
      this.setLoginButtonEnabled(true);
      localStorage.setItem('LBE', true);
      this.setErr("");
      this.$router.push('/');
    },
    async loginUser() {
      this.loading = true;
      try {
        const response = await login(this.loginInfo.usernameOrEmail, this.loginInfo.password);
        console.log('Login Response:', response);
        
        if (response.access_token) {
          localStorage.setItem('token', response.access_token);
          
          const user = await user_profile();
          
          this.setLoginButtonEnabled(true);
          localStorage.setItem('LBE', true);
          
          this.setUsername(user.username);
          localStorage.setItem('username', user.username);
          
          this.setTeamname(user.team_name);
          if (user.team_name) {
            localStorage.setItem('teamname', user.team_name);
          }
          
          this.setScore(user.score);
          localStorage.setItem('score', user.score);
          
          this.setIsLogin(true);
          localStorage.setItem('isLogin', 'true');
          
          this.setErr("");
          
          this.setIsLeader(user.is_leader);
          if (user.is_leader) {
            localStorage.setItem('isLeader', user.is_leader);
          }
          
          this.$message.success('登录成功');
          this.$router.push('/');
        }
      } catch (error) {
        const msg = error.response?.data?.detail || "Login failed";
        this.setErr(msg);
        console.error('Login Error:', error);
      } finally {
        this.loading = false;
      }
    },
    Reg() {
      this.setLog(false);
      this.setReg(true);
      this.setErr("");
    },
    FoP() {
      this.setLog(false);
      this.setFoPa(true);
      this.setErr("");
    },
  },
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 50px;
}
.auth-card {
  width: 400px;
}
.auth-title {
  font-size: 18px;
  font-weight: bold;
}
.full-width-btn {
  width: 100%;
}
.auth-links {
  display: flex;
  justify-content: space-between;
}
</style>
