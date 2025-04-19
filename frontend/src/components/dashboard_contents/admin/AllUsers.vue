<template>
  <div class="all-users">

    <!-- Professionals Table -->
    <div class="table-section">
      <h3>All Professionals</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Blocked</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.username }}</td>
            <td>{{ professional.description }}</td>
            <td>{{ professional.blocked ? "Yes" : "No" }}</td>
            <td>
              <button
                class="block-btn"
                :class="{ 'unblock-btn': professional.blocked }"
                @click="toggleBlockUser(professional.user_id, 'P', professional.blocked)"
              >
                {{ professional.blocked ? "Unblock" : "Block" }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="height: 10px;">

    </div>
    <!-- Customers Table -->
    <div class="table-section">
      <h3>All Customers</h3>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Blocked</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in customers" :key="customer.id">
            <td>{{ customer.username }}</td>
            <td>{{ customer.email }}</td>
            <td>{{ customer.blocked ? "Yes" : "No" }}</td>
            <td>
              <button
                class="block-btn"
                :class="{ 'unblock-btn': customer.blocked }"
                @click="toggleBlockUser(customer.user_id, 'C', customer.blocked)"
              >
                {{ customer.blocked ? "Unblock" : "Block" }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import api from "@/api";

export default {
  name: "AllUsers",
  data() {
    return {
      professionals: [],
      customers: [],
    };
  },
  async created() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("token");

        // Fetch Professionals
        const professionalsRes = await axios.get("/api/get_all_professionals", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.professionals = professionalsRes.data.professionals || [];

        console.log("professionals", JSON.stringify(this.professionals));

        // Fetch Customers
        const customersRes = await axios.get("/api/get_all_customers", {
          headers: { Authorization: `Bearer ${token}` },
        });

        console.log("customers", JSON.stringify(customersRes.data.customers));
        this.customers = customersRes.data.customers || [];
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },

  async toggleBlockUser(userId, role, isBlocked) {
  if (!confirm(`Are you sure you want to ${isBlocked ? "unblock" : "block"} this user?`)) return;

  console.log(`Toggling block status for user ${userId} with role ${role}`);

  try {
    const token = localStorage.getItem("token");
    const response = await axios.post(
      `/api/block_user/${userId}`,
    );
    console.log(response.data);

    if (response.data.success) {
      // Find the user and update block status locally
      if (role === "P") {
        this.professionals = this.professionals.map((prof) =>
          prof.id === userId ? { ...prof, blocked: !isBlocked } : prof
        );
      } else if (role === "C") {
        this.customers = this.customers.map((cust) =>
          cust.id === userId ? { ...cust, blocked: !isBlocked } : cust
        );
      }
    } else {
      alert("Failed to update block status.");
    }
  } catch (error) {
    console.error("Error updating block status:", error);
    alert("Failed to update block status.");
  }
}
  },
};
</script>

<style scoped>
.all-users {
  max-width: 1000px;
  padding: 20px;  /* Adds internal spacing */
  font-family: Arial, sans-serif;
}

h2, h3 {
  text-align: center;
  margin-bottom: 15px;
}

.table-section {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); /* Adds subtle shadow */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background: #007bff;
  color: white;
  text-transform: uppercase;
}

tr:nth-child(even) {
  background: #f2f2f2;
}

tr:hover {
  background: #ddd;
}

.block-btn {
  border: none;
  padding: 7px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.2s;
}

.block-btn {
  background-color: red;
  color: white;
}

.block-btn:hover {
  background-color: darkred;
}

.unblock-btn {
  background-color: green !important;
}

.unblock-btn:hover {
  background-color: darkgreen !important;
}
</style>
