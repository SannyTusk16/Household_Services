<template>
  <div>
    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 10px;">
      <h1> Current Request Being Handled</h1>
      <!-- Table Header -->
      <div style="display: flex; flex-direction: row; font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 5px;">
        <div style="flex: 1;">Service Request ID</div>
        <div style="flex: 1;">Service Name</div>
        <div style="flex: 1;">Service Date</div>
        <div style="flex: 1;">Service Time</div>
        <div style="flex: 1;">Actions</div>

      </div>
      <!-- Loading Indicator -->
      <div v-if="loading" style="display: flex; justify-content: center;">
        <p>Loading...</p>
      </div>

      <!-- No Requests Message -->
      <div v-else-if="acceptedServiceRequests.length == 0" style="text-align: center;">
        <p>No Request Being Handled At The Moment</p>
      </div>
      <!-- Service Requests List -->
       
      <div v-if="acceptedServiceRequests.length!==0" v-for="request in acceptedServiceRequests" :key="request.request_id" 
           style="display: flex; flex-direction: row; border-bottom: 1px solid #ccc; padding: 5px;">
        <div style="flex: 1;">{{ request.request_id }}</div>
        <div style="flex: 1;">{{ request.service_type }}</div>
        <div style="flex: 1;"> {{ formatDate(request.date_created) }} </div>
        <div style="flex: 1;"> {{ formatTime(request.date_created) }} </div>
        <div style="flex: 1; display: flex; gap: 10px;">
          <button 
            @click="finishRequest(request.request_id)" 
            :disabled="request.status.toLowerCase().trim() !== 'concluded'"
            style="background-color: green; color: white; border: none; padding: 5px; cursor: pointer;"
            :style="{ opacity: request.status.toLowerCase().trim() !== 'concluded' ? 0.5 : 1, cursor: request.status.toLowerCase().trim() !== 'concluded' ? 'not-allowed' : 'pointer' }"
          >
            Finish
          </button>

          <button 
            @click="abandonRequest(request.request_id)" 
            :disabled="request.status.toLowerCase().trim() !== 'concluded'"
            style="background-color: red; color: white; border: none; padding: 5px; cursor: pointer;"
            :style="{ opacity: request.status.toLowerCase().trim() !== 'concluded' ? 0.5 : 1, cursor: request.status.toLowerCase().trim() !== 'concluded' ? 'not-allowed' : 'pointer' }"
          >
            Abandon
          </button>
        </div>
      </div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 80px;"> 
      <h1> Service Requests </h1>
    <div style="display: flex; flex-direction: column; gap: 10px;">
      <!-- Table Header -->
      <div style="display: flex; flex-direction: row; font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 5px;">
        <div style="flex: 1;">Service Request ID</div>
        <div style="flex: 1;">Service Name</div>
        <div style="flex: 1;">Service Date</div>
        <div style="flex: 1;">Service Time</div>
        <div style="flex: 1;">Status</div>
        <div style="flex: 1;">Actions</div>
      </div>
      <!-- Loading Indicator -->
      <div v-if="loading" style="display: flex; justify-content: center;">
        <p>Loading...</p>
      </div>

      <!-- No Requests Message -->
      <div v-else-if="serviceRequests.length == 0" style="text-align: center;">
        <p>No pending service requests.</p>
      </div>
      <!-- Service Requests List -->
      <div v-if="serviceRequests.length!==0" v-for="request in serviceRequests" :key="request.request_id" 
           style="display: flex; flex-direction: row; border-bottom: 1px solid #ccc; padding: 5px;">
        <div style="flex: 1;">{{ request.request_id }}</div>
        <div style="flex: 1;">{{ request.service_type }}</div>
        <div style="flex: 1;"> {{ formatDate(request.date_created) }} </div>
        <div style="flex: 1;"> {{ formatTime(request.date_created) }} </div>
        <div style="flex: 1; font-weight: bold;" :class="statusClass(request.status)">
          {{ request.status }}
        </div>
        <div style="flex: 1; display: flex; gap: 10px;">
          <button @click="acceptRequest(request.request_id)" style="background-color: green; color: white; border: none; padding: 5px; cursor: pointer;">Accept</button>
          <button @click="rejectRequest(request.request_id)" style="background-color: red; color: white; border: none; padding: 5px; cursor: pointer;">Reject</button>
        </div>
      </div>
    </div>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 80px;">
      <h1> All Requests Handled</h1>
      <!-- Table Header -->
      <div style="display: flex; flex-direction: row; font-weight: bold; border-bottom: 2px solid #000; padding-bottom: 5px;">
        <div style="flex: 1;">Service Request ID</div>
        <div style="flex: 1;">Service Name</div>
        <div style="flex: 1;">Service Date</div>
        <div style="flex: 1;">Service Time</div>
        <div style="flex: 1;">End Date</div>
        <div style="flex: 1;">End Time</div>
        <div style="flex: 1;">Status</div>

      </div>
      <!-- Loading Indicator -->
      <div v-if="loading" style="display: flex; justify-content: center;">
        <p>Loading...</p>
      </div>

      <!-- No Requests Message -->
      <div v-else-if="pastServiceRequests.length == 0" style="text-align: center;">
        <p>No Past Services Recorded</p>
      </div>
      <!-- Service Requests List -->
       
      <div v-if="pastServiceRequests.length!==0" v-for="request in pastServiceRequests" :key="request.request_id" 
           style="display: flex; flex-direction: row; border-bottom: 1px solid #ccc; padding: 5px;">  
        <div style="flex: 1;">{{ request.request_id }}</div>
        <div style="flex: 1;">{{ request.service_type }}</div>
        <div style="flex: 1;"> {{ formatDate(request.date_created) }} </div>
        <div style="flex: 1;"> {{ formatTime(request.date_created) }} </div>
        <div style="flex: 1;"> {{ formatDate(request.date_completed) }} </div>
        <div style="flex: 1;"> {{ formatTime(request.date_completed) }} </div>
        <div style="flex: 1; font-weight: bold;" :class="statusClass(request.status)">
          {{ request.status }}
        </div>
      </div>
    </div>
  </div>
</template>



<script>
import axios from "axios";
import ProfessionalServiceRequests from "@/components/dashboard_contents/ProfessionalServiceRequests.vue";
import { h } from "vue";

export default {
  name: "ProfessionalServiceRequests",
  components: {
    ProfessionalServiceRequests,
  },
  data() {
    return {
      serviceRequests: [],
      pastServiceRequests: [],
      acceptedServiceRequests: [],
      allServiceRequests: [],
      loading: true,
    };
  },
  methods: {
    formatDate(dateTime) {
    return new Date(dateTime).toLocaleDateString();
    },
    formatTime(dateTime) {
    return new Date(dateTime).toLocaleTimeString();
    },
    async fetchRequests() {
      try {
        this.loading = true;

        // Retrieve user ID and JWT token from localStorage
        const user_id = localStorage.getItem("user_id");
        const token = localStorage.getItem("token");

        if (!user_id || !token) {
          console.error("User ID or token missing!");
          alert("Authentication error. Please log in again.");
          this.loading = false;
          return;
        }

        // Fetch professional ID using user ID
        const response1 = await axios.get(`http://127.0.0.1:5000/user_professional_id/${user_id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        const professional_id = response1.data.professional_id;
        console.log("Fetched professional ID:", professional_id);

        // Fetch service requests for the logged-in professional
        const response = await axios.get(`http://127.0.0.1:5000/professional_service_request/${professional_id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Debugging: Print the full API response
        console.log("Full API Response:", JSON.stringify(response.data, null, 2));

        // Handle different possible response structures
        const requests = response.data.requests || response.data.data?.requests || [];

        // Filter service requests based on status
        this.serviceRequests = requests.filter(req => req.status.toLowerCase().trim() === "pending");
        this.pastServiceRequests = requests.filter(req => req.status.toLowerCase().trim() !== "pending");
        this.acceptedServiceRequests = requests.filter(req => ["accepted", "concluded"].includes(req.status.toLowerCase().trim()));


        // Debugging: Confirm filtered lists
        console.log("Pending Requests:", JSON.stringify(this.serviceRequests, null, 2));
        console.log("Finished Requests:", JSON.stringify(this.pastServiceRequests,null,2));
        console.log("History Requests (Accepted):", JSON.stringify(this.historyServiceRequests, null, 2));

        this.loading = false;
      } catch (error) {
        console.error("Error fetching service requests:", error);
        alert("Failed to load service requests.");
        this.loading = false;
      }
    },  
    async acceptRequest(requestId) {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          `http://127.0.0.1:5000/service-requests/${requestId}/accept`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        alert("Request accepted!");
        this.fetchRequests(); // Refresh list
      } catch (error) {
        console.error("Failed to accept request:", error);
        alert("Error accepting request.");
      }
    },
    async rejectRequest(requestId) {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          `http://127.0.0.1:5000/service-requests/${requestId}/reject`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        alert("Request rejected!");
        this.fetchRequests(); // Refresh list
      } catch (error) {
        console.error("Failed to reject request:", error);
        alert("Error rejecting request.");
      }
    },
    
    async finishRequest(requestId) {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          `http://127.0.0.1:5000/service-requests/${requestId}/finish`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        alert("Request Finised!");
        this.fetchRequests(); // Refresh list
      } catch (error) {
        console.error("Failed to finish request:", error);
        alert("Error finishing request.");
      }
    },
    async abandonRequest(requestId) {
      try {
        const token = localStorage.getItem("token");

        await axios.post(
          `http://127.0.0.1:5000/service-requests/${requestId}/abandon`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        alert("Request Abandoned!");
        this.fetchRequests(); // Refresh list
      } catch (error) {
        console.error("Failed to abandon request:", error);
        alert("Error abandon-ing request.");
      }
    },
    statusClass(status) {
      return {
        "status-pending": status === "Pending",
        "status-accepted": status === "Accepted",
        "status-rejected": status === "Rejected",
        "status-finished": status === "Finished",
        "status-abandoned": status === "Abandoned",
      };
    },
  },
  mounted() {
    this.fetchRequests();
  },
};
</script>

<style scoped>
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
</style>