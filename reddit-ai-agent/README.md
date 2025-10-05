# Reddit AI Agent

## Overview
The Reddit AI Agent is a Python-based application designed to monitor niche Reddit communities, identify recurring user problems, and send a weekly summary email to the product team. The agent connects to the Reddit API, analyzes user posts to extract common pain points, and formats this information into a report that is sent via email.

## Project Structure
```
reddit-ai-agent
├── src
│   ├── main.py               # Entry point of the application
│   ├── reddit
│   │   └── fetcher.py        # Fetches posts from Reddit
│   ├── analysis
│   │   └── problem_identifier.py # Identifies recurring problems
│   ├── email
│   │   └── sender.py         # Sends email reports
│   └── utils
│       └── helpers.py        # Utility functions
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd reddit-ai-agent
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Reddit API credentials and email settings in the appropriate files.

## Usage
To run the application, execute the following command:
```
python src/main.py
```
This will initiate the process of fetching posts, analyzing them for recurring problems, and sending the report via email.

## Features
- Connects to the Reddit API to fetch posts from specified subreddits.
- Filters posts based on popularity and recency.
- Identifies common user problems using a language model.
- Formats and sends a weekly summary email to the product team.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.