#!/usr/bin/env python3
"""
Test script to verify Google grounding functionality
"""

import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

# Load environment variables
load_dotenv()

def test_grounding():
    """Test the grounding functionality"""
    try:
        # Configure the client
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Define the grounding tool
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        
        # Configure generation settings with grounding
        config = types.GenerateContentConfig(
            tools=[grounding_tool]
        )
        
        # Test query
        prompt = "Who won the Euro 2024 football championship?"
        
        print("Testing grounding functionality...")
        print(f"Query: {prompt}")
        
        # Make the request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        print(f"Response: {response.text}")
        print("\nGrounding test completed successfully!")
        
    except Exception as e:
        print(f"Error testing grounding: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_grounding()