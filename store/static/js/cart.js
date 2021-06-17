var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) 
{
    // When the button is pressed
    updateBtns[i].addEventListener('click', function () {
        // Set the variables below to the data that is being passed through 
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        // If the user is a guest user 
        if (user == 'AnonymousUser') 
        {
            // Call addCookieitem and pass through the productId and the action 
            addCookieItem(productId, action)
            console.log('AnonymousUser')
        } 
        // If the user is a authenticated user
        else 
        {
            // Call updateStudentOrder and pass through the productId and the action 
            updateStudentOrder(productId, action)
        }
    })
}

function updateStudentOrder(productId, action) 
{
    console.log('User is authenticated, sending data...')

    // update_item URL 
    var url = '/update_item/'

    // Send corresponding data into the update_item view
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log('data', data)
        });
    
    // Reload the page 
    location.reload()
}

// This sets up the calculator page after a guest visitor selects a material 
function addCookieItem(productId, action) 
{
    // If the action was to add the product 
    if (action == 'add') 
    {
        // Add the product to the cart with quantity = 1
        cart[productId] = {'quantity': 1 },
        // Reload the page
        location.reload()
    }

    // if the action was to remove the product
    if (action == 'remove') 
    {
        // Delete the product from the cart 
        delete cart[productId];
    }
    
    // Send the cart data 
    console.log('CART:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}
