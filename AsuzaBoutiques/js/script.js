// --- LOGIQUE DU CARROUSEL ---
let index = 0;
const slides = document.querySelectorAll(".slide");
const nextBtn = document.querySelector(".next");
const prevBtn = document.querySelector(".prev");

function showSlide(i) {
    slides.forEach((slide) => { slide.style.display = "none"; });
    if (slides[i]) slides[i].style.display = "block";
}

function nextSlide() {
    if (slides.length === 0) return;
    index = (index + 1) % slides.length;
    showSlide(index);
}

function prevSlide() {
    if (slides.length === 0) return;
    index = (index - 1 + slides.length) % slides.length;
    showSlide(index);
}

if (nextBtn) nextBtn.addEventListener("click", nextSlide);
if (prevBtn) prevBtn.addEventListener("click", prevSlide);

if (slides.length > 0) {
    setInterval(nextSlide, 5000);
}

// --- LOGIQUE DU PANIER ---
const openCartBtn = document.getElementById('open-cart-btn');
const closeCartBtn = document.getElementById('close-cart-btn');
const cartDrawer = document.getElementById('cart-drawer');
const cartOverlay = document.getElementById('cart-overlay');
const cartItemsContainer = document.getElementById('cart-items');
const emptyCartMsg = document.getElementById('empty-cart-msg');
const cartTotalEl = document.getElementById('cart-total');
const cartCountEl = document.getElementById('cart-count');

let cart = [];

function openCart() {
    if (cartOverlay && cartDrawer) {
        cartOverlay.classList.remove('hidden');
        setTimeout(() => {
            cartOverlay.classList.remove('opacity-0');
            cartDrawer.classList.remove('translate-x-full');
        }, 10);
    }
}

function closeCart() {
    if (cartOverlay && cartDrawer) {
        cartOverlay.classList.add('opacity-0');
        cartDrawer.classList.add('translate-x-full');
        setTimeout(() => {
            cartOverlay.classList.add('hidden');
        }, 300);
    }
}

if (openCartBtn) openCartBtn.addEventListener('click', openCart);
if (closeCartBtn) closeCartBtn.addEventListener('click', closeCart);
if (cartOverlay) cartOverlay.addEventListener('click', closeCart);

window.addToCart = function(name, price, image) {
    cart.push({ name, price, image });
    updateCartUI();
    openCart();
};

window.removeFromCart = function(idx) {
    cart.splice(idx, 1);
    updateCartUI();
};

function updateCartUI() {
    if (!cartItemsContainer || !cartCountEl || !cartTotalEl) return;
    
    cartItemsContainer.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        if (emptyCartMsg) {
            cartItemsContainer.appendChild(emptyCartMsg);
            emptyCartMsg.style.display = 'block';
        }
    } else {
        if (emptyCartMsg) emptyCartMsg.style.display = 'none';
        
        cart.forEach((item, idx) => {
            total += item.price;
            
            const itemEl = document.createElement('div');
            itemEl.className = 'flex items-center space-x-4 border-b border-gray-100 pb-4';
            itemEl.innerHTML = `
                <img src="${item.image}" alt="${item.name}" class="w-16 h-20 object-cover">
                <div class="flex-1">
                    <h4 class="text-xs font-bold uppercase tracking-wider">${item.name}</h4>
                    <p class="text-sm text-gray-500 mt-1">${item.price.toFixed(2).replace('.', ',')} EUR</p>
                </div>
                <button onclick="removeFromCart(${idx})" class="text-xs tracking-widest uppercase text-red-500 hover:text-black transition">Retirer</button>
            `;
            cartItemsContainer.appendChild(itemEl);
        });
    }

    cartCountEl.textContent = cart.length;
    cartTotalEl.textContent = `${total.toFixed(2).replace('.', ',')} EUR`;
}

// --- LOGIQUE DE LA PAGE PRODUIT (MODALE) ---
const productModal = document.getElementById('product-modal');
const closeProductModalBtn = document.getElementById('close-modal-btn');
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const modalPrice = document.getElementById('modal-price');
const modalDesc = document.getElementById('modal-desc');
const modalAddBtn = document.getElementById('modal-add-btn');

let currentProduct = null;

// Ouvrir la fiche produit
window.openProductModal = function(name, price, image, description) {
    currentProduct = { name, price, image };
    
    // Injecter les données
    modalImage.src = image;
    modalTitle.textContent = name;
    modalPrice.textContent = `${price.toFixed(2).replace('.', ',')} EUR`;
    modalDesc.textContent = description;

    // Réinitialiser les tailles
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('border-black', 'bg-black', 'text-white'));

    // Afficher la modale avec un effet de fondu
    productModal.classList.remove('hidden');
    setTimeout(() => {
        productModal.classList.remove('opacity-0');
    }, 10);
    
    // Empêcher le défilement de la page en arrière-plan
    document.body.style.overflow = 'hidden';
};

// Fermer la fiche produit
function closeProductModal() {
    productModal.classList.add('opacity-0');
    setTimeout(() => {
        productModal.classList.add('hidden');
        document.body.style.overflow = 'auto'; // Réactiver le scroll
    }, 500); // 500ms correspond à la durée de la transition CSS
}

if (closeProductModalBtn) closeProductModalBtn.addEventListener('click', closeProductModal);

// Gérer la sélection des tailles
const sizeBtns = document.querySelectorAll('.size-btn');
sizeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Enlever la sélection de tous les boutons
        sizeBtns.forEach(b => b.classList.remove('border-black', 'bg-black', 'text-white'));
        // Ajouter la sélection sur le bouton cliqué
        e.target.classList.add('border-black', 'bg-black', 'text-white');
    });
});

// Ajouter au panier depuis la modale
if (modalAddBtn) {
    modalAddBtn.addEventListener('click', () => {
        if (currentProduct) {
            // Appelle la fonction d'ajout au panier que nous avons créée précédemment
            addToCart(currentProduct.name, currentProduct.price, currentProduct.image);
            closeProductModal(); // Ferme la fiche produit pour voir le tiroir du panier
        }
    });
}