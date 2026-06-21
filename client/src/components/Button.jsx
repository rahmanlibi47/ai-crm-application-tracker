const Button = ({
  children,
  loading,
  ...props
}) => {
  return (
    <button
      disabled={loading}
      {...props}
    >
      {loading
        ? "Please wait..."
        : children}
    </button>
  );
};

export default Button;