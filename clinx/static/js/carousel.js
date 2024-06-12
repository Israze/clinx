let currentIndex = 0;
  const items = document.querySelectorAll('.carousel-item');
  const totalItems = items.length;

  function showItem(index) {
    items.forEach(item => {
      item.style.transform = `translateX(-${index * 100}%)`;
    });
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % totalItems;
    showItem(currentIndex);
  }

  function prevSlide() {
    currentIndex = (currentIndex - 1 + totalItems) % totalItems;
    showItem(currentIndex);
  }