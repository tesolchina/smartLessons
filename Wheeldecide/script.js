document.addEventListener('DOMContentLoaded', function () {

    // --- 1. CONFIGURATION: EDIT THIS SECTION ---

    // CHANGED: Use an array to store multiple valid passwords.
    // You can add as many passwords as you like, separated by commas.
    const CORRECT_PASSWORDS = ["simon1979", "talia2025"]; 

    // The rest of your configuration remains the same.
    const classesData = [
        { name: 'EEGC-36', file: 'iframes/EEGC-36.html' },
        { name: 'EEGC-37', file: 'iframes/EEGC-37.html' },
        { name: 'EEGC-38', file: 'iframes/EEGC-38.html' },
        { name: 'UE1-37', file: 'iframes/UE1-37.html' },
        { name: 'GCAP3056', file: 'iframes/GCAP3056.html' },
        { name: 'GCAP3226', file: 'iframes/GCAP3226.html' }
    ];
    // --- END OF CONFIGURATION ---


    // --- 2. PASSWORD PROTECTION LOGIC ---
    const loginScreen = document.getElementById('login-screen');
    const appContent = document.getElementById('app-content');
    const loginForm = document.getElementById('login-form');
    const passwordInput = document.getElementById('password-input');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // CHANGED: Check if the entered password is included in the array of correct passwords.
        if (CORRECT_PASSWORDS.includes(passwordInput.value)) {
            // Correct password
            loginScreen.style.display = 'none';
            appContent.style.display = 'flex';
            initializeApp();
        } else {
            // Incorrect password
            errorMessage.textContent = 'Incorrect password. Please try again.';
            passwordInput.value = '';
            passwordInput.focus();
        }
    });


    // --- 3. MAIN APPLICATION LOGIC (No changes needed here) ---
    function initializeApp() {
        const sidebar = document.getElementById('sidebar');
        const content = document.getElementById('content');
        const sidebarCollapseBtn = document.getElementById('sidebarCollapse');
        const classMenu = document.getElementById('class-menu');
        const iframeContainer = document.getElementById('iframe-container');

        function loadWheel(filePath) {
            fetch(filePath)
                .then(response => {
                    if (!response.ok) { throw new Error('Network response was not ok'); }
                    return response.text();
                })
                .then(html => {
                    iframeContainer.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching the iFrame file:', error);
                    iframeContainer.innerHTML = `<p style="color: red;">Error: Could not load the content. Please check if the file path '${filePath}' is correct in script.js.</p>`;
                });
        }

        classesData.forEach(classInfo => {
            const listItem = document.createElement('li');
            const button = document.createElement('button');
            button.textContent = classInfo.name;
            
            button.addEventListener('click', () => {
                loadWheel(classInfo.file);
            });

            listItem.appendChild(button);
            classMenu.appendChild(listItem);
        });

        sidebarCollapseBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
            content.classList.toggle('active');
        });
    }
});