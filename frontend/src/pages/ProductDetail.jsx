import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { FaLeaf, FaWater, FaRecycle, FaArrowLeft, FaExchangeAlt, FaPlus } from 'react-icons/fa';
import Swal from 'sweetalert2';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [sustainability, setSustainability] = useState(null);
  const [substitutes, setSubstitutes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [lists, setLists] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedList, setSelectedList] = useState('');
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    loadProductDetails();
  }, [id]);

  const loadProductDetails = async () => {
    try {
      const [productRes, sustainabilityRes, substitutesRes, listsRes] = await Promise.all([
        api.get(`/products/${id}`),
        api.get(`/products/${id}/sustainability`),
        api.get(`/products/${id}/substitutes`),
        api.get('/shopping-lists/')
      ]);
      
      setProduct(productRes.data);
      setSustainability(sustainabilityRes.data);
      setSubstitutes(substitutesRes.data);
      setLists(listsRes.data);
    } catch (err) {
      setError('Error al cargar detalles del producto');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToList = async () => {
    if (!selectedList) {
      Swal.fire('Error', 'Selecciona una lista', 'error');
      return;
    }

    try {
      await api.post(`/shopping-lists/${selectedList}/items`, {
        product_id: parseInt(id),
        quantity: parseInt(quantity)
      });
      
      setShowAddModal(false);
      setSelectedList('');
      setQuantity(1);
      
      Swal.fire('Añadido', 'Producto agregado a la lista', 'success');
    } catch (err) {
      Swal.fire('Error', 'No se pudo agregar el producto', 'error');
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#27ae60';
    if (score >= 60) return '#f39c12';
    return '#e74c3c';
  };

  if (loading) return <div style={styles.loading}>Cargando...</div>;
  if (error) return <div style={styles.error}>{error}</div>;
  if (!product) return <div style={styles.error}>Producto no encontrado</div>;

  return (
    <div style={styles.container}>
      <Link to="/products" style={styles.backButton}>
        <FaArrowLeft /> Volver a productos
      </Link>

      <div style={styles.content}>
        <div style={styles.mainInfo}>
          <div style={styles.imageContainer}>
            {product.image_url ? (
              <img src={product.image_url} alt={product.name} style={styles.image} />
            ) : (
              <div style={styles.noImage}>Sin imagen</div>
            )}
          </div>

          <div style={styles.details}>
            <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem'}}>
              <div>
                <h1 style={styles.title}>{product.name}</h1>
                <p style={styles.brand}>{product.brand}</p>
                <p style={styles.category}>{product.category}</p>
              </div>
              <button onClick={() => setShowAddModal(true)} style={styles.addToListButton}>
                <FaPlus /> Agregar a Lista
              </button>
            </div>
            
            <div style={styles.price}>${product.price.toLocaleString()} / {product.unit}</div>
            
            {product.barcode && (
              <p style={styles.barcode}>Código de barras: {product.barcode}</p>
            )}

            {product.calories && (
              <div style={styles.nutrition}>
                <h3>Información Nutricional (por 100g)</h3>
                <div style={styles.nutritionGrid}>
                  <div>Calorías: {product.calories} kcal</div>
                  <div>Proteínas: {product.protein}g</div>
                  <div>Grasas: {product.fat}g</div>
                  <div>Carbohidratos: {product.carbs}g</div>
                </div>
              </div>
            )}
          </div>
        </div>

        {sustainability && (
          <div style={styles.section}>
            <h2>Análisis de Sostenibilidad</h2>
            
            <div style={styles.scoreCard}>
              <div style={styles.mainScore}>
                <FaLeaf style={{fontSize: '3rem', color: getScoreColor(product.eco_score || 0)}} />
                <div>
                  <div style={{fontSize: '2.5rem', fontWeight: 'bold', color: getScoreColor(product.eco_score || 0)}}>
                    {(product.eco_score || 0).toFixed(1)}
                  </div>
                  <div style={{color: '#666'}}>Eco-Score</div>
                </div>
              </div>
              
              <div style={{padding: '1rem', background: '#f9f9f9', borderRadius: '8px', marginTop: '1rem'}}>
                <div style={{fontSize: '0.9rem', color: '#666', marginBottom: '1rem'}}>Análisis Detallado:</div>
                
                <div style={{marginBottom: '1rem'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem'}}>
                    <strong>Económico:</strong>
                    <span>{(sustainability.economic_score || 0).toFixed(1)}</span>
                  </div>
                  <div style={{width: '100%', height: '8px', background: '#e0e0e0', borderRadius: '4px', overflow: 'hidden'}}>
                    <div style={{
                      width: `${sustainability.economic_score || 0}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, #f39c12, #e67e22)',
                      transition: 'width 0.5s ease'
                    }} />
                  </div>
                </div>

                <div style={{marginBottom: '1rem'}}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem'}}>
                    <strong>Ambiental:</strong>
                    <span>{(sustainability.environmental_score || 0).toFixed(1)}</span>
                  </div>
                  <div style={{width: '100%', height: '8px', background: '#e0e0e0', borderRadius: '4px', overflow: 'hidden'}}>
                    <div style={{
                      width: `${sustainability.environmental_score || 0}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, #27ae60, #229954)',
                      transition: 'width 0.5s ease'
                    }} />
                  </div>
                </div>

                <div>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem'}}>
                    <strong>Social:</strong>
                    <span>{(sustainability.social_score || 0).toFixed(1)}</span>
                  </div>
                  <div style={{width: '100%', height: '8px', background: '#e0e0e0', borderRadius: '4px', overflow: 'hidden'}}>
                    <div style={{
                      width: `${sustainability.social_score || 0}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, #3498db, #2980b9)',
                      transition: 'width 0.5s ease'
                    }} />
                  </div>
                </div>
              </div>
            </div>

            <div style={styles.metrics}>
              <div style={styles.metric}>
                <FaLeaf style={{fontSize: '2rem', color: '#27ae60'}} />
                <div>
                  <div style={styles.metricValue}>{product.carbon_footprint} kg CO₂</div>
                  <div style={styles.metricLabel}>Huella de Carbono</div>
                </div>
              </div>

              <div style={styles.metric}>
                <FaWater style={{fontSize: '2rem', color: '#3498db'}} />
                <div>
                  <div style={styles.metricValue}>{product.water_usage} L</div>
                  <div style={styles.metricLabel}>Uso de Agua</div>
                </div>
              </div>

              <div style={styles.metric}>
                <FaRecycle style={{fontSize: '2rem', color: '#f39c12'}} />
                <div>
                  <div style={styles.metricValue}>{product.packaging_score}/100</div>
                  <div style={styles.metricLabel}>Puntuación Empaque</div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div style={styles.section}>
          <h2>
            <FaExchangeAlt style={{marginRight: '10px'}} />
            Alternativas Más Sostenibles
          </h2>
          
          {substitutes.length > 0 ? (
            <div style={styles.substitutesGrid}>
              {substitutes.map(item => {
                const sub = item.product || item;
                // Solo mostrar si realmente es más sostenible
                if ((sub.eco_score || 0) <= product.eco_score) return null;
                
                return (
                  <Link to={`/products/${sub.id}`} key={sub.id} style={styles.substituteCard}>
                    <h3>{sub.name || 'Producto sin nombre'}</h3>
                    <p style={styles.substituteBrand}>{sub.brand || ''}</p>
                    <div style={styles.substituteScore}>
                      <FaLeaf style={{color: getScoreColor(sub.eco_score || 0)}} />
                      <span style={{color: getScoreColor(sub.eco_score || 0), fontWeight: 'bold'}}>
                        {sub.eco_score || 0}/100
                      </span>
                    </div>
                    <div style={styles.substitutePrice}>${(sub.price || 0).toLocaleString()}</div>
                    <div style={styles.badge}>
                      +{((sub.eco_score || 0) - product.eco_score).toFixed(1)} puntos más sostenible
                    </div>
                    {item.recommendation_reason && (
                      <p style={{fontSize: '0.85rem', color: '#666', marginTop: '0.5rem'}}>
                        {item.recommendation_reason}
                      </p>
                    )}
                  </Link>
                );
              }).filter(Boolean)}
            </div>
          ) : (
            <div style={{
              padding: '2rem',
              textAlign: 'center',
              background: '#f9f9f9',
              borderRadius: '8px',
              color: '#666'
            }}>
              <FaLeaf style={{fontSize: '3rem', color: '#27ae60', marginBottom: '1rem'}} />
              <p style={{fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>
                ¡Excelente elección!
              </p>
              <p>
                Este producto ya es una de las mejores opciones en su categoría. 
                No hay alternativas más sostenibles disponibles.
              </p>
            </div>
          )}
        </div>
      </div>

      {showAddModal && (
        <div style={styles.modal}>
          <div style={styles.modalContent}>
            <h2>Agregar a Lista</h2>
            <div style={styles.form}>
              <div style={styles.formGroup}>
                <label>Selecciona una lista:</label>
                <select
                  value={selectedList}
                  onChange={(e) => setSelectedList(e.target.value)}
                  style={styles.select}
                >
                  <option value="">Selecciona...</option>
                  {lists.map(list => (
                    <option key={list.id} value={list.id}>
                      {list.name} {list.budget ? `- Presupuesto: $${list.budget.toLocaleString()}` : ''}
                    </option>
                  ))}
                </select>
              </div>
              
              <div style={styles.formGroup}>
                <label>Cantidad:</label>
                <input
                  type="number"
                  min="1"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                  style={styles.input}
                />
              </div>

              <div style={styles.modalButtons}>
                <button onClick={handleAddToList} style={styles.modalButtonPrimary}>
                  Agregar
                </button>
                <button onClick={() => setShowAddModal(false)} style={styles.modalButtonSecondary}>
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  backButton: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem',
    color: '#27ae60',
    textDecoration: 'none',
    marginBottom: '1.5rem',
    fontSize: '1rem',
  },
  loading: {
    textAlign: 'center',
    padding: '3rem',
    fontSize: '1.2rem',
  },
  error: {
    background: '#ffebee',
    color: '#c62828',
    padding: '1rem',
    borderRadius: '8px',
    margin: '2rem',
    textAlign: 'center',
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    gap: '2rem',
  },
  mainInfo: {
    display: 'grid',
    gridTemplateColumns: '1fr 2fr',
    gap: '2rem',
    background: 'white',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  imageContainer: {
    width: '100%',
    height: '400px',
    background: '#f5f5f5',
    borderRadius: '8px',
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
    color: '#ccc',
    fontSize: '1.2rem',
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  title: {
    fontSize: '2rem',
    color: '#333',
    marginBottom: '0.5rem',
  },
  brand: {
    fontSize: '1.2rem',
    color: '#666',
  },
  category: {
    fontSize: '1rem',
    color: '#999',
  },
  price: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#27ae60',
    marginTop: '1rem',
  },
  barcode: {
    fontSize: '0.9rem',
    color: '#999',
    marginTop: '0.5rem',
  },
  nutrition: {
    marginTop: '1.5rem',
    padding: '1rem',
    background: '#f9f9f9',
    borderRadius: '8px',
  },
  nutritionGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '0.5rem',
    marginTop: '0.5rem',
  },
  section: {
    background: 'white',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  scoreCard: {
    display: 'flex',
    flexDirection: 'column',
    gap: '2rem',
    marginTop: '1.5rem',
  },
  mainScore: {
    display: 'flex',
    alignItems: 'center',
    gap: '1.5rem',
    padding: '1.5rem',
    background: '#f9f9f9',
    borderRadius: '8px',
  },
  scores: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
  },
  scoreItem: {
    display: 'grid',
    gridTemplateColumns: '120px 1fr 60px',
    alignItems: 'center',
    gap: '1rem',
  },
  scoreLabel: {
    fontWeight: 'bold',
    color: '#666',
  },
  scoreBar: {
    height: '20px',
    background: '#e0e0e0',
    borderRadius: '10px',
    overflow: 'hidden',
  },
  scoreBarFill: {
    height: '100%',
    transition: 'width 0.5s',
  },
  scoreValue: {
    fontWeight: 'bold',
    textAlign: 'right',
  },
  metrics: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1.5rem',
    marginTop: '2rem',
  },
  metric: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
    padding: '1rem',
    background: '#f9f9f9',
    borderRadius: '8px',
  },
  metricValue: {
    fontSize: '1.3rem',
    fontWeight: 'bold',
    color: '#333',
  },
  metricLabel: {
    fontSize: '0.9rem',
    color: '#666',
  },
  substitutesGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
    gap: '1.5rem',
    marginTop: '1.5rem',
  },
  substituteCard: {
    padding: '1.5rem',
    background: '#f9f9f9',
    borderRadius: '8px',
    textDecoration: 'none',
    color: 'inherit',
    transition: 'transform 0.3s',
  },
  substituteBrand: {
    color: '#666',
    fontSize: '0.9rem',
    marginTop: '0.25rem',
  },
  substituteScore: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    margin: '0.75rem 0',
  },
  substitutePrice: {
    fontSize: '1.3rem',
    fontWeight: 'bold',
    color: '#27ae60',
  },
  badge: {
    marginTop: '0.75rem',
    padding: '0.5rem',
    background: '#e8f5e9',
    color: '#27ae60',
    borderRadius: '6px',
    fontSize: '0.85rem',
    fontWeight: 'bold',
  },
  addToListButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    padding: '0.75rem 1.5rem',
    background: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: 'bold',
    cursor: 'pointer',
    transition: 'background 0.3s',
  },
  modal: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0,0,0,0.5)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
  },
  modalContent: {
    background: 'white',
    padding: '2rem',
    borderRadius: '12px',
    minWidth: '400px',
    maxWidth: '500px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1.5rem',
    marginTop: '1rem',
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  select: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '5px',
    fontSize: '1rem',
  },
  input: {
    padding: '0.75rem',
    border: '1px solid #ddd',
    borderRadius: '5px',
    fontSize: '1rem',
  },
  modalButtons: {
    display: 'flex',
    gap: '1rem',
    marginTop: '1rem',
  },
  modalButtonPrimary: {
    flex: 1,
    padding: '0.75rem',
    background: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    fontSize: '1rem',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
  modalButtonSecondary: {
    flex: 1,
    padding: '0.75rem',
    background: '#95a5a6',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    fontSize: '1rem',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
};

export default ProductDetail;
