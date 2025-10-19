/**
 * Slide 01 - QR Code Module JavaScript
 * Contains functionality specific to slide 1 QR code display
 */

// Slide 01 specific functions
const slide01 = {
    
    // Initialize slide 01
    init: function() {
        console.log('Slide 01 (QR Code) initialized');
        this.setupEventListeners();
    },
    
    // Setup event listeners for slide 01
    setupEventListeners: function() {
        // Add any slide-specific event listeners here
        document.addEventListener('DOMContentLoaded', () => {
            this.checkQRCodeImage();
        });
    },
    
    // Check if QR code image loads properly
    checkQRCodeImage: function() {
        const qrImage = document.querySelector('img[alt="QR Code for presentation"]');
        if (qrImage) {
            qrImage.onload = function() {
                console.log('QR code image loaded successfully');
            };
            qrImage.onerror = function() {
                console.error('Failed to load QR code image');
                this.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkZhaWxlZCB0byBsb2FkIFFSIGNvZGU8L3RleHQ+PC9zdmc+';
            };
        }
    },
    
    // Get the content for slide 01
    getContent: function() {
        return `
            <div class="text-center p-8">
                <div class="text-4xl mb-4">📱</div>
                <h3 class="text-xl font-bold text-blue-600 dark:text-blue-400 mb-4">QR Code - Access Presentation</h3>
                <p class="text-gray-600 dark:text-gray-400 mb-4">Scan to access this presentation on your device</p>
                
                <!-- QR Code Image -->
                <div class="flex justify-center mb-4">
                    <div class="bg-white p-4 rounded-lg shadow-lg border-2 border-gray-200">
                        <img src="modules/slide01/flipped926_qr.png" 
                             alt="QR Code for presentation" 
                             class="w-48 h-48 mx-auto" 
                             loading="lazy" />
                    </div>
                </div>
                
                <!-- Information Box -->
                <div class="mt-4 p-4 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
                    <p class="text-sm text-blue-700 dark:text-blue-300 mb-2">
                        <strong>URL:</strong> https://smartlessons.hkbu.tech/talks/flipped926.html
                    </p>
                    <p class="text-xs text-blue-600 dark:text-blue-400">
                        Share this QR code with participants to let them follow along on their devices
                    </p>
                </div>
                
                <!-- Action Buttons -->
                <div class="mt-6 flex justify-center space-x-4">
                    <button onclick="copyToClipboard('https://smartlessons.hkbu.tech/talks/flipped926.html')" 
                            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all text-sm">
                        📋 Copy URL
                    </button>
                    <button onclick="downloadQRCode()" 
                            class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all text-sm">
                        💾 Download QR
                    </button>
                </div>
            </div>
        `;
    },
    
    // Cleanup when leaving slide 01
    cleanup: function() {
        console.log('Slide 01 cleanup');
        // Remove any slide-specific event listeners or timers
    }
};

// Global utility functions for slide 01
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('URL copied to clipboard!', 'success');
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            fallbackCopyTextToClipboard(text);
        });
    } else {
        fallbackCopyTextToClipboard(text);
    }
}

function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showNotification('URL copied to clipboard!', 'success');
        } else {
            showNotification('Failed to copy URL', 'error');
        }
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showNotification('Failed to copy URL', 'error');
    }
    
    document.body.removeChild(textArea);
}

function downloadQRCode() {
    const qrImage = document.querySelector('img[alt="QR Code for presentation"]');
    if (qrImage) {
        const link = document.createElement('a');
        link.download = 'flipped926_qr_code.png';
        link.href = qrImage.src;
        link.click();
        showNotification('QR code download started!', 'success');
    } else {
        showNotification('QR code image not found', 'error');
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} fixed top-4 right-4 z-50 px-4 py-2 rounded-lg shadow-lg transition-all duration-300`;
    notification.style.transform = 'translateX(100%)';
    
    // Set styles based on type
    const styles = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        info: 'bg-blue-500 text-white'
    };
    notification.className += ` ${styles[type]}`;
    notification.textContent = message;
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = slide01;
}