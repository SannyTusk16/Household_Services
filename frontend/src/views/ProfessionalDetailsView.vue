<template>
  <div class="professional-details">
    <h1>Professional Details</h1>

    <!-- Input field for additional details -->
    <textarea
      v-model="additionalDetails"
      placeholder="Enter additional details (optional)"
      rows="3"
      class="additional-details-input"
    ></textarea>

    <button 
      @click="sendServiceRequest"
      :disabled="disableRequestButton"
      class="send-request-btn"
    >
      {{ disableRequestButton ? "Professional is Busy" : "Send Service Request" }}
    </button>

    <div v-if="loading">Loading...</div>

    <div v-else>
      <div class="info-box">
        <h2>{{ professional.name }}</h2>
        <p><strong>ID:</strong> {{ professional.id }}</p>
        <p><strong>Email:</strong> {{ professional.email }}</p>
        <p><strong>Phone:</strong> {{ professional.phone }}</p>
        <p><strong>Address:</strong> {{ professional.address }}</p>
        <p><strong>Service Type:</strong> {{ professional.service_type }}</p>
      </div>

      <h2>Service Requests Handled</h2>
      <table v-if="serviceRequests.length">
        <thead>
          <tr>
            <th>Request ID</th>
            <th>Customer Name</th>
            <th>Service</th>
            <th>Status</th>
            <th>Date Created</th>
            <th>Date Completed</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.request_id">
            <td>{{ request.request_id }}</td>
            <td>{{ request.username || 'Loading...' }}</td>
            <td>{{ request.service_type }}</td>
            <td :class="getStatusClass(request.status)">{{ request.status }}</td>
            <td>{{ request.date_created }}</td>
            <td>{{ request.date_completed }}</td>
          </tr>
        </tbody>
      </table>  
      <p v-else>No service requests found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import api from "@/api";

export default {
  name: "ProfessionalDetails",
  data() {
    return {
      professional: {
        id: "",
        name: "Loading...",
        email: "",
        phone: "",
        address: "",
        service_type: "",
      },
      additionalDetails: "", // Added for additional details
      serviceRequests: [],
      loading: true,
      disableRequestButton: true,
    };
  },
  async created() {
    await this.fetchProfessionalDetails();
    await this.fetchServiceRequests();
    await this.checkProfessionalPending();
  },
  methods: {
    getStatusClass(status) {
      switch (status.toLowerCase()) {
        case "finished":
          return "status-finished"; // Green
        case "abandoned":
          return "status-abandoned"; // Red
        case "pending":
          return "status-pending"; // Yellow
        default:
          return "";
      }
    },
    async checkProfessionalPending() {
      try {
        const professional_id = this.$route.query.id || localStorage.getItem("professional_id");
        const response = await axios.get(`/api/check_professional_pending/${professional_id}`);
        const { professional_has_pending } = response.data;
        this.disableRequestButton = professional_has_pending;
      } catch (error) {
        console.error("Error checking professional's pending requests:", error);
        this.disableRequestButton = true;
      }
    },

    async sendServiceRequest() {
      try {
        const professional_id = this.$route.query.id || localStorage.getItem("professional_id");
        const user_id = localStorage.getItem("user_id");

        console.log("Sending request with:", { 
          professional_id, 
          user_id, 
          service_type: this.professional.service_type, 
          additional_details: this.additionalDetails 
        });

        if (!user_id || !this.professional.service_type) {
          alert("User ID or Service Type is missing!");
          return;
        }

        const response = await axios.post("/api/create_service_request", {
          professional_id,
          user_id,
          service_type: this.professional.service_type,
          additional_details: this.additionalDetails || "", // Ensure empty string if undefined
        });

        alert(response.data.message);
        this.additionalDetails = ""; // Reset after sending
      } catch (error) {
        console.error("Error sending service request:", error);
        alert(error.response?.data?.error || "Failed to send request");
      }
    },

    async fetchProfessionalDetails() {
      try {
        const professional_id = this.$route.query.id || localStorage.getItem("professional_id");

        if (!professional_id) {
          console.error("Professional ID is missing!");
          return;
        }

        const profResponse = await axios.get(`/api/get_professional/${professional_id}`);
        const professionalData = profResponse.data;

        const userResponse = await axios.get(`/api/get_user/${professionalData.user_id}`);
        const userData = userResponse.data;

        this.professional = {
          id: professionalData.user_id,
          name: userData.name,
          email: userData.email,
          phone: userData.phone,
          address: userData.address,
          service_type: professionalData.service_type,
        };
      } catch (error) {
        console.error("Error fetching professional details:", error);
      }
    },

    async fetchServiceRequests() {
      try {
        const professional_id = this.$route.query.id || localStorage.getItem("professional_id");
        const response = await axios.get(`/api/professional_service_request/${professional_id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        console.log("Service Requests:", JSON.stringify(response.data, null, 2));

        let requests = response.data.requests || [];

        for (let request of requests) {
          try { 
            console.log("Fetching customer name for ID", request.user_id);
            user_id = request.user_id;
            const customerResponse = await axios.get(`/api/get_user/${user_id}`);
            request.customer_name = customerResponse.data.name;
          } catch (error) {
            console.error(`Error fetching customer name for ID ${request.customer_id}:`, error);
            request.customer_name = "Unknown";
          }
        }

        this.serviceRequests = requests;
      } catch (error) {
        console.error("Error fetching service requests:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.professional-details {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

.info-box {
  background: #f8f8f8;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 10px;
}

th {
  background: #f0f0f0;
}

.status-finished {
  color: green;
  font-weight: bold;
}

.status-abandoned {
  color: red;
  font-weight: bold;
}

.status-pending {
  color: rgb(129, 129, 14);
  font-weight: bold;
}

/* Added styles for additional details input */
.additional-details-input {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: none;
}
</style>
