/* Christmas Season Script - Enhanced Realism */
document.addEventListener("DOMContentLoaded", function () {
    const snowContainer = document.createElement('div');
    snowContainer.id = 'snow-container';
    Object.assign(snowContainer.style, {
        position: 'fixed',
        top: '0',
        left: '0',
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: '9999',
        overflow: 'hidden'
    });
    document.body.appendChild(snowContainer);

    function createSnowflake() {
        if (document.hidden) return; // Save resources when tab is inactive

        const snowflake = document.createElement('div');
        snowflake.classList.add('snowflake');
        
        // Randomize depth (layers)
        const depth = Math.random();
        let size, duration, blur, opacity, zIndex;

        if (depth < 0.3) { // Close & Large
            size = Math.random() * 6 + 5;
            duration = Math.random() * 4 + 6;
            blur = '2px';
            opacity = 0.8;
            zIndex = '10000';
        } else if (depth < 0.7) { // Middle
            size = Math.random() * 4 + 3;
            duration = Math.random() * 6 + 10;
            blur = '0px';
            opacity = 0.6;
            zIndex = '9999';
        } else { // Far & Small
            size = Math.random() * 2 + 1;
            duration = Math.random() * 10 + 15;
            blur = '1px';
            opacity = 0.4;
            zIndex = '9998';
        }

        const wind = (Math.random() - 0.5) * 50; // Horizontal drift

        Object.assign(snowflake.style, {
            left: Math.random() * 100 + 'vw',
            width: `${size}px`,
            height: `${size}px`,
            opacity: opacity,
            filter: `blur(${blur})`,
            animationDuration: `${duration}s`,
            animationName: wind > 0 ? 'fall-right' : 'fall-left', // Different wind directions
            zIndex: zIndex
        });

        // Add custom keyframes if they don't exist
        if (!document.getElementById('snow-keyframes')) {
            const style = document.createElement('style');
            style.id = 'snow-keyframes';
            style.innerHTML = `
                @keyframes fall-right {
                    0% { transform: translateY(-10px) translateX(0); }
                    100% { transform: translateY(110vh) translateX(50px); }
                }
                @keyframes fall-left {
                    0% { transform: translateY(-10px) translateX(0); }
                    100% { transform: translateY(110vh) translateX(-50px); }
                }
            `;
            document.head.appendChild(style);
        }

        snowContainer.appendChild(snowflake);

        setTimeout(() => {
            snowflake.remove();
        }, duration * 1000);
    }

    // Limit max snowflakes for performance
    const MAX_SNOWFLAKES = 40;
    
    // Smoother generation interval (increased from 300 to 500 for better performance)
    setInterval(() => {
        if (document.querySelectorAll('.snowflake').length < MAX_SNOWFLAKES) {
            createSnowflake();
        }
    }, 500);
});
