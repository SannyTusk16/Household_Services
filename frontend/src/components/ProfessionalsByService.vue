<template>
  <div class="professionals-by-service">
    <h3>Professionals for {{ service_name }}</h3>

    <div v-if="loading">
      <p>Loading professionals...</p>
    </div>
    
    <div v-else-if="professionals.length">
      <table>
        <thead>
          <tr>
            <th>Professional Name</th>
            <th>Description</th>
            <th>Rating</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.professional_id">
            <td><strong>{{ professional.username }}</strong></td>
            <td>{{ professional.description }}</td>
            <td>⭐ {{ professional.rating ? Number(professional.rating).toFixed(2) : "N/A" }}</td>
            <td>
              <button @click="goToProfessional(professional.professional_id)">View</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <p>No professionals available for this service.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import api from "@/api";

export default {
  name: "ProfessionalsByService",
  data() {
    return {
      professionals: [],
      service_name: "Loading...",
      loading: true,
    };
  },
  async created() {
    await this.fetchServiceDetails();
    await this.fetchProfessionals();
  },
  methods: {
    async fetchServiceDetails() {
      try {
        const service_id = localStorage.getItem("service_id");
        const response = await axios.get(`/api/get_service/${service_id}`);
        this.service_name = response.data.service_name;
      } catch (error) {
        console.error("Error fetching service details:", error);
      }
    },
    async fetchProfessionals() {
      try {
        const service_id = localStorage.getItem("service_id");
        const response = await axios.get(`/api/get_service_professionals/${service_id}`);

        console.log("API Response:", response.data);  // Debugging

        if (Array.isArray(response.data.professionals)) {
          this.professionals = response.data.professionals.map(prof => ({
            ...prof,
            rating: prof.rating ? Number(prof.rating).toFixed(2) : null
          }));
        } else {
          console.error("Unexpected API response format:", response.data);
        }
      } catch (error) {
        console.error("Error fetching professionals:", error);
      } finally {
        this.loading = false;
      }
    },
    goToProfessional(professionalId) {
      console.log("Navigating to professional details:", professionalId);
      this.$router.push({ path: `/professionalDetails`, query: { id: professionalId } });
      localStorage.setItem("professional_id", professionalId);
    },
  },
};
</script>

<style scoped>
.professionals-by-service {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}
</style>
