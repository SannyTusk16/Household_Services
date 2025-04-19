<template>
  <div class="search-services">
    <h3>Search Services</h3>

    <!-- Search Input -->
    <input type="text" v-model="searchQuery" placeholder="Search for a service..." @input="debouncedFilterServices"/>

    <!-- Services List -->
    <div v-if="filteredServices.length">
      <ul>
        <li v-for="service in filteredServices" :key="service.id" @click="goToService(service.id)">
          <strong>{{ service.name }}</strong> - {{ service.description }} - ₹{{ service.price }}
        </li>
      </ul>
    </div>

    <div v-else>
      <p> -.- </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash"; // Import lodash for debouncing
import api from "@/api";

export default {
  name: "SearchServices",
  data() {
    return {
      searchQuery: "",
      services: [],
      filteredServices: [],
    };
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get("/api/get_all_services");
        console.log("API Response:", response.data);

        if (Array.isArray(response.data)) {
          this.services = response.data;
          this.filteredServices = []; // Ensure nothing is shown initially
          console.log("Services Loaded:", this.services);
        } else {
          console.error("Unexpected API response format:", response.data);
          this.services = [];
          this.filteredServices = [];
        }
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    filterServices() {
      const query = this.searchQuery.toLowerCase().trim();
      
      if (!query) {
        this.filteredServices = []; // Show nothing when input is empty
        return;
      }

      this.filteredServices = this.services.filter(service => 
        (service.name && service.name.toLowerCase().includes(query)) || 
        (service.description && service.description.toLowerCase().includes(query)) || 
        (service.price && service.price.toString().includes(query))
      );

      console.log("Filtered Services:", this.filteredServices);
    },
    goToService(serviceId) {
      this.$router.push({ path: `/about`, query: { id: serviceId } });
      localStorage.setItem("service_id", serviceId);
    },
    getImageUrl(serviceId) {
      return `/images/service-${serviceId}.jpg`; // Replace with your actual image logic
    }
  },
  mounted() {
    this.fetchServices();
    this.debouncedFilterServices = _.debounce(this.filterServices, 300);
  },
};
</script>

<style scoped>
.search-services {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  background: #f8f8f8;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 5px;
  cursor: pointer;
}

.service-img {
  width: 50px;
  height: 50px;
  margin-left: 10px;
  cursor: pointer;
}
</style>
