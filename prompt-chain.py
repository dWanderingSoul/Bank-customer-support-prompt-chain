
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CATEGORIES = [
    "Account Opening",
    "Billing Issue",
    "Account Access",
    "Transaction Inquiry",
    "Card Services",
    "Account Statement",
    "Loan Inquiry",
    "General Information",
]

def call_llm(prompt: str) -> str:
    """
    Sends a single-turn prompt to the model and returns plain text output.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_prompt_chain(query: str):
    """
    Executes the full 5-stage prompt chain and returns
    a list of intermediate results in order.
    
    Args:
        query (str): Customer's free-text query
        
    Returns:
        list: Five intermediate outputs [intent, categories, chosen, details, response]
    """
    # ============================================================
    # STAGE 1: INTERPRET CUSTOMER INTENT
    # ============================================================
    prompt_1 = f"""Analyze the following customer query and identify the primary intent or concern the customer is expressing.

Customer Query: {query}

Provide:
1. A concise one-sentence summary of the customer's intent
2. Up to three short intent keywords (single words)

Format your response clearly."""

    out1 = call_llm(prompt_1)
    
    # ============================================================
    # STAGE 2: MAP TO POSSIBLE CATEGORIES
    # ============================================================
    prompt_2 = f"""Based on the customer's intent and original query, suggest the top 3 most relevant categories from the following list. Rank them in order of relevance.

Available Categories:
{chr(10).join(f'- {cat}' for cat in CATEGORIES)}

For each suggested category, provide 1-2 short reasons why it might apply.

Customer Query: {query}
Interpreted Intent: {out1}

Format your response as a ranked list with explanations."""

    out2 = call_llm(prompt_2)
    
    # ============================================================
    # STAGE 3: CHOOSE THE MOST APPROPRIATE CATEGORY
    # ============================================================
    prompt_3 = f"""Review the suggested categories below and select the single most appropriate category that best matches the customer's intent.

Category Suggestions:
{out2}

Provide:
1. The chosen category name (exactly as listed)
2. A one-sentence explanation for why this is the best match

If none of the suggestions fit well, choose "General Information" as the default."""

    out3 = call_llm(prompt_3)
    
    # ============================================================
    # STAGE 4: EXTRACT ADDITIONAL DETAILS
    # ============================================================
    prompt_4 = f"""Identify any additional details or information needed to fully address the customer's request.

Customer Query: {query}
Chosen Category: {out3}

For each required detail, provide:
- Label: (e.g., "Transaction Date")
- Reason: (why this information is needed)
- Question: (how to ask the customer for this information)

If no additional details are needed, respond with: "No additional details required"

Format your response as a structured list."""

    out4 = call_llm(prompt_4)
    
    # ============================================================
    # STAGE 5: GENERATE SHORT RESPONSE
    # ============================================================
    prompt_5 = f"""Generate a professional, helpful response to the customer based on the information gathered.

Customer Query: {query}
Interpreted Intent: {out1}
Chosen Category: {out3}
Required Details: {out4}

Your response should:
- Acknowledge the customer's concern
- Be 2-4 sentences long
- Be professional and empathetic
- Request any missing information if needed
- Provide clear next steps

Write only the customer response, without any preamble or labels."""

    out5 = call_llm(prompt_5)
    
    return [out1, out2, out3, out4, out5]

if __name__ == "__main__":
    # Test queries
    test_queries = [
        "I noticed an unfamiliar charge on my debit card for $40 yesterday.",
        "I can't log into my account and need to check my balance urgently",
        "How do I apply for a personal loan?",
        "Can you send me my account statement for last month?"
    ]
    
    print("="*80)
    print("BANK CUSTOMER SUPPORT PROMPT CHAIN - TEST RESULTS")
    print("="*80)
    
    for i, sample in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {sample}")
        print('='*80)
        
        try:
            results = run_prompt_chain(sample)
            
            stage_names = [
                "Intent Interpretation",
                "Category Suggestions",
                "Chosen Category",
                "Required Details",
                "Customer Response"
            ]
            
            for idx, (name, result) in enumerate(zip(stage_names, results), 1):
                print(f"\nSTAGE {idx} - {name}:")
                print("-" * 60)
                print(result)
                
        except Exception as e:
            print(f"Error: {e}")
        
        print()