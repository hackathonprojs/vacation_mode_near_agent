# Knowledge Preservation Agent

An AI-powered assistant designed to preserve and transfer knowledge when team members leave the company. It maintains institutional memory by making departed employees' work knowledge, decisions, and context accessible through their documentation history. The system uses Slack messages, Google drive documents, Gmail emails, and other work artifacts to answer questions about past projects, decisions, and processes. As a secondary feature, it can also serve as a helpful proxy while current team members are on vacation, ensuring uninterrupted time off.

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
- Integration via connectors using the Slack API, Gmail API, and Google Drive API
- Uses OCR to extract text from Google Drive documents and Gmail attachments.
- Integrates the Microsoft Presidio SDK to detect and remove Personally Identifiable Information (PII) before embedding.
- Powered by LLaMA v3 70B Instruct model
- Configurable parameters for different use cases



## Technical Details


### Installations

Upload data into vector datastore

```
python3 /home/t/.nearai/registry/solwu.near/vacation-mode/0.0.1/vector.py
```

This uploads all .md file in this folder and underlying folders.

Run agent locally

```
nearai agent interactive /home/t/.nearai/registry/solwu.near/vacation-mode/0.0.1 --local
```

Upload the agent to Near AI Hub

```
nearai registry upload /home/t/.nearai/registry/solwu.near/vacation-mode/0.0.1
```

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
- Gmail emails
- Other indexed work-related content

## Privacy and Security

The agent works with your pre-processed and indexed data, ensuring that sensitive information is handled securely within your configured environment.

## Future Roadmap

The following improvements and features are planned for future releases:

- Additional connector support e.g Outlook, Microsoft Teams, Jira, Dropbox, One Drive
- Authentication and Access levels (Certain users like only the manager is able to access the agent)
- An out of office agent for your colleagues on vacation
- Adding/Deleting embeddings in existing agents

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

This project is licensed under the MIT License 

## Setup

**For a gmail service account:**

1. Create a service account for your organization
   
2. Open the service account in your cloud console and add a key

3. Add key for service account
   
   ![image]( https://i.imgur.com/A2wpnIH.png)
  
   
4. In the dropdown menu choose create key, then choose key type json

   ![image](https://i.imgur.com/Xd5ZRT5.png)

6. Place in root directory of project folder
   



**For slack:**

You will need to create a slack app and get a slackbot token in order to read messages from your workspace

![image](https://i.imgur.com/wuPtijL.png)

The following scopes are required:

![image](https://i.imgur.com/JO5g5vh.png)


**Create a .env file:**

Create a .env file inside root directory of your project replacing the follow fields with yours

```
SLACK_BOT_TOKEN={INSERT TOKEN HERE}

SERVICE_ACCOUNT_FILE_PATH={PATH TO SERVICE ACCOUNT JSON FILE}

DELEGATED_USER_EMAIL={THE EMAIL OF THE USER YOU IN YOUR ORGANIZATION YOU WANT TO PULL EMAILS FROM e.g david@coolcompany.ai}
```

**Install the dependencies:**
```
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

To run the connector scripts to pull user's emails, google drive documents, and slack workspace messages:
```
python .\gmail_connector.py

python .\google_drive_connector.py

python .\slack_connector.py
```

Remove pii from the connector output:
```
python .\pii_remover.py
```

Covert json output to markdown before uploading to agent
```
python .\json_to_markdown.py
```




