// --- 1. SIMULATION DE BASE DE DONNÉES (LocalStorage) ---

// On récupère les produits sauvegardés, ou on crée un tableau vide si c'est la première fois
let products = JSON.parse(localStorage.getItem('zaraCloneProducts')) || [];

function saveProducts() {
    localStorage.setItem('zaraCloneProducts', JSON.stringify(products));
}

function renderTable() {
    const tableBody = document.getElementById('productTableBody');
    tableBody.innerHTML = ''; // On vide le tableau avant de le recréer

    products.forEach((product, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.category}</td>
            <td>${parseFloat(product.price).toFixed(2).replace('.', ',')} €</td>
            <td>
                <button class="btn-delete" onclick="deleteProduct(${index})">Supprimer</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
    
    // Met à jour le graphique des catégories à chaque modification
    updateCategoryChart();
}

function deleteProduct(index) {
    products.splice(index, 1); // Retire le produit du tableau
    saveProducts(); // Sauvegarde le nouveau tableau
    renderTable(); // Réaffiche la vue
}

// Ajout d'un produit via le formulaire
document.getElementById('productForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const newProduct = {
        name: document.getElementById('name').value,
        price: document.getElementById('price').value,
        category: document.getElementById('category').value,
        image: document.getElementById('image').value
    };

    products.push(newProduct);
    saveProducts();
    renderTable();

    this.reset(); // Vide le formulaire
});

// Affichage initial du tableau au chargement de la page
renderTable();


// --- 2. CONFIGURATION DES GRAPHIQUES (Chart.js) ---

// Graphique des ventes (Données statiques simulées)
const ctxSales = document.getElementById('salesChart').getContext('2d');
new Chart(ctxSales, {
    type: 'line',
    data: {
        labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        datasets: [{
            label: 'Ventes (€)',
            data: [420, 580, 450, 700, 950, 1200, 1245],
            borderColor: '#000000',
            backgroundColor: 'rgba(0, 0, 0, 0.05)',
            borderWidth: 2,
            fill: true,
            tension: 0.4 // Courbe douce
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            y: { beginAtZero: true, grid: { borderDash: [5, 5] } },
            x: { grid: { display: false } }
        }
    }
});

// Graphique de répartition par catégorie (Données dynamiques selon le LocalStorage)
let categoryChartInstance = null;

function updateCategoryChart() {
    // Calcul de la répartition
    let countFemme = products.filter(p => p.category === 'Femme').length;
    let countHomme = products.filter(p => p.category === 'Homme').length;
    let countAcc = products.filter(p => p.category === 'Accessoires').length;

    const ctxCategory = document.getElementById('categoryChart').getContext('2d');
    
    // Si le graphique existe déjà, on le détruit avant de le recréer pour éviter les bugs
    if (categoryChartInstance) {
        categoryChartInstance.destroy();
    }

    categoryChartInstance = new Chart(ctxCategory, {
        type: 'doughnut',
        data: {
            labels: ['Femme', 'Homme', 'Accessoires'],
            datasets: [{
                data: [countFemme, countHomme, countAcc],
                backgroundColor: ['#000000', '#777777', '#cccccc'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            cutout: '75%', // Règle l'épaisseur de l'anneau pour un look plus élégant
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}