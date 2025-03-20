<template>
  <div class="hello">
    <h1>Welcome Admin</h1>
    <AllUsers /> 
    <AllServices />
  </div>
</template>

<script>
import axios from "axios";
import AllUsers from "./dashboard_contents/AllUsers.vue";
import AllServices from "./dashboard_contents/AllServices.vue";
export default {
  name: "HelloWorld",
  components: {
    AllUsers,
    AllServices,
  },
  props: {
    msg: String,
  },
  methods: {
    handleSubmit() {
      // handle login logic here
      console.log("Login form submitted");
    },
    goToRegister() {
      // Redirect to register page or show register form
      console.log("Go to register page");
    },
  },
};
</script>

<style scoped>
.hello {
  display: grid;
  place-items: center; /* Centers both horizontally & vertically */
  height: 100vh;
  background-color: transparent;
  grid-template-rows: 20px  400px; /* Two rows: one for the heading, one for the component */
  row-gap: 20px; /* Space between elements */
}

.form-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
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
