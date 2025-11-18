import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FaUser, FaLock, FaEnvelope, FaLeaf } from 'react-icons/fa';

const Register = () => {
  const [formData, setFormData] = useState({ email: '', username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (formData.password.length < 6) {
      setError('La contraseña debe tener al menos 6 caracteres');
      setLoading(false);
      return;
    }

    try {
      await register(formData.email, formData.username, formData.password);
      navigate('/products');
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al registrarse');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <FaLeaf style={styles.logo} />
          <h2>Crear Cuenta</h2>
          <p>Únete a la comunidad LiquiVerde</p>
        </div>

        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <FaEnvelope style={styles.icon} />
            <input
              type="email"
              placeholder="Correo electrónico"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              style={styles.input}
            />
          </div>

          <div style={styles.inputGroup}>
            <FaUser style={styles.icon} />
            <input
              type="text"
              placeholder="Nombre de usuario"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
              style={styles.input}
            />
          </div>

          <div style={styles.inputGroup}>
            <FaLock style={styles.icon} />
            <input
              type="password"
              placeholder="Contraseña (mínimo 6 caracteres)"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              style={styles.input}
            />
          </div>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Creando cuenta...' : 'Registrarse'}
          </button>
        </form>

        <p style={styles.footer}>
          ¿Ya tienes cuenta? <Link to="/login" style={styles.link}>Inicia sesión aquí</Link>
        </p>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: 'calc(100vh - 100px)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)',
    padding: '2rem',
  },
  card: {
    background: 'white',
    padding: '3rem',
    borderRadius: '15px',
    boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
    maxWidth: '450px',
    width: '100%',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2rem',
  },
  logo: {
    fontSize: '3rem',
    color: '#27ae60',
    marginBottom: '1rem',
  },
  error: {
    background: '#ffebee',
    color: '#c62828',
    padding: '0.75rem',
    borderRadius: '8px',
    marginBottom: '1.5rem',
    fontSize: '0.9rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
  },
  inputGroup: {
    position: 'relative',
    display: 'flex',
    alignItems: 'center',
  },
  icon: {
    position: 'absolute',
    left: '15px',
    color: '#27ae60',
    fontSize: '1.2rem',
  },
  input: {
    width: '100%',
    padding: '0.9rem 1rem 0.9rem 3rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '1rem',
    transition: 'border-color 0.3s',
    outline: 'none',
  },
  button: {
    background: '#27ae60',
    color: 'white',
    padding: '1rem',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1.1rem',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'background 0.3s',
  },
  footer: {
    textAlign: 'center',
    marginTop: '1.5rem',
    color: '#666',
  },
  link: {
    color: '#27ae60',
    fontWeight: 'bold',
    textDecoration: 'none',
  },
};

export default Register;
