<template>
  <div class="auth-container">
    <el-card class="auth-card">
      <div slot="header" class="clearfix">
        <span class="auth-title">找回密码</span>
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

      <div v-if="!btn">
        <el-form :model="form" :rules="rules" ref="forgetForm" label-position="top">
            <el-form-item label="邮箱" prop="email">
                <el-input v-model="form.email" placeholder="请输入注册邮箱" prefix-icon="el-icon-message"></el-input>
            </el-form-item>
             <el-form-item>
                <el-button type="primary" @click="sendCode" class="full-width-btn" :loading="loading">发送验证码</el-button>
            </el-form-item>
        </el-form>
      </div>

      <div v-else>
         <el-form :model="resetForm" :rules="resetRules" ref="resetForm" label-position="top">
            <el-form-item label="验证码" prop="code">
                <el-input v-model="resetForm.code" placeholder="请输入验证码" prefix-icon="el-icon-key"></el-input>
            </el-form-item>
            <el-form-item label="新密码" prop="newPassword">
                <el-input v-model="resetForm.newPassword" type="password" placeholder="请输入新密码" prefix-icon="el-icon-lock" show-password></el-input>
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirmNewPassword">
                <el-input v-model="resetForm.confirmNewPassword" type="password" placeholder="请再次输入新密码" prefix-icon="el-icon-lock" show-password></el-input>
            </el-form-item>
             <el-form-item>
                <el-button type="primary" @click="doReset" class="full-width-btn" :loading="loading">重置密码</el-button>
            </el-form-item>
         </el-form>
      </div>
      
      <div class="auth-links">
         <el-button type="text" @click="close">返回登录</el-button>
      </div>

    </el-card>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import { forgetPassword, resetPassword } from '../UserSystemApi/UserApi.js';

export default {
  name: 'ForgetPassword',
  data() {
    var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.resetForm.newPassword) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
    return {
      form: {
        email: ''
      },
      resetForm: {
          code: '',
          newPassword: '',
          confirmNewPassword: ''
      },
      loading: false,
      btn: false, // false: step 1 (email), true: step 2 (code + password)
      rules: {
          email: [
            { required: true, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
          ]
      },
      resetRules: {
          code: [
              { required: true, message: '请输入验证码', trigger: 'blur' }
          ],
          newPassword: [
              { required: true, message: '请输入新密码', trigger: 'blur' },
              { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
          ],
          confirmNewPassword: [
              { validator: validatePass2, trigger: 'blur' }
          ]
      }
    };
  },
  computed: {
    ...mapState(['err']),
  },
  methods: {
    ...mapMutations(['setLog','setFoPa','setErr','setLoginButtonEnabled']),
    close() {
      this.setFoPa(false);
      this.setLog(true);
      this.setErr("");
    },
    async sendCode() {
        this.$refs['forgetForm'].validate(async (valid) => {
            if (valid) {
                this.loading = true;
                try {
                    const response = await forgetPassword(this.form.email);
                    // Mock success for now if backend returns empty/warning
                    if (response && response.status === 'success') {
                         this.btn = true;
                         this.setErr("");
                         this.$message.success('验证码已发送');
                    } else {
                         // Fallback for not implemented
                         this.$message.warning("此功能暂未开放 (Backend Not Implemented)");
                         // For demo purposes, let's proceed to step 2 anyway?
                         // No, better to be honest.
                    }
                } catch (error) {
                    this.setErr(error.response?.data?.detail || "发送验证码失败");
                } finally {
                    this.loading = false;
                }
            }
        });
    },
    async doReset() {
        this.$refs['resetForm'].validate(async (valid) => {
            if (valid) {
                this.loading = true;
                try {
                    const response = await resetPassword(this.resetForm.code, this.form.email, this.resetForm.newPassword);
                    if (response && response.status === 'success') {
                         this.$message.success('密码重置成功，请登录');
                         this.close();
                    } else {
                        this.$message.warning("重置密码失败 (Backend Not Implemented)");
                    }
                } catch (error) {
                    this.setErr(error.response?.data?.detail || "重置密码失败");
                } finally {
                    this.loading = false;
                }
            }
        });
    }
  }
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
