function changeImage(thumb) {
    document.querySelector('.main-image img').src = thumb.src.replace('&w=150', '&w=1000');
    document.querySelectorAll('.thumbnails img').forEach(img => img.classList.remove('active'));
    thumb.classList.add('active');
}

document.querySelectorAll('.color-select').forEach(color => {
    color.addEventListener('click', function() {
        document.querySelectorAll('.color-select').forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
    });
});

const qtyInput = document.getElementById('qty');
function increment() {
    qtyInput.value = parseInt(qtyInput.value) + 1;
}
function decrement() {
    if(parseInt(qtyInput.value) > 1) {
        qtyInput.value = parseInt(qtyInput.value) - 1;
    }
}

function addToCart() {
    const btn = document.querySelector('.add-to-cart');
    const toast = document.getElementById('toast');
    const cartCount = document.querySelector('.cart-count');
    
    // Animation
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    
    setTimeout(() => {
        btn.innerHTML = 'Add to Cart';
        
        // Show Toast
        toast.className = 'show';
        setTimeout(() => { toast.className = toast.className.replace('show', ''); }, 3000);

        // Update Cart
        let currentCount = parseInt(cartCount.innerText);
        cartCount.innerText = currentCount + parseInt(qtyInput.value);
    }, 800);
}
