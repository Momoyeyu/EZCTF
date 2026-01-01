<template>
  <div id="bkg">
    <DeleteTeam v-if="deleteTeam"/>
    <ChangeTeamname v-if="changeTeamname"/>
    <ChangeLeader v-if="changeLeader"/>
    <KickMember v-if="kickMember"/>
    <InviteMember v-if="inviteMember"/>
    <div id="manageTeam" v-if="manageTeam">
      <button @click="close()" class="close-btn">&#10006;</button>
      <h1>战队管理</h1>
      <p>
        战队名称：{{ teamInfo.name }}  &nbsp; 战队人数: {{ team.membernum }}/{{ team.maxnum }}
        <button @click="changeteaminfo()">修改名称</button>
      </p>
      <h2>战队成员</h2>
      <button @click="Invite()">邀请成员</button>
      <br><br>
      <div class="scrollable-table-container">
        <table class="three-column-table">
        <thead>
            <tr>
            <th>成员</th>
            <th>积分</th>
            <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="member in members" :key="member.username">
            <td>{{ member.username }}</td>
            <td>{{ member.score }}</td>
            <td>
                <button @click="changeTeamLeader(member.username)" v-if="checkLeader(member.username)">队长转让</button> &nbsp;
                <button @click="kickmember(member.username)" v-if="checkLeader(member.username)">移出战队</button>
            </td>
            </tr>
        </tbody>
        </table>
      </div>
      <br>
      <h2 v-if="team.check">申请列表</h2>
      <div class="scrollable-table-container">
        <table class="three-column-table" v-if="team.check">
        <thead>
            <tr>
            <th>申请</th>
            <th>积分</th>
            <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="applicant in applicants" :key="applicant.score">
            <td>{{ applicant.username }}</td>
            <td>{{ applicant.score }}</td>
            <td>
                <button @click="verify_apply(applicant.username,true)">通过</button> &nbsp;
                <button @click="verify_apply(applicant.username,false)">拒绝</button>
            </td>
            </tr>
        </tbody>
        </table>
      </div>
      <br><br>
      <button @click="delete_Team()">解散战队</button>
    </div>
  </div>
</template>
  
<script>
  import DeleteTeam from '@/components/DeleteTeam.vue'
  import ChangeTeamname from '@/components/ChangeTeamname.vue'
  import ChangeLeader from '@/components/ChangeLeader.vue'
  import KickMember from '@/components/KickMember.vue'
  import InviteMember from '@/components/InviteMember.vue'
  import { mapState, mapMutations } from 'vuex';
  import { teamDetail,verifyApply } from '@/UserSystemApi/TeamApi';
  import { getApply } from '@/UserSystemApi/MessageApi';
  export default {
    components:{DeleteTeam,ChangeTeamname,ChangeLeader,KickMember,InviteMember},
    data() {
      return {
        members: [
          { username: "-", score: "-" },
        ],
        applicants: [
          { name: "-", score: "-" },
        ],
        team: {
          membernum: '',
          maxnum: '10',
          check: true,
        },
      };
    },
    computed: {
    ...mapState(['userInfoButtonEnabled','username','teamname','isLeader','isMember','deleteTeam','changeTeamname','manageTeam','newLeader','changeLeader','kickMember','kMember','inviteMember']),
    teamInfo() {
      return{
          leader_name: this.$store.state.username,
          name: this.$store.state.teamname,
      }
    },
    },
    mounted() {
      this.team_detail(this.teamInfo.name);
      this.get_apply();
    },
    methods: {
      ...mapMutations(['setUserInfoButtonEnabled','setUsername','setTeamname','setIsLeader','setIsMember','setDeleteTeam','setChangeTeamname','setManageTeam','setNewLeader','setChangeLeader','setKMember','setKickMember','setInviteMember']),
      close() {
        this.setUserInfoButtonEnabled(true);
        localStorage.setItem('UBE',true);
        this.$router.push('/');
      },
      delete_Team(){
        this.setDeleteTeam(true);
        this.setManageTeam(false);
      },
      changeTeamLeader(name){
        this.setChangeLeader(true);
        this.setManageTeam(false);
        this.setNewLeader(name);
      },
      changeteaminfo(){
        this.setChangeTeamname(true);
        this.setManageTeam(false);
      },
      kickmember(name) {
        this.setKickMember(true);
        this.setManageTeam(false);
        this.setKMember(name);
      },
      invite_member(){
        this.setInviteMember(true);
        this.setManageTeam(false);
      },
      Invite(){
        this.setManageTeam(false);
        this.setInviteMember(true);
      },
      async team_detail(name) {
        try {
          const response = await teamDetail(name);
          console.log('获取用户列表响应', response);
          if(response.ret==='success'){
            this.members=response.data.members;
            this.team.membernum=response.data.team_member;
            console.log(response.data);
          }
        } catch (error) {
          console.error('错误:', error);
        }
      },
      async verify_apply(name,state) {
        try {
          const response = await verifyApply(name,state);
          console.log('通过审核响应', response);
          if(response.ret==='success'){
            alert(response.msg);
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('错误:', error);
        }
      },
      async get_apply() {
        try {
          const response = await getApply();
          console.log('获取申请列表响应', response);
          if(response.ret==='success'){
            this.applicants=response.data.applicant_list;
          }
        } catch (error) {
          alert(error.response.data.msg);
          console.error('错误:', error);
        }
      },
      checkLeader(name){
        if(name==this.teamInfo.leader_name){
          return false;
        }
        return true;
      }
    },
  };
</script>

<style>
#bkg{
height:87vh;
background-image:url("../assets/背景.png");
background-size:cover;
}
#manageTeam {
    top: auto;
    left: auto;
    position: absolute;
    width: 800px;
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
    z-index: 2;
}
.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
.scrollable-table-container {
  max-height: 160px; 
  overflow-y: auto; 
}
.three-column-table {
  width: 60%;
  margin-left: 20%;
}

.three-column-table th,
.three-column-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.three-column-table th:first-child,
.three-column-table td:first-child {
  text-align: center;
}

</style>
  