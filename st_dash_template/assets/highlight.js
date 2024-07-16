// assets/highlight.js

// Function to initialize highlight.js
function initializeHighlighting() {
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
}

// Initialize highlight.js on page load
document.addEventListener('DOMContentLoaded', (event) => {
    initializeHighlighting();
});

// Initialize highlight.js on Dash callback updates
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clients: {
        initializeHighlighting: function(value) {
            setTimeout(initializeHighlighting, 0);
            return null;
        }
    }
});
