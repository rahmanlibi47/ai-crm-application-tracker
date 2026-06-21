const Input = ({ label, error, ...props }) => {
  return (
    <div>
      {label && <label>{label}</label>}

      <input {...props} />

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}
    </div>
  );
};

export default Input;