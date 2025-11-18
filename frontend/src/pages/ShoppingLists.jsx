import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { FaPlus, FaShoppingCart, FaTrash } from 'react-icons/fa';
import Swal from 'sweetalert2';

const ShoppingLists = () => {
  const [lists, setLists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newList, setNewList] = useState({ name: '', budget: '' });

  useEffect(() => {
    loadLists();
  }, []);

  const loadLists = async () => {
    try {
      const response = await api.get('/shopping-lists/');
      setLists(response.data);
    } catch (err) {
      setError('Error al cargar listas de compras');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await api.post('/shopping-lists/', {
        name: newList.name,
        budget: parseFloat(newList.budget)
      });
      setNewList({ name: '', budget: '' });
      setShowCreateModal(false);
      loadLists();
      Swal.fire('Creada', 'Lista de compras creada correctamente', 'success');
    } catch (err) {
      Swal.fire('Error', 'No se pudo crear la lista', 'error');
    }
  };

  const handleDelete = async (listId) => {
    const result = await Swal.fire({
      title: '¿Eliminar lista?',
      text: 'Esta acción eliminará la lista y todos sus productos',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#e74c3c',
      cancelButtonColor: '#95a5a6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    });
    
    if (!result.isConfirmed) return;
    
    try {
      await api.delete(`/shopping-lists/${listId}`);
      loadLists();
      Swal.fire('Eliminada', 'Lista eliminada correctamente', 'success');
    } catch (err) {
      Swal.fire('Error', 'No se pudo eliminar la lista', 'error');
    }
  };

  if (loading) return <div style={styles.loading}>Cargando...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>Mis Listas de Compras</h1>
        <button onClick={() => setShowCreateModal(true)} style={styles.createButton}>
          <FaPlus /> Nueva Lista
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.grid}>
        {lists.map(list => (
          <div key={list.id} style={styles.card}>
            <div style={styles.cardHeader}>
              <Link to={`/shopping-lists/${list.id}`} style={styles.cardTitle}>
                <FaShoppingCart style={{marginRight: '10px'}} />
                {list.name}
              </Link>
              <button onClick={() => handleDelete(list.id)} style={styles.deleteButton}>
                <FaTrash />
              </button>
            </div>

            <div style={styles.cardBody}>
              <div style={styles.stat}>
                <span style={styles.statLabel}>Presupuesto:</span>
                <span style={styles.statValue}>${list.budget?.toLocaleString()}</span>
              </div>

              {list.is_optimized && (
                <>
                  <div style={styles.stat}>
                    <span style={styles.statLabel}>Costo Total:</span>
                    <span style={styles.statValue}>${list.total_cost?.toLocaleString()}</span>
                  </div>
                  <div style={styles.stat}>
                    <span style={styles.statLabel}>Ahorro:</span>
                    <span style={{...styles.statValue, color: '#27ae60'}}>
                      ${list.total_savings?.toLocaleString()}
                    </span>
                  </div>
                  <div style={styles.stat}>
                    <span style={styles.statLabel}>Eco Score:</span>
                    <span style={{...styles.statValue, color: '#27ae60'}}>
                      {list.total_eco_score?.toFixed(1)}
                    </span>
                  </div>
                </>
              )}

              <div style={styles.badge}>
                {list.is_optimized ? '✓ Optimizada' : 'Sin optimizar'}
              </div>
            </div>

            <Link to={`/shopping-lists/${list.id}`} style={styles.viewButton}>
              Ver Detalles
            </Link>
          </div>
        ))}
      </div>

      {lists.length === 0 && (
        <div style={styles.empty}>
          <FaShoppingCart style={{fontSize: '4rem', color: '#ccc', marginBottom: '1rem'}} />
          <p>No tienes listas de compras todavía</p>
          <button onClick={() => setShowCreateModal(true)} style={styles.emptyButton}>
            Crear Primera Lista
          </button>
        </div>
      )}

      {showCreateModal && (
        <div style={styles.modal}>
          <div style={styles.modalContent}>
            <h2>Nueva Lista de Compras</h2>
            <form onSubmit={handleCreate} style={styles.form}>
              <input
                type="text"
                placeholder="Nombre de la lista"
                value={newList.name}
                onChange={(e) => setNewList({ ...newList, name: e.target.value })}
                required
                style={styles.input}
              />
              <input
                type="number"
                placeholder="Presupuesto"
                value={newList.budget}
                onChange={(e) => setNewList({ ...newList, budget: e.target.value })}
                required
                step="0.01"
                style={styles.input}
              />
              <div style={styles.modalButtons}>
                <button type="button" onClick={() => setShowCreateModal(false)} style={styles.cancelButton}>
                  Cancelar
                </button>
                <button type="submit" style={styles.submitButton}>
                  Crear
                </button>
              </div>
            </form>
          </div>
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
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
  },
  createButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    background: '#27ae60',
    color: 'white',
    padding: '0.75rem 1.5rem',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    cursor: 'pointer',
    fontWeight: 'bold',
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
    marginBottom: '1rem',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '1.5rem',
  },
  card: {
    background: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    overflow: 'hidden',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1.5rem',
    background: 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)',
    color: 'white',
  },
  cardTitle: {
    fontSize: '1.3rem',
    fontWeight: 'bold',
    color: 'white',
    textDecoration: 'none',
    display: 'flex',
    alignItems: 'center',
  },
  deleteButton: {
    background: 'rgba(255,255,255,0.2)',
    color: 'white',
    border: 'none',
    padding: '0.5rem',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '1rem',
  },
  cardBody: {
    padding: '1.5rem',
  },
  stat: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '0.75rem',
  },
  statLabel: {
    color: '#666',
  },
  statValue: {
    fontWeight: 'bold',
    color: '#333',
  },
  badge: {
    display: 'inline-block',
    padding: '0.5rem 1rem',
    background: '#e8f5e9',
    color: '#27ae60',
    borderRadius: '20px',
    fontSize: '0.85rem',
    fontWeight: 'bold',
    marginTop: '0.5rem',
  },
  viewButton: {
    display: 'block',
    textAlign: 'center',
    padding: '1rem',
    background: '#f5f5f5',
    color: '#27ae60',
    textDecoration: 'none',
    fontWeight: 'bold',
  },
  empty: {
    textAlign: 'center',
    padding: '4rem 2rem',
    color: '#999',
  },
  emptyButton: {
    marginTop: '1rem',
    background: '#27ae60',
    color: 'white',
    padding: '0.75rem 2rem',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    cursor: 'pointer',
    fontWeight: 'bold',
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
    maxWidth: '500px',
    width: '90%',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    marginTop: '1rem',
  },
  input: {
    padding: '0.75rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '1rem',
    outline: 'none',
  },
  modalButtons: {
    display: 'flex',
    gap: '1rem',
    marginTop: '0.5rem',
  },
  cancelButton: {
    flex: 1,
    padding: '0.75rem',
    background: '#e0e0e0',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    cursor: 'pointer',
  },
  submitButton: {
    flex: 1,
    padding: '0.75rem',
    background: '#27ae60',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
};

export default ShoppingLists;
