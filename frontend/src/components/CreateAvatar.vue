<template>
    <div class="avatar">
      <div class="avatar-circle">
        {{ getInitials }}
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      username: String,
    },
    computed: {
      getInitials() {
        if (this.username) {
          const names = this.username.split(' ');
          return names
            .map((name) => name.charAt(0))
            .slice(0, 2)
            .join('')
            .toUpperCase();
        } else {
          return 'U'; 
        }
      },
    },
  };
  </script>
  
  <style>
  .avatar {
    display: inline-block;
    position: relative;
  }
  
  .avatar-circle {
    width: 50px;
    height: 50px;
    border-radius: 50px;
    background-color: #3498db;
    color: white;
    font-size: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
</style>
  