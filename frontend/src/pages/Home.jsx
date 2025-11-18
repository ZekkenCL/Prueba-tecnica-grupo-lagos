import { Link } from 'react-router-dom';
import { FaLeaf, FaShoppingCart, FaChartLine, FaRecycle } from 'react-icons/fa';

const Home = () => {
  return (
    <div style={styles.container}>
      <div style={styles.hero}>
        <h1 style={styles.title}>
          <FaLeaf style={{color: '#27ae60', marginRight: '15px'}} />
          Bienvenido a LiquiVerde
        </h1>
        <p style={styles.subtitle}>
          Tu plataforma inteligente para compras sostenibles y económicas
        </p>
        <p style={styles.description}>
          Ahorra dinero mientras tomas decisiones que cuidan el planeta
        </p>
        <Link to="/register" style={styles.ctaButton}>
          Comenzar Ahora
        </Link>
      </div>

      <div style={styles.features}>
        <div style={styles.feature}>
          <FaShoppingCart style={styles.featureIcon} />
          <h3>Listas Optimizadas</h3>
          <p>Crea listas de compras que se ajusten a tu presupuesto y objetivos</p>
        </div>

        <div style={styles.feature}>
          <FaChartLine style={styles.featureIcon} />
          <h3>Análisis de Sostenibilidad</h3>
          <p>Conoce el impacto ambiental y social de tus compras</p>
        </div>

        <div style={styles.feature}>
          <FaRecycle style={styles.featureIcon} />
          <h3>Alternativas Inteligentes</h3>
          <p>Descubre productos más sostenibles y económicos</p>
        </div>
      </div>

      <div style={styles.stats}>
        <div style={styles.stat}>
          <h2>20+</h2>
          <p>Productos Disponibles</p>
        </div>
        <div style={styles.stat}>
          <h2>30%</h2>
          <p>Ahorro Promedio</p>
        </div>
        <div style={styles.stat}>
          <h2>50%</h2>
          <p>Reducción Huella Carbono</p>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: 'calc(100vh - 100px)',
  },
  hero: {
    textAlign: 'center',
    padding: '4rem 2rem',
    background: 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)',
    borderRadius: '15px',
    marginBottom: '3rem',
  },
  title: {
    fontSize: '3rem',
    color: '#1b5e20',
    marginBottom: '1rem',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  subtitle: {
    fontSize: '1.5rem',
    color: '#2e7d32',
    marginBottom: '0.5rem',
  },
  description: {
    fontSize: '1.1rem',
    color: '#43a047',
    marginBottom: '2rem',
  },
  ctaButton: {
    display: 'inline-block',
    background: '#27ae60',
    color: 'white',
    padding: '1rem 2.5rem',
    borderRadius: '30px',
    textDecoration: 'none',
    fontSize: '1.1rem',
    fontWeight: 'bold',
    transition: 'all 0.3s',
    boxShadow: '0 4px 15px rgba(39, 174, 96, 0.3)',
  },
  features: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '2rem',
    marginBottom: '3rem',
  },
  feature: {
    background: 'white',
    padding: '2rem',
    borderRadius: '10px',
    textAlign: 'center',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  featureIcon: {
    fontSize: '3rem',
    color: '#27ae60',
    marginBottom: '1rem',
  },
  stats: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '2rem',
    padding: '2rem',
    background: 'white',
    borderRadius: '10px',
  },
  stat: {
    textAlign: 'center',
  },
};

export default Home;
