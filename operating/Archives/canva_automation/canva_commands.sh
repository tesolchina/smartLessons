#!/bin/bash
# Canva Collaborative CLI - Easy Commands
# Usage examples for creating and sharing Canva presentations

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "🎨 Canva Collaborative CLI - Quick Commands"
echo "================================================"

# Function to create LANG 2077 slides with specific collaborators
create_lang2077_collaborative() {
    echo "🎓 Creating LANG 2077 slides with collaboration..."
    
    # Default HKBU Language Centre collaborators
    COLLABORATORS=(
        "department.head@hkbu.edu.hk"
        "course.coordinator@hkbu.edu.hk" 
        "teaching.assistant@hkbu.edu.hk"
        "admin.support@hkbu.edu.hk"
    )
    
    # Join array elements with spaces
    COLLAB_LIST=$(IFS=' '; echo "${COLLABORATORS[*]}")
    
    echo "👥 Inviting collaborators:"
    for email in "${COLLABORATORS[@]}"; do
        echo "   - $email"
    done
    
    echo ""
    echo "🚀 Starting Canva automation..."
    
    cd "$SCRIPT_DIR"
    python3 canva_collaborative_cli.py \
        --collaborators $COLLAB_LIST \
        --template "academic presentation university" \
        --course "LANG2077"
}

# Function to create general collaborative presentation
create_collaborative_presentation() {
    echo "📊 Creating collaborative presentation..."
    echo "Enter collaborator emails (separated by spaces):"
    read -r collaborators
    
    echo "Enter template search term (e.g., 'academic presentation'):"
    read -r template
    
    if [ -z "$template" ]; then
        template="professional presentation"
    fi
    
    cd "$SCRIPT_DIR"
    python3 canva_collaborative_cli.py \
        --collaborators $collaborators \
        --template "$template"
}

# Function to show usage examples
show_usage() {
    echo ""
    echo "📋 Usage Examples:"
    echo ""
    echo "1. Create LANG 2077 slides with default collaborators:"
    echo "   ./canva_commands.sh lang2077"
    echo ""
    echo "2. Create custom collaborative presentation:"
    echo "   ./canva_commands.sh create"
    echo ""
    echo "3. Create with specific collaborators:"
    echo "   python3 canva_collaborative_cli.py --collaborators user1@hkbu.edu.hk user2@hkbu.edu.hk"
    echo ""
    echo "4. Create with custom template:"
    echo "   python3 canva_collaborative_cli.py --template 'creative colorful' --collaborators team@hkbu.edu.hk"
    echo ""
    echo "📧 Collaborator Features:"
    echo "   - Automatic email invitations sent"
    echo "   - Edit permissions granted by default"
    echo "   - Shareable link generated"
    echo "   - Real-time collaborative editing"
    echo ""
    echo "🔧 Setup Requirements:"
    echo "   1. Update .env.collaborative with your Canva email"
    echo "   2. Install dependencies: pip3 install -r requirements.txt"
    echo "   3. Make sure Chrome browser is installed"
    echo ""
}

# Main command handler
case "$1" in
    "lang2077"|"LANG2077")
        create_lang2077_collaborative
        ;;
    "create"|"new")
        create_collaborative_presentation
        ;;
    "help"|"--help"|"-h"|"")
        show_usage
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_usage
        ;;
esac
