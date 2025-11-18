import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { FaArrowLeft, FaPlus, FaTrash, FaMagic, FaExchangeAlt, FaLeaf, FaSpinner } from 'react-icons/fa';
import Swal from 'sweetalert2';

const ShoppingListDetail = () => {
  const { id } = useParams();
  const [list, setList] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [optimizing, setOptimizing] = useState(false);
  const [substituting, setSubstituting] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [editingBudget, setEditingBudget] = useState(false);
  const [newBudget, setNewBudget] = useState('');

  useEffect(() => {
    loadListDetails();
    loadProducts();
  }, [id]);

  const loadListDetails = async () => {
    try {
      const response = await api.get(`/shopping-lists/${id}`);
      setList(response.data);
    } catch (err) {
      console.error('Error loading list');
    } finally {
      setLoading(false);
    }
  };

  const loadProducts = async () => {
    try {
      const response = await api.get('/products/');
      setProducts(response.data);
    } catch (err) {
      console.error('Error loading products');
    }
  };

  const handleAddItem = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/shopping-lists/${id}/items`, {
        product_id: parseInt(selectedProduct),
        quantity: parseInt(quantity)
      });
      setShowAddModal(false);
      setSelectedProduct('');
      setQuantity(1);
      loadListDetails();
    } catch (err) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'No se pudo agregar el producto'
      });
    }
  };

  const handleRemoveItem = async (itemId) => {
    const result = await Swal.fire({
      title: '¿Eliminar producto?',
      text: 'Esta acción no se puede deshacer',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#e74c3c',
      cancelButtonColor: '#95a5a6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    });
    
    if (!result.isConfirmed) return;
    
    try {
      await api.delete(`/shopping-lists/${id}/items/${itemId}`);
      loadListDetails();
      Swal.fire('Eliminado', 'Producto eliminado de la lista', 'success');
    } catch (err) {
      Swal.fire('Error', 'No se pudo eliminar el producto', 'error');
    }
  };

  const handleUpdateQuantity = async (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    
    try {
      await api.patch(`/shopping-lists/${id}/items/${itemId}`, {
        quantity: parseInt(newQuantity)
      });
      loadListDetails();
    } catch (err) {
      Swal.fire('Error', 'No se pudo actualizar la cantidad', 'error');
    }
  };

  const handleUpdateBudget = async () => {
    if (!newBudget || newBudget <= 0) {
      Swal.fire('Error', 'El presupuesto debe ser mayor a 0', 'error');
      return;
    }
    
    try {
      await api.patch(`/shopping-lists/${id}`, {
        budget: parseFloat(newBudget)
      });
      setEditingBudget(false);
      loadListDetails();
      Swal.fire('Actualizado', 'Presupuesto actualizado correctamente', 'success');
    } catch (err) {
      Swal.fire('Error', 'No se pudo actualizar el presupuesto', 'error');
    }
  };

  const handleOptimize = async () => {
    setOptimizing(true);
    try {
      const response = await api.post(`/shopping-lists/${id}/optimize`, {
        budget: list.budget
      });
      
      // Mostrar resultados de la optimización
      const result = response.data;
      await loadListDetails();
      
      Swal.fire({
        icon: 'success',
        title: '¡Lista optimizada!',
        html: `
          <div style="text-align: left; padding: 10px;">
            <p><strong>Productos seleccionados:</strong> ${result.selected_items || 0}</p>
            <p><strong>Costo total:</strong> $${result.total_cost?.toLocaleString() || 0}</p>
            <p><strong>Eco-score promedio:</strong> ${result.average_eco_score?.toFixed(1) || 0}</p>
            <p><strong>Presupuesto:</strong> $${list.budget?.toLocaleString()}</p>
          </div>
        `,
        confirmButtonColor: '#27ae60'
      });
    } catch (err) {
      console.error('Error al optimizar:', err);
      Swal.fire({
        icon: 'error',
        title: 'Error al optimizar',
        text: err.response?.data?.detail || err.message
      });
    } finally {
      setOptimizing(false);
    }
  };

  const handleSubstitute = async () => {
    setSubstituting(true);
    try {
      const response = await api.post(`/shopping-lists/${id}/substitute`);
      const result = response.data;
      const subs = result.substitutions || [];
      
      if (subs.length === 0) {
        Swal.fire({
          icon: 'info',
          title: 'Sin sustituciones',
          text: 'No se encontraron alternativas más sostenibles para esta lista',
          confirmButtonColor: '#3498db'
        });
        setSubstituting(false);
        return;
      }

      // Mostrar cada sustitución para que el usuario decida
      let accepted = 0;
      let totalSavings = 0;
      let totalScoreImprovement = 0;

      for (const sub of subs) {
        const result = await Swal.fire({
          title: '¿Aceptar sustitución?',
          html: `
            <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center; padding: 20px;">
              <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <h3 style="margin: 0 0 10px 0; color: #e74c3c;">Actual</h3>
                <p style="font-size: 1.1rem; font-weight: bold; margin: 5px 0;">${sub.original.name}</p>
                <p style="color: #666; margin: 5px 0;">Precio: $${sub.original.price}</p>
                <p style="color: #666; margin: 5px 0;">Eco-score: ${sub.original.eco_score}/100</p>
              </div>
              
              <div style="font-size: 2rem; color: #27ae60;">→</div>
              
              <div style="text-align: center; padding: 15px; background: #e8f5e9; border-radius: 8px;">
                <h3 style="margin: 0 0 10px 0; color: #27ae60;">Alternativa</h3>
                <p style="font-size: 1.1rem; font-weight: bold; margin: 5px 0;">${sub.substitute.name}</p>
                <p style="color: #666; margin: 5px 0;">Precio: $${sub.substitute.price}</p>
                <p style="color: #27ae60; font-weight: bold; margin: 5px 0;">Eco-score: ${sub.substitute.eco_score}/100</p>
              </div>
            </div>
            <div style="margin-top: 15px; padding: 10px; background: #fff3cd; border-radius: 5px;">
              <p style="margin: 5px 0;"><strong>Razón:</strong> ${sub.reason}</p>
              <p style="margin: 5px 0;"><strong>Diferencia de precio:</strong> $${sub.savings > 0 ? '+' : ''}${sub.savings.toFixed(0)}</p>
              <p style="margin: 5px 0;"><strong>Mejora eco-score:</strong> +${sub.score_improvement.toFixed(1)} puntos</p>
            </div>
          `,
          icon: 'question',
          showCancelButton: true,
          confirmButtonColor: '#27ae60',
          cancelButtonColor: '#95a5a6',
          confirmButtonText: '✓ Aceptar',
          cancelButtonText: '✗ Rechazar',
          width: '700px'
        });

        if (result.isConfirmed) {
          // Aplicar la sustitución
          try {
            const itemToUpdate = list.items.find(item => item.product.id === sub.original.id);
            if (itemToUpdate) {
              // Eliminar el item original
              await api.delete(`/shopping-lists/${id}/items/${itemToUpdate.id}`);
              // Agregar el sustituto
              await api.post(`/shopping-lists/${id}/items`, {
                product_id: sub.substitute.id,
                quantity: itemToUpdate.quantity
              });
              accepted++;
              totalSavings += sub.savings;
              totalScoreImprovement += sub.score_improvement;
            }
          } catch (err) {
            console.error('Error applying substitution:', err);
          }
        }
      }

      // Recargar lista
      await loadListDetails();

      // Mostrar resumen
      if (accepted > 0) {
        Swal.fire({
          icon: 'success',
          title: `¡${accepted} productos sustituidos!`,
          html: `
            <div style="text-align: center; padding: 10px;">
              <p><strong>Ahorro total:</strong> $${Math.abs(totalSavings).toFixed(0)}</p>
              <p><strong>Mejora eco-score:</strong> +${totalScoreImprovement.toFixed(1)}</p>
            </div>
          `,
          confirmButtonColor: '#27ae60'
        });
      } else {
        Swal.fire({
          icon: 'info',
          title: 'Sin cambios',
          text: 'No se aceptaron sustituciones',
          confirmButtonColor: '#3498db'
        });
      }
    } catch (err) {
      console.error('Error al sustituir:', err);
      Swal.fire({
        icon: 'error',
        title: 'Error al sustituir',
        text: err.response?.data?.detail || err.message
      });
    } finally {
      setSubstituting(false);
    }
  };

  if (loading) return <div style={styles.loading}>Cargando...</div>;
  if (!list) return <div style={styles.error}>Lista no encontrada</div>;

  const budgetUsage = list.total_cost && list.budget ? (list.total_cost / list.budget) * 100 : 0;
  const budgetColor = budgetUsage > 100 ? '#e74c3c' : budgetUsage > 80 ? '#f39c12' : '#27ae60';

  return (
    <div style={styles.container}>
      <Link to="/shopping-lists" style={styles.backButton}>
        <FaArrowLeft /> Volver a mis listas
      </Link>

      <div style={styles.header}>
        <div>
          <h1>{list.name}</h1>
          {editingBudget ? (
            <div style={{display: 'flex', gap: '10px', alignItems: 'center', marginTop: '10px'}}>
              <span>Presupuesto: $</span>
              <input
                type="number"
                value={newBudget}
                onChange={(e) => setNewBudget(e.target.value)}
                style={styles.budgetInput}
                autoFocus
              />
              <button onClick={handleUpdateBudget} style={styles.saveBudgetButton}>✓</button>
              <button onClick={() => setEditingBudget(false)} style={styles.cancelBudgetButton}>✕</button>
            </div>
          ) : (
            <p style={styles.subtitle}>
              Presupuesto: ${list.budget?.toLocaleString()}
              <button 
                onClick={() => {
                  setNewBudget(list.budget);
                  setEditingBudget(true);
                }} 
                style={styles.editBudgetButton}
              >
                ✏️
              </button>
            </p>
          )}
        </div>
        <button onClick={() => setShowAddModal(true)} style={styles.addButton}>
          <FaPlus /> Agregar Producto
        </button>
      </div>

      {list.total_cost && (
        <div style={styles.summary}>
          <div style={styles.summaryCard}>
            <div style={styles.summaryLabel}>Costo Total</div>
            <div style={styles.summaryValue}>${list.total_cost.toLocaleString()}</div>
          </div>
          <div style={styles.summaryCard}>
            <div style={styles.summaryLabel}>Ahorro</div>
            <div style={{...styles.summaryValue, color: '#27ae60'}}>
              ${list.total_savings?.toLocaleString() || 0}
            </div>
          </div>
          <div style={styles.summaryCard}>
            <div style={styles.summaryLabel}>Eco Score</div>
            <div style={{...styles.summaryValue, color: '#27ae60'}}>
              <FaLeaf /> {list.total_eco_score?.toFixed(1) || 0}
            </div>
          </div>
          <div style={styles.summaryCard}>
            <div style={styles.summaryLabel}>Uso del Presupuesto</div>
            <div style={{...styles.summaryValue, color: budgetColor}}>
              {budgetUsage.toFixed(1)}%
            </div>
            <div style={styles.budgetBar}>
              <div style={{...styles.budgetBarFill, width: `${Math.min(budgetUsage, 100)}%`, background: budgetColor}} />
            </div>
          </div>
        </div>
      )}

      <div style={styles.actions}>
        <button onClick={handleOptimize} disabled={optimizing || !list.items?.length} style={styles.actionButton}>
          {optimizing ? <FaSpinner style={{animation: 'spin 1s linear infinite'}} /> : <FaMagic />}
          {optimizing ? 'Optimizando...' : 'Optimizar Lista'}
        </button>
        <button onClick={handleSubstitute} disabled={substituting || !list.items?.length} style={styles.actionButton}>
          {substituting ? <FaSpinner style={{animation: 'spin 1s linear infinite'}} /> : <FaExchangeAlt />}
          {substituting ? 'Sustituyendo...' : 'Buscar Alternativas'}
        </button>
      </div>

      {list.items && list.items.length > 0 ? (
        <div style={styles.items}>
          <h2>Productos en la Lista</h2>
          <div style={styles.itemsGrid}>
            {list.items.map(item => (
              <div key={item.id} style={styles.itemCard}>
                <div style={styles.itemHeader}>
                  <div>
                    {item.is_substituted && (
                      <div style={styles.substituteBadge}>
                        <FaExchangeAlt /> Producto Sustituido
                      </div>
                    )}
                    <Link to={`/products/${item.product.id}`} style={styles.itemName}>
                      {item.product.name}
                    </Link>
                  </div>
                  <button onClick={() => handleRemoveItem(item.id)} style={styles.removeButton}>
                    <FaTrash />
                  </button>
                </div>

                <p style={styles.itemBrand}>{item.product.brand}</p>
                
                <div style={styles.itemDetails}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
                    <span style={styles.itemLabel}>Cantidad:</span>
                    <button 
                      onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                      style={styles.quantityButton}
                      disabled={item.quantity <= 1}
                    >
                      -
                    </button>
                    <input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) => handleUpdateQuantity(item.id, e.target.value)}
                      style={styles.quantityInput}
                    />
                    <button 
                      onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                      style={styles.quantityButton}
                    >
                      +
                    </button>
                  </div>
                  <div>
                    <span style={styles.itemLabel}>Precio unitario:</span>
                    <span style={styles.itemValue}>${item.product.price.toLocaleString()}</span>
                  </div>
                  <div>
                    <span style={styles.itemLabel}>Subtotal:</span>
                    <span style={{...styles.itemValue, fontWeight: 'bold', color: '#27ae60'}}>
                      ${(item.product.price * item.quantity).toLocaleString()}
                    </span>
                  </div>
                </div>

                <div style={styles.ecoScore}>
                  <FaLeaf style={{color: '#27ae60'}} />
                  <span>Eco Score: {item.product.eco_score}/100</span>
                </div>

                {item.original_product_id && (
                  <div style={styles.originalProduct}>
                    <small>Reemplazó producto anterior para mejor sostenibilidad</small>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div style={styles.empty}>
          <p>No hay productos en esta lista</p>
          <button onClick={() => setShowAddModal(true)} style={styles.emptyButton}>
            Agregar Primer Producto
          </button>
        </div>
      )}

      {showAddModal && (
        <div style={styles.modal}>
          <div style={styles.modalContent}>
            <h2>Agregar Producto</h2>
            <form onSubmit={handleAddItem} style={styles.form}>
              <select
                value={selectedProduct}
                onChange={(e) => setSelectedProduct(e.target.value)}
                required
                style={styles.select}
              >
                <option value="">Selecciona un producto</option>
                {products.map(product => (
                  <option key={product.id} value={product.id}>
                    {product.name} - ${product.price} ({product.brand})
                  </option>
                ))}
              </select>
              
              <input
                type="number"
                placeholder="Cantidad"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                required
                min="1"
                style={styles.input}
              />

              <div style={styles.modalButtons}>
                <button type="button" onClick={() => setShowAddModal(false)} style={styles.cancelButton}>
                  Cancelar
                </button>
                <button type="submit" style={styles.submitButton}>
                  Agregar
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
  backButton: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem',
    color: '#27ae60',
    textDecoration: 'none',
    marginBottom: '1.5rem',
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
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
  },
  subtitle: {
    color: '#666',
    fontSize: '1.1rem',
  },
  addButton: {
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
  summary: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '1.5rem',
    marginBottom: '2rem',
  },
  summaryCard: {
    background: 'white',
    padding: '1.5rem',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  summaryLabel: {
    color: '#666',
    fontSize: '0.9rem',
    marginBottom: '0.5rem',
  },
  summaryValue: {
    fontSize: '1.8rem',
    fontWeight: 'bold',
    color: '#333',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
  },
  budgetBar: {
    height: '8px',
    background: '#e0e0e0',
    borderRadius: '4px',
    marginTop: '0.5rem',
    overflow: 'hidden',
  },
  budgetBarFill: {
    height: '100%',
    transition: 'width 0.5s',
  },
  actions: {
    display: 'flex',
    gap: '1rem',
    marginBottom: '2rem',
  },
  actionButton: {
    flex: 1,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '0.5rem',
    background: '#3498db',
    color: 'white',
    padding: '1rem',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    cursor: 'pointer',
    fontWeight: 'bold',
  },
  items: {
    background: 'white',
    padding: '2rem',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  itemsGrid: {
    display: 'grid',
    gap: '1.5rem',
    marginTop: '1.5rem',
  },
  itemCard: {
    padding: '1.5rem',
    background: '#f9f9f9',
    borderRadius: '8px',
    position: 'relative',
  },
  substituteBadge: {
    background: '#e8f5e9',
    color: '#27ae60',
    padding: '0.5rem 0.75rem',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: 'bold',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.3rem',
    marginBottom: '0.5rem',
  },
  quantityButton: {
    background: '#3498db',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    width: '30px',
    height: '30px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold',
  },
  quantityInput: {
    width: '60px',
    textAlign: 'center',
    border: '1px solid #ddd',
    borderRadius: '4px',
    padding: '5px',
    fontSize: '14px',
  },
  budgetInput: {
    width: '120px',
    padding: '8px',
    fontSize: '16px',
    border: '2px solid #3498db',
    borderRadius: '5px',
    textAlign: 'right',
  },
  editBudgetButton: {
    marginLeft: '10px',
    background: 'transparent',
    border: 'none',
    cursor: 'pointer',
    fontSize: '16px',
  },
  saveBudgetButton: {
    background: '#27ae60',
    color: 'white',
    border: 'none',
    padding: '8px 12px',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  cancelBudgetButton: {
    background: '#e74c3c',
    color: 'white',
    border: 'none',
    padding: '8px 12px',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '18px',
    fontWeight: 'bold',
  },
  itemHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'start',
    marginBottom: '0.5rem',
  },
  itemName: {
    fontSize: '1.2rem',
    fontWeight: 'bold',
    color: '#333',
    textDecoration: 'none',
  },
  removeButton: {
    background: '#e74c3c',
    color: 'white',
    border: 'none',
    padding: '0.5rem 0.75rem',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  itemBrand: {
    color: '#666',
    marginBottom: '1rem',
  },
  itemDetails: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '0.75rem',
    marginBottom: '0.75rem',
  },
  itemLabel: {
    color: '#666',
    fontSize: '0.9rem',
    marginRight: '0.5rem',
  },
  itemValue: {
    color: '#333',
    fontWeight: '500',
  },
  ecoScore: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    color: '#27ae60',
    fontWeight: 'bold',
  },
  originalProduct: {
    marginTop: '0.75rem',
    padding: '0.5rem',
    background: '#fff3cd',
    borderRadius: '5px',
    color: '#856404',
  },
  empty: {
    textAlign: 'center',
    padding: '4rem 2rem',
    background: 'white',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
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
  select: {
    padding: '0.75rem',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '1rem',
    outline: 'none',
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

export default ShoppingListDetail;
