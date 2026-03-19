document.addEventListener('DOMContentLoaded', () => {
  const gridEl = document.getElementById('game-grid');
  const feedbackForm = document.getElementById('feedback-form');
  const formStatus = document.getElementById('form-status');

  // Render games to the grid
  function renderGames(gamesArray) {
    if (!gamesArray || gamesArray.length === 0) {
      gridEl.innerHTML = '<div class="error-message" style="background:#f9f2e0; border-left-color:#c4a24b;">✖ no games received</div>';
      return;
    }

    const cardsHTML = gamesArray.map(game => {
      const cover = game.cover_url || 'https://picsum.photos/300/180?grayscale';
      const url = game.url || '#';
      const price = game.price || (game.min_price === 0 ? 'Free' : (game.min_price ? `$${(game.min_price/100).toFixed(2)}` : 'Free'));
      
      const isAdult = game.classification === 'adult' || true; // Forzamos true para esta integración
      return `
        <a href="${url}" target="_blank" rel="noopener noreferrer" class="game-card ${isAdult ? 'adult-content' : ''}">
          <img class="game-cover" src="${cover}" alt="${game.title} cover" loading="lazy">
          <div class="card-content">
            <div class="game-title">${game.title}</div>
            <div class="game-meta">
              <span class="game-author">${game.user ? game.user.username : 'unknown'}</span>
              <span class="game-price">${price}</span>
            </div>
          </div>
        </a>
      `;
    }).join('');

    gridEl.innerHTML = cardsHTML;
  }

  // Fetch games from our local proxy API
  async function fetchItchGames() {
    try {
      // Fetching from the local proxy to avoid CORS and hide API key
      const response = await fetch('/api/games');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.games || [];
    } catch (error) {
      console.error("Error fetching games:", error);
      throw error;
    }
  }

  function loadContent() {
    gridEl.innerHTML = '<div class="loader">⌛ contacting itch.io ...</div>';
    fetchItchGames()
      .then(games => renderGames(games))
      .catch(() => {
        gridEl.innerHTML = '<div class="error-message">⚡ failed to fetch from itch.io</div>';
      });
  }

  // Handle feedback form submission
  if (feedbackForm) {
    feedbackForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const submitBtn = feedbackForm.querySelector('.submit-btn');
      const formData = new FormData(feedbackForm);
      const data = Object.fromEntries(formData.entries());
      
      submitBtn.disabled = true;
      submitBtn.textContent = 'Enviando...';
      formStatus.className = 'form-status';
      
      try {
        const response = await fetch('/api/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Error al enviar');
        
        formStatus.textContent = '¡Gracias por tu feedback! El mensaje ha sido enviado.';
        formStatus.className = 'form-status success';
        feedbackForm.reset();
      } catch (error) {
        formStatus.textContent = 'Hubo un error al enviar el mensaje. Por favor, intenta de nuevo.';
        formStatus.className = 'form-status error';
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Feedback';
      }
    });
  }

  // Initialize
  loadContent();

  // Register Service Worker for PWA
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .then((registration) => {
          console.log('ServiceWorker registration successful with scope: ', registration.scope);
        }, (err) => {
          console.log('ServiceWorker registration failed: ', err);
        });
    });
  }
});
