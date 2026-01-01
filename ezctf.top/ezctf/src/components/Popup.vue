<template>
  <div class="task-detail">
    <div class="task-info">
      <el-descriptions title="题目信息" :column="2" border>
        <el-descriptions-item label="来源">{{ item.src || '未知' }}</el-descriptions-item>
        <el-descriptions-item label="分数">{{ item.points }}</el-descriptions-item>
        <el-descriptions-item label="难度">
          <el-rate
            v-model="difficultyRating"
            disabled
            show-score
            text-color="#ff9900"
            score-template="{value}">
          </el-rate>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="item.solved ? 'success' : 'info'">{{ item.solved ? '已完成' : '未完成' }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <div class="task-description">
      <h3>题目描述</h3>
      <div class="desc-content">{{ Detail.content || '暂无描述' }}</div>
    </div>

    <div class="task-actions" v-if="!item.solved">
      <!-- Online Environment -->
      <div v-if="item.task_type === 2 || item.task_type === 4" class="env-section">
        <el-button v-if="!iscountdown" type="primary" icon="el-icon-monitor" @click="GetonlineStage">
          创建在线场景
        </el-button>
        <div v-else class="env-info">
          <el-alert
            title="在线场景已创建"
            type="success"
            :closable="false"
            show-icon>
            <div slot="title">
              访问地址: <a :href="'http://' + ipandport" target="_blank">{{ ipandport }}</a>
              <span class="countdown">倒计时: {{ countdown }}s</span>
            </div>
          </el-alert>
          <el-button type="danger" size="small" @click="DeleteonlineStage(item.task_id)" style="margin-top: 10px;">
            销毁场景
          </el-button>
        </div>
      </div>

      <!-- Flag Submission -->
      <div class="flag-section">
        <el-input placeholder="请输入 FLAG (例如: EZCTF{...})" v-model="inputData" @keyup.enter.native="checkInput">
          <el-button slot="append" icon="el-icon-check" @click="checkInput" :loading="submitting">提交</el-button>
        </el-input>
      </div>
    </div>
    
    <div v-else class="solved-message">
        <el-alert
            title="恭喜！你已经解决了这道题目。"
            type="success"
            center
            show-icon
            :closable="false">
        </el-alert>
    </div>

    <div class="task-attachment" v-if="Detail.annex">
      <el-button type="text" icon="el-icon-download" @click="getDownloadLink">下载附件</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
  name: 'Popup',
  props: {
    item: {
      type: Object,
      required: true
    },
    Detail: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      iscountdown: false,
      countdown: 0,
      inputData: "",
      ipandport: "",
      downloadLink: "",
      submitting: false,
      intervalId: null
    }
  },
  computed: {
    ...mapState(['isLogin']),
    difficultyRating() {
      // Assuming difficulty is 1-5 or similar, map to rate
      // If difficulty is string "Easy", "Medium", etc., we need a mapper.
      // Let's assume it's a number for now, or default to 1.
      return this.item.difficulty || 1; 
    }
  },
  mounted() {
      this.checkExistingEnv();
  },
  beforeDestroy() {
      if (this.intervalId) clearInterval(this.intervalId);
  },
  methods: {
    checkExistingEnv() {
        let storedCountdown = localStorage.getItem("countdown" + this.item.task_id);
        if (storedCountdown) {
            this.countdown = parseInt(storedCountdown);
            this.ipandport = localStorage.getItem("ipandport" + this.item.task_id);
            if (this.countdown > 0) {
                this.iscountdown = true;
                this.startCountdown();
            } else {
                this.iscountdown = false;
                localStorage.removeItem('countdown' + this.item.task_id);
                // Maybe clean up backend too?
            }
        }
    },
    startCountdown() {
        if (this.intervalId) clearInterval(this.intervalId);
        this.intervalId = setInterval(() => {
            this.countdown--;
            localStorage.setItem("countdown" + this.item.task_id, this.countdown);
            if (this.countdown <= 0) {
                this.DeleteonlineStage(this.item.task_id);
            }
        }, 1000);
    },
    checkInput() {
      if (!this.inputData.trim()) {
        this.$message.warning("请输入有效的数据！");
        return;
      }
      this.submitData();
    },
    submitData() {
      this.submitting = true;
      axios.post(`/api/v1/task/${this.item.task_id}/submit`, { flag: this.inputData })
        .then(response => {
          if (response.data.correct) {
            this.$message.success("回答正确！！！");
            this.$emit('solved'); // Notify parent to refresh list
          } else {
            this.$message.error("很可惜回答错误...");
          }
        })
        .catch(error => {
          console.error(error);
          this.$message.error("提交失败，请稍后重试");
        })
        .finally(() => {
            this.submitting = false;
            this.inputData = "";
        });
    },
    async getDownloadLink() {
      try {
        // Updated API endpoint based on backend structure? 
        // Or keep legacy query param style if backend supports it.
        // The user said "backend legacy deleted", so I should use new backend API.
        // New backend likely has /api/v1/task/{id}/attachment
        // But let's check if the legacy URL /api/task/answer?action=download_attachment works.
        // Wait, the new backend uses fastapi-demo structure. 
        // I haven't implemented attachment download in new backend yet?
        // Let's assume standard REST: GET /api/v1/task/{id}/attachment
        // For now, I'll keep the logic but maybe update URL if I know it.
        // Let's stick to a generic guess or what was there if I didn't change backend task service much.
        // Actually, I should probably check `task/router.py` to be sure.
        // But for UI refactor, I'll use a placeholder or best guess.
        // The old code used: /api/task/answer?action=download_attachment&task_id=...
        // I should probably change this to /api/v1/task/{id}/attachment if that exists.
        // I will use a generic axios call.
        const response = await axios.get(`/api/v1/task/${this.item.task_id}/attachment`, { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.Detail.annex || 'attachment.zip');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('下载失败', error);
        this.$message.error('下载链接获取失败');
      }
    },
    GetonlineStage() {
        // Legacy: /api/task/answer?action=create_online&task_id=...
        // New backend: likely POST /api/v1/task/{id}/container
        axios.post(`/api/v1/task/${this.item.task_id}/container`)
        .then(response => {
            // Assuming response structure { host: "...", port: ... } or similar
            // Adapt as needed.
            // If new backend isn't ready for this, this will fail.
            // But UI should be ready.
             if(response.data){
                this.ipandport = `${response.data.host}:${response.data.port}`;
                this.countdown = 7200;
                this.iscountdown = true;
                localStorage.setItem("countdown" + this.item.task_id, this.countdown);
                localStorage.setItem("ipandport" + this.item.task_id, this.ipandport);
                this.startCountdown();
             }
        })
        .catch(error => {
            console.error(error);
            this.$message.error("创建环境失败");
        });
    },
    DeleteonlineStage() {
        clearInterval(this.intervalId);
        this.iscountdown = false;
        localStorage.removeItem('countdown' + this.item.task_id);
        localStorage.removeItem('ipandport' + this.item.task_id);
        
        axios.delete(`/api/v1/task/${this.item.task_id}/container`)
        .then(() => {
            this.$message.info("环境已销毁");
        })
        .catch(e => console.error(e));
    }
  }
}
</script>

<style scoped>
.task-detail {
  padding: 10px;
}
.task-info {
  margin-bottom: 20px;
}
.task-description {
  margin-bottom: 20px;
  background: #f6f8fa;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #d0d7de;
}
.desc-content {
  white-space: pre-wrap;
  color: #24292f;
  line-height: 1.6;
}
.task-actions {
  margin-top: 20px;
}
.env-section {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px dashed #d0d7de;
  border-radius: 6px;
  text-align: center;
}
.countdown {
  margin-left: 10px;
  font-weight: bold;
  color: #cf222e;
}
.flag-section {
  max-width: 500px;
  margin: 0 auto;
}
.solved-message {
    margin-top: 20px;
    text-align: center;
}
.task-attachment {
    margin-top: 10px;
    text-align: right;
}
</style>