const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Enable CORS for all routes
app.use(cors());

// Parse JSON bodies
app.use(express.json());

// Serve static files from the root directory
app.use(express.static(__dirname));

// Serve component files specifically
app.use('/components', express.static(path.join(__dirname, 'components')));

// API route for component loading (if needed for future enhancements)
app.get('/api/component/:name', (req, res) => {
    const componentName = req.params.name;
    const componentPath = path.join(__dirname, 'components', `${componentName}.html`);
    
    res.sendFile(componentPath, (err) => {
        if (err) {
            console.error(`Error serving component ${componentName}:`, err);
            res.status(404).json({ error: 'Component not found' });
        }
    });
});

// Serve the main index.html for all other routes (SPA support)
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
    console.log(`🚀 Workshop server running on port ${PORT}`);
    console.log(`📖 Access your workshop at: http://localhost:${PORT}`);
    console.log(`🎯 Workshop planning document: http://localhost:${PORT}/workshop-planning-document.md`);
});
