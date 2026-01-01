<template>
    <div id="noTeam">
        <button @click="close()" class="close-btn">&#10006;</button>
      <h1>选择战队</h1>
      <div>
        <button @click="CreateTeam()" class="btn">创建战队</button> |
        <button @click="JoinTeam()" class="btn">加入战队</button>
      </div>
    </div>
</template>

<script>
    import { mapState, mapMutations } from 'vuex';
    export default {
        computed: {
            ...mapState(['userInfoButtonEnabled','noTeam','createTeam','joinTeam',]),
        },
        methods: {
            ...mapMutations(['setUserInfoButtonEnabled','setNoTeam','setCreateTeam','setJoinTeam',]),
            close() {
                this.setUserInfoButtonEnabled(true);
                this.setNoTeam(false);
            },
            CreateTeam(){
                this.setNoTeam(false);
                this.setCreateTeam(true);
            },
            JoinTeam(){
                this.setNoTeam(false);
                this.setJoinTeam(true);
            }
        }
    };

</script>

<style>
#noTeam {
    margin-top:-200px;
    margin-left:520px;
    position: absolute;
    top: auto;
    left: auto;
    width: 250px;
    height: 120px;
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
}

.btn{
    border: none;
    outline: none;
    box-shadow: none;
    background-color: #1e1e1e;
    color: white;
    width: 100px;
    height: 20px;
    border-radius: 5px;
    cursor: pointer;
}

.btn:hover{
    background-color: grey;
}

.close-btn {
    text-decoration: none;
    color:white;
    position: absolute;
    top: 10px;
    right: 10px;
    cursor: pointer;
}
</style>
