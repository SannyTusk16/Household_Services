<template>
    <div class="all-professionals">
      <h3>All Professionals</h3>
  
      <div v-if="professionals.length">
        <ul>
          <li v-for="professional in professionals" :key="professional.id" @click="goToProfessional(professional.id)">
            <strong>{{ professional.name }}</strong> - {{ professional.description }} - ₹{{ professional.price }}
            <img :src="getImageUrl(professional.id)" alt="Professional Image" class="professional-img" />
          </li>
        </ul>
      </div>
  
      <div v-else>
        <p>Loading professionals...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import api from "@/api";
  
  export default {
    name: "AllProfessionals",
    data() {
      return {
        professionals: [],
      };
    },
    async created() {
      await this.fetchProfessionals();
    },
    methods: {
      async fetchProfessionals() {
        try {
          const response = await axios.get("/api/get_all_professionals");
          console.log("API Response:", response.data);

          if (Array.isArray(response.data)) {
            console.log("First Professional Object:", response.data[0]); // Debugging
            this.professionals = response.data;
          } else {
            console.error("Unexpected API response format:", response.data);
            this.professionals = [];
          }
        } catch (error) {
          console.error("Error fetching professionals:", error);
        }
      },
      goToProfessional(professionalId) {
        console.log("Navigating to professional:", professionalId); // Debugging

        if (!professionalId) {
          console.error("Error: professionalId is null or undefined!");
          return;
        }

        this.$router.push({ path: `/professionalDetails`, query: { id: professionalId } });
        localStorage.setItem("professional_id", professionalId);
      },
      getImageUrl(professionalId) {
        return `/images/professional-${professionalId}.jpg`; // Adjust image path based on your storage setup
      },
    },
  };
  </script>
  
  <style scoped>
  .all-professionals {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    text-align: center;
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
  