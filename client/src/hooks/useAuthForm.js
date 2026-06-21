import { useState } from "react";

export const useAuthForm = (
  initialValues
) => {
  const [values, setValues] =
    useState(initialValues);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleChange = (e) => {
    const { name, value } =
      e.target;

    setValues((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return {
    values,
    setValues,
    loading,
    setLoading,
    error,
    setError,
    handleChange,
  };
};