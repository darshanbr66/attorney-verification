// services/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  // baseURL: "https://attorney-verification.onrender.com",
});

export default API;