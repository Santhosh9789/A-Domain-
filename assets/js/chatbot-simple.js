/**
 * BLUEIDEALTECK - AUTO-LEARNING CHATBOT
 * Automatically analyzes website content and answers based on what's on the page!
 */

class BlueidealteckChatbot {
  constructor() {
    this.userInfo = {
      country: 'IN',
      currency: 'INR',
      email: null,
      phone: null
    };
    this.conversationHistory = [];
    this.websiteKnowledge = null;
    this.init();
  }

  async init() {
    await this.detectRegion();
    this.analyzeWebsite(); // Auto-analyze website content!
    this.createChatbot();
    this.attachEvents();
  }

  async detectRegion() {
    try {
      const response = await fetch('https://ipapi.co/json/');
      const data = await response.json();
      this.userInfo.country = data.country_code;
      
      if (data.country_code === 'IN') {
        this.userInfo.currency = 'INR';
      } else if (['GB', 'DE', 'FR', 'IT', 'ES'].includes(data.country_code)) {
        this.userInfo.currency = 'EUR';
      } else {
        this.userInfo.currency = 'USD';
      }
    } catch (error) {
      this.userInfo.currency = 'INR';
    }
  }

  analyzeWebsite() {
    console.log('🤖 Analyzing website content...');
    
    // Auto-extract all headings
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => ({
      level: h.tagName,
      text: h.textContent.trim()
    }));

    // Auto-extract all services
    const services = [];
    document.querySelectorAll('.service-single-main-wrapper-five, .service-item').forEach(service => {
      const title = service.querySelector('h5, h4, h3, .title');
      const desc = service.querySelector('p, .disc, .description');
      if (title && desc) {
        services.push({
          name: title.textContent.trim(),
          description: desc.textContent.trim()
        });
      }
    });

    // Auto-extract contact info
    const contactSection = document.querySelector('#contact, .contact');
    let contact = {
      email: 'info@blueidealteck.com',
      phone: '+91 9789836077',
      address: '1/11 Anna Nagar, Mangalampet, Virudhachalam, Tamil Nadu, India - 606104'
    };
    
    if (contactSection) {
      const emailLink = contactSection.querySelector('a[href^="mailto:"]');
      const phoneLink = contactSection.querySelector('a[href^="tel:"]');
      if (emailLink) contact.email = emailLink.textContent.trim();
      if (phoneLink) contact.phone = phoneLink.textContent.trim();
    }

    // Auto-extract stats
    const stats = {};
    document.querySelectorAll('.stats-item, .stat, [class*="stat"]').forEach(stat => {
      const number = stat.querySelector('.number, h1, h2, strong');
      const label = stat.querySelector('.label, p, span');
      if (number && label) {
        stats[label.textContent.trim()] = number.textContent.trim();
      }
    });

    // Auto-extract all paragraphs for context
    const allText = Array.from(document.querySelectorAll('p')).map(p => p.textContent.trim()).join(' ');

    this.websiteKnowledge = {
      headings,
      services,
      contact,
      stats,
      fullText: allText,
      lastUpdated: new Date()
    };

    console.log('✅ Website analyzed! Found:', {
      headings: headings.length,
      services: services.length,
      stats: Object.keys(stats).length
    });
  }

  createChatbot() {
    const html = `
      <div id="chat-btn" class="chat-btn">💬</div>
      <div id="chat-window" class="chat-window">
        <div class="chat-header">
          <div class="chat-header-left">
            <h3>Blueidealteck Assistant</h3>
            <span class="chat-status">● Online</span>
          </div>
          <button id="chat-close">×</button>
        </div>
        <div id="chat-body" class="chat-body" data-lenis-prevent>
          <div class="chat-msg bot">
            <div class="msg-avatar">🤖</div>
            <div class="msg-content">
              <p>Hi! I'm your Blueidealteck assistant. 👋</p>
              <p>I've analyzed this website and can answer any questions about our services, projects, and how we can help you!</p>
              <div class="quick-btns">
                <button class="quick-btn" data-msg="What services do you offer?">Services</button>
                <button class="quick-btn" data-msg="What are your prices?">Pricing</button>
                <button class="quick-btn" data-msg="Tell me about your projects">Projects</button>
                <button class="quick-btn" data-msg="How can I contact you?">Contact</button>
              </div>
            </div>
          </div>
        </div>
        <div class="chat-input-box">
          <input type="text" id="chat-input" placeholder="Ask me anything about our services...">
          <button id="chat-send">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
  }

  attachEvents() {
    document.getElementById('chat-btn').onclick = () => this.openChat();
    document.getElementById('chat-close').onclick = () => this.closeChat();
    document.getElementById('chat-send').onclick = () => this.sendMsg();
    document.getElementById('chat-input').onkeypress = (e) => {
      if (e.key === 'Enter') this.sendMsg();
    };
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('quick-btn')) {
        this.sendMsg(e.target.dataset.msg);
      }
    });
  }

  openChat() {
    document.getElementById('chat-window').classList.add('open');
  }

  closeChat() {
    document.getElementById('chat-window').classList.remove('open');
  }

  sendMsg(text = null) {
    const input = document.getElementById('chat-input');
    const msg = text || input.value.trim();
    if (!msg) return;

    this.addMsg(msg, 'user');
    input.value = '';
    this.conversationHistory.push({role: 'user', msg, time: new Date()});

    setTimeout(() => {
      const reply = this.getSmartReply(msg);
      this.addMsg(reply, 'bot');
      this.conversationHistory.push({role: 'bot', msg: reply, time: new Date()});
      this.saveHistory();
    }, 600);
  }

  addMsg(text, type) {
    const body = document.getElementById('chat-body');
    const div = document.createElement('div');
    div.className = `chat-msg ${type}`;
    
    if (type === 'bot') {
      div.innerHTML = `
        <div class="msg-avatar">🤖</div>
        <div class="msg-content"><p>${this.formatMsg(text)}</p></div>
      `;
    } else {
      div.innerHTML = `
        <div class="msg-content"><p>${this.formatMsg(text)}</p></div>
        <div class="msg-avatar">👤</div>
      `;
    }
    
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
  }

  formatMsg(text) {
    return text.replace(/\n/g, '<br>');
  }

  getSmartReply(msg) {
    const m = msg.toLowerCase();
    const kb = this.websiteKnowledge;
    
    // Email/Phone capture
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
    if (emailRegex.test(msg)) {
      this.userInfo.email = msg.match(emailRegex)[0];
      this.captureLead();
      return `Perfect! I've saved your email: ${this.userInfo.email} 📧\n\nOur team will reach out within 24 hours. What else can I help you with?`;
    }
    
    const phoneRegex = /[\d\s\-\+\(\)]{10,}/;
    if (phoneRegex.test(msg) && !this.userInfo.email) {
      this.userInfo.phone = msg.match(phoneRegex)[0];
      return `Great! I've noted your phone: ${this.userInfo.phone} 📱\n\nWhat's your email so we can send you details?`;
    }
    
    // Services - Auto-detected from website!
    if (m.includes('service') || m.includes('what do you do') || m.includes('what do you offer')) {
      if (kb.services.length > 0) {
        let response = "**Our Services:** 🎯\n\n";
        kb.services.forEach((service, i) => {
          response += `**${i+1}. ${service.name}**\n${service.description}\n\n`;
        });
        response += "Which service interests you most?";
        return response;
      }
      return "We offer comprehensive software development services. Let me connect you with our team for details!\n\nWhat's your email?";
    }
    
    // Specific service search
    for (const service of kb.services) {
      if (m.includes(service.name.toLowerCase()) || 
          service.name.toLowerCase().split(' ').some(word => m.includes(word))) {
        return `**${service.name}** 🚀\n\n${service.description}\n\n📊 **Our Track Record:**\n• 10 Modern Web Applications\n• 350+ Hours of Support\n• 3 Expert Developers\n• 100% Client Satisfaction\n\nWant to discuss your ${service.name.toLowerCase()} project?`;
      }
    }
    
    // Pricing
    if (m.includes('price') || m.includes('cost') || m.includes('pricing') || m.includes('budget') || m.includes('quote')) {
      return this.getPricing();
    }
    
    // Projects/Portfolio
    if (m.includes('project') || m.includes('portfolio') || m.includes('work') || m.includes('example')) {
      return `We've successfully delivered **10 Modern Web Applications**! 🚀\n\nOur work includes:\n• Healthcare platforms\n• E-commerce solutions\n• Fintech applications\n• E-learning systems\n• Food delivery apps\n\n📊 **Our Stats:**\n• 10 Modern Web Applications\n• 350+ Hours of Support\n• 3 Dedicated Developers\n• 100% Client Satisfaction\n\nVisit: blueidealteck.com/Projects/\n\nWant to be our next success story?`;
    }
    
    // Contact - Auto-detected!
    if (m.includes('contact') || m.includes('email') || m.includes('phone') || m.includes('call') || m.includes('reach')) {
      return `**Let's Connect!** 📞\n\n📧 **Email:** ${kb.contact.email}\n📱 **Phone:** ${kb.contact.phone}\n🌐 **Website:** blueidealteck.com\n📍 **Location:** ${kb.contact.address}\n\n💼 We work with clients globally!\n\nShare your email for a FREE consultation!`;
    }
    
    // Process/How we work
    if (m.includes('process') || m.includes('how do you work') || m.includes('methodology')) {
      return `**Our Development Process:** 🔄\n\n**1. Discovery & Planning**\nWe analyze your needs and create a strategic roadmap\n\n**2. Design & Prototyping**\nUser-centric designs and interactive prototypes\n\n**3. Development & Testing**\nAgile development with continuous testing\n\n**4. Deployment & Support**\nSmooth launch with ongoing maintenance\n\nWe follow Agile methodology with 2-week sprints!\n\nReady to start your project?`;
    }
    
    // Technologies
    if (m.includes('technology') || m.includes('tech stack') || m.includes('tools') || m.includes('framework')) {
      return `**Our Technology Expertise:** 💻\n\n🎨 **Frontend:** React, Next.js, Vue.js, Angular, TypeScript\n\n⚙️ **Backend:** Node.js, Python/Django, Java/Spring, PHP/Laravel\n\n📱 **Mobile:** React Native, Flutter, Swift, Kotlin\n\n☁️ **Cloud & DevOps:** AWS, Azure, Google Cloud, Docker, Kubernetes, Jenkins\n\n🗄️ **Databases:** PostgreSQL, MongoDB, MySQL, Redis, Firebase\n\n🤖 **AI/ML:** TensorFlow, PyTorch, Scikit-learn, OpenAI\n\nWhat technology are you interested in?`;
    }
    
    // Timeline
    if (m.includes('how long') || m.includes('timeline') || m.includes('duration') || m.includes('time')) {
      return `**Project Timelines:** ⏱️\n\n⚡ Simple MVP: 4-8 weeks\n📱 Mobile/Web App: 2-4 months\n🏢 Enterprise Software: 4-8 months\n🤖 AI/ML Solutions: 6-12 months\n\n✨ We use Agile methodology:\n• 2-week sprints\n• Regular demos\n• Continuous feedback\n\nWant to discuss your project timeline?`;
    }
    
    // Team/About
    if (m.includes('team') || m.includes('who are you') || m.includes('about') || m.includes('company')) {
      return `**About Blueidealteck** 🚀\n\nWe're a boutique software development team focused on quality over quantity!\n\n📊 **Our Stats:**\n• 10 Modern Web Applications Delivered\n• 350+ Hours of Support Provided\n• 3 Dedicated Expert Developers\n• 100% Client Satisfaction Rate\n\n💡 We help businesses thrive in the digital era with custom software solutions!\n\nWant to work with us?`;
    }
    
    // Greetings
    if (m.includes('hi') || m.includes('hello') || m.includes('hey')) {
      return `Hello! 👋 Great to hear from you!\n\nI've analyzed this website and can help you with:\n• Our ${kb.services.length} specialized services\n• Project portfolio & case studies\n• Technology stack & expertise\n• Development process\n• Pricing & timelines\n\nWhat would you like to know?`;
    }
    
    // Smart search in website content
    const searchTerms = msg.split(' ').filter(word => word.length > 3);
    for (const term of searchTerms) {
      if (kb.fullText.toLowerCase().includes(term.toLowerCase())) {
        // Found the term in website content
        const context = this.extractContext(kb.fullText, term);
        if (context) {
          return `I found information about "${term}" on our website:\n\n${context}\n\nWould you like to know more about this?`;
        }
      }
    }
    
    // Default
    return `I understand you're asking about "${msg}".\n\nI can help you with:\n• **Services** - Our ${kb.services.length} specialized services\n• **Projects** - 10 Modern Web Applications\n• **Technologies** - Complete tech stack\n• **Process** - Our development approach\n• **Contact** - Get in touch\n\nWhat would you like to know more about?`;
  }

  extractContext(text, term) {
    const index = text.toLowerCase().indexOf(term.toLowerCase());
    if (index === -1) return null;
    
    const start = Math.max(0, index - 100);
    const end = Math.min(text.length, index + 200);
    let context = text.substring(start, end).trim();
    
    if (context.length > 250) {
      context = context.substring(0, 250) + '...';
    }
    
    return context;
  }

  getPricing() {
    const curr = this.userInfo.currency;
    
    if (curr === 'INR') {
      return `**Our Premium Pricing (India):** 💎\n\n💎 **Hourly Rate:** ₹6,000-12,000/hour\n📦 **Fixed Projects:** Starting from ₹1,00,000 (1 Lakh+)\n👥 **Dedicated Team:** ₹6,50,000-12,00,000/month\n🚀 **Enterprise Solutions:** ₹40,00,000+\n\n📊 **Our Track Record:**\n• 10 Modern Web Applications Delivered\n• 350+ Hours of Support Provided\n• 3 Dedicated Expert Developers\n• 100% Client Satisfaction Rate\n\n💡 **Sample Projects:**\n• Simple Website: ₹1,00,000 - ₹3,00,000\n• E-commerce: ₹5,00,000 - ₹15,00,000\n• Mobile App: ₹8,00,000 - ₹20,00,000\n\nWant a FREE consultation?`;
    } else if (curr === 'EUR') {
      return `**Our Premium Pricing (Europe):** 💎\n\n💎 **Hourly Rate:** €70-140/hour\n📦 **Fixed Projects:** Starting from €9,000\n👥 **Dedicated Team:** €7,500-14,000/month\n🚀 **Enterprise Solutions:** €45,000+\n\n📊 **Track Record:**\n• 10 Modern Web Applications\n• 350+ Hours of Support\n• 3 Expert Developers\n• 100% Client Satisfaction\n\nWant a detailed quote?`;
    } else {
      return `**Our Premium Pricing:** 💎\n\n💎 **Hourly Rate:** $75-150/hour\n📦 **Fixed Projects:** Starting from $10,000\n👥 **Dedicated Team:** $8,000-15,000/month\n🚀 **Enterprise Solutions:** $50,000+\n\n📊 **Track Record:**\n• 10 Modern Web Applications\n• 350+ Hours of Support\n• 3 Expert Developers\n• 100% Client Satisfaction\n\nWant a detailed quote?`;
    }
  }

  captureLead() {
    const leadData = {
      email: this.userInfo.email,
      phone: this.userInfo.phone,
      country: this.userInfo.country,
      conversation: this.conversationHistory,
      timestamp: new Date().toISOString()
    };
    console.log('Lead captured:', leadData);
    localStorage.setItem('chatLead', JSON.stringify(leadData));
  }

  saveHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(this.conversationHistory));
  }
}

// Initialize
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new BlueidealteckChatbot());
} else {
  new BlueidealteckChatbot();
}
