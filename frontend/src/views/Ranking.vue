<template>
  <div class="ranking-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span class="page-title"><i class="el-icon-trophy"></i> 排行榜</span>
      </div>
      
      <el-tabs v-model="activeTab" type="card">
        <el-tab-pane label="用户排行" name="user">
          <span slot="label"><i class="el-icon-user"></i> 用户排行</span>
          
          <!-- My User Rank -->
          <el-alert
            v-if="myUserRank"
            type="success"
            :closable="false"
            class="my-rank-alert"
            show-icon>
            <div slot="title">
              我的排名: #{{ myUserRank.rank }} ({{ myUserRank.score }} pts)
            </div>
          </el-alert>

          <el-table
            :data="users"
            stripe
            style="width: 100%"
            v-loading="loading">
            <el-table-column
              prop="rank"
              label="排名"
              width="80"
              align="center">
              <template slot-scope="scope">
                <div class="rank-badge" :class="'rank-' + scope.row.rank">
                  <span v-if="scope.row.rank <= 3"><i class="el-icon-medal"></i></span>
                  {{ scope.row.rank }}
                </div>
              </template>
            </el-table-column>
            <el-table-column
              prop="username"
              label="用户"
              min-width="180">
              <template slot-scope="scope">
                <div class="user-info">
                   <el-avatar size="small" :src="scope.row.avatar_url || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'"></el-avatar>
                   <span class="username">{{ scope.row.username }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column
              prop="score"
              label="积分"
              width="120"
              sortable>
            </el-table-column>
            <el-table-column
              prop="last_answer_time"
              label="最后提交"
              width="180">
              <template slot-scope="scope">
                {{ formatDate(scope.row.last_answer_time) }}
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="战队排行" name="team">
          <span slot="label"><i class="el-icon-s-flag"></i> 战队排行</span>
          
          <!-- My Team Rank -->
          <el-alert
            v-if="myTeamRank"
            type="info"
            :closable="false"
            class="my-rank-alert"
            show-icon>
            <div slot="title">
              我的战队: {{ myTeamRank.team_name }} - 排名: #{{ myTeamRank.rank }} ({{ myTeamRank.score }} pts)
            </div>
          </el-alert>

          <el-table
            :data="teams"
            stripe
            style="width: 100%"
            v-loading="loading">
            <el-table-column
              prop="rank"
              label="排名"
              width="80"
              align="center">
              <template slot-scope="scope">
                 <div class="rank-badge" :class="'rank-' + scope.row.rank">
                  <span v-if="scope.row.rank <= 3"><i class="el-icon-medal"></i></span>
                  {{ scope.row.rank }}
                </div>
              </template>
            </el-table-column>
            <el-table-column
              prop="team_name"
              label="战队名称"
              min-width="180">
            </el-table-column>
            <el-table-column
              prop="member_count"
              label="人数"
              width="100">
            </el-table-column>
            <el-table-column
              prop="score"
              label="总积分"
              width="120"
              sortable>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { getUserRanking, user_profile } from '@/UserSystemApi/UserApi';
import { getTeamRanking } from '@/UserSystemApi/TeamApi';
import moment from 'moment';

export default {
  name: 'Ranking',
  data() {
    return {
      activeTab: 'user',
      users: [],
      teams: [],
      loading: false,
      currentUser: null,
      myUserRank: null,
      myTeamRank: null,
    };
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        // Fetch current user info for highlighting
        try {
            this.currentUser = await user_profile();
        } catch (e) {
            console.warn("Not logged in or failed to fetch profile");
        }

        const [usersData, teamsData] = await Promise.all([
          getUserRanking(),
          getTeamRanking()
        ]);
        
        this.users = usersData;
        this.teams = teamsData;

        // Find my ranks
        if (this.currentUser) {
            this.myUserRank = this.users.find(u => u.username === this.currentUser.username);
            if (this.currentUser.team_id) {
                this.myTeamRank = this.teams.find(t => t.team_id === this.currentUser.team_id);
            }
        }

      } catch (error) {
        this.$message.error('获取排行榜失败');
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateStr) {
        if (!dateStr) return '-';
        return moment(dateStr).format('YYYY-MM-DD HH:mm:ss');
    }
  }
};
</script>

<style scoped>
.ranking-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
}

.my-rank-alert {
  margin-bottom: 20px;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.username {
    font-weight: 500;
}

.rank-badge {
    font-weight: bold;
    color: #606266;
}

.rank-1 {
    color: #f56c6c;
    font-size: 1.2em;
}

.rank-2 {
    color: #e6a23c;
    font-size: 1.1em;
}

.rank-3 {
    color: #409eff;
    font-size: 1.1em;
}
</style>
