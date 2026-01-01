<template>
  <el-card class="box-card" shadow="hover" :body-style="{ padding: '0px' }" @click.native="$emit('click', item)">
    <div class="card-content">
      <div class="card-left">
        <div class="card-header">
          <span class="task-title">{{ item.task_name }}</span>
          <el-tag size="mini" :type="item.solved ? 'success' : 'info'" effect="dark" class="status-tag">
            {{ item.solved ? '已解决' : '未解决' }}
          </el-tag>
        </div>
        <div class="card-meta">
          <div class="meta-item">
            <i class="el-icon-trophy"></i> {{ item.points }} pts
          </div>
          <div class="meta-item">
            <i class="el-icon-user"></i> {{ item.solve_count }} solved
          </div>
        </div>
      </div>
      <div class="card-right" :class="{ 'solved': item.solved }">
        <i :class="item.solved ? 'el-icon-success' : 'el-icon-circle-check'"></i>
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'Question',
  props: {
    item: {
      type: Object,
      required: true,
    }
  }
}
</script>

<style scoped>
.box-card {
  width: 100%;
  cursor: pointer;
  background-color: #161b22;
  border: 1px solid #30363d;
  color: #c9d1d9;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.box-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  border-color: #8b949e;
}

.card-content {
  display: flex;
  height: 100px;
}

.card-left {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.task-title {
  font-size: 18px;
  font-weight: 600;
  color: #58a6ff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 180px;
}

.card-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #8b949e;
}

.meta-item i {
  margin-right: 4px;
}

.card-right {
  width: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #21262d;
  font-size: 40px;
  color: #30363d;
}

.card-right.solved {
  background-color: #238636;
  color: #ffffff;
}

.status-tag {
  margin-left: 10px;
}
</style>
