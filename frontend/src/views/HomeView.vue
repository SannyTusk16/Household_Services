<template>
  <div class="home">
    <div class="home-header">
      <h2>Household Services</h2>
      <h3 class="username">{{ username }}</h3>
      <button @click="logout" class="logout-btn">Logout</button>
    </div>

    <div v-if="currentRole !== null"> 
      <ServiceRequests v-if="currentRole === 'P'" />
      <SearchServices v-if="currentRole === 'C'" />
      <PrevServiceRequests v-if="currentRole === 'C'" />
      <DashboardBlueprint v-if="currentRole === 'C'" />
      <HelloWorld v-if="currentRole === 'A'" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ServiceRequests from "@/components/dashboard_contents/ProfessionalServiceRequests.vue";
import SearchServices from "@/components/dashboard_contents/SearchServices.vue";
import DashboardBlueprint from "@/components/dashboard_contents/DashboardBlueprint.vue";
import HelloWorld from "@/components/HelloWorld.vue";
import PrevServiceRequests from "@/components/dashboard_contents/PrevServiceRequests.vue";

export default {
  components: {
    ServiceRequests,
    SearchServices,
    DashboardBlueprint,
    HelloWorld,
    PrevServiceRequests,
    
  },
  data() {
    return {
      username: "Loading...",
      currentRole: null,
    };
  },
  async created() {
    await this.fetchUserRole(); // Ensure `user_id` is set
    await this.getUserName();   // Now it's safe to fetch username
  },
  methods: {
    async getUserName() {
      try {
        const token = localStorage.getItem("token");
        const user_id = localStorage.getItem("user_id");

        if (!user_id) {
          console.error("No user_id found in localStorage!");
          return;
        }

        const response = await axios.get(`http://127.0.0.1:5000/get_user_name/${user_id}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        console.log("Fetched User Name:", response.data.username);
        this.username = response.data.username;
      } catch (error) {
        console.error("Error fetching user name:", error);
        this.username = "Unknown";
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
        console.log("No token found, redirecting...");
        this.$router.push("/login");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:5000/current_user", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.data && response.data.role) {
          console.log("User Role:", response.data.role);

          this.currentRole = response.data.role;
          localStorage.setItem("role", this.currentRole);
          localStorage.setItem("user_id", response.data.user_id); // Ensure user_id is stored
        } else {
          throw new Error("Invalid role data received");
        }
      } catch (error) {
        console.error("Error fetching role:", error);
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        this.$router.push("/login");
      }
    },
  },
};
</script>

<style scoped>
.home-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 10px 20px;
}

.username {
  flex: 2;
  color: green;
  text-align: right;
}

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

@media (max-width: 768px) {
  .home-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .username {
    text-align: left;
    flex: unset;
  }
}
</style>
