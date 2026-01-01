<template>
  <div class="nav-container">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" router background-color="#161b22" text-color="#c9d1d9" active-text-color="#c9d1d9">
      <el-menu-item index="/home" class="logo-item">
        <i class="iconfont icon-xE990"></i> EZCTF
      </el-menu-item>
      <el-menu-item index="/ranking">
        <i class="iconfont icon-paixingbang"></i> Ranking
      </el-menu-item>
      
      <div class="right-menu">
        <el-button v-if="!isLogin" type="primary" size="small" @click="handleLoginClick" :disabled="!loginButtonEnabled">
          登录 / 注册
        </el-button>

        <el-dropdown v-else trigger="click" @command="handleCommand">
          <span class="el-dropdown-link">
            <CreateAvatar :username="userInfo.name" class="nav-avatar"/>
            <span class="nav-username">{{ userInfo.name }}</span>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown" class="user-dropdown">
            <el-dropdown-item class="user-info-item" disabled>
              <div>积分: {{ userInfo.score }}</div>
              <div>战队: {{ userInfo.team || '无战队' }}</div>
            </el-dropdown-item>
            <el-dropdown-item command="message" divided>
              <i class="iconfont icon-xiaoxi"></i> 消息通知
              <el-badge :value="messnum" v-if="num(messnum)" class="item-badge" />
            </el-dropdown-item>
            <el-dropdown-item command="team">
              <i class="iconfont icon-yusherenyuan"></i> 我的战队
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <i class="iconfont icon-chilun"></i> 用户设置
            </el-dropdown-item>
            <el-dropdown-item command="logout" divided>
              <i class="iconfont icon-guanji"></i> 退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-menu>
  </div>
</template>

<script>
import CreateAvatar from '../components/CreateAvatar.vue';
import { mapState, mapMutations } from 'vuex';
import { logoutUser } from '@/UserSystemApi/UserApi';
import { messNum } from '@/UserSystemApi/MessageApi';

export default {
  name: 'Navigation',
  components: {
    CreateAvatar,
  },
  data() {
    return {
      activeIndex: '/home',
      messnum: '',
    };
  },
  computed: {
    ...mapState([
      'loginButtonEnabled',
      'username',
      'teamname',
      'score',
      'isLogin',
      'setInfo',
    ]),
    userInfo() {
      return {
        name: this.$store.state.username,
        score: this.$store.state.score,
        team: this.$store.state.teamname,
      };
    },
  },
  methods: {
    ...mapMutations([
      'setLoginButtonEnabled',
      'setIsLogin',
      'setLog',
      'setInfoBoard',
      'setManageTeam',
      'setSetInfo',
      'setModifyUser',
      'setDeleteUser',
      'setUsername',
      'setScore',
      'setTeamname',
      'setIsLeader'
    ]),
    handleLoginClick() {
        this.setLog(true);
        this.$router.push('/Log');
    },
    handleCommand(command) {
      switch (command) {
        case 'message':
          this.message();
          break;
        case 'team':
          this.team();
          break;
        case 'settings':
          this.setinfo();
          break;
        case 'logout':
          this.quit();
          break;
      }
    },
    async quit() {
      // await logoutUser(); // Backend is stateless JWT, client side clear is enough usually, but can call backend
      localStorage.clear();
      this.setIsLogin(false);
      this.setLoginButtonEnabled(true);
      this.setUsername('');
      this.setScore('');
      this.setTeamname('');
      this.setIsLeader(false);
      this.$router.push('/home');
      window.location.reload();
    },
    message() {
      this.setInfoBoard(true);
      this.$router.push('/home');
    },
    team() {
      if (!this.userInfo.team) {
          this.$router.push('/NoTeam');
      } else {
          this.setManageTeam(true);
          this.$router.push('/TeamInfo');
      }
    },
    setinfo() {
      this.setSetInfo(true);
      this.setModifyUser(false);
      this.setDeleteUser(false);
      this.$router.push('/LoginSystem');
    },
    num(n) {
      return n && n > 0;
    }
  },
  watch: {
    $route(to) {
      this.activeIndex = to.path;
    }
  },
  mounted() {
      this.activeIndex = this.$route.path;
      // Mock message num for now or call api
      // messNum().then(res => this.messnum = res);
  }
};
</script>

<style scoped>
.nav-container {
    border-bottom: 1px solid #30363d;
}
.el-menu-demo {
    display: flex;
    align-items: center;
    border-bottom: none !important;
    max-width: 1200px;
    margin: 0 auto;
}
.logo-item {
    font-size: 18px;
    font-weight: bold;
}
.right-menu {
    margin-left: auto;
    display: flex;
    align-items: center;
    padding-right: 20px;
}
.el-dropdown-link {
    cursor: pointer;
    color: #c9d1d9;
    display: flex;
    align-items: center;
}
.nav-avatar {
    width: 30px;
    height: 30px;
    margin-right: 8px;
    display: inline-block;
}
.nav-username {
    margin-right: 5px;
}
.user-dropdown {
    background-color: #161b22;
    border-color: #30363d;
}
/* This part might need global css for dropdown items in body */
</style>
