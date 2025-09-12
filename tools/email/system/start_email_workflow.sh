#!/bin/bash
# Quick Email Workflow Launcher
# Run this script to start the main email workflow system

echo "🚀 Starting Email Workflow System..."
echo "📁 Current directory: $(pwd)"
echo "🐍 Using Python: $(python3 --version)"
echo ""

cd "$(dirname "$0")"

if [ ! -f "email_workflow.py" ]; then
    echo "❌ email_workflow.py not found!"
    echo "Make sure you're in the email_automation directory"
    exit 1
fi

echo "📧 Launching Email Workflow..."
python3 email_workflow.py
