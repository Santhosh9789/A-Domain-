/**
 * BLUEIDEALTECK - AI CHATBOT FOR CUSTOMER SUPPORT
 * Intelligent chatbot with:
 * - Natural language understanding
 * - Context-aware responses
 * - Lead capture
 * - Multi-language support
 * - Integration with email
 */

class BlueidealteckChatbot {
  constructor() {
    this.isOpen = false;
    this.conversationHistory = [];
    this.userInfo = {
      country: null,
      currency: 'USD',
      language: 'en'
    };
    this.knowledgeBase = this.initializeKnowledgeBase();
    
    this.init();
  }

  async init() {
    await this.detectUserRegion();
    this.createChatWidget();
    this.attachEventListeners();
    this.loadConversationHistory();
  }

  async detectUserRegion() {
    try {
      const response = await fetch('https://ipapi.co/json/');
      const data = await response.json();
      
      this.userInfo.country = data.country_code;
      this.userInfo.language = data.languages?.split(',')[0] || 'en';
      
      // Set currency based on country
      if (data.country_code === 'IN') {
        this.userInfo.currency = 'INR';
      } else if (['GB', 'DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'PT', 'IE'].includes(data.country_code)) {
        this.userInfo.currency = 'EUR';
      } else if (['US', 'CA', 'AU', 'NZ', 'SG'].includes(data.country_code)) {
        this.userInfo.currency = 'USD';
      } else {
        this.userInfo.currency = 'USD';
      }
      
      console.log('User region detected:', this.userInfo);
    } catch (error) {
      console.log('Using default region (India)');
      this.userInfo.country = 'IN';
      this.userInfo.currency = 'INR';
      this.userInfo.language = 'en';
    }
  }

  initializeKnowledgeBase() {
    return {
      greetings: {
        keywords: ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening'],
        responses: [
          "Hello! 👋 I'm Blue, your AI assistant at Blueidealteck. How can I help you today?",
          "Hi there! 😊 Welcome to Blueidealteck. What can I assist you with?",
          "Hey! 🎉 Thanks for reaching out. How may I help you?"
        ]
      },
      services: {
        keywords: ['service', 'what do you do', 'what do you offer', 'capabilities', 'solutions'],
        responses: [
          "We offer comprehensive software development services:\n\n🤖 AI & Machine Learning\n☁️ Cloud Computing (AWS, Azure, GCP)\n💻 Custom Web Development\n📱 Mobile App Development\n🔧 DevOps & CI/CD\n🎨 UI/UX Design\n\nWhich service interests you?"
        ]
      },
      pricing: {
        keywords: ['price', 'cost', 'how much', 'pricing', 'budget', 'quote', 'rate', 'charges'],
        response: (currency) => {
          if (currency === 'INR') {
            return "We offer premium software development services with transparent pricing:\n\n💎 **Hourly Rate**: ₹6,000-12,000/hour (based on expertise level)\n📦 **Fixed Price Projects**: Starting from ₹1,00,000 (1 Lakh+)\n👥 **Dedicated Team**: ₹6,50,000-12,00,000/month per developer\n🚀 **Enterprise Solutions**: Custom quotes (typically ₹40,00,000+)\n\n✨ Why our rates reflect quality:\n• Senior developers with 5-10+ years experience\n• Enterprise-grade code quality & best practices\n• 24/7 support & maintenance\n• Proven track record with 100+ successful projects\n• Quality assurance & comprehensive warranty\n• Milestone-based payments (pay as we deliver)\n\nWould you like a FREE consultation to discuss your project? Our team can provide a detailed quote!";
          } else if (currency === 'EUR') {
            return "We offer premium software development services:\n\n💎 **Hourly Rate**: €70-140/hour\n📦 **Fixed Price Projects**: Starting from €9,000\n👥 **Dedicated Team**: €7,500-14,000/month per developer\n🚀 **Enterprise Solutions**: Custom quotes (€45,000+)\n\n✨ Why our rates reflect quality:\n• Senior developers with 5-10+ years experience\n• Enterprise-grade code quality & best practices\n• 24/7 support & maintenance\n• Proven track record with 100+ successful projects\n• Quality assurance & comprehensive warranty\n• Milestone-based payments (pay as we deliver)\n\nWould you like a FREE consultation?";
          } else {
            return "We offer premium software development services:\n\n💎 **Hourly Rate**: $75-150/hour\n📦 **Fixed Price Projects**: Starting from $10,000\n👥 **Dedicated Team**: $8,000-15,000/month per developer\n🚀 **Enterprise Solutions**: Custom quotes ($50,000+)\n\n✨ Why our rates reflect quality:\n• Senior developers with 5-10+ years experience\n• Enterprise-grade code quality & best practices\n• 24/7 support & maintenance\n• Proven track record with 100+ successful projects\n• Quality assurance & comprehensive warranty\n• Milestone-based payments (pay as we deliver)\n\nWould you like a FREE consultation?";
          }
        }
      },
      technologies: {
        keywords: ['technology', 'tech stack', 'tools', 'languages', 'framework'],
        responses: [
          "We specialize in modern technologies:\n\n🎨 Frontend: React, Next.js, Vue.js\n⚙️ Backend: Python/Django, Node.js, Java\n📱 Mobile: React Native, Flutter\n☁️ Cloud: AWS, Azure, Google Cloud\n🔧 DevOps: Docker, Kubernetes, Jenkins\n🤖 AI/ML: TensorFlow, PyTorch\n\nWhat technology are you interested in?"
        ]
      },
      timeline: {
        keywords: ['how long', 'timeline', 'duration', 'when', 'time'],
        responses: [
          "Project timelines vary based on complexity:\n\n⚡ Simple MVP: 4-8 weeks\n📱 Mobile/Web App: 2-4 months\n🏢 Enterprise Software: 4-8 months\n🤖 AI/ML Solutions: 6-12 months\n\nWe follow Agile methodology with 2-week sprints. Want to discuss your project timeline?"
        ]
      },
      contact: {
        keywords: ['contact', 'email', 'phone', 'call', 'reach', 'talk'],
        responses: [
          "I'd love to connect you with our team! 📞\n\n📧 Email: info@blueidealteck.com\n📱 Phone: +91 9789836077\n🌐 Website: blueidealteck.com\n\nOr I can schedule a FREE consultation for you right now. What's your email?"
        ]
      },
      location: {
        keywords: ['where', 'location', 'office', 'address'],
        responses: [
          "We're located in:\n\n📍 1/11 Anna Nagar, Mangalampet\nVirudhachalam(tk), Cuddalore(dist)\nTamil Nadu, India - 606104\n\n🌍 We work with clients globally across USA, UK, Europe, Australia, and Asia!\n\nWhere are you located?"
        ]
      },
      portfolio: {
        keywords: ['portfolio', 'projects', 'work', 'examples', 'case studies'],
        responses: [
          "We've delivered 100+ successful projects! 🎉\n\nCheck out our portfolio:\n🔗 blueidealteck.com/Projects/\n\nWe've worked on:\n• Healthcare & Telemedicine apps\n• E-commerce platforms\n• Fintech solutions\n• AI-powered applications\n• Cloud migrations\n\nWant to see specific examples?"
        ]
      },
      careers: {
        keywords: ['job', 'career', 'hiring', 'work with you', 'join'],
        responses: [
          "Exciting! We're always looking for talented people! 🚀\n\n🔗 View open positions: blueidealteck.com/careers/\n\nWe offer:\n✅ Competitive salary\n✅ Remote work options\n✅ Learning opportunities\n✅ Great team culture\n\nWhat role are you interested in?"
        ]
      },
      help: {
        keywords: ['help', 'support', 'assist', 'question'],
        responses: [
          "I'm here to help! 😊 You can ask me about:\n\n💼 Our Services\n💰 Pricing\n🛠️ Technologies\n⏱️ Project Timelines\n📞 Contact Information\n💼 Careers\n📁 Portfolio\n\nWhat would you like to know?"
        ]
      }
    };
  }

  createChatWidget() {
    const chatHTML = `
      <!-- Chat Button -->
      <div id="chat-button" class="chat-button">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <span class="chat-badge">1</span>
      </div>

      <!-- Chat Window -->
      <div id="chat-window" class="chat-window">
        <div class="chat-header">
          <div class="chat-header-info">
            <div class="chat-avatar">🤖</div>
            <div>
              <h3>Blueidealteck Assistant</h3>
              <p class="chat-status">
                <span class="status-dot"></span> Online
              </p>
            </div>
          </div>
          <button id="chat-close" class="chat-close">×</button>
        </div>

        <div id="chat-messages" class="chat-messages">
          <div class="chat-message bot-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
              <p>Hi! I'm your Blueidealteck assistant. 👋</p>
              <p>I can help you with:</p>
              <div class="quick-replies">
                <button class="quick-reply" data-message="Tell me about your services">Our Services</button>
                <button class="quick-reply" data-message="What are your pricing options?">Pricing</button>
                <button class="quick-reply" data-message="I want to start a project">Start Project</button>
                <button class="quick-reply" data-message="Show me your portfolio">Portfolio</button>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input-container">
          <input 
            type="text" 
            id="chat-input" 
            placeholder="Type your message..." 
            autocomplete="off"
          />
          <button id="chat-send" class="chat-send">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', chatHTML);
  }

  attachEventListeners() {
    const chatButton = document.getElementById('chat-button');
    const chatClose = document.getElementById('chat-close');
    const chatSend = document.getElementById('chat-send');
    const chatInput = document.getElementById('chat-input');

    chatButton.addEventListener('click', () => this.toggleChat());
    chatClose.addEventListener('click', () => this.toggleChat());
    chatSend.addEventListener('click', () => this.sendMessage());
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') this.sendMessage();
    });

    // Quick replies
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('quick-reply')) {
        const message = e.target.getAttribute('data-message');
        this.sendMessage(message);
      }
    });
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    const chatWindow = document.getElementById('chat-window');
    const chatButton = document.getElementById('chat-button');
    const chatBadge = chatButton.querySelector('.chat-badge');

    if (this.isOpen) {
      chatWindow.classList.add('open');
      chatButton.classList.add('active');
      if (chatBadge) chatBadge.style.display = 'none';
      document.getElementById('chat-input').focus();
    } else {
      chatWindow.classList.remove('open');
      chatButton.classList.remove('active');
    }
  }

  sendMessage(text = null) {
    const input = document.getElementById('chat-input');
    const message = text || input.value.trim();

    if (!message) return;

    // Add user message
    this.addMessage(message, 'user');
    input.value = '';

    // Save to history
    this.conversationHistory.push({ role: 'user', message, timestamp: new Date() });

    // Get AI response
    setTimeout(() => {
      const response = this.getAIResponse(message);
      this.addMessage(response, 'bot');
      this.conversationHistory.push({ role: 'bot', message: response, timestamp: new Date() });
      this.saveConversationHistory();
    }, 500);
  }

  addMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageHTML = `
      <div class="chat-message ${sender}-message">
        <div class="message-avatar">${sender === 'bot' ? '🤖' : '👤'}</div>
        <div class="message-content">
          <p>${this.formatMessage(text)}</p>
          <span class="message-time">${new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}</span>
        </div>
      </div>
    `;

    messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  formatMessage(text) {
    // Convert line breaks to <br>
    return text.replace(/\n/g, '<br>');
  }

  getAIResponse(userMessage) {
    const message = userMessage.toLowerCase();

    // Check each category in knowledge base
    for (const [category, data] of Object.entries(this.knowledgeBase)) {
      for (const keyword of data.keywords) {
        if (message.includes(keyword)) {
          // Handle pricing with currency
          if (category === 'pricing' && typeof data.response === 'function') {
            return data.response(this.userInfo.currency);
          }
          const responses = data.responses || [data.response];
          return responses[Math.floor(Math.random() * responses.length)];
        }
      }
    }

    // Check for email pattern (lead capture)
    const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
    if (emailRegex.test(userMessage)) {
      this.userInfo.email = userMessage.match(emailRegex)[0];
      this.captureLeadToEmail();
      return `Great! I've saved your email: ${this.userInfo.email} 📧\n\nOur team will reach out to you within 24 hours. In the meantime, is there anything else I can help you with?`;
    }

    // Check for phone pattern
    const phoneRegex = /[\d\s\-\+\(\)]{10,}/;
    if (phoneRegex.test(userMessage)) {
      this.userInfo.phone = userMessage.match(phoneRegex)[0];
      return `Perfect! I've noted your phone number: ${this.userInfo.phone} 📱\n\nWhat's the best email to reach you at?`;
    }

    // Default response
    return `I understand you're asking about "${userMessage}". Let me connect you with our team for a detailed answer! 😊\n\nCould you share your email so we can follow up with you?`;
  }

  captureLeadToEmail() {
    // Send lead info to backend/email
    const leadData = {
      email: this.userInfo.email,
      phone: this.userInfo.phone || 'Not provided',
      conversation: this.conversationHistory,
      timestamp: new Date().toISOString(),
      source: 'AI Chatbot'
    };

    // Send to your backend or email service
    fetch('/api/capture-lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(leadData)
    }).catch(err => console.log('Lead capture:', leadData));

    console.log('Lead captured:', leadData);
  }

  saveConversationHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(this.conversationHistory));
  }

  loadConversationHistory() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
      this.conversationHistory = JSON.parse(saved);
    }
  }
}

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.chatbot = new BlueidealteckChatbot();
});
