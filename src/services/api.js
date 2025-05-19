import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const registerTeacher = async (teacherData) => {
  const formData = new FormData();
  formData.append('first_name', teacherData.first_name);
  formData.append('last_name', teacherData.last_name);
  formData.append('email', teacherData.email);
  formData.append('photo', teacherData.photo);

  return api.post('/teachers', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getTeachers = async () => {
  return api.get('/teachers');
};

export const registerAttendance = async (teacherId, entry = true) => {
  return api.post('/attendance', { teacher_id: teacherId, entry });
};

export const getAttendance = async () => {
  return api.get('/attendance');
};