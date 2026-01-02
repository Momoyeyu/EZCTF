import axios from 'axios';

axios.defaults.withCredentials = true;
const BASE_URL = process.env.VUE_APP_BACKEND_URL || 'http://localhost:8000'; 

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

export const getTeamRanking = async () => {
  try {
    const response = await api.get('/api/v1/team/rank');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const createTeam = async (leaderId, teamName, allowJoin) => {
    try {
      const requestData = {
          team_name: teamName,
          allow_join: allowJoin,
      };
      // Note: leader_id is not needed in request body as it is inferred from current user
      const response = await api.post('/api/v1/team/',requestData); 
      return response.data;
    } catch (error) {
      throw error;
    }
};
  
  
export const joinTeam = async (teamname) => {
  try {
    const requestData = {
      team_name: teamname,
    };

    const response = await api.post('/api/v1/team/join', requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const quitTeam = async () => {
  try {
    const requestData = {};
    const response = await api.post(`/api/v1/team/quit`, requestData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const searchTeam = async (key_word) => {
  try {
    const response = await api.get(`/api/v1/team/?keyword=${key_word}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const teamDetail = async (teamName) => {
  try {
    const response = await api.get(`/api/v1/team/name/${teamName}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const changeTeamLeader = async (newLeaderName) => {
  try {
    const response = await api.post('/api/v1/team/change_leader', { username: newLeaderName });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const kickMember = async (username) => {
    try {
        const response = await api.post('/api/v1/team/kick', { username: username });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const changeTeamName = async (newTeamName) => {
    try {
        const me = await api.get('/api/v1/user/me');
        const teamId = me.data.team_id;
        if (!teamId) throw new Error("No team");
        
        const response = await api.patch(`/api/v1/team/${teamId}`, { team_name: newTeamName });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const verifyApply = async (username, allow) => {
    // Not implemented in backend
    console.warn("verifyApply not implemented");
    return {};
};

export const delete_Team = async (password) => {
  try {
    const meResponse = await api.get('/api/v1/user/me');
    const teamId = meResponse.data.team_id;
    if (!teamId) {
        throw new Error("User is not in a team");
    }

    const response = await api.delete(`/api/v1/team/${teamId}`);
    return response.status;
  } catch (error) {
    throw error;
  }
};

export const Invite = async (name) => {
   // Not implemented
   console.warn("Invite not implemented");
   return {};
};

