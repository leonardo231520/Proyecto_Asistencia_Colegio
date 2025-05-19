import { Container, Typography, Box } from '@mui/material';

function Home() {
  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4" gutterBottom>
          Bienvenido al Sistema de Asistencia
        </Typography>
        <Typography variant="body1">
          Utiliza el menú superior para registrar docentes o gestionar asistencias.
        </Typography>
      </Box>
    </Container>
  );
}

export default Home;