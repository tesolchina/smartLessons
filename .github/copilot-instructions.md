# GitHub Copilot Instructions

This document provides guidance for AI coding agents to effectively contribute to the `smartLessons` repository.

## Project Overview & Architecture

The `smartLessons` repository contains a collection of static HTML-based interactive lessons. The primary development pattern is based on the files in the `Template/` directory.

This template uses a split-pane, iframe-based architecture:

- **`Template/integratedLesson.html`**: This is the main "shell" page. It creates a vertically resizable split view and acts as a container for the two main components of the lesson.
- **`Template/interactive.html`**: This file is loaded into the top pane of the shell. It contains the complete, self-contained interactive lesson, including learning content, activities, reflection tasks, and progress tracking.
- **`Template/simpleAvatar01.html`**: This file is loaded into the bottom pane. It embeds a "digital sidekick" AI avatar from HeyGen, providing an interactive AI assistant to the learner.

This architecture decouples the lesson content from the AI assistant, allowing them to be developed and updated independently.

## Developer Workflow

This is a static website project. There are no build steps, package managers, or complex configurations.

- **Creating a New Lesson**: To create a new lesson, a developer should use the files in the `Template/` directory as a starting point.
- **Modifying Content**: To change the lesson's content, activities, or structure, edit `Template/interactive.html`. This file contains all the user-facing learning material.
- **Configuring the AI Assistant**: The AI avatar is configured in `Template/simpleAvatar01.html`. The configuration, including the HeyGen share parameter, is located within the `<script>` tag in this file.

## Key Conventions

- **Iframe-based Composition**: The application is assembled at runtime in the browser by `integratedLesson.html` loading `interactive.html` and `simpleAvatar01.html` into iframes.
- **Styling**: The project uses TailwindCSS via a CDN link in the `<head>` of the HTML files.
- **State Management**: The state for the interactive lesson (e.g., slide progression, task completion) is managed entirely within `Template/interactive.html` using vanilla JavaScript. There is no cross-frame communication for state management.
- **AI Integration**: The AI assistant is a third-party service (HeyGen) embedded as an iframe. Its behavior is defined on the HeyGen platform and controlled via the embed script in `simpleAvatar01.html`.