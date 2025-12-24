document.querySelector('.newsletter button').addEventListener('click', function() {
    const input = document.querySelector('.newsletter input');
    if(input.value) {
        this.innerHTML = "Subscribed!";
        this.style.background = "#27ae60";
        input.value = "";
    } else {
        alert("Please enter a valid email.");
    }
});

// Parallax Effect
window.addEventListener('scroll', function() {
    const scrolled = window.scrollY;
    document.querySelector('.parallax-hero').style.backgroundPositionY = -(scrolled * 0.5) + 'px';
});
