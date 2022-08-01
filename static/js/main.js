const alert = document.getElementById('alert');
const empty = document.getElementById('empty');

setTimeout(function() {
    alert.style.display = 'none';
}, 2500);

setTimeout(function() {
    empty.style.display = 'block';
}, 2500);
