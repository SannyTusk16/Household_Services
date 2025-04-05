<template>
  <div class="admin-dashboard">
    <h1>Welcome Admin</h1>

    <div class="dashboard-container">
      <div class="dashboard-section">
        <h2>All Users</h2>
        <div class="scrollable-content">
          <AllUsers />
        </div>
      </div>

      <div class="dashboard-section">
        <h2>All Services</h2>
        <div class="scrollable-content">
          <AllServices />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AllUsers from "./dashboard_contents/AllUsers.vue";
import AllServices from "./dashboard_contents/AllServices.vue";

export default {
  name: "AdminDashboard",
  components: {
    AllUsers,
    AllServices,
  },
};
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
  min-height: 100vh;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

.dashboard-container {
  display: flex;
  gap: 20px;
  width: 90%;
  max-width: 1200px;
  justify-content: center;
}

.dashboard-section {
  flex: 1;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  max-width: 50%;
  display: flex;
  flex-direction: column;
}

h2 {
  text-align: center;
  color: #42b983;
}

.scrollable-content {
  max-height: 400px; /* Prevents overflow */
  overflow-y: auto;
  padding: 10px;
  border-top: 2px solid #ddd;
}

@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
  }
  
  .dashboard-section {
    max-width: 100%;
  }
}
</style>
