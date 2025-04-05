<template>
  <div class="login-container">
    <h3>Login</h3>
    <div class="input-group">
      <label for="user_id">User ID</label>
      <input v-model="user_id" type="text" id="user_id" required />
    </div>

    <div class="input-group">
      <label for="password">Password</label>
      <input v-model="password" type="password" id="password" required />
    </div>

    <button @click="login" class="login-btn">Login</button>
    <router-link to="/register">
      <button class="register-btn">Register</button>
    </router-link>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      user_id: "",
      password: "",
    };
  },
  methods: {
  async login() {
    try {
      const response = await axios.post("http://127.0.0.1:5000/login", {
        user_id: this.user_id,
        password: this.password,
      });

      if (response.data.access_token) {
        const token = response.data.access_token;

        // ✅ Store token in local storage
        localStorage.setItem("token", token);

        alert("Login successful!");
        console.log("Access Token:", token);

        // ✅ Redirect to home page
        this.$router.push("/home");
      }
    } catch (error) {
      console.error("Login Error:", error);
      alert("Invalid credentials. Please try again.");
      }
    },
  },
};
</script>


<style scoped>
.hello {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100vh;
  background-color: transparent;
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
