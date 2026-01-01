<template>
    <div id="kickmember">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>踢出成员</h1>
      <p v-if="err" id="er">{{ err }}</p>
      <br v-if="!err">
      <p>是否将{{ kMember }}踢出战队?</p><br>
      <button @click="kick_member()">确认</button>
    </div>
</template>
  
<script>
  import { mapState, mapMutations } from 'vuex';
  import { kickoutMember } from '@/UserSystemApi/TeamApi';
  export default {
    computed: {
    ...mapState(['kickMember','manageTeam','kMember','err']),
    },
    methods: {
      ...mapMutations(['setKickMember','setManageTeam','setKMember','setErr']),
      async kick_member() {
        try {
          const response = await kickoutMember(this.$store.state.kMember);
          console.log('踢出成员响应:', response);
          if (response.ret === "success") {
            alert("成员踢出成功！");
            this.setKickMember(false);
            this.setKMember("");
            this.setManageTeam(true);
            this.setErr("");
          }
        } catch (error) {
          this.setErr(error.response.data.msg);
        }
      },
      close() {
        this.setKickMember(false);
        this.setKMember("");
        this.setManageTeam(true);
        this.setErr("");
      },
    },
  };
</script>
<style>
#kickmember {
    top: auto;
    left: auto;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 200px;
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
 