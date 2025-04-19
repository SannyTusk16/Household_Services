<template>
  <div class="login-container">
    <h2>Login</h2>
    <div class="input-group">
      <label for="mail_id">Mail ID</label>
      <input v-model="mail_id" type="text" id="mail_id" required />
    </div>

    <div class="input-group">
      <label for="password">Password</label>
      <input v-model="password" type="password" id="password" required />
    </div>

    <button @click="login" class="login-btn">Login</button>
    <button class="register-btn" @click="$emit('switch-view', 'register')">
      Register
    </button>

    <div class="recaptcha-container">
      <vue-recaptcha
        ref="recaptcha"
        sitekey="6Lc1lAsrAAAAAPz9TfqUGQMogpi-WDtOK7tVTjpX"
        @verify="onCaptchaVerified"
        @expired="onCaptchaExpired"
      ></vue-recaptcha>
    </div>
  </div>
</template>

<script>
import VueRecaptcha from 'vue-recaptcha';
import axios from 'axios';

export default {
  components: {
    'vue-recaptcha': VueRecaptcha,
  },
  data() {
    return {
      mail_id: "",
      password: '',
      recaptchaToken: null,
    };
  },
  methods: {
    onCaptchaVerified(response) {
      this.recaptchaToken = response;
    },
    onCaptchaExpired() {
      this.recaptchaToken = null;
    },
    async login() {
      if (!this.recaptchaToken) {
        alert('Please complete the CAPTCHA.');
        return;
      }

      try {
        const response = await axios.post('/api/login', {
          mail_id: this.mail_id,
          password: this.password,
          recaptcha_token: this.recaptchaToken,
        });

        if (response.data.access_token) {
          const token = response.data.access_token;
          localStorage.setItem('token', token);
          alert('Login successful!');
          this.$router.push('/home');
        }
      } catch (error) {
        console.error('Login Error:', error);
        alert('Invalid credentials or failed CAPTCHA. Please try again.');
        this.$refs.recaptcha.reset();
        this.recaptchaToken = null;
      }
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
  height: 100vh;
  background-color: transparent;
}

.form-container {
  background-color: transparent;
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
.recaptcha-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

</style>
