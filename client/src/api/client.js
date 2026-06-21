import axios from "axios";

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL,
  withCredentials: true,
});

export const applicationApi =
  axios.create({
    baseURL:
      import.meta.env
        .VITE_APPLICATION_API_URL,
  });