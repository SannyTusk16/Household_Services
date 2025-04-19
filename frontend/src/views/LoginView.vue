<template>
  <div class="hello">
    <div class="titlediv">
      <img src="../assets/logo.png" alt="Logo" class="logo" style="width: 200px; height: 200px;" />
      <h1 class="title">HouseHold Services</h1>
      <p class="subtitle">Your one-stop solution for all household needs</p>
    </div>
    <div class="empty"></div>
    <div class="form-container">
      <UserLoginView v-if="currentView === 'login'" @switch-view="switchView" />
      <UserRegisterView v-if="currentView === 'register'" @switch-view="switchView" />
    </div>
  </div>
</template>
  <script>
  import UserLoginView from "@/components/UserLoginView.vue";
  import UserRegisterView from "@/components/UserRegisterView.vue";
  import api from "@/api";

  export default {
    name: "LoginView",
    components: {
      UserLoginView,
      UserRegisterView,
    },
    data() {
      return {
        currentView: "login", 
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
margin-left: 100px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color:transparent;
  min-height: 100vh;
  overflow: hidden;
}

.form-container {
  background-color: transparent;
  padding: 30px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.titlediv {
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
  top: 35%;
  left: 25%;
  position: absolute;
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