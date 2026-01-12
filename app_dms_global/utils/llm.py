# utils/llm.py - MOCK VERSION ONLY
import time
import random
import json
from pathlib import Path
from typing import Optional

class DevelopmentLLM:
    """
    Development-only LLM that generates realistic mock responses.
    No API calls, no rate limits.
    """
    
    def __init__(self, cache_dir: str = ".llm_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        print("🚀 Development LLM initialized (no API calls)")
    
    def _get_mock_response(self, prompt: str, system: str) -> str:
        """Generate a realistic mock response."""
        
        # Extract keywords from prompt
        prompt_lower = prompt.lower()
        
        # Determine response type based on content
        if any(word in prompt_lower for word in ['financial', 'revenue', 'ebitda', 'profit']):
            template = """**Financial Analysis**

Based on the provided financial documents:
- Revenue projected to grow at 12-18% CAGR over next 3 years
- EBITDA margins expected to stabilize around 22-25%
- Cash flow positive by Q4 Year 1
- Key financial metrics show sustainable growth trajectory

**Recommendation**: Financial projections appear realistic and achievable."""
        
        elif any(word in prompt_lower for word in ['market', 'competitive', 'industry']):
            template = """**Market Analysis**

Market assessment indicates:
- Total Addressable Market: $1.8B - $2.5B range
- Serviceable Addressable Market: $450M - $600M
- Annual market growth rate: 10-14%
- 3 major competitors control ~55% market share
- Clear differentiation opportunity identified

**Recommendation**: Strong market positioning potential."""
        
        elif any(word in prompt_lower for word in ['risk', 'challenge', 'threat']):
            template = """**Risk Assessment**

Identified risk factors:
1. **Market Risk**: Moderate (evolving competitive landscape)
2. **Execution Risk**: Low-Medium (experienced team in place)
3. **Financial Risk**: Low (strong projected cash flows)
4. **Regulatory Risk**: Medium (monitor policy changes)

**Recommendation**: Risks appear manageable with proper mitigation."""
        
        elif any(word in prompt_lower for word in ['structure', 'legal', 'governance']):
            template = """**Structural Analysis**

Corporate structure assessment:
- Legal entity structure appropriate for target markets
- Governance framework aligns with best practices
- Equity structure supports growth objectives
- Compliance systems appear adequate

**Recommendation**: Structure supports business objectives."""
        
        else:
            template = """**Comprehensive Analysis**

Based on document review and {system} assessment:
- Strong fundamentals identified across key metrics
- Growth trajectory appears sustainable
- Competitive advantages clearly articulated
- Risk profile within acceptable parameters

**Recommendation**: Proceed with recommended due diligence steps.""".format(system=system)
        
        # Add some variability
        variations = [
            "Analysis indicates favorable conditions.",
            "Assessment shows promising opportunity.",
            "Review suggests viable investment case.",
            "Evaluation reveals strong potential."
        ]
        
        return template + f"\n\n*Note: {random.choice(variations)}*"
    
    def ask(self, prompt: str, system: str = "You are a senior investment analyst.", **kwargs) -> str:
        """Generate a mock response."""
        
        # Simulate processing time
        time.sleep(random.uniform(0.3, 1.2))
        
        print(f"📝 Dev LLM processing: {prompt[:60]}...")
        
        # Generate response
        response = self._get_mock_response(prompt, system)
        
        return response
    
    def batch_ask(self, prompts: list, system: str = "You are a senior investment analyst.", **kwargs):
        """Process multiple prompts."""
        responses = []
        for i, prompt in enumerate(prompts):
            print(f"📋 Dev LLM processing {i+1}/{len(prompts)}...")
            response = self.ask(prompt, system, **kwargs)
            responses.append(response)
            
            if i < len(prompts) - 1:
                time.sleep(random.uniform(0.5, 1.0))
        
        return responses


# Create global instance
llm = DevelopmentLLM()

# Backward compatible function
def ask(prompt: str, system: str = "You are a senior investment analyst.", **kwargs):
    return llm.ask(prompt, system, **kwargs)


if __name__ == "__main__":
    # Test
    test = "Analyze the financial projections and market opportunity."
    print("Testing Development LLM...")
    result = ask(test)
    print(f"✅ Response: {result[:100]}...")