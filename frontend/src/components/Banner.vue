<template>
      <div class="banner">
        <div class="wrap">
            <div class="banner-box"></div>
        </div>
    </div>
</template>

<script>
export default {
name:'Banner',
}
</script>

<style>
.banner{
  width: 100%;
  margin-bottom: 5px;
}
.banner-box{
  width: 1200px;
  height: 400px;
  margin: 10px auto;
  background-image: url('../assets/1.png');
  background-size: 100%;
  animation: banner 6s linear infinite;
  border: 2px solid #161b22;
  border-radius: 5px;
} 
.banner-box:hover{
  animation-play-state: paused;
}
</style>