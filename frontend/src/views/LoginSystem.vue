<template>
    <div id="bkg">
        <Login v-if="log"/>
        <Registration v-if="reg"/>
        <ForgetPassword v-if="FoPa"/>
    </div>
</template>
<script>
import { mapState, mapMutations } from 'vuex';
import Registration from '@/components/Registration.vue';
import Login from '@/components/Login.vue';
import ForgetPassword from '@/components/ForgetPassword.vue';
export default {
    components: { Registration,Login,ForgetPassword },
    computed: {
    ...mapState(['log','reg','FoPa',]),
    },
    methods: {
    ...mapMutations(['setLog','setReg','setFoPa',]),
    }
}
</script>
    
<style>
#bkg{
height:87vh;
width: 1600px;
margin: 0 auto;
background-image:url("../assets/背景.png");
background-size:cover;
display: flex;  
justify-content: center;  
align-items: center; 
}
</style>