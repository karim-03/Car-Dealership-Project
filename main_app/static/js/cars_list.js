function getCookie(name){
    const v = `; ${document.cookie}`;
    const parts = v.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.book-btn').forEach(function(btn){
        btn.addEventListener('click', function(){
            const carId = this.dataset.carId;
            const li = this.closest('li');
            if (li){
                const b = li.querySelector('.book-btn');
                if (b) b.replaceWith(document.createTextNode('- Request sent!'));
            }
            fetch(`/cars/${carId}/book/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            });
        });
    });
});