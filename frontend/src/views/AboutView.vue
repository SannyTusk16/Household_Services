<template>
    <div class="home">
      <div class="home-header" style="display: flex; flex-direction: row; gap: 40px;">
        <h2 style="flex: 10;">Household Services</h2>
        <h3 style="flex: 1;">{{ username }}</h3>
        <router-link to="/login">
          <button class="logout-btn">Logout</button>
        </router-link>
      </div>
  
      <h1>{{ service_name }}</h1>
  
      <!-- Include the SearchProfessional component -->
      <SearchProfessional v-if="service_id" />
      <ProfessionalsByService />
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import SearchProfessional from "@/components/SearchProfessional.vue";
  import ProfessionalsByService from "@/components/ProfessionalsByService.vue";
  
  export default {
    components: {
      SearchProfessional,
        ProfessionalsByService,
    },
    data() {
      return {
        username: "Loading...",
        currentRole: null, // Initially null to prevent undesired rendering
        service_id: localStorage.getItem("service_id"),
        service_name: "Loading...",
        service_description: "Loading...",
      };
    },
    async created() {
      await this.fetchUserRole();
      await this.getUserName();
      await this.getServiceDetails();
    },
    methods: {
      async getUserName() {
        try {
          const token = localStorage.getItem("token");
          const user_id = localStorage.getItem("user_id");
          const response = await axios.get(`http://127.0.0.1:5000/get_user_name/${user_id}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          console.log("Fetched User Name from API:", response.data.username);
          this.username = response.data.username;
        } catch (error) {
          console.error("Error fetching user name:", error);
        }
      },
      async getServiceDetails() {
        try {
          const service_id = localStorage.getItem("service_id");
          const response = await axios.get(`http://127.0.0.1:5000/get_service/${service_id}`);
          console.log("Fetched Service Details from API:", JSON.stringify(response.data));
          this.service_name = response.data.service_name;
          this.service_description = response.data.service_description;
        } catch (error) {
          console.error("Error fetching service details:", error);
        }
      },
      async logout() {
      try {
        console.log("Logging out...");
        localStorage.clear();
        sessionStorage.clear();
        this.$router.push("/"); // Redirect to login
      } catch (error) {
        console.error("Logout error:", error);
      }
    },
      async fetchUserRole() {
        const token = localStorage.getItem("token");
        if (!token) {
          console.log("No token found, redirecting to login...");
          this.$router.push("/login");
          return;
        }
  
        try {
          const response = await axios.get("http://127.0.0.1:5000/current_user", {
            headers: { Authorization: `Bearer ${token}` },
          });
          localStorage.setItem("user_id", response.data.user_id);
  
          if (response.data && response.data.role) {
            console.log("Fetched Role from API:", response.data.role);
            this.currentRole = response.data.role;
            localStorage.setItem("role", this.currentRole);
          } else {
            throw new Error("Invalid role data received");
          }
        } catch (error) {
          console.error("Error fetching user role:", error);
          localStorage.removeItem("token"); // Clear token on failure
          localStorage.removeItem("role"); // Clear role too
          this.$router.push("/login");
        }
      },
    },
  };
  </script>
  <style scoped>
  .logout-btn {
  background-color: #f44336;
  color: white;
  width: 90px;
  height: 40px;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>