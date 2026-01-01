<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <div slot="header" class="clearfix">
        <span class="auth-title">用户注册</span>
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

      <el-form :model="user" :rules="rules" ref="registerForm" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="user.username" placeholder="请输入用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="user.email" placeholder="请输入邮箱" prefix-icon="el-icon-message"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="user.password" type="password" placeholder="请输入密码" prefix-icon="el-icon-lock" show-password></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="user.confirmPassword" type="password" placeholder="请再次输入密码" prefix-icon="el-icon-lock" show-password></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm('registerForm')" class="full-width-btn" :loading="loading">注册</el-button>
        </el-form-item>
        
        <div class="auth-links">
             <el-button type="text" @click="close">已有账号？去登录</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { register, login, user_profile } from '../UserSystemApi/UserApi.js';
import { mapState, mapMutations } from 'vuex';

export default {
  name: 'Registration',
  data() {
    var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.user.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
    return {
      user: {
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
      },
      loading: false,
      rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
            { pattern: /^[a-zA-Z0-9_]+$/, message: '只能包含字母、数字和下划线', trigger: 'blur' }
          ],
          email: [
            { required: false, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
          ],
          confirmPassword: [
            { validator: validatePass2, trigger: 'blur' }
          ]
      }
    };
  },
  computed: {
    ...mapState(['err']),
  },
  methods: {
    ...mapMutations([
      'setLoginButtonEnabled',
      'setUsername',
      'setReg',
      'setLog',
      'setErr',
      'setIsLogin',
      'setTeamname',
      'setScore',
      'setIsLeader'
    ]),
    close() {
      this.setReg(false);
      this.setLog(true);
      this.setErr("");
    },
    submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.doRegister();
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
    async doRegister() {
      this.loading = true;
      try {
        const response = await register(this.user.username, this.user.password, this.user.email);
        console.log('Register Response:', response);
        
        if (response.id) {
          this.setErr("");
          this.$message.success('注册成功，正在自动登录...');
          await this.loginUser();
        }
      } catch (error) {
        const msg = error.response?.data?.detail || "Registration failed";
        this.setErr(msg);
        console.error('Register Error:', error);
      } finally {
        this.loading = false;
      }
    },
    async loginUser() {
      try {
        const response = await login(this.user.username, this.user.password);
        if (response.access_token) {
          localStorage.setItem('token', response.access_token);
          const user = await user_profile();

          this.$router.push('/');
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
          
          this.close(); // Return to login view logic which usually closes modal or redirects
        }
      } catch (error) {
          console.error("Auto login failed after registration", error);
      }
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
    text-align: center;
    margin-top: 10px;
}
</style>
