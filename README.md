# DailyAssistant

AI-powered daily assistant for academic and research tasks, featuring secure credential management and integration with Google APIs, document processing, and specialized tools for research projects.

## Features

- **Secure Credential Management**: Environment variable-based configuration for API keys and sensitive data
- **Google APIs Integration**: Secure authentication for Google Docs, Drive, and Slides
- **Document Processing**: PDF to markdown conversion, document enhancement tools
- **Email Automation**: Smart email handling and automated responses
- **Research Tools**: Specialized modules for various research projects
- **Project Organization**: Structured tools for different academic projects

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone https://github.com/simonwang/DailyAssistant.git
   cd DailyAssistant
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

2. **Configure Environment**
   ```bash
   cp .env.template .env
   # Edit .env with your credentials
   ```

3. **Security Setup**
   - Follow the [Security Migration Guide](docs/SECURITY_MIGRATION_GUIDE.md)
   - Never commit credentials to git
   - Use environment variables for all sensitive data

## Structure

- `dailyassistant/` - Core application package
- `tools/` - Utility scripts and modules
- `projects/` - Specific research projects
- `docs/` - Documentation and guides
- `config/` - Configuration and security modules

## Security

This project implements secure credential management:
- All API keys and sensitive data use environment variables
- No credentials are stored in repository files
- Comprehensive .gitignore prevents accidental credential commits
- See [Security Migration Guide](docs/SECURITY_MIGRATION_GUIDE.md) for details

## Contributing

1. Ensure all credentials use environment variables
2. Follow the project structure guidelines
3. Update documentation for new features
4. Test all changes before committing

## License

MIT License - see LICENSE file for details.