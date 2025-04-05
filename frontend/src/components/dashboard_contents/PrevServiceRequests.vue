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

        console.log("past services:",JSON.stringify(response.data, null, 2));
        

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
          alert("Error: Missing professional ID.");
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
  max-width: 700px;
  margin: auto;
  padding: 20px;
  text-align: center;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

/* Table Container */
.table-wrapper {
  max-height: 250px; /* Allows scrolling */
  overflow-y: auto;
  border-radius: 5px;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #42b983;
  color: white;
  position: relative;
  top: 0;
  z-index: 1;
}

tbody tr:hover {
  background-color: #f1f1f1;
}

/* Buttons */
.btn {
  padding: 8px 12px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.btn-conclude {
  background-color: #42b983;
  color: white;
}

.btn-review {
  background-color: #ffa500;
  color: white;
}

.btn:hover {
  opacity: 0.8;
}

/* Modal Styling */
/* Modal Overlay */
.modal-overlay {
  position: fixed; /* Ensure it stays in place */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050; /* Ensure it's above all UI elements */
}

/* Modal Content */
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 400px;
  max-width: 90%;
  z-index: 1051; /* Keep it above the overlay */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  position: relative;
}


.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.btn-submit {
  background-color: #42b983;
  color: white;
}

.btn-cancel {
  background-color: #ff4d4d;
  color: white;
}

/* No Requests */
.no-requests {
  color: #777;
  font-size: 16px;
  margin-top: 20px;
}
body.modal-open {
  overflow: hidden;
}

</style>
