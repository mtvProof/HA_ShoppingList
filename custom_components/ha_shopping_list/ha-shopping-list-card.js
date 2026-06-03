class HAShoppingListCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please define an entity');
    }
    this.config = config;
  }

  set hass(hass) {
    if (!this.content) {
      const card = document.createElement('ha-card');
      card.innerHTML = `
        <div style="padding: 16px;">
          <iframe src="/api/ha_shopping_list/panel" 
                  style="width: 100%; height: 600px; border: none;">
          </iframe>
        </div>
      `;
      this.appendChild(card);
      this.content = card;
    }
  }

  getCardSize() {
    return 10;
  }
}

customElements.define('ha-shopping-list-card', HAShoppingListCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'ha-shopping-list-card',
  name: 'HA Shopping List Card',
  description: 'Shopping list with categories and recipes'
});
