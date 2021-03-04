
var updateBtns = document.getElementsByClassName('update-cart')

/*
js function for add to cart funtion 
first we get element by the class name, and then we created a loop to loop through
function - when i is less than 0, it should be incremented
assigning i to the function name (updateBtns)

*/

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('ProductId:', productId, 'Action:', action)

		console.log('USER:', user)
		if (user === 'AnonymousUser'){
			console.log('Not logged in')

		}else {
			updateUserOrder(productId, action)
		}

		})
	
}

function updateUserOrder(productId, action){
	console.log('USER is logged in, sending data...')

	var url = '/update_item/'

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,

		}, 
		// JSON.stringify means- to convert or send the data as string 
		body:JSON.stringify({'productId': productId, 'action':action})
	})
	.then((response) =>{
		return response.json()
	})

	.then((data) =>{
		console.log('data:', data)
		// this will reload the page each time the add or remove function is called 
		location.reload()
	});



}
