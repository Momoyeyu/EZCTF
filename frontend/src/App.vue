<template>
  <div id="app">
      <Navigation/>
      <div class="main-content">
        <router-view/>
      </div>
  </div>
  </template>
  <script>
  import Navigation from './components/Navigation.vue'
  export default {
    components: { Navigation },
    name:'App'
  }
  </script>
  
  <style>
  body {
    background-color: #0d1117; /* Darker GitHub theme */
    color: #c9d1d9;
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  }
  #app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  .main-content {
    flex: 1;
    padding: 20px;
  }
  
  /* Element UI Dark Mode Overrides (Basic) */
  .el-card {
    background-color: #161b22;
    border-color: #30363d;
    color: #c9d1d9;
  }
  .el-card__header {
    border-bottom-color: #30363d;
  }
  .el-input__inner {
    background-color: #0d1117;
    border-color: #30363d;
    color: #c9d1d9;
  }
  .el-button--primary {
    background-color: #238636;
    border-color: #238636;
  }
  .el-button--primary:hover {
    background-color: #2ea043;
    border-color: #2ea043;
  }
  .el-menu {
    background-color: #161b22;
    border-bottom-color: #30363d !important;
  }
  .el-menu--horizontal>.el-menu-item {
    color: #c9d1d9;
  }
  .el-menu--horizontal>.el-menu-item:hover, .el-menu--horizontal>.el-menu-item:focus {
    background-color: #0d1117 !important;
    color: #58a6ff !important;
  }
  .el-menu--horizontal>.el-menu-item.is-active {
    border-bottom-color: #f78166 !important;
    color: #c9d1d9 !important;
  }
  </style>
  