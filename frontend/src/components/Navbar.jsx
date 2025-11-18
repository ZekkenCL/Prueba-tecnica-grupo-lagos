import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { FaLeaf, FaShoppingCart, FaUser, FaSignOutAlt } from 'react-icons/fa';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <Link to="/" style={styles.logo}>
          <FaLeaf style={styles.logoIcon} />
          LiquiVerde
        </Link>

        <div style={styles.links}>
          {user ? (
            <>
              <Link to="/products" style={styles.link}>
                Productos
              </Link>
              <Link to="/shopping-lists" style={styles.link}>
                <FaShoppingCart style={{marginRight: '5px'}} />
                Mis Listas
              </Link>
              <span style={styles.username}>
                <FaUser style={{marginRight: '5px'}} />
                {user.username}
              </span>
              <button onClick={logout} style={styles.logoutButton}>
                <FaSignOutAlt />
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={styles.link}>
                Iniciar Sesión
              </Link>
              <Link to="/register" style={styles.registerButton}>
                Registrarse
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

const styles = {
  nav: {
    background: 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)',
    padding: '1rem 0',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 1rem',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    fontSize: '1.8rem',
    fontWeight: 'bold',
    color: 'white',
    textDecoration: 'none',
    display: 'flex',
    alignItems: 'center',
  },
  logoIcon: {
    marginRight: '10px',
  },
  links: {
    display: 'flex',
    gap: '1.5rem',
    alignItems: 'center',
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    fontSize: '1rem',
    fontWeight: '500',
    display: 'flex',
    alignItems: 'center',
    transition: 'opacity 0.3s',
  },
  username: {
    color: 'white',
    fontSize: '0.95rem',
    display: 'flex',
    alignItems: 'center',
  },
  registerButton: {
    background: 'white',
    color: '#27ae60',
    padding: '0.5rem 1.2rem',
    borderRadius: '25px',
    textDecoration: 'none',
    fontWeight: 'bold',
    transition: 'all 0.3s',
  },
  logoutButton: {
    background: 'rgba(255,255,255,0.2)',
    border: 'none',
    color: 'white',
    padding: '0.5rem 0.8rem',
    borderRadius: '50%',
    cursor: 'pointer',
    fontSize: '1.1rem',
    display: 'flex',
    alignItems: 'center',
    transition: 'all 0.3s',
  },
};

export default Navbar;
