import axios from "axios";

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL,
});

export const applicationApi = axios.create({
  baseURL: import.meta.env.VITE_APPLICATION_API_URL,
});

applicationApi.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});