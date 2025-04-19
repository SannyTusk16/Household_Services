  <template>
    <div class="dashboard-blueprint">
      <div class="dashboard-content">
        <h3>All Services</h3>
        <div v-if="loading">Loading...</div>
        <div v-else-if="error" class="error-message">{{ error }}</div>
        <div v-else class="services-container">
          <ServiceComponent
            v-for="service in services"
            :key="service.id"
            :description="service.description"
            :serviceId="service.id"
            :name="service.name"
            :price="service.price"
          />

        </div>
      </div>
    </div>
  </template>

  <script>
  import axios from "axios";
  import ServiceComponent from "@/components/dashboard_contents/ServiceComponent.vue";
  import api from "@/api";

  export default {
    name: "DashboardBlueprint",
    components: {
      ServiceComponent,
    },
    data() {
      return {
        services: [],
        loading: true,
        error: null,
      };
    },
    methods: {
      async fetchServices() {
        try {
          const response = await axios.get("/api/get_all_services");
          this.services = response.data;
          console.log("Services:", JSON.stringify(this.services, null, 2));
        } catch (error) {
          console.error("Error fetching services:", error);
          this.error = "Failed to load services.";
        } finally {
          this.loading = false;
        }
      },
      goToService(serviceId) {
        this.$router.push({ path: "/about", query: { id: serviceId } });
      },
    },
    mounted() {
      this.fetchServices();
    },
  };
  </script>

  <style scoped>
  .dashboard-blueprint {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .services-container {
    display: flex;
    flex-direction: row;
    gap: 20px;
    flex-wrap: wrap;
  }

  .error-message {
    color: red;
    font-weight: bold;
  }
  </style>
