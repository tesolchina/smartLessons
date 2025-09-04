// js/shell.js

(function(){
    const avatarBox = document.getElementById('avatarBox');
    const header = document.getElementById('avatarBoxHeader');
    const resizeHandle = document.getElementById('avatarResizeHandle');
    const closeBtn = document.getElementById('avatarBoxCloseBtn');
    const restoreBtn = document.getElementById('restoreAvatarBtn');
    const ASPECT = 400 / 340; // height / width

    // --- Default Sizing and Positioning ---
    function getDefaultBox() {
        const isMobile = window.innerWidth <= 700;
        if (isMobile) {
            let width = Math.min(window.innerWidth * 0.86, 360);
            let height = width * ASPECT;
            if (height > window.innerHeight * 0.85) {
                height = window.innerHeight * 0.85;
                width = height / ASPECT;
            }
            return { width: width, height: height, right: 6, bottom: 6 };
        }
        return { width: 340, height: 400, right: 32, bottom: 32 };
    }

    function setDefaultPositionAndSize() {
        const box = getDefaultBox();
        avatarBox.style.width = box.width + 'px';
        avatarBox.style.height = box.height + 'px';
        avatarBox.style.left = 'auto';
        avatarBox.style.top = 'auto';
        avatarBox.style.right = box.right + 'px';
        avatarBox.style.bottom = box.bottom + 'px';
    }
    setDefaultPositionAndSize();

    // --- Dragging Logic ---
    let isDragging = false, dragStartX, dragStartY, dragStartLeft, dragStartTop;
    
    function startDrag(clientX, clientY) {
        isDragging = true;
        avatarBox.classList.add('active');
        dragStartX = clientX;
        dragStartY = clientY;
        const rect = avatarBox.getBoundingClientRect();
        dragStartLeft = rect.left;
        dragStartTop = rect.top;
        document.body.style.userSelect = 'none';
    }

    function onDrag(clientX, clientY) {
        if (!isDragging) return;
        let left = dragStartLeft + (clientX - dragStartX);
        let top = dragStartTop + (clientY - dragStartY);
        const boxW = avatarBox.offsetWidth, boxH = avatarBox.offsetHeight;
        left = Math.max(0, Math.min(left, window.innerWidth - boxW));
        top = Math.max(0, Math.min(top, window.innerHeight - boxH));
        avatarBox.style.left = left + 'px';
        avatarBox.style.top = top + 'px';
        avatarBox.style.right = 'auto';
        avatarBox.style.bottom = 'auto';
    }

    function stopDrag() {
        isDragging = false;
        avatarBox.classList.remove('active');
        document.body.style.userSelect = '';
    }

    header.addEventListener('mousedown', (e) => startDrag(e.clientX, e.clientY));
    document.addEventListener('mousemove', (e) => onDrag(e.clientX, e.clientY));
    document.addEventListener('mouseup', stopDrag);

    header.addEventListener('touchstart', (e) => { e.preventDefault(); startDrag(e.touches[0].clientX, e.touches[0].clientY); }, { passive: false });
    document.addEventListener('touchmove', (e) => { if(isDragging) { e.preventDefault(); onDrag(e.touches[0].clientX, e.touches[0].clientY); } }, { passive: false });
    document.addEventListener('touchend', stopDrag);

    // --- Resizing Logic (Fixed Aspect Ratio) ---
    let isResizing = false, resizeStartX, resizeStartY, resizeStartW, resizeStartH;

    function startResize(clientX, clientY, e) {
        isResizing = true;
        avatarBox.classList.add('active');
        resizeStartX = clientX;
        resizeStartY = clientY;
        resizeStartW = avatarBox.offsetWidth;
        resizeStartH = avatarBox.offsetHeight;
        document.body.style.userSelect = 'none';
        e.stopPropagation();
        e.preventDefault();
    }

    function onResize(clientX, clientY) {
        if (!isResizing) return;
        let deltaX = clientX - resizeStartX;
        let deltaY = clientY - resizeStartY;
        let delta = Math.max(deltaX, deltaY / ASPECT);
        
        let newW = Math.max(170, resizeStartW + delta);
        let newH = newW * ASPECT;

        if (newW > window.innerWidth - 10) { newW = window.innerWidth - 10; newH = newW * ASPECT; }
        if (newH > window.innerHeight - 10) { newH = window.innerHeight - 10; newW = newH / ASPECT; }
        
        avatarBox.style.width = newW + 'px';
        avatarBox.style.height = newH + 'px';
    }

    function stopResize() {
        isResizing = false;
        avatarBox.classList.remove('active');
        document.body.style.userSelect = '';
    }

    resizeHandle.addEventListener('mousedown', (e) => startResize(e.clientX, e.clientY, e));
    document.addEventListener('mousemove', (e) => onResize(e.clientX, e.clientY));
    document.addEventListener('mouseup', stopResize);

    resizeHandle.addEventListener('touchstart', (e) => startResize(e.touches[0].clientX, e.touches[0].clientY, e), { passive: false });
    document.addEventListener('touchmove', (e) => { if(isResizing) { e.preventDefault(); onResize(e.touches[0].clientX, e.touches[0].clientY); } }, { passive: false });
    document.addEventListener('touchend', stopResize);

    // --- Close/Hide/Show Logic ---
    closeBtn.addEventListener('click', () => {
        avatarBox.style.display = 'none';
        restoreBtn.style.display = 'block';
    });

    restoreBtn.addEventListener('click', () => {
        setDefaultPositionAndSize();
        avatarBox.style.display = 'flex';
        restoreBtn.style.display = 'none';
    });

    // Double click to restore
    window.addEventListener('dblclick', () => {
        if (avatarBox.style.display === 'none') {
            setDefaultPositionAndSize();
            avatarBox.style.display = 'flex';
            restoreBtn.style.display = 'none';
        }
    });

    // --- Window Resize Handling ---
    window.addEventListener('resize', () => {
        let rect = avatarBox.getBoundingClientRect();
        if (rect.right > window.innerWidth) { avatarBox.style.left = (window.innerWidth - rect.width - 10) + 'px'; avatarBox.style.right = 'auto'; }
        if (rect.bottom > window.innerHeight) { avatarBox.style.top = (window.innerHeight - rect.height - 10) + 'px'; avatarBox.style.bottom = 'auto'; }
        if (rect.left < 0) { avatarBox.style.left = '10px'; avatarBox.style.right = 'auto'; }
        if (rect.top < 0) { avatarBox.style.top = '10px'; avatarBox.style.bottom = 'auto'; }
        if (window.innerWidth < 200 || window.innerHeight < 200) { setDefaultPositionAndSize(); }
    });

    window.addEventListener('orientationchange', () => setTimeout(setDefaultPositionAndSize, 400));
})();