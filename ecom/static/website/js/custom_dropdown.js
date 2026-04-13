



//sticky
var sticky_menu = document.getElementById("header_sticky");
    
$(window).scroll(function() {
    const scrollTop = $(window).scrollTop();
    
    if (scrollTop > 300) {
        sticky_menu.classList.add('sticky');
    } else if( scrollTop < 100){
        sticky_menu.classList.remove('sticky');
    }
});




document.addEventListener('click', function (event) {
    const pocketBox = document.getElementById('cart-pocket-box');
    const pocketContainer = document.getElementById('pocket-container');
    const cartButtons = document.querySelectorAll('.cart-qty-box');

    const clickedOutsideCurrencyButtons = !Array.from(cartButtons).some((button) => button.contains(event.target));
    if (!pocketContainer.contains(event.target) && clickedOutsideCurrencyButtons) {
        pocketBox.style.display = 'none';
        document.body.classList.remove('item-modal-open');
    }
});


//Pocket
function cart_open() {

    document.body.classList.remove('modal-open');
    document.getElementById('currency-box').style.display = 'none';

    const pocketBox = document.getElementById('cart-pocket-box');
    const pocketContainer = document.getElementById('pocket-container');
    console.log(pocketBox, pocketContainer);
    
    if (!pocketBox || !pocketContainer) {
        console.error('Required elements not found.');
        return;
    }

    if (pocketBox.style.display === 'block') {
        pocketBox.style.display = 'none';
        document.body.classList.remove('item-modal-open');
    } else {
        pocketBox.style.display = 'block';
        document.body.classList.add('item-modal-open');
    }

}

// For cart pocket
document.addEventListener('DOMContentLoaded', () => {
    // Add event listeners to all plus buttons
    document.querySelectorAll('.plus').forEach(button => {
        button.addEventListener('click', () => {
            // Get the associated input field
            const input = button.parentElement.querySelector('.pocket_qty');
            if (input) {
                const max = parseInt(input.getAttribute('max')) || Infinity;
                let value = parseInt(input.value) || 0;

                // Increment value if below the max limit
                if (value < max) {
                    input.value = value + 1;
                }
            }
        });
    });

    // Add event listeners to all minus buttons
    document.querySelectorAll('.minus').forEach(button => {
        button.addEventListener('click', () => {
            // Get the associated input field
            const input = button.parentElement.querySelector('.pocket_qty');
            if (input) {
                const min = parseInt(input.getAttribute('min')) || 0;
                let value = parseInt(input.value) || 0;

                // Decrement value if above the min limit
                if (value > min) {
                    input.value = value - 1;
                }
            }
        });
    });
});


function closeCartPopup() {
    document.body.classList.remove('item-modal-open');
    document.getElementById('cart-pocket-box').style.display = 'none';
}

setTimeout(function() {
    const messagesElement = document.querySelector(".messages");
    if (messagesElement) {
        messagesElement.style.display = "none";
    }
}, 3000);

const errorElements = document.querySelectorAll('.error');
errorElements.forEach((element) => {
  setTimeout(() => {
    element.style.display = 'none';
  }, 3000);
});

function search_box() {
    document.getElementById('search-box').classList.add('active');
}
$(document).click(function (event) {
    if (!$(event.target).closest('#search-box').length) {
        $('#search-box').removeClass('active');
    }
});
