# Knowledge Preservation Agent

An AI-powered assistant designed to preserve and transfer knowledge when team members leave the company. It maintains institutional memory by making departed employees' work knowledge, decisions, and context accessible through their documentation history. The system analyzes historical Slack messages, documents, and other work artifacts to answer questions about past projects, decisions, and processes. As a secondary feature, it can also serve as a helpful proxy while current team members are on vacation, ensuring uninterrupted time off.

[View Presentation](https://docs.google.com/presentation/d/17McpAm_a2MEW5haEsuEvKD8Fb_gE-fqYbdHGKLkCGm8/edit?usp=sharing)

## Demo Video
https://docs.google.com/presentation/d/17McpAm_a2MEW5haEsuEvKD8Fb_gE-fqYbdHGKLkCGm8/edit#slide=id.g340d32eb7a8_3_76


## Overview

The Knowledge Preservation agent is designed to:
- Preserve institutional knowledge when employees depart
- Provide insights into past decisions and their context
- Answer questions about completed projects and processes
- Make historical work discussions and documentation searchable
- Maintain continuity of knowledge across team changes
- Additionally, support current employees during vacation time

## Features

- Vector store-based document retrieval
- Integration with Slack messages and work documentation
- Powered by LLaMA v3 70B Instruct model
- Vector store-based document retrieval
- Configurable parameters for different use cases

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

Additional connector support e.g Outlook, Microsoft Teams, Jira, Dropbox, One Drive

Authentication and Access levels (Certain users like only the manager is able to access the agent)

An out of office agent for your colleagues on vacation

Adding/Deleting embeddings in existing agents

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
- Configurable information filtering before vector store indexing
- Audit logging of all queries and responses

## Version

Current version: 0.0.2

## License

Proprietary - All rights reserved 
