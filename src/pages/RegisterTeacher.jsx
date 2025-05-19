import { useState } from 'react';
import { Container, TextField, Button, Box, Typography } from '@mui/material';
import { registerTeacher } from '../services/api';

function RegisterTeacher() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    photo: null,
  });
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: files ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerTeacher(formData);
      setMessage('Docente registrado correctamente');
      setFormData({ first_name: '', last_name: '', email: '', photo: null });
    } catch (error) {
      setMessage('Error al registrar: ' + error.response?.data?.error);
    }
  };

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4" gutterBottom>
          Registrar Docente
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Nombre"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Apellido"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Correo"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            fullWidth
            margin="normal"
            required
          />
          <input
            type="file"
            name="photo"
            accept="image/*"
            onChange={handleChange}
            style={{ marginTop: '16px' }}
            required
          />
          <Box mt={2}>
            <Button type="submit" variant="contained" color="primary">
              Registrar
            </Button>
          </Box>
        </form>
        {message && (
          <Typography color={message.includes('Error') ? 'error' : 'success'} mt={2}>
            {message}
          </Typography>
        )}
      </Box>
    </Container>
  );
}

export default RegisterTeacher;