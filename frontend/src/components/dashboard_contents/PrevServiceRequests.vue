<template>
  <div class="service-requests-container">
    <h1>Previous Service Requests</h1>

    <div v-if="serviceRequests.length > 0" class="table-container">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Details</th>
            <th>Professional ID</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="serviceRequest in serviceRequests.slice(-3)" :key="serviceRequest.id">
            <td>{{ serviceRequest.date_created }}</td>
            <td>{{ serviceRequest.additional_details }}</td>
            <td>{{ serviceRequest.professional_id }}</td>
            <td :class="getStatusClass(serviceRequest.status)"> {{ serviceRequest.status }} </td>
            <td>
              <button v-if="serviceRequest.status === 'Pending'" @click="concludeRequest(serviceRequest.id)">
                Conclude
              </button>
              <button v-if="serviceRequest.status === 'Finished'" @click="openReviewModal(serviceRequest.professional_id)">
                Give Review
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <p>No previous service requests found.</p>
    </div>

    <!-- Review Modal -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Give Review</h2>
        <label for="rating">Rating (1-5):</label>
        <input type="number" id="rating" v-model="reviewData.rating" min="1" max="5" />

        <label for="review">Review:</label>
        <textarea id="review" v-model="reviewData.review"></textarea>

        <button @click="submitReview">Submit</button>
        <button @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ServiceRequests",
  data() {
    return {
      serviceRequests: [],
      showModal: false,
      reviewData: {
        professional_id: null,
        rating: "",
        review: "",
      }
    };
  },
  methods: {
    getStatusClass(status) {
      switch (status) {
        case "Pending":
          return "status-pending";
        case "Concluded":
          return "status-concluded";
        case "Finished":
          return "status-finished";
        case "Rejected":
          return "status-rejected";
        case "Abandoned":
          return "status-abandoned";
        default:
          return "status-default";
      }
    },
    async fetchServiceRequests() {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          console.error("Missing token");
          return;
        }

        const response = await axios.get("http://127.0.0.1:5000/past-service-requests-customers", {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (Array.isArray(response.data)) {
          this.serviceRequests = response.data;
        } else {
          console.error("Unexpected API response format:", response.data);
          this.serviceRequests = [];
        }
      } catch (error) {
        console.error("Error fetching service requests:", error);
      }
    },
    async concludeRequest(requestId) {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          console.error("Missing token");
          return;
        }

        const response = await axios.post(`http://127.0.0.1:5000/conclude-request/${requestId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        console.log(response.data);
        alert("Request has been concluded!");
        await this.fetchServiceRequests();
      } catch (error) {
        console.error("Error concluding request:", error);
        alert("Failed to conclude request.");
      }
    },
    openReviewModal(professionalId) {
      this.reviewData.professional_id = professionalId;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.reviewData = { professional_id: null, rating: "", review: "" };
    },
    async submitReview() {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          console.error("Missing token");
          return;
        }

        const response = await axios.post("http://127.0.0.1:5000/submit-review", this.reviewData, {
          headers: { Authorization: `Bearer ${token}` }
        });

        console.log(response.data);
        alert("Review submitted successfully!");
        this.closeModal();
      } catch (error) {
        console.error("Error submitting review:", error);
        alert("Failed to submit review.");
      }
    }
  },
  async created() {
    await this.fetchServiceRequests();
  }
};
</script>

<style scoped>
.service-requests-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  text-align: center;
}

.table-container {
  max-height: 150px; /* Allows scrolling */
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 5px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f8f8;
  position: sticky;
  top: 0;
  z-index: 1;
}

tbody tr:hover {
  background-color: #f1f1f1;
}

/* Status Colors */
.status-pending { color: #ff9800; font-weight: bold; }
.status-concluded { color: #2196F3; font-weight: bold; }
.status-finished { color: #4caf50; font-weight: bold; }
.status-rejected, .status-abandoned { color: #f44336; font-weight: bold; }
.status-default { color: #525252; }

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

button {
  margin: 10px;
  padding: 8px;
  cursor: pointer;
}
</style>
