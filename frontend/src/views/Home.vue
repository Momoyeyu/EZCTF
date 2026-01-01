<template>
<div>
<Banner/>
<div class="wrap">
<Showquestion/>
<Notice/>
<ModifyUser v-if="modifyUser"/>
<DeleteUser v-if="deleteUser"/>
<InfoBoard v-if="infoBoard"/>
<NoTeam v-if="noTeam"/>
<CreateTeam v-if="createTeam"/>
<JoinTeam v-if="joinTeam"/>
<AcceptInvitation v-if="acceptInvite" />
</div>
</div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';
import Banner from '../components/Banner.vue';
import Showquestion from '../components/Showquestion.vue';
import Notice from '../components/Notice.vue';
import ModifyUser from '../components/ModifyUser.vue';
import DeleteUser from '../components/DeleteUser.vue';
import InfoBoard from '../components/InfoBoard.vue';
import NoTeam from '../components/NoTeam/NoTeam.vue';
import CreateTeam from '../components/NoTeam/CreateTeam.vue';
import JoinTeam from '../components/NoTeam/JoinTeam.vue';
import AcceptInvitation from '../components/AcceptInvitation.vue';
export default {
name:'Ranking',
components:{Banner,Showquestion,Notice,ModifyUser,DeleteUser,InfoBoard,NoTeam,CreateTeam,JoinTeam,AcceptInvitation},
computed: {
    ...mapState(['modifyUser','deleteUser','infoBoard','noTeam','createTeam','joinTeam','acceptInvite']),
},
methods: {
  ...mapMutations(['setModifyUser','setDeleteUser','setInfoBoard','setNoTeam','setCreateTeam','setJoinTeam','setAcceptInvite']),
}
}
</script>

<style>
.wrap{
  width: 1300px;
  margin: 0 auto;
}
</style>