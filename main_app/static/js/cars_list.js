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
                if (b)  {
                    const span = document.createElement('span');
                    span.textContent = 'Request sent!';
                    span.style.cssText = 'float:right; padding: 2px 2px;';
                    b.replaceWith(span);
                }
            }
            fetch(`/cars/${carId}/book/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            });
        });
    });
});