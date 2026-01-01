<template>
  <div class="show-question-container">
    <el-card class="box-card-container">
      <el-tabs v-model="activeCategory" @tab-click="handleTabClick" type="card">
        <el-tab-pane label="Misc" name="0">
          <span slot="label"><i class="el-icon-files"></i> Misc</span>
        </el-tab-pane>
        <el-tab-pane label="Crypto" name="1">
          <span slot="label"><i class="el-icon-lock"></i> Crypto</span>
        </el-tab-pane>
        <el-tab-pane label="Web" name="2">
          <span slot="label"><i class="el-icon-monitor"></i> Web</span>
        </el-tab-pane>
        <el-tab-pane label="Reverse" name="3">
          <span slot="label"><i class="el-icon-refresh"></i> Reverse</span>
        </el-tab-pane>
        <el-tab-pane label="Pwn" name="4">
          <span slot="label"><i class="el-icon-cpu"></i> Pwn</span>
        </el-tab-pane>
      </el-tabs>

      <div class="task-list" v-loading="loading">
        <el-empty v-if="retlist.length === 0 && !loading" description="暂无题目"></el-empty>
        <el-row :gutter="20" v-else>
          <el-col :xs="24" :sm="12" :md="12" :lg="8" :xl="6" v-for="item in retlist" :key="item.task_id">
            <Question :item="item" @click="openTaskDetail" />
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-dialog
      :title="currentTask.task_name"
      :visible.sync="dialogVisible"
      width="60%"
      :before-close="handleClose"
      custom-class="task-detail-dialog">
      <Popup v-if="currentTask && currentTaskDetail" :item="currentTask" :Detail="currentTaskDetail" @solved="handleSolved"/>
      <div v-else class="loading-detail" v-loading="detailLoading">
        <div style="height: 200px;"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import Question from './Question.vue';
import Popup from './Popup.vue';
import { mapState } from 'vuex';

export default {
  name: 'Showquestion',
  components: { Question, Popup },
  data() {
    return {
      activeCategory: '0',
      retlist: [],
      loading: false,
      dialogVisible: false,
      currentTask: {},
      currentTaskDetail: null,
      detailLoading: false
    };
  },
  computed: {
    ...mapState(['isLogin']),
  },
  methods: {
    handleTabClick(tab) {
      if (this.isLogin) {
        this.fetchData(tab.name);
      } else {
        this.$message.warning("前面的区域登录以后再来探索吧~~");
        this.$router.push("/Log");
      }
    },
    fetchData(category) {
      this.loading = true;
      axios.get('/api/v1/task/?category=' + category)
        .then(response => {
          // Backend returns List[TaskRead]
          this.retlist = response.data.map(t => ({
            ...t,
            task_id: t.id,
            task_name: t.title,
            points: t.score,
            solve_count: t.solve_count || 0,
            solved: t.solved || false // Backend should populate this if user is logged in
          }));
        })
        .catch(error => {
          console.error(error);
          this.$message.error("获取题目列表失败");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    openTaskDetail(item) {
      this.currentTask = item;
      this.dialogVisible = true;
      this.detailLoading = true;
      this.currentTaskDetail = null;

      // Fetch task detail (description, etc.)
      // Assuming backend endpoint /api/v1/task/{id} returns details
      axios.get('/api/v1/task/' + item.task_id)
        .then(response => {
          const t = response.data;
          this.currentTaskDetail = {
            ...t,
            task_name: t.title,
            content: t.description,
            annex: t.annex
          };
        })
        .catch(error => {
          console.error(error);
          this.$message.error("获取题目详情失败");
        })
        .finally(() => {
          this.detailLoading = false;
        });
    },
    handleClose(done) {
      done();
    },
    handleSolved() {
      // Refresh list to update solved status
      this.fetchData(this.activeCategory);
      // Maybe close dialog or keep it open
    }
  },
  mounted() {
    if (this.isLogin) {
      this.fetchData(this.activeCategory);
    } else {
        // If not logged in, maybe show something else or redirect?
        // Original code alerted and redirected.
        // For better UX, we can let them see the list but not click?
        // Or just follow original logic.
        // But mounted is called when component is created.
        // If we redirect immediately, it might be jarring.
        // Let's check logic.
        // Original: mounted -> changediv(0) -> check login -> alert -> redirect.
        // I'll keep it simple: fetch data if login, otherwise let user navigate or show empty.
        // But Navigation.vue handles login button.
        // If user clicks "Challenge" link and is not logged in, we probably want to redirect.
        // But let's verify token validity or just rely on store.
    }
  },
  watch: {
      isLogin(val) {
          if (val) {
              this.fetchData(this.activeCategory);
          }
      }
  }
}
</script>

<style scoped>
.show-question-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.box-card-container {
  background-color: #0d1117; /* Dark theme background */
  border: 1px solid #30363d;
  min-height: 600px;
}

/* Customize Tabs */
::v-deep .el-tabs__item {
  color: #8b949e;
  font-size: 16px;
}
::v-deep .el-tabs__item.is-active {
  color: #58a6ff;
  background-color: #161b22 !important;
  border-bottom-color: #161b22 !important;
}
::v-deep .el-tabs__nav-wrap::after {
  background-color: #30363d;
}
::v-deep .el-card__body {
    padding: 20px;
    background-color: #0d1117;
}

.task-list {
  margin-top: 20px;
}

.loading-detail {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Dialog Customization */
::v-deep .task-detail-dialog {
    border-radius: 8px;
}
::v-deep .task-detail-dialog .el-dialog__header {
    border-bottom: 1px solid #ebeef5;
}
::v-deep .task-detail-dialog .el-dialog__body {
    padding: 20px;
}
</style>
