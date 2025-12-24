/**
 * BLUEIDEALTECK - SMART SEASONAL & FESTIVAL EFFECTS SYSTEM
 * Automatically changes website theme based on:
 * - Current season (Spring, Summer, Fall, Winter)
 * - Major festivals (Christmas, Diwali, New Year, Holi, etc.)
 * - User's geographic location
 * - Cultural celebrations worldwide
 */

class SmartSeasonalEffects {
  constructor() {
    this.userLocation = null;
    this.currentDate = new Date();
    this.activeTheme = null;
    
    this.init();
  }

  async init() {
    // Get user's location
    await this.getUserLocation();
    
    // Determine and apply appropriate theme
    const theme = this.determineTheme();
    this.applyTheme(theme);
    
    // Check for theme changes every hour
    setInterval(() => {
      const newTheme = this.determineTheme();
      if (newTheme !== this.activeTheme) {
        this.applyTheme(newTheme);
      }
    }, 3600000); // 1 hour
  }

  async getUserLocation() {
    try {
      // Try to get location from IP
      const response = await fetch('https://ipapi.co/json/');
      const data = await response.json();
      
      this.userLocation = {
        country: data.country_code,
        countryName: data.country_name,
        region: data.region,
        city: data.city,
        latitude: data.latitude,
        longitude: data.longitude,
        timezone: data.timezone
      };
      
      console.log('User location detected:', this.userLocation);
    } catch (error) {
      // Fallback to India if location detection fails
      this.userLocation = {
        country: 'IN',
        countryName: 'India',
        region: 'Tamil Nadu',
        timezone: 'Asia/Kolkata'
      };
      console.log('Using default location (India)');
    }
  }

  determineTheme() {
    const month = this.currentDate.getMonth() + 1; // 1-12
    const day = this.currentDate.getDate();
    const country = this.userLocation?.country || 'IN';

    // Priority 1: Check for major festivals (highest priority)
    const festival = this.checkFestivals(month, day, country);
    if (festival) return festival;

    // Priority 2: Check for seasonal themes
    const season = this.getSeason(month, country);
    return season;
  }

  checkFestivals(month, day, country) {
    const festivals = {
      // Global Festivals
      'CHRISTMAS': { month: 12, days: [24, 25, 26], countries: ['ALL'] },
      'NEW_YEAR': { month: 1, days: [1, 2], countries: ['ALL'] },
      'NEW_YEAR_EVE': { month: 12, days: [31], countries: ['ALL'] },
      'VALENTINES': { month: 2, days: [14], countries: ['ALL'] },
      'HALLOWEEN': { month: 10, days: [31], countries: ['US', 'CA', 'GB', 'IE', 'AU'] },
      'THANKSGIVING': { month: 11, days: [23, 24, 25, 26], countries: ['US'] }, // 4th Thursday
      
      // Indian Festivals (approximate dates - these vary by lunar calendar)
      'DIWALI': { month: 10, days: [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31], countries: ['IN'] },
      'DIWALI_NOV': { month: 11, days: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], countries: ['IN'] },
      'HOLI': { month: 3, days: [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], countries: ['IN'] },
      'PONGAL': { month: 1, days: [14, 15, 16, 17], countries: ['IN'] },
      'INDEPENDENCE_DAY_IN': { month: 8, days: [15], countries: ['IN'] },
      'REPUBLIC_DAY_IN': { month: 1, days: [26], countries: ['IN'] },
      'GANESH_CHATURTHI': { month: 9, days: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], countries: ['IN'] },
      
      // Chinese Festivals
      'CHINESE_NEW_YEAR': { month: 1, days: [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31], countries: ['CN', 'TW', 'HK', 'SG'] },
      'CHINESE_NEW_YEAR_FEB': { month: 2, days: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], countries: ['CN', 'TW', 'HK', 'SG'] },
      
      // Islamic Festivals (approximate - vary by lunar calendar)
      'EID': { month: 4, days: [10, 11, 12, 13, 14, 15], countries: ['SA', 'AE', 'PK', 'BD', 'MY', 'ID'] },
      'EID_MAY': { month: 5, days: [1, 2, 3, 4, 5], countries: ['SA', 'AE', 'PK', 'BD', 'MY', 'ID'] },
      
      // Other Regional Festivals
      'INDEPENDENCE_DAY_US': { month: 7, days: [4], countries: ['US'] },
      'CANADA_DAY': { month: 7, days: [1], countries: ['CA'] },
      'BASTILLE_DAY': { month: 7, days: [14], countries: ['FR'] },
      'AUSTRALIA_DAY': { month: 1, days: [26], countries: ['AU'] },
      
      // Tech/Business Events
      'BLACK_FRIDAY': { month: 11, days: [24, 25, 26, 27, 28, 29], countries: ['ALL'] },
      'CYBER_MONDAY': { month: 11, days: [27, 28, 29, 30], countries: ['ALL'] },
    };

    for (const [festivalName, config] of Object.entries(festivals)) {
      if (config.month === month && config.days.includes(day)) {
        if (config.countries.includes('ALL') || config.countries.includes(country)) {
          return festivalName;
        }
      }
    }

    return null;
  }

  getSeason(month, country) {
    // Northern Hemisphere (US, Europe, India, China, etc.)
    const northernHemisphere = ['US', 'CA', 'GB', 'FR', 'DE', 'IN', 'CN', 'JP', 'KR'];
    // Southern Hemisphere (Australia, New Zealand, South America, South Africa)
    const southernHemisphere = ['AU', 'NZ', 'BR', 'AR', 'ZA'];

    const isNorthern = northernHemisphere.includes(country);
    const isSouthern = southernHemisphere.includes(country);

    if (isNorthern || !isSouthern) {
      // Northern Hemisphere Seasons
      if (month >= 3 && month <= 5) return 'SPRING';
      if (month >= 6 && month <= 8) return 'SUMMER';
      if (month >= 9 && month <= 11) return 'FALL';
      return 'WINTER'; // Dec, Jan, Feb
    } else {
      // Southern Hemisphere Seasons (opposite)
      if (month >= 3 && month <= 5) return 'FALL';
      if (month >= 6 && month <= 8) return 'WINTER';
      if (month >= 9 && month <= 11) return 'SPRING';
      return 'SUMMER'; // Dec, Jan, Feb
    }
  }

  applyTheme(theme) {
    if (this.activeTheme === theme) return;
    
    console.log(`Applying theme: ${theme}`);
    this.activeTheme = theme;

    // Remove all existing theme classes
    document.body.classList.remove(
      'theme-christmas', 'theme-new-year', 'theme-diwali', 'theme-holi',
      'theme-halloween', 'theme-valentines', 'theme-spring', 'theme-summer',
      'theme-fall', 'theme-winter', 'theme-independence', 'theme-eid',
      'theme-chinese-new-year', 'theme-pongal', 'theme-thanksgiving'
    );

    // Load appropriate CSS and JS
    this.loadThemeAssets(theme);

    // Add theme class to body
    const themeClass = `theme-${theme.toLowerCase().replace(/_/g, '-')}`;
    document.body.classList.add(themeClass);

    // Initialize theme-specific effects
    this.initializeThemeEffects(theme);
  }

  loadThemeAssets(theme) {
    const themeMap = {
      'CHRISTMAS': 'christmas',
      'NEW_YEAR': 'newyear',
      'NEW_YEAR_EVE': 'newyear',
      'DIWALI': 'diwali',
      'DIWALI_NOV': 'diwali',
      'HOLI': 'holi',
      'HALLOWEEN': 'halloween',
      'VALENTINES': 'valentines',
      'SPRING': 'spring',
      'SUMMER': 'summer',
      'FALL': 'fall',
      'WINTER': 'winter',
      'PONGAL': 'pongal',
      'INDEPENDENCE_DAY_IN': 'independence-india',
      'INDEPENDENCE_DAY_US': 'independence-us',
      'EID': 'eid',
      'EID_MAY': 'eid',
      'CHINESE_NEW_YEAR': 'chinese-new-year',
      'CHINESE_NEW_YEAR_FEB': 'chinese-new-year',
      'THANKSGIVING': 'thanksgiving',
      'BLACK_FRIDAY': 'black-friday',
      'GANESH_CHATURTHI': 'ganesh-chaturthi'
    };

    const themeName = themeMap[theme] || 'default';

    // Remove existing theme stylesheets
    document.querySelectorAll('link[data-theme-css]').forEach(link => link.remove());
    document.querySelectorAll('script[data-theme-js]').forEach(script => script.remove());

    // Load new theme CSS
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = `assets/season/${themeName}.css`;
    cssLink.setAttribute('data-theme-css', '');
    cssLink.onerror = () => {
      console.log(`Theme CSS not found: ${themeName}.css, using default`);
    };
    document.head.appendChild(cssLink);

    // Load new theme JS
    const script = document.createElement('script');
    script.src = `assets/season/${themeName}.js`;
    script.setAttribute('data-theme-js', '');
    script.onerror = () => {
      console.log(`Theme JS not found: ${themeName}.js, using default`);
    };
    document.body.appendChild(script);
  }

  initializeThemeEffects(theme) {
    // Theme-specific initialization
    const effects = {
      'CHRISTMAS': () => this.christmasEffects(),
      'DIWALI': () => this.diwaliEffects(),
      'DIWALI_NOV': () => this.diwaliEffects(),
      'HOLI': () => this.holiEffects(),
      'NEW_YEAR': () => this.newYearEffects(),
      'NEW_YEAR_EVE': () => this.newYearEffects(),
      'HALLOWEEN': () => this.halloweenEffects(),
      'SPRING': () => this.springEffects(),
      'SUMMER': () => this.summerEffects(),
      'FALL': () => this.fallEffects(),
      'WINTER': () => this.winterEffects(),
    };

    if (effects[theme]) {
      setTimeout(() => effects[theme](), 500);
    }
  }

  // Theme-specific effect methods
  christmasEffects() {
    console.log('🎄 Christmas effects activated!');
    // Effects are handled by christmas.js
  }

  diwaliEffects() {
    console.log('🪔 Diwali effects activated!');
    this.createFireworks();
    this.createDiyas();
  }

  holiEffects() {
    console.log('🎨 Holi effects activated!');
    this.createColorSplashes();
  }

  newYearEffects() {
    console.log('🎉 New Year effects activated!');
    this.createConfetti();
    this.createFireworks();
  }

  halloweenEffects() {
    console.log('🎃 Halloween effects activated!');
    this.createSpookyEffects();
  }

  springEffects() {
    console.log('🌸 Spring effects activated!');
    this.createFlowers();
    this.createButterflies();
  }

  summerEffects() {
    console.log('☀️ Summer effects activated!');
    this.createSunshine();
  }

  fallEffects() {
    console.log('🍂 Fall effects activated!');
    this.createFallingLeaves();
  }

  winterEffects() {
    console.log('❄️ Winter effects activated!');
    this.createSnowflakes();
  }

  // Helper methods for effects
  createFireworks() {
    // Fireworks animation
    const container = document.createElement('div');
    container.className = 'fireworks-container';
    container.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
    document.body.appendChild(container);

    setInterval(() => {
      const firework = document.createElement('div');
      firework.className = 'firework';
      firework.style.cssText = `
        position:absolute;
        left:${Math.random() * 100}%;
        top:${Math.random() * 50}%;
        width:5px;
        height:5px;
        background:${['#ff0', '#f0f', '#0ff', '#f00', '#0f0'][Math.floor(Math.random() * 5)]};
        border-radius:50%;
        animation:firework-burst 1s ease-out;
      `;
      container.appendChild(firework);
      setTimeout(() => firework.remove(), 1000);
    }, 2000);
  }

  createDiyas() {
    // Diya (oil lamp) decorations
    const header = document.querySelector('.header');
    if (header) {
      const diya = document.createElement('div');
      diya.innerHTML = '🪔';
      diya.style.cssText = 'position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:24px;animation:flicker 2s infinite;';
      header.style.position = 'relative';
      header.appendChild(diya);
    }
  }

  createColorSplashes() {
    // Holi color splashes
    document.addEventListener('click', (e) => {
      const splash = document.createElement('div');
      splash.style.cssText = `
        position:fixed;
        left:${e.clientX}px;
        top:${e.clientY}px;
        width:50px;
        height:50px;
        background:${['#ff0080', '#00ff80', '#8000ff', '#ff8000', '#00ffff'][Math.floor(Math.random() * 5)]};
        border-radius:50%;
        opacity:0.7;
        pointer-events:none;
        animation:splash-fade 1s ease-out;
        z-index:9999;
      `;
      document.body.appendChild(splash);
      setTimeout(() => splash.remove(), 1000);
    });
  }

  createConfetti() {
    // Confetti animation
    for (let i = 0; i < 50; i++) {
      setTimeout(() => {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
          position:fixed;
          left:${Math.random() * 100}%;
          top:-10px;
          width:10px;
          height:10px;
          background:${['#ff0', '#f0f', '#0ff', '#f00', '#0f0'][Math.floor(Math.random() * 5)]};
          animation:confetti-fall ${3 + Math.random() * 2}s linear;
          z-index:9999;
          pointer-events:none;
        `;
        document.body.appendChild(confetti);
        setTimeout(() => confetti.remove(), 5000);
      }, i * 100);
    }
  }

  createSnowflakes() {
    // Snowflake animation (reuse existing christmas.js logic)
    console.log('Snowflakes created');
  }

  createFallingLeaves() {
    // Falling autumn leaves
    setInterval(() => {
      const leaf = document.createElement('div');
      leaf.innerHTML = ['🍂', '🍁'][Math.floor(Math.random() * 2)];
      leaf.style.cssText = `
        position:fixed;
        left:${Math.random() * 100}%;
        top:-50px;
        font-size:${20 + Math.random() * 20}px;
        animation:leaf-fall ${5 + Math.random() * 5}s linear;
        z-index:9999;
        pointer-events:none;
      `;
      document.body.appendChild(leaf);
      setTimeout(() => leaf.remove(), 10000);
    }, 1000);
  }

  createFlowers() {
    // Spring flowers
    const flowers = ['🌸', '🌺', '🌻', '🌷', '🌹'];
    const footer = document.querySelector('.footer');
    if (footer) {
      const flowerDecor = document.createElement('div');
      flowerDecor.innerHTML = flowers.map(f => `<span style="margin:0 10px;font-size:24px;">${f}</span>`).join('');
      flowerDecor.style.cssText = 'text-align:center;padding:20px 0;';
      footer.prepend(flowerDecor);
    }
  }

  createButterflies() {
    // Animated butterflies
    setInterval(() => {
      const butterfly = document.createElement('div');
      butterfly.innerHTML = '🦋';
      butterfly.style.cssText = `
        position:fixed;
        left:${Math.random() * 100}%;
        top:${Math.random() * 100}%;
        font-size:30px;
        animation:butterfly-fly ${10 + Math.random() * 10}s linear;
        z-index:9999;
        pointer-events:none;
      `;
      document.body.appendChild(butterfly);
      setTimeout(() => butterfly.remove(), 20000);
    }, 5000);
  }

  createSunshine() {
    // Summer sunshine effect
    document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
  }

  createSpookyEffects() {
    // Halloween spooky effects
    const ghosts = ['👻', '🎃', '🦇', '🕷️'];
    setInterval(() => {
      const ghost = document.createElement('div');
      ghost.innerHTML = ghosts[Math.floor(Math.random() * ghosts.length)];
      ghost.style.cssText = `
        position:fixed;
        left:${Math.random() * 100}%;
        top:-50px;
        font-size:40px;
        animation:ghost-float ${8 + Math.random() * 4}s linear;
        z-index:9999;
        pointer-events:none;
      `;
      document.body.appendChild(ghost);
      setTimeout(() => ghost.remove(), 12000);
    }, 3000);
  }
}

// Initialize the smart seasonal system
document.addEventListener('DOMContentLoaded', () => {
  window.seasonalEffects = new SmartSeasonalEffects();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
  @keyframes firework-burst {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(20); opacity: 0; }
  }
  @keyframes splash-fade {
    0% { transform: scale(0); opacity: 0.7; }
    100% { transform: scale(3); opacity: 0; }
  }
  @keyframes confetti-fall {
    to { transform: translateY(100vh) rotate(360deg); }
  }
  @keyframes leaf-fall {
    to { transform: translateY(100vh) rotate(720deg); }
  }
  @keyframes butterfly-fly {
    0%, 100% { transform: translate(0, 0); }
    25% { transform: translate(100px, -50px); }
    50% { transform: translate(200px, 0); }
    75% { transform: translate(100px, 50px); }
  }
  @keyframes ghost-float {
    to { transform: translateY(100vh) translateX(${Math.random() * 200 - 100}px); }
  }
  @keyframes flicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
  }
`;
document.head.appendChild(style);
