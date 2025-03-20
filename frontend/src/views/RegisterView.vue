<template>
    <div class="hello">
      <h2>HouseHold Services App</h2>
      <div class="empty"></div>
      <div class="form-container">
        <UserRegisterView v-if="currentView === 'register'" @switch-view="switchView" />
      </div>
    </div>
  </template>
  <script>
  import UserRegisterView from "@/components/UserRegisterView.vue";
  
  export default {
    name: "RegisterView",
    components: {
      UserRegisterView,
    },
    data() {
      return {
        currentView: "register", // Default view is 'register'
      };
    },
    methods: {
      switchView(view) {
        this.currentView = view;
      },
    },
  };
  </script>
  
  <style scoped>
  
  html, body {
    margin: 0;
    height: 100%;
  }
  .hello {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: transparent;
    min-height: 100vh;
    overflow: hidden;
  }
  
  .form-container {
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
    width: 100%;
    max-width: 400px;
    text-align: center;
  }
  
  h2 {
    font-size: 2em;
    margin-bottom: 20px;
    color: #333;
  }
  
  .input-group {
    margin-bottom: 15px;
    text-align: left;
  }
  
  .input-group label {
    display: block;
    font-size: 1em;
    color: #555;
    margin-bottom: 5px;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    font-size: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
  }
  
  .input-group input:focus {
    border-color: #42b983;
    outline: none;
  }
  
  .login-btn {
    width: 100%;
    padding: 12px;
    font-size: 1.2em;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .login-btn:hover {
    background-color: #379f72;
  }
  
  .register-btn {
    width: 100%;
    padding: 12px;
    font-size: 1.2em;
    background-color: #f2f2f2;
    color: #42b983;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s ease;
  }
  
  .register-btn:hover {
    background-color: #e0e0e0;
  }
  .empty {
    flex: 1;
  }
  </style>