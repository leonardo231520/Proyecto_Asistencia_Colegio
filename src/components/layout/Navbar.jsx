import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';

function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          Sistema de Asistencia
        </Typography>
        <Button color="inherit" component={Link} to="/">
          Inicio
        </Button>
        <Button color="inherit" component={Link} to="/register-teacher">
          Registrar Docente
        </Button>
        <Button color="inherit" component={Link} to="/attendance">
          Asistencias
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;