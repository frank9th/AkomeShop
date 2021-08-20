

const paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener("submit", payWithPaystack, false);
function payWithPaystack(e) {
  e.preventDefault();
  let handler = PaystackPop.setup({
    key: 'pk_test_be1fde51bac01013e0eb9cc23355f7237ea80261', // Replace with your public key

    //email = $("#email-address").value();
    email: document.getElementById("email-address").value,
    amount: document.getElementById("amount").value * 100,
    ref: document.getElementById("ref").value,

    //ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
    // label: "Optional string that replaces customer email"
    onClose: function(){
      alert('Window closed.');
    },
    callback: function(response){
      location.replace('/confirm/' + response.reference )
      let message = 'Payment complete! Reference: ' + response.reference ;
      $("#alert").show();
      $("#alert").text(message)
      //alert(message);

      $.ajax({
        type: "GET",
        url : "/confirm/" + response.reference,
        success:function(data){
          if (response.data.status == 200){
            console.log('payment succesfull')
          }
          console.log(data.status)

        }
            

      });
      


    }
  });
  handler.openIframe();
};





