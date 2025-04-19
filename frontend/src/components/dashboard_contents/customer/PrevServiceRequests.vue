<template>
  <div class="service-requests-container">
    <h1>Previous Service Requests</h1>

    <div v-if="serviceRequests.length > 0" class="table-wrapper">
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
              <button 
                v-if="serviceRequest.status === 'Pending' || serviceRequest.status === 'Accepted'"
                class="btn btn-conclude"
                @click="concludeRequest(serviceRequest.id)">
                Conclude
              </button>
              <button 
                v-if="serviceRequest.status === 'Finished' || serviceRequest.status === 'Abandoned'"
                class="btn btn-review"
                @click="openReviewModal(serviceRequest.professional_id)">
                Give Review
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-requests">
      <p>No previous service requests found.</p>
    </div>

    <!-- Review Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Give Review</h2>
        <label for="rating">Rating (1-5):</label>
        <input type="number" id="rating" v-model="reviewData.rating" min="1" max="5" />

        <label for="review">Review:</label>
        <textarea id="review" v-model="reviewData.review"></textarea>

        <div class="modal-actions">
          <button class="btn btn-submit" @click="submitReview">Submit</button>
          <button class="btn btn-cancel" @click="closeModal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
import api from "@/api";

export default {
  name: "ServiceRequests",
  data() {
    return {
      serviceRequests: [],
      showModal: false,
      loading:true,
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
      this.loading = true;
      try {
        const token = localStorage.getItem("token");
        if (!token) throw new Error("Missing token");

        const response = await axios.get("/api/past-service-requests-customers", {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.serviceRequests = Array.isArray(response.data) ? response.data : [];
      } catch (error) {
        console.error("Error fetching service requests:", error);
        this.$toast.error("Failed to fetch service requests.");
      } finally {
        this.loading = false;
      }
    },
    async concludeRequest(requestId) {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          console.error("Missing token");
          return;
        }

        const response = await axios.post(`/api/conclude-request/${requestId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        console.log(response.data);
        this.$toast.success("Request concluded successfully!");
        await this.fetchServiceRequests();
      } catch (error) {
        console.error("Error concluding request:", error);
        this.$toast.error("Failed to conclude request.");
      }
    },
    openReviewModal(professionalId) {
      this.reviewData.professional_id = professionalId;
      this.showModal = true;
      document.body.classList.add("modal-open"); // Prevent scrolling
    },

    closeModal() {
      this.showModal = false;
      document.body.classList.remove("modal-open"); // Re-enable scrolling
    },
    async submitReview() {
      try {
        const token = localStorage.getItem("token");

        if (!token) {
          console.error("Missing token");
          return;
        }

        if (!this.reviewData.professional_id) {
          console.error("Missing professional_id for review");
          this.$toast.error("Error: Missing professional ID.");
          return;
        }

        const response = await axios.post("/api/submit-review", this.reviewData, {
          headers: { Authorization: `Bearer ${token}` }
        });

        console.log(response.data);
        this.$toast.success("Review submitted successfully!");
        this.closeModal();
      } catch (error) {
        console.error("Error submitting review:", error);
        this.$toast.error("Failed to submit review.");
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
  max-width: 900px;
  margin: auto;
  padding: 30px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  margin-bottom: 24px;
  color: #2c502f;
  font-size: 28px;
  font-weight: 600;
}

/* Table */
.table-wrapper {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 15px;
}

th {
  background-color: #2c3e50;
  color: white;
  font-weight: 500;
  padding: 14px;
  position: sticky;
  top: 0;
  z-index: 1;
}

td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #eee;
  color: #555;
}

tbody tr:hover {
  background-color: #f9f9f9;
  transition: background 0.2s ease;
}

/* Status colors */
.status-pending {
  color: #f39c12;
  font-weight: 500;
}

.status-concluded {
  color: #16a085;
  font-weight: 500;
}

.status-finished {
  color: #2ecc71;
  font-weight: 500;
}

.status-rejected,
.status-abandoned {
  color: #e74c3c;
  font-weight: 500;
}

/* Buttons */
.btn {
  padding: 8px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease-in-out;
}

.btn-conclude {
  background-color: #2ecc71;
  color: white;
}

.btn-review {
  background-color: #f39c12;
  color: white;
}

.btn:hover {
  transform: translateY(-1px);
  opacity: 0.9;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 420px;
  max-width: 95%;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  text-align: left;
}

.modal-content h2 {
  margin-bottom: 18px;
  font-size: 22px;
  color: #333;
}

.modal-content label {
  font-weight: 500;
  margin-top: 10px;
  display: block;
  color: #444;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-top: 6px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-submit {
  background-color: #3498db;
  color: white;
}

.btn-cancel {
  background-color: #e74c3c;
  color: white;
}

body.modal-open {
  overflow: hidden;
}

/* No Requests */
.no-requests {
  color: #888;
  font-size: 17px;
  margin-top: 30px;
}
</style>
