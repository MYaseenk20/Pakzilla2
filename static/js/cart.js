const update_button=document.getElementsByClassName('update-cart');
console.log(update_button)
for(var i=0; i<update_button.length; i++){
    update_button[i].addEventListener('click',function(e){
        e.preventDefault();
        var productid=this.dataset.product;
        var action=this.dataset.action;
        console.log('productid',productid,'action',action)
        if(user=='AnonymousUser'){
            addCookieitem(productid,action)
        }
        else{
            updatecartuser(productid,action)
        }
    })
}
function addCookieitem(productid,action){
    if(action == 'add'){
        if(cart[productid]===undefined){
            cart[productid]={'quantity':1}
        }else{
            cart[productid]['quantity']+=1
        }
           }
    if(action == 'remove'){
        cart[productid][quantity]-=1
        if(cart[productid]['quantity']<=0){
        console.log('item should be deleted')
        delete cart[productid]
        }
    }
      document.location.reload(true);
      location.reload();
      window.location.reload();

     console.log('cart:',cart)
    document.cookie='cart=' + JSON.stringify(cart) + ';domain;path=/'
}






function updatecartuser(productid,action){
    var url='/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
        'content-type':'application/json',
         'X-CSRFToken':csrftoken,
         },
    body:JSON.stringify({'productid':productid,'action':action})
    })
   .then((response)=>{
        return response.json()
   })
   .then((data)=>{
        console.log('data:',data)
        document.location.reload(true);
   })
        window.location.reload();

}


























