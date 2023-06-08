document.addEventListener('DOMContentLoaded', () => {
    const cartItems = document.getElementById('cart-items');
    const totalAmount = document.getElementById('total-amount');
    const checkoutButton = document.getElementById('checkout-button');
  
    // Function to dynamically add selected items and quantities to the cart
    function addToCart(item, quantity) {
      const cartItem = document.createElement('div');
      cartItem.classList.add('cart-item');
      cartItem.innerHTML = `
        <span class="item-name">${item}</span>
        <span class="item-quantity">${quantity}</span>
      `;
      cartItems.appendChild(cartItem);
    }
  
    // Function to calculate and update the total amount
    function updateTotal() {
      const items = document.getElementsByClassName('cart-item');
      let total = 0;
      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const quantity = parseInt(item.querySelector('.item-quantity').innerText);
        total += quantity;
      }
      totalAmount.innerText = `$${total.toFixed(2)}`;
    }
  
    // Event listener for checkout button
    checkoutButton.addEventListener('click', () => {
      // Implement your checkout logic here
    });
  
    // Usage example:
    addToCart('Item 1', 2);
    addToCart('Item 2', 1);
    updateTotal();
  });
  