<template>
    <div id="changeTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>修改战队名称</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <input v-model="newTeamname" placeholder="请输入新战队名" /><br><br>
      <button @click="change_Team()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { changeTeamName } from '@/UserSystemApi/TeamApi';
  export default {
    data() {
      return {
        newTeamname: "",
      };
    },
    computed: {
    ...mapState(['teamname','changeTeamname','manageTeam','err']),
    isValid(string) {
          const Regex = /^[a-zA-Z0-9_]+$/;
          return (string) => Regex.test(string);
    },
    },
    methods: {
      ...mapMutations(['setTeamname','setChangeTeamname','setManageTeam','setErr']),
      async change_Team() {
        try {
          if (!this.isValid(this.newTeamname)) {
              this.setErr("战队名只能包含数字、字母和下划线");
              return;
          }
          const response = await changeTeamName(this.newTeamname);
          console.log('修改信息响应:', response);
          if (response.ret === 'success') {
            alert(response.msg);
            this.setChangeTeamname(false);
            this.setManageTeam(true);
            this.setTeamname(response.data.team_name);
            localStorage.setItem('teamname', response.data.team_name);
            this.setErr("");
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
        }
      },
      close() {
        this.setChangeTeamname(false);
        this.setManageTeam(true);
        this.setErr("");
      },
    },
  };
</script>
<style>
#changeTeam {
    top: auto;
    left: auto;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 180px;
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
    z-index: 10;
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
 