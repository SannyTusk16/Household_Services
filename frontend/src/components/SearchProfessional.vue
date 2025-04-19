<template>
  <div class="search-professionals">
    <h3>Search Professionals</h3>

    <!-- Search Input -->
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search for a professional..."
      @input="debouncedFilterProfessionals"
    />

    <!-- Professionals List -->
    <div v-if="filteredProfessionals.length">
      <ul>
        <li
          v-for="professional in filteredProfessionals"
          :key="professional.professional_id"
          @click="goToProfessional(professional.professional_id)"
        >
          <strong>{{ professional.username }}</strong> - 
          {{ professional.description }} - ₹{{ professional.price }}
          <img
            :src="getImageUrl(professional.professional_id)"
            alt="Professional Image"
            class="professional-img"
            @click.stop="goToProfessional(professional.professional_id)"
          />
        </li>
      </ul>
    </div>

    <div v-else>
      <p>Enter a valid query</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import _ from "lodash"; // Import lodash for debouncing
import api from "@/api";

export default {
  name: "SearchProfessionals",
  data() {
    return {
      searchQuery: "",
      professionals: [],
      filteredProfessionals: [],
      debouncedFilterProfessionals: null,
    };
  },
  methods: {
    async fetchProfessionals() {
      try {
        const service_id = localStorage.getItem("service_id");
        const response = await axios.get(
          `/api/get_service_professionals/${service_id}`
        );
        console.log("API Response:", JSON.stringify(response.data, null, 2));

        if (Array.isArray(response.data.professionals)) {
          this.professionals = response.data.professionals;
        } else {
          console.error("Unexpected API response format:", response.data);
          this.professionals = [];
        }
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    filterProfessionals() {
      const query = this.searchQuery.toLowerCase().trim();

      if (!query) {
        this.filteredProfessionals = []; // Show nothing if input is empty
        return;
      }

      this.filteredProfessionals = this.professionals.filter((professional) =>
        (professional.username &&
          professional.username.toLowerCase().includes(query)) ||
        (professional.description &&
          professional.description.toLowerCase().includes(query)) ||
        (professional.price && professional.price.toString().includes(query))
      );

      console.log("Filtered professionals:", this.filteredProfessionals);
    },
    goToProfessional(professionalId) {
      console.log("Navigating to professional:", professionalId);
      this.$router.push({ path: `/about`, query: { id: professionalId } });
      localStorage.setItem("professional_id", professionalId);
    },
    getImageUrl(professionalId) {
      return `/images/professional-${professionalId}.jpg`;
    },
  },
  mounted() {
    this.fetchProfessionals();
    this.debouncedFilterProfessionals = _.debounce(this.filterProfessionals, 300);
  },
};
</script>

<style scoped>
.search-professionals {
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

.professional-img {
  width: 50px;
  height: 50px;
  margin-left: 10px;
  cursor: pointer;
}
</style>
