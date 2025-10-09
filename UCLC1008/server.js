// server.js - Main backend file
const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Store chat sessions (in production, use a database)
const chatSessions = new Map();

// Routes
app.post('/api/chat', async (req, res) => {
    try {
        const { message, sessionId, strategy } = req.body;
        
        // Create or get session
        if (!chatSessions.has(sessionId)) {
            chatSessions.set(sessionId, {
                messages: [],
                strategy: strategy,
                startTime: new Date()
            });
        }
        
        const session = chatSessions.get(sessionId);
        
        // Add user message to session
        session.messages.push({
            role: 'user',
            content: message,
            timestamp: new Date()
        });
        
        // Generate AI response based on strategy
        const aiResponse = await generateAIResponse(message, strategy, session);
        
        // Add AI response to session
        session.messages.push({
            role: 'assistant',
            content: aiResponse,
            timestamp: new Date()
        });
        
        res.json({
            response: aiResponse,
            sessionId: sessionId,
            strategy: strategy
        });
        
    } catch (error) {
        console.error('Chat error:', error);
        res.status(500).json({ 
            error: 'Failed to process message',
            message: 'Please try again later.'
        });
    }
});

app.post('/api/feedback', async (req, res) => {
    try {
        const { sessionId, rating, feedback, email } = req.body;
        
        // Here you would typically save to a database
        console.log('Feedback received:', { sessionId, rating, feedback, email });
        
        // Send email (you'd use a service like SendGrid, Mailgun, etc.)
        await sendFeedbackEmail(sessionId, rating, feedback, email);
        
        res.json({ success: true, message: 'Feedback submitted successfully' });
        
    } catch (error) {
        console.error('Feedback error:', error);
        res.status(500).json({ error: 'Failed to submit feedback' });
    }
});

app.get('/api/chat-history/:sessionId', (req, res) => {
    const { sessionId } = req.params;
    const session = chatSessions.get(sessionId);
    
    if (!session) {
        return res.status(404).json({ error: 'Session not found' });
    }
    
    res.json({
        messages: session.messages,
        strategy: session.strategy,
        duration: calculateDuration(session.startTime)
    });
});

// AI Response Generation
async function generateAIResponse(message, strategy, session) {
    // You can integrate with various AI services here
    
    // Option A: Use OpenAI API
    return await generateWithOpenAI(message, strategy, session);
    
    // Option B: Use a local model (if you have the hardware)
    // return await generateWithLocalModel(message, strategy, session);
    
    // Option C: Use another AI service
    // return await generateWithOtherService(message, strategy, session);
}

async function generateWithOpenAI(message, strategy, session) {
    const systemPrompt = `You are an experienced academic English teacher specializing in paraphrasing techniques. Your primary goal is to guide students in practicing paraphrasing effectively using one of the following strategies:

1. Using synonyms and antonyms
2. Changing the word form
3. Changing the voice (active ↔ passive)
4. Changing sentence patterns
5. Using all of the strategies above

Current strategy: ${getStrategyName(strategy)}

${getStrategyInstructions(strategy)}

Response style:
• Begin by confirming and briefly explaining the student's chosen strategy if this is the first message about it.
• Provide clear, step-by-step guidance
• Offer constructive, detailed feedback
• Use positive, encouraging language
• Be explicit about the importance of understanding each step`;

    try {
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-4',
            messages: [
                { role: 'system', content: systemPrompt },
                ...session.messages.slice(-6).map(msg => ({
                    role: msg.role,
                    content: msg.content
                }))
            ],
            temperature: 0.7,
            max_tokens: 500
        }, {
            headers: {
                'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        return response.data.choices[0].message.content;
    } catch (error) {
        console.error('OpenAI API error:', error);
        throw new Error('Failed to generate AI response');
    }
}

// Helper functions
function getStrategyName(strategy) {
    const strategies = {
        '1': 'Using synonyms and antonyms',
        '2': 'Changing word forms',
        '3': 'Changing voice',
        '4': 'Changing sentence patterns',
        '5': 'Using all strategies combined',
        'general': 'General inquiries'
    };
    return strategies[strategy] || 'General paraphrasing';
}

function getStrategyInstructions(strategy) {
    // Return specific instructions for each strategy
    const instructions = {
        '1': `Focus on teaching synonyms and antonyms replacement. Provide examples and ask students to practice with similar exercises.`,
        '2': `Teach how to change word forms (nouns to verbs, adjectives to adverbs, etc.). Demonstrate with clear examples.`,
        '3': `Explain active and passive voice conversion. Provide step-by-step guidance on voice changes.`,
        '4': `Show how to break complex sentences into simpler ones or combine simple sentences.`,
        '5': `Integrate all strategies for comprehensive paraphrasing practice.`,
        'general': `Help with general paraphrasing questions and academic writing advice.`
    };
    return instructions[strategy] || instructions['general'];
}

function calculateDuration(startTime) {
    const endTime = new Date();
    const duration = Math.floor((endTime - startTime) / 1000);
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    return `${minutes}m ${seconds}s`;
}

async function sendFeedbackEmail(sessionId, rating, feedback, email) {
    // Implementation for sending email (using SendGrid, Mailgun, etc.)
    console.log(`Would send email with feedback:`, { sessionId, rating, feedback, email });
    // Actual implementation would go here
}
app.get('/health', (req, res) => {
    res.status(200).json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development'
    });
});

// Root endpoint
app.get('/', (req, res) => {
    res.json({ 
        message: 'Paraphrasing Teacher Backend API',
        version: '1.0.0',
        endpoints: ['/api/chat', '/api/feedback', '/api/chat-history/:sessionId']
    });
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
    console.log('UNHANDLED REJECTION! 💥 Shutting down...');
    console.log(err.name, err.message);
    process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
    console.log('UNCAUGHT EXCEPTION! 💥 Shutting down...');
    console.log(err.name, err.message);
    process.exit(1);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
// Add this at the end of server.js, before app.listen
// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ 
        status: 'OK', 
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development'
    });
});

// Root endpoint
app.get('/', (req, res) => {
    res.json({ 
        message: 'Paraphrasing Teacher Backend API',
        version: '1.0.0',
        endpoints: ['/api/chat', '/api/feedback', '/api/chat-history/:sessionId']
    });
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
    console.log('UNHANDLED REJECTION! 💥 Shutting down...');
    console.log(err.name, err.message);
    process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
    console.log('UNCAUGHT EXCEPTION! 💥 Shutting down...');
    console.log(err.name, err.message);
    process.exit(1);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});