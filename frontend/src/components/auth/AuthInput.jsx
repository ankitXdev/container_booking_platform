/*
|--------------------------------------------------------------------------
| AuthInput
|--------------------------------------------------------------------------
| Reusable labelled input for auth forms.
| Supports disabled state and aria-invalid for accessibility.
|--------------------------------------------------------------------------
*/

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
  disabled,
  "aria-invalid": ariaInvalid,
}) => {
  return (
    <div className="form-group">

      {label && (
        <label htmlFor={name}>
          {label}
        </label>
      )}

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
        disabled={disabled}
        aria-invalid={ariaInvalid}
      />

    </div>
  );
};

export default AuthInput;