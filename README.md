# Vacation Mode Agent

An AI-powered assistant that helps answer questions about your work while you're away on vacation or off work. This agent acts as your knowledgeable proxy, responding to your manager's and colleagues' work-related questions using your Slack messages and other work documentation, allowing you to enjoy an uninterrupted vacation.

## Overview

The Vacation Mode agent is designed to:
- Answer your manager's and colleagues' questions while you're away
- Maintain work continuity without disturbing your vacation time
- Access and search through Slack messages and other work-related documents
- Provide relevant context from your communication history
- Help reduce work interruptions during your time off

## Features

- Vector store-based document retrieval
- Integration with Slack messages and work documentation
- Powered by LLaMA v3 70B Instruct model
- Configurable model parameters
- Efficient context-aware responses

## Technical Details

### Requirements

- Python 3.x
- nearai library
- Access to Fireworks AI model API
- Configured vector store

### Configuration

The agent uses the following default configuration (from metadata.json):
```json
{
  "model": "llama-v3p1-70b-instruct",
  "model_provider": "fireworks",
  "model_temperature": 1.0,
  "model_max_tokens": 16384
}
```

### Project Structure

- `agent.py`: Main agent implementation
- `vector.py`: Vector store utilities
- `data_connectors/`: Data source connectors
- `metadata.json`: Project configuration
- `slack_messages.md`: Processed Slack message data
- `gdrive_results.md`: Google Drive data results

## Usage

The agent automatically processes incoming queries and responds with relevant information from your work history. It searches through your indexed documents and communications to provide context-appropriate answers.

## Data Sources

The agent can access and utilize:
- Slack messages
- Google Drive documents
- Other indexed work-related content

## Privacy and Security

The agent works with your pre-processed and indexed data, ensuring that sensitive information is handled securely within your configured environment.

## Future Work

The following improvements and features are planned for future releases:

### Data Processing
- Implement improved chunking strategies for better context preservation
- Optimize document segmentation for more accurate responses
- Enhanced preprocessing of different document types

### Additional Data Sources
- Integration with meeting notes and recordings
- Calendar event context and history
- Project management tools integration
- Email integration
- Code repository comments and documentation

### Security and Privacy Enhancements
- Granular access control for different types of information
- Role-based access restrictions
- Automated removal of sensitive information (PII, confidential data)
- Configurable information filtering before vector store indexing
- Audit logging of all queries and responses

## Version

Current version: 0.0.2

## License

Proprietary - All rights reserved 