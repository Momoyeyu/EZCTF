import axios from 'axios';
axios.defaults.withCredentials = true;
const BASE_URL = 'http://localhost:8000'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to inject the token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const login = async (usernameOrEmail, password1) => {
  try {
    const requestData = {
      username: usernameOrEmail,
      password: password1,
    };

    const response = await api.post('/api/v1/user/login', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const register = async (username, password, email) => {
  try {
    const requestData = {
      username: username,
      password: password,
      email: email,
    };

    const response = await api.post('/api/v1/user/register', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const validateCode = async (username, valid_code) => {
  console.warn("validateCode not implemented in backend");
  return { status: 'error', msg: 'Not implemented' };
};

export const forgetPassword = async (email) => {
  console.warn("forgetPassword not implemented in backend");
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500));
  // Return a mock failure or success depending on what we want to show.
  // Since we don't have email server, let's return error to avoid misleading user.
  // Or return success but log warning.
  return { status: 'error', detail: '邮件服务暂未配置' };
};

export const resetPassword = async (valid_code,email,new_password) => {
  console.warn("resetPassword not implemented in backend");
  await new Promise(resolve => setTimeout(resolve, 500));
  return { status: 'error', detail: '重置密码功能暂不可用' };
};

export const modifyUserInfo = async (old_username,new_username,password) => {
  try {
    const requestData = {};
    if (new_username) requestData.nickname = new_username; 
    if (password) requestData.password = password;

    const response = await api.patch('/api/v1/user/me', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const logoutUser = async () => {
    // Client side logout only
    localStorage.removeItem('token');
    return { status: 'success' };
};

export const deleteUserInfo = async (password) => {
   try {
     // Verify password first if needed, but for now just delete
     // Ideally we should ask for password to confirm.
     // Backend doesn't support password verification on delete yet, so just delete.
     const response = await api.delete('/api/v1/user/me');
     return response.data;
   } catch (error) {
     throw error;
   }
};

export const user_profile = async () => {
  try {
    const response = await api.get('/api/v1/user/me');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getUserRanking = async () => {
  try {
    const response = await api.get('/api/v1/user/rank');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const profile = async (username) => {
    console.warn("profile(username) is deprecated, use user_profile() for current user");
    return {}; 
};
