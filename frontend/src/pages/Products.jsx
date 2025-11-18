import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { FaSearch, FaLeaf, FaShoppingCart } from 'react-icons/fa';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  useEffect(() => {
    loadProducts();
    loadCategories();
  }, []);

  const loadProducts = async () => {
    try {
      const response = await api.get('/products/');
      setProducts(response.data);
    } catch (err) {
      setError('Error al cargar productos');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await api.get('/products/categories');
      setCategories(response.data.map(cat => cat.name));
    } catch (err) {
      console.error('Error loading categories');
    }
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          product.brand?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = !selectedCategory || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getEcoColor = (score) => {
    if (score >= 80) return '#27ae60';
    if (score >= 60) return '#f39c12';
    return '#e74c3c';
  };

  if (loading) return <div style={styles.loading}>Cargando productos...</div>;
  if (error) return <div style={styles.error}>{error}</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>Productos Disponibles</h1>
        <p>Explora nuestro catálogo de productos sostenibles</p>
      </div>

      <div style={styles.filters}>
        <div style={styles.searchBox}>
          <FaSearch style={styles.searchIcon} />
          <input
            type="text"
            placeholder="Buscar productos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={styles.searchInput}
          />
        </div>

        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          style={styles.select}
        >
          <option value="">Todas las categorías</option>
          {categories.map(cat => (
            <option key={cat} value={cat}>{cat}</option>
          ))}
        </select>
      </div>

      <div style={styles.grid}>
        {filteredProducts.map(product => (
          <Link to={`/products/${product.id}`} key={product.id} style={styles.card}>
            <div style={styles.imageContainer}>
              {product.image_url ? (
                <img src={product.image_url} alt={product.name} style={styles.image} />
              ) : (
                <div style={styles.noImage}><FaShoppingCart /></div>
              )}
            </div>

            <div style={styles.cardContent}>
              <h3 style={styles.productName}>{product.name}</h3>
              <p style={styles.brand}>{product.brand}</p>
              <p style={styles.category}>{product.category}</p>

              <div style={styles.ecoScore}>
                <FaLeaf style={{color: getEcoColor(product.eco_score), marginRight: '5px'}} />
                <span style={{color: getEcoColor(product.eco_score), fontWeight: 'bold'}}>
                  {product.eco_score}/100
                </span>
              </div>

              <div style={styles.footer}>
                <span style={styles.price}>${product.price.toLocaleString()}</span>
                <span style={styles.unit}>{product.unit}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div style={styles.noResults}>
          No se encontraron productos que coincidan con tu búsqueda
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    maxWidth: '1400px',
    margin: '0 auto',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2rem',
  },
  loading: {
    textAlign: 'center',
    padding: '3rem',
    fontSize: '1.2rem',
    color: '#666',
  },
  error: {
    background: '#ffebee',
    color: '#c62828',
    padding: '1rem',
    borderRadius: '8px',
    margin: '2rem',
    textAlign: 'center',
  },
  filters: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '2rem',
    flexWrap: 'wrap',
  },
  searchBox: {
    position: 'relative',
    flex: '1',
    minWidth: '250px',
  },
  searchIcon: {
    position: 'absolute',
    left: '15px',
    top: '50%',
    transform: 'translateY(-50%)',
    color: '#999',
  },
  searchInput: {
    width: '100%',
    padding: '0.75rem 1rem 0.75rem 3rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '1rem',
    outline: 'none',
  },
  select: {
    padding: '0.75rem 1rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '1rem',
    outline: 'none',
    minWidth: '200px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: '1.5rem',
  },
  card: {
    background: 'white',
    borderRadius: '12px',
    overflow: 'hidden',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    transition: 'transform 0.3s, box-shadow 0.3s',
    textDecoration: 'none',
    color: 'inherit',
  },
  imageContainer: {
    width: '100%',
    height: '200px',
    background: '#f5f5f5',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  image: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
  },
  noImage: {
    fontSize: '3rem',
    color: '#ccc',
  },
  cardContent: {
    padding: '1.25rem',
  },
  productName: {
    fontSize: '1.1rem',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '0.5rem',
  },
  brand: {
    fontSize: '0.9rem',
    color: '#666',
    marginBottom: '0.25rem',
  },
  category: {
    fontSize: '0.85rem',
    color: '#999',
    marginBottom: '0.75rem',
  },
  ecoScore: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '0.75rem',
    fontSize: '1rem',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: '0.75rem',
    borderTop: '1px solid #eee',
  },
  price: {
    fontSize: '1.3rem',
    fontWeight: 'bold',
    color: '#27ae60',
  },
  unit: {
    fontSize: '0.9rem',
    color: '#999',
  },
  noResults: {
    textAlign: 'center',
    padding: '3rem',
    color: '#999',
    fontSize: '1.1rem',
  },
};

export default Products;
