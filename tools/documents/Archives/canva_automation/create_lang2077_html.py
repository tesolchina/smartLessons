#!/usr/bin/env python3
"""
LANG 2077 HTML Slides Creator
Creates a web-based presentation from lang2077_slides_content.md
"""

import os
from datetime import datetime


def create_html_slides():
    """Create HTML slides from LANG 2077 content."""
    
    print("🌐 Creating LANG 2077 HTML Slides")
    print("=" * 40)
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LANG 2077: Language Skills for human-AI partnership</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #8B0000 0%, #A52A2A 100%);
            color: #333;
            overflow: hidden;
        }
        
        .slideshow-container {
            position: relative;
            max-width: 100%;
            height: 100vh;
            margin: auto;
        }
        
        .slide {
            display: none;
            padding: 40px;
            text-align: center;
            height: 100vh;
            background: white;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            position: relative;
        }
        
        .slide.active {
            display: block;
        }
        
        /* HKBU Header */
        .slide-header {
            position: absolute;
            top: 20px;
            right: 30px;
            color: #8B0000;
            font-size: 14px;
            font-weight: bold;
        }
        
        /* Title Slide */
        .title-slide {
            background: linear-gradient(45deg, #8B0000, #A52A2A);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        .title-slide h1 {
            font-size: 4em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .title-slide .subtitle {
            font-size: 1.8em;
            margin-bottom: 20px;
            font-weight: 300;
        }
        
        .title-slide .subtitle2 {
            font-size: 1.4em;
            margin-bottom: 40px;
            font-weight: bold;
            color: #FFD700;
        }
        
        .title-slide .footer {
            font-size: 1.1em;
            color: #FFD700;
            font-weight: 300;
        }
        
        /* Content Slides */
        .content-slide h2 {
            color: #8B0000;
            font-size: 2.5em;
            margin-bottom: 40px;
            border-bottom: 3px solid #FFD700;
            padding-bottom: 15px;
        }
        
        .content-slide h3 {
            color: #A52A2A;
            font-size: 1.8em;
            margin-bottom: 30px;
            text-align: left;
        }
        
        .content-slide ul {
            text-align: left;
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        
        .content-slide li {
            margin-bottom: 8px;
        }
        
        .content-slide .main-point {
            color: #8B0000;
            font-weight: bold;
            font-size: 1.3em;
            margin-bottom: 15px;
            margin-top: 20px;
        }
        
        .content-slide .sub-point {
            color: #333;
            margin-left: 20px;
            font-size: 1.1em;
        }
        
        /* Navigation */
        .nav {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
        }
        
        .nav-btn {
            background: #8B0000;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .nav-btn:hover {
            background: #A52A2A;
            transform: translateY(-2px);
        }
        
        .nav-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        /* Slide Counter */
        .slide-counter {
            position: absolute;
            bottom: 30px;
            right: 30px;
            color: #8B0000;
            font-weight: bold;
        }
        
        /* Instructions */
        .instructions {
            position: absolute;
            top: 30px;
            left: 30px;
            color: #666;
            font-size: 14px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .slide {
                padding: 20px;
            }
            
            .title-slide h1 {
                font-size: 2.5em;
            }
            
            .content-slide h2 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="slideshow-container">
        <div class="instructions">
            Use ← → keys or buttons to navigate | Press F11 for fullscreen
        </div>
        
        <!-- Slide 1: Title -->
        <div class="slide active title-slide">
            <h1>LANG 2077</h1>
            <div class="subtitle">Language Skills for human-AI partnership:</div>
            <div class="subtitle2">Customizing Chatbots to Empower Communities</div>
            <div class="footer">Dr. Simon Wang | Language Centre, HKBU | Fall 2025</div>
        </div>
        
        <!-- Slide 2: Learning Outcomes -->
        <div class="slide content-slide">
            <div class="slide-header">HKBU Language Centre</div>
            <h2>What Students Will Learn</h2>
            <h3>Learning Outcomes & Objectives</h3>
            
            <div class="main-point">• Language Skills Development</div>
            <ul class="sub-point">
                <li>Academic communication in AI contexts</li>
                <li>Technical writing for AI applications</li>
                <li>Cross-cultural communication strategies</li>
            </ul>
            
            <div class="main-point">• AI Partnership Skills</div>
            <ul class="sub-point">
                <li>Understanding AI capabilities and limitations</li>
                <li>Effective human-AI collaboration</li>
                <li>Prompt engineering and chatbot interaction</li>
            </ul>
            
            <div class="main-point">• Community Engagement</div>
            <ul class="sub-point">
                <li>Identifying community needs</li>
                <li>Designing solutions with community partners</li>
                <li>Presenting results to stakeholders</li>
            </ul>
        </div>
        
        <!-- Slide 3: Community Empowerment -->
        <div class="slide content-slide">
            <div class="slide-header">HKBU Language Centre</div>
            <h2>Empowering Communities Through AI</h2>
            <h3>Service Learning Component</h3>
            
            <div class="main-point">• Community Partner Collaboration</div>
            <ul class="sub-point">
                <li>Work with local NGOs and organizations</li>
                <li>Identify real community challenges</li>
                <li>Co-design AI-enhanced solutions</li>
            </ul>
            
            <div class="main-point">• Chatbot Customization Projects</div>
            <ul class="sub-point">
                <li>Develop task-specific chatbots</li>
                <li>Adapt language for target audiences</li>
                <li>Test and iterate with community feedback</li>
            </ul>
            
            <div class="main-point">• Student Deliverables & Impact</div>
            <ul class="sub-point">
                <li>Final presentation to community partners</li>
                <li>Reflection essays on AI ethics</li>
                <li>Portfolio of customized AI tools</li>
            </ul>
        </div>
        
        <!-- Slide 4: Course Information -->
        <div class="slide content-slide">
            <div class="slide-header">HKBU Language Centre</div>
            <h2>Course Information</h2>
            
            <div class="main-point">• Course Structure & Timeline</div>
            <ul class="sub-point">
                <li>Week-by-week breakdown of activities and assignments</li>
            </ul>
            
            <div class="main-point">• Assessment Methods</div>
            <ul class="sub-point">
                <li>Grading rubrics, participation expectations, project criteria</li>
            </ul>
            
            <div class="main-point">• Required Resources</div>
            <ul class="sub-point">
                <li>Textbooks, software, online platforms students will use</li>
            </ul>
            
            <div class="main-point">• Contact Information</div>
            <ul class="sub-point">
                <li>Office hours, email, course website, support resources</li>
            </ul>
        </div>
        
        <!-- Navigation -->
        <div class="nav">
            <button class="nav-btn" onclick="changeSlide(-1)" id="prevBtn">❮ Previous</button>
            <button class="nav-btn" onclick="changeSlide(1)" id="nextBtn">Next ❯</button>
        </div>
        
        <div class="slide-counter">
            <span id="currentSlide">1</span> / <span id="totalSlides">4</span>
        </div>
    </div>

    <script>
        let currentSlideIndex = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        document.getElementById('totalSlides').textContent = totalSlides;
        
        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove('active'));
            slides[index].classList.add('active');
            
            document.getElementById('currentSlide').textContent = index + 1;
            document.getElementById('prevBtn').disabled = (index === 0);
            document.getElementById('nextBtn').disabled = (index === totalSlides - 1);
        }
        
        function changeSlide(direction) {
            currentSlideIndex += direction;
            if (currentSlideIndex < 0) currentSlideIndex = 0;
            if (currentSlideIndex >= totalSlides) currentSlideIndex = totalSlides - 1;
            showSlide(currentSlideIndex);
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', function(event) {
            if (event.key === 'ArrowLeft') changeSlide(-1);
            if (event.key === 'ArrowRight') changeSlide(1);
            if (event.key === 'Home') { currentSlideIndex = 0; showSlide(0); }
            if (event.key === 'End') { currentSlideIndex = totalSlides - 1; showSlide(totalSlides - 1); }
        });
        
        // Initialize
        showSlide(0);
        
        // Auto-fullscreen hint
        setTimeout(() => {
            if (!document.fullscreenElement) {
                console.log('Tip: Press F11 for fullscreen presentation mode');
            }
        }, 2000);
    </script>
</body>
</html>"""
    
    # Save HTML file
    slides_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/operating/canva_automation/generated_slides"
    os.makedirs(slides_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"LANG2077_slides_web_{timestamp}.html"
    filepath = os.path.join(slides_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML slides created: {filepath}")
    print(f"🌐 Open in browser for presentation")
    print(f"📱 Responsive design works on mobile/tablet")
    print(f"⌨️  Use arrow keys or buttons to navigate")
    print(f"🔗 Can be shared via web hosting or email")
    
    return filepath


if __name__ == "__main__":
    create_html_slides()
