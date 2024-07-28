document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'https://jsonplaceholder.typicode.com/posts';

    function fetchProducts() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('productsContainer');
                container.innerHTML = '';
                data.forEach(product => {
                    const card = document.createElement('div');
                    card.className = 'product-card';
                    card.innerHTML = `
                        <h3>${product.title}</h3>
                        <p class="price">$${Math.floor(Math.random() * 100)}</p> <!-- استفاده از قیمت تصادفی برای تست -->
                        <p>${product.body}</p>
                        <div class="actions">
                            <button onclick="editProduct(${product.id})">edit</button>
                            <button onclick="deleteProduct(${product.id})">delete</button>
                        </div>
                    `;
                    container.appendChild(card);
                });
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    function showModal(title, product = {}) {
        const modal = document.getElementById('modal');
        const modalTitle = document.getElementById('modalTitle');
        const form = document.getElementById('productForm');
        
        modalTitle.textContent = title;
        form.reset();
        document.getElementById('productId').value = product.id || '';
        
        if (product.id) {
            document.getElementById('title').value = product.title;
            document.getElementById('price').value = Math.floor(Math.random() * 100); // قیمت تصادفی برای تست
            document.getElementById('description').value = product.body;
        }
        
        modal.classList.remove('hidden');
    }

    document.getElementById('addProductBtn').addEventListener('click', () => {
        showModal('افزودن محصول جدید');
    });

    document.getElementById('productForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const id = document.getElementById('productId').value;
        const title = document.getElementById('title').value;
        const price = document.getElementById('price').value;
        const description = document.getElementById('description').value;
        
        const method = id ? 'PATCH' : 'POST';
        const url = id ? `${apiUrl}/${id}` : apiUrl;
        
        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, body: description })
        })
        .then(response => {
            if (response.ok) {
                fetchProducts(); // داده‌ها را مجدداً از API بارگذاری می‌کنیم تا تغییرات نمایش داده شوند
                document.getElementById('modal').classList.add('hidden');
            } else {
                throw new Error('Error saving product');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('modal').classList.add('hidden');
    });

    window.editProduct = function(id) {
        fetch(`${apiUrl}/${id}`)
            .then(response => response.json())
            .then(product => {
                showModal('ویرایش محصول', product);
            })
            .catch(error => console.error('Error fetching product:', error));
    };

    window.deleteProduct = function(id) {
        if (confirm('آیا مطمئن هستید که می‌خواهید این محصول را حذف کنید؟')) {
            fetch(`${apiUrl}/${id}`, {
                method: 'DELETE',
            })
            .then(response => {
                if (response.ok) {
                    fetchProducts(); // داده‌ها را مجدداً از API بارگذاری می‌کنیم تا تغییرات نمایش داده شوند
                } else {
                    throw new Error('Error deleting product');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    };

    fetchProducts();
});
