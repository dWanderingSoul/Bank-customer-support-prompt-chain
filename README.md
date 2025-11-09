# Bank Customer Support Prompt Chain

An intelligent customer support system that uses AI prompt chaining to process and respond to customer queries in a structured, step-by-step manner.

## Overview

This project implements a 5-stage prompt chain that:
1. **Interprets** customer intent from free-text queries
2. **Maps** the query to possible categories
3. **Selects** the most appropriate category
4. **Extracts** additional details from the query
5. **Generates** a professional response to the customer

## Categories

All queries are classified into one of these categories:
- Account Opening
- Billing Issue
- Account Access
- Transaction Inquiry
- Card Services
- Account Statement
- Loan Inquiry
- General Information

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API key**
   
   **Option A: Environment Variable (Recommended)**
   ```bash
   # On Windows
   set OPENAI_API_KEY=your-api-key-here
   
   # On macOS/Linux
   export OPENAI_API_KEY=your-api-key-here
   ```
   
   **Option B: .env file**
   ```bash
   # Create a .env file in the project root
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

## Usage

### Running the Script

```bash
python prompt-chain.py
```

This will run the test examples included in the script.

### Using in Your Code

```python
from prompt_chain import run_prompt_chain

# Process a customer query
customer_query = "I can't log into my account and need help urgently"
results = run_prompt_chain(customer_query)

# Access individual stage results
intent = results[0]                  # Stage 1: Intent
suggested_categories = results[1]    # Stage 2: Category mapping
selected_category = results[2]       # Stage 3: Category selection
extracted_details = results[3]       # Stage 4: Detail extraction
final_response = results[4]          # Stage 5: Final response

print(f"Response: {final_response}")
```

## Example Output

```
Query: "I can't log into my account and I need to check my balance urgently"

Stage 1 - Intent Interpretation:
The customer is unable to access their account and needs urgent assistance with login issues to check their balance.

Stage 2 - Suggested Categories:
• Account Access - The customer explicitly mentions they cannot log into their account
• General Information - Could be seeking general help with account issues

Stage 3 - Selected Category:
Account Access - This is the most appropriate category because the customer's primary issue is inability to log in, which directly relates to account access problems.

Stage 4 - Extracted Details:
1. Extracted Details:
   - Urgency level: High (customer mentions "urgently")
   - Primary need: Check balance
   
2. Missing Details:
   - Username or account number
   - Error messages received
   - Device/platform being used
   - Last successful login date

Stage 5 - Final Response:
I understand you're having trouble accessing your account and need to check your balance urgently. Let me help you resolve this right away. Could you please provide your username or registered email address, and let me know if you're seeing any specific error messages when trying to log in?
```

## Project Structure

```
.
├── prompt-chain.py      # Main implementation file
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
├── README.md           # This file
└── .env                # API keys (create this, never commit!)
```

## API Costs

This implementation uses OpenAI's `gpt-4o-mini` model, which is cost-effective for this use case:
- Each query processes through 5 API calls
- Estimated cost: ~$0.001 - $0.003 per complete query chain
- Adjust the model in the code if needed (e.g., `gpt-4` for higher quality)

## Security Notes

⚠️ **IMPORTANT**: Never commit your API keys to version control!
- API keys are stored in environment variables or `.env` files
- The `.gitignore` file prevents accidental commits
- If you accidentally commit a key, revoke it immediately and generate a new one

## Troubleshooting

### "OpenAI API key not found"
- Ensure your `OPENAI_API_KEY` environment variable is set
- Check that your API key is valid and active
- Verify you have API credits available

### "Module not found: openai"
- Run `pip install -r requirements.txt`
- Ensure you're using the correct Python environment

### Rate Limit Errors
- Wait a few seconds between requests
- Consider implementing exponential backoff
- Check your OpenAI usage limits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is created for educational purposes as part of the AI for Developers course.

## Support

For issues or questions:
1. Check the [OpenAI API documentation](https://platform.openai.com/docs)
2. Review the troubleshooting section above
3. Open an issue in this repository

## Acknowledgments

- Built using OpenAI's GPT-4o-mini model
- Part of the "AI for Developers" course prompt chaining assignment
