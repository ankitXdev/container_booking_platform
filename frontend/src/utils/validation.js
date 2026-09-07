export const validateEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
    email
  );
};

export const validateName = (name) => {
  return name.trim().length >= 2;
};

export const validatePassword = (password) => {
  return password.length >= 16;
};

export const validateConfirmPassword = (
  password,
  confirmPassword
) => {
  return password === confirmPassword;
};