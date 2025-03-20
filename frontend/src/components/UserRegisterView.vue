<template>
  <div class="hello">
    <div class="empty"></div>
    <div class="form-container">
      <h2>Register</h2>
      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <label>Email:</label>
          <input type="email" v-model="formData.email" required />
        </div>

        <div class="input-group">
          <label>Username:</label>
          <input type="text" v-model="formData.username" required />
        </div>

        <div class="input-group">
          <label>Address:</label>
          <input type="text" v-model="formData.address" required />
        </div>

        <div class="input-group">
          <label>Phone:</label>
          <input type="text" v-model="formData.phone" required />
        </div>

        <div class="input-group">
          <label>Password:</label>
          <input type="password" v-model="formData.password" required />
        </div>

        <div class="role-selection-bar">
          <button 
            type="button"
            class="role-option"
            :class="{ selected: formData.role === 'C' }"
            @click="formData.role = 'C'"
          >
            Customer
          </button>
          <button 
            type="button"
            class="role-option"
            :class="{ selected: formData.role === 'P' }"
            @click="formData.role = 'P'"
          >
            Service Professional
          </button>
        </div>

        <!-- Resume Upload (Only for Professionals) -->
        <div class="input-group" v-if="formData.role === 'P'">
          <label>Resume (PDF only):</label>
          <input type="file" @change="handleFileUpload" accept="application/pdf" />
        </div>

        <!-- Dropdown for Services (Only for Professionals) -->
        <div class="input-group" v-if="formData.role === 'P'">
          <label>Service Type:</label>
          <select v-model="formData.service_type" required>
            <option value="" disabled>Select a service</option>
            <option v-for="service in services" :key="service.id" :value="service.name">
              {{ service.name }}
            </option>
          </select>
        </div>

        <button type="submit" class="register-btn">Register</button>
      </form>
    </div>
    <div class="empty"></div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserRegisterView",
  data() {
    return {
      formData: {
        email: "",
        username: "",
        address: "",
        phone: "",
        password: "",
        role: "C",
        resume: null,
        service_type: "",
      },
      services: [], // Store services fetched from API
    };
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_all_services");
        this.services = response.data; // Store service list
      } catch (error) {
        console.error("Failed to fetch services:", error);
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file && file.type === "application/pdf") {
        this.formData.resume = file;
      } else {
        alert("Please upload a valid PDF file.");
        event.target.value = ""; // Reset file input
      }
    },
    async handleSubmit() {
      if (this.formData.role === "P" && !this.formData.resume) {
        alert("Please upload your resume.");
        return;
      }

      const formData = new FormData();
      formData.append("email", this.formData.email);
      formData.append("username", this.formData.username);
      formData.append("address", this.formData.address);
      formData.append("phone", this.formData.phone);
      formData.append("password", this.formData.password);
      formData.append("role", this.formData.role);
      formData.append("service_type", this.formData.service_type);
      formData.append("description", "hi there");

      if (this.formData.role === "P") {
        formData.append("resume", this.formData.resume);
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/register", formData);

        console.log("Response:", response.data);
        alert(response.data.message);
        this.$router.push("/"); // Navigate to login page after registration
      } catch (error) {
        console.error("Registration failed:", error);
        alert(error.response?.data?.message || "Registration failed.");
      }
    },
  },
  mounted() {
    this.fetchServices(); // Fetch services when the component loads
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

.input-group select {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.role-selection-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.role-option {
  padding: 10px;
  font-size: 1em;
  background-color: #f2f2f2;
  color: #42b983;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.role-option:hover {
  background-color: #e0e0e0;
}

.selected {
  background-color: #42b983;
  color: white;
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

.register-btn {
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

.register-btn:hover {
  background-color: #379f72;
}
</style>
