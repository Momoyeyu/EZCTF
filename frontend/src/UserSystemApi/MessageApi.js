import axios from 'axios';
axios.defaults.withCredentials = true;
const BASE_URL = 'http://8.130.98.1:8080'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getMessage = async () => {
    try {
      const response = await api.get(`/api/common/message?action=get_messages`);
      return response.data;
    } catch (error) {
      throw error;
    }
};

export const getApply = async () => {
  try {
    const response = await api.get(`/api/common/message?action=get_applications`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const checkAll = async () => {
    try {
      const response = await api.get(`/api/common/message?action=check_all`);
      return response.data;
    } catch (error) {
      throw error;
    }
};

export const checkMessage = async (id) => {
  try {
    const response = await api.get(`/api/common/message?action=check_message&message_id=${id}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const messNum = async () => {
  try {
    const response = await api.get(`/api/common/message?action=get_unchecked_count`);
    return response.data;
  } catch (error) {
    throw error;
  }
};
