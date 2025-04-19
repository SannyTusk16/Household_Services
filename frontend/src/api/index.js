// src/api/index.js
import axios from "axios";

const api = axios.create({
  baseURL: "/", // no localhost, no port
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

export default api;
