import { useState, useEffect } from 'react';
import { Container, Table, TableBody, TableCell, TableHead, TableRow, Button, Typography, Box } from '@mui/material';
import { getTeachers, getAttendance, registerAttendance } from '../services/api';

function Attendance() {
  const [teachers, setTeachers] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [teachersRes, attendanceRes] = await Promise.all([
          getTeachers(),
          getAttendance(),
        ]);
        setTeachers(teachersRes.data);
        setAttendance(attendanceRes.data);
      } catch (error) {
        setMessage('Error al cargar datos: ' + error.message);
      }
    };
    fetchData();
  }, []);

  const handleAttendance = async (teacherId, entry) => {
    try {
      await registerAttendance(teacherId, entry);
      setMessage(`Asistencia ${entry ? 'entrada' : 'salida'} registrada correctamente`);
      const attendanceRes = await getAttendance();
      setAttendance(attendanceRes.data);
    } catch (error) {
      setMessage('Error al registrar asistencia: ' + error.response?.data?.error);
    }
  };

  return (
    <Container>
      <Box mt={4}>
        <Typography variant="h4" gutterBottom>
          Gestionar Asistencias
        </Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Docente</TableCell>
              <TableCell>Entrada</TableCell>
              <TableCell>Salida</TableCell>
              <TableCell>Estado</TableCell>
              <TableCell>Acciones</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {attendance.map((record) => (
              <TableRow key={record.id}>
                <TableCell>{`${record.first_name} ${record.last_name}`}</TableCell>
                <TableCell>{record.entry_time || '-'}</TableCell>
                <TableCell>{record.exit_time || '-'}</TableCell>
                <TableCell>{record.status}</TableCell>
                <TableCell>
                  {!record.exit_time && (
                    <Button
                      variant="contained"
                      color="secondary"
                      onClick={() => handleAttendance(record.teacher_id, false)}
                    >
                      Registrar Salida
                    </Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Box mt={4}>
          <Typography variant="h6">Registrar Nueva Entrada</Typography>
          {teachers.map((teacher) => (
            <Button
              key={teacher.id}
              variant="contained"
              color="primary"
              onClick={() => handleAttendance(teacher.id, true)}
              style={{ margin: '8px' }}
            >
              Entrada: {`${teacher.first_name} ${teacher.last_name}`}
            </Button>
          ))}
        </Box>
        {message && (
          <Typography color={message.includes('Error') ? 'error' : 'success'} mt={2}>
            {message}
          </Typography>
        )}
      </Box>
    </Container>
  );
}

export default Attendance;