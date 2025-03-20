<template>
    <div class="all-services">
      <h2>All Services</h2>
  
      <!-- Services Table -->
      <div class="table-section">
        <table>
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Description</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.service_id">
              <td>{{ service.name }}</td>
              <td>{{ service.description }}</td>
              <td>${{ service.price.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Add Service Button -->
      <button class="add-service-btn" @click="showModal = true">Add Service</button>
  
      <!-- Modal for Adding Service -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <h3>Add New Service</h3>
          <label>Service Name:</label>
          <input type="text" v-model="newService.service_name" placeholder="Enter service name" />
  
          <label>Description:</label>
          <input type="text" v-model="newService.description" placeholder="Enter description" />
  
          <label>Price:</label>
          <input type="number" v-model="newService.price" placeholder="Enter price" />
  
          <div class="modal-actions">
            <button @click="addService">Add</button>
            <button @click="showModal = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "AllServices",
    data() {
      return {
        services: [],
        showModal: false,
        newService: {
          service_name: "",
          description: "",
          price: null,
        },
      };
    },
    async created() {
      await this.fetchServices();
    },
    methods: {
      async fetchServices() {
        try {
          const response = await axios.get("http://127.0.0.1:5000/get_all_services");
          console.log("Services:", JSON.stringify(response.data, null, 2));
          this.services = response.data || [];
        } catch (error) {
          console.error("Error fetching services:", error);
        }
      },
  
      async addService() {
        if (!this.newService.service_name || !this.newService.price) {
          alert("Service name and price are required!");
          return;
        }
  
        try {
          const response = await axios.post("http://127.0.0.1:5000/add_service", this.newService);
          if (response.data.success) {
            this.services.push({
              service_id: response.data.service_id,
              ...this.newService,
            });
            alert("Service added successfully!");
            this.showModal = false;
            this.newService = { service_name: "", description: "", price: null };
          } else {
            alert("Failed to add service.");
          }
        } catch (error) {
          console.error("Error adding service:", error);
          alert("Failed to add service.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .all-services {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  h2 {
    text-align: center;
  }
  
  .table-section {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #ffffff;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 10px;
    text-align: left;
  }
  
  th {
    background: #007bff;
    color: white;
  }
  
  tr:nth-child(even) {
    background: #f2f2f2;
  }
  
  tr:hover {
    background: #ddd;
  }
  
  /* Add Service Button */
  .add-service-btn {
    display: block;
    width: 200px;
    margin: 20px auto;
    padding: 10px;
    border: none;
    background-color: #28a745;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .add-service-btn:hover {
    background-color: #218838;
  }
  
  /* Modal Styling */
  .modal-overlay {
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
  
  .modal {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    width: 300px;
  }
  
  .modal h3 {
    margin-bottom: 15px;
  }
  
  .modal label {
    display: block;
    margin: 10px 0 5px;
  }
  
  .modal input {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }
  
  .modal-actions {
    display: flex;
    justify-content: space-between;
  }
  
  .modal-actions button {
    padding: 8px 12px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .modal-actions button:first-child {
    background-color: #007bff;
    color: white;
  }
  
  .modal-actions button:last-child {
    background-color: #dc3545;
    color: white;
  }
  
  .modal-actions button:hover {
    opacity: 0.8;
  }
  </style>
  