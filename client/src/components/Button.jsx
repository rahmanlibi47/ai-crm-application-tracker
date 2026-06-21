const Button = ({ children, loading, disabled, ...props }) => {
  return (
    <button
      disabled={loading || disabled}
      {...props}
    >
      {loading ? "Please wait..." : children}
    </button>
  );
};

export default Button;