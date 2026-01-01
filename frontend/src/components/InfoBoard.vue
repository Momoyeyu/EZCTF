<template>
  <div class="message-list">
    <button @click="close()" class="close-btn">&#10006;</button>
    <h2>消息列表</h2>
    <div class="btnSet">
      <button @click="checkall()" class="btn">全部标记为已读</button> |
      <button @click="clear()" class="btn1">清空</button>
    </div>
    <br><br>
    <div class="scrollable-container">
      <ul>
      <li v-for="message in reversedMessages" :key="message.message_id">
        <div @click="clickMess(message.message_id, message.msg_type,message.checked,message.origin)" class="message-item" v-if="fil(message.receiver)||fil(message.origin)">
          <div class="message-origin">{{ message.origin }} :</div>
          <div class="sign" v-if="!message.checked"></div>
          <div class="message-text">{{ mess(message.msg_type, message.message) }}</div>
        </div>
      </li>
    </ul>
    </div>
  </div>
</template>

<script>
import { getMessage, checkMessage, checkAll } from '../UserSystemApi/MessageApi.js';
import { mapState, mapMutations } from 'vuex';
export default {
  data() {
    return {
      messages: [
        { message_id:"", receiver:"", origin:"", message:"", create_time:'', msg_type:'', checked:''},
      ],
      name: this.$store.state.username,
      num:"",
    };
  },
  computed: {
    ...mapState(['userInfoButtonEnabled','infoBoard','acceptInvite','inviter','username']),
    reversedMessages() {
      return this.messages.slice().reverse();
    },
  },
  mounted() {
      this.getMessages();
  },
  methods: {
    ...mapMutations(['setUserInfoButtonEnabled','setInfoBoard','setAcceptInvite','setInviter']),
    close() {
      this.setUserInfoButtonEnabled(true);
      this.setInfoBoard(false);
    },
    async getMessages() {
        try {
          const response = await getMessage();
          console.log('获取信息响应', response);
          if(response.ret==='success'){
            this.messages=response.data.message_list;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
    },
    async checkall() {
        try {
          const response = await checkAll();
          console.log('已读信息响应', response);
          if(response.ret==='success'){
            console.log(response.data);
            this.messages.forEach(message => {
              message.checked = 1;
            });
          }
        } catch (error) {
          console.error('错误:', error);
        }
    },
    async checkMessage(id) {
        try {
          const response = await checkMessage(id);
          console.log('已读信息响应', response);
          if(response.ret==='success'){
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
    },
    clickMess(id,type,checked,inviter){
      if(checked==0){
        this.checkMessage(id);
        const clickedMessage = this.messages.find(message => message.message_id === id);
        if (clickedMessage) {
          clickedMessage.checked = 1;
        }
      }
      if(type==4&&inviter!=this.name){
          this.setInviter(inviter);
          this.setAcceptInvite(true);
          this.setInfoBoard(false);
        }
      if(type==3){
        this.$router.push("/ManageTeam");
      }
    },
    clear(){
      this.messages=[];
    },
    fil(name){
      if(this.name==name){
        return true;
      }
      return false;
    },
    mess(type,message){
      if(type==5){
        return "您被踢出了"+message;
      }
      return message;
    }
  },
};
</script>

<style scoped>
.message-list {
  margin-top:-290px;
  margin-left:400px;
  position: absolute;
  width: 500px;
  height: 400px;
  justify-content: center;
  align-items: center;
  background-color: #1e1e1e;
  padding: 20px;
  border-style: solid;
  border-radius: 5px;
  border-color:white;
  border-width: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  color:white;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

.message-item {
  background-color: grey;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #ccc;
  cursor: pointer;
}

.message-item:hover{
  border-color: red;
}
.message-origin {
  font-weight: bold;
}

.message-text {
  margin-top: 5px;
}

.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
.scrollable-container {
  max-height: 280px; 
  overflow-y: auto; 
}
.btn{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 110px;
    height: 30px;
    border-radius: 5px;
    cursor: pointer;
  }

  .btn1{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 50px;
    height: 30px;
    border-radius: 5px;
    cursor: pointer;
  }
  .btn:hover{
    background-color: grey;
  }

  .btn1:hover{
    background-color: grey;
  }

  .btnSet{
    position: absolute;
    right: 20px;
  }

  .sign{
    width: 8px;
    height: 8px;
    position: relative;
    top: 5px;
    left: 10px;
    background-color: red;
    border-radius: 50%;
  }
</style>
