const AuthInput = ({
  label,
  name,
  type = "text",
  value,
  onChange,
  placeholder,
  required = true,
  minLength,
  autoComplete,
}) => {
  return (
    <div className="form-group">

      <label htmlFor={name}>
        {label}
      </label>

      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        minLength={minLength}
        autoComplete={autoComplete}
      />

    </div>
  );
};

export default AuthInput;