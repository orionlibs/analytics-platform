"""LLM-based text extraction for complex fields."""

import llm
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
import re
import os
from pathlib import Path
from dotenv import load_dotenv


class LLMExtractor:
    """Extract structured data from text using LLM."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """Initialize with specified model."""
        # Try to load .env file from various locations
        self._load_env_file()
        
        # Check if API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        
        try:
            if api_key:
                # If we have an API key from env, ensure it's set for llm
                os.environ['OPENAI_API_KEY'] = api_key
                
            self.model = llm.get_model(model_name)
            # Test if the model works by making a simple request
            test_response = self.model.prompt("Say 'ok' if you're working")
            if test_response and test_response.text():
                self.available = True
            else:
                raise Exception("Model test failed")
        except Exception as e:
            if "No key found" in str(e) or "OPENAI_API_KEY" in str(e):
                print(f"⚠️  OpenAI API key not configured")
                print("   To use LLM features, either:")
                print("   1. Create a .env file with OPENAI_API_KEY=your-key")
                print("   2. Set the OPENAI_API_KEY environment variable")
                print("   3. Run: llm keys set openai")
            else:
                print(f"⚠️  LLM not available: {e}")
            print("   The tool will use regex-only extraction")
            self.model = None
            self.available = False
    
    def _load_env_file(self):
        """Load .env file from various locations."""
        # Try multiple locations for .env file
        possible_paths = [
            Path.cwd() / '.env',  # Current directory
            Path(__file__).parent.parent / '.env',  # Project root
            Path.home() / '.env',  # Home directory
        ]
        
        for env_path in possible_paths:
            if env_path.exists():
                load_dotenv(env_path)
                if os.getenv('OPENAI_API_KEY'):
                    print(f"✅ Loaded OpenAI API key from {env_path}")
                    break
    
    def extract_sponsors(self, staffing_text: str) -> Dict[str, List[str]]:
        """Extract GC and TC sponsors from staffing section."""
        if not self.available:
            return {"gc_sponsors": [], "tc_sponsors": [], "project_lead": None}
            
        prompt = f"""Extract sponsor information from this staffing section.
        
Return a JSON object with these fields:
- gc_sponsors: array of strings, each string should be "Name (Affiliation)" or just "Name" if no affiliation
- tc_sponsors: array of strings, each string should be "Name (Affiliation)" or just "Name" if no affiliation  
- project_lead: single string "Name (Affiliation)" or just "Name" if no affiliation, or null if not found

Example output:
{{
  "gc_sponsors": ["@danielgblanco (New Relic)"],
  "tc_sponsors": ["@tedsuo (Grafana Labs)", "@dyladan (Dynatrace)"],
  "project_lead": "@johndoe (Example Corp)"
}}

Text to analyze:
{staffing_text}

Return only valid JSON, no markdown formatting."""
        
        try:
            response = self.model.prompt(prompt)
            result = json.loads(response.text())
            
            # Ensure all values are strings, not dicts
            if isinstance(result.get('gc_sponsors'), list):
                result['gc_sponsors'] = [self._format_person(p) for p in result['gc_sponsors']]
            if isinstance(result.get('tc_sponsors'), list):
                result['tc_sponsors'] = [self._format_person(p) for p in result['tc_sponsors']]
            if result.get('project_lead'):
                result['project_lead'] = self._format_person(result['project_lead'])
                
            return result
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error extracting sponsors: {e}")
            return {"gc_sponsors": [], "tc_sponsors": [], "project_lead": None}
    
    def _format_person(self, person):
        """Format a person entry to a string."""
        if isinstance(person, str):
            return person
        elif isinstance(person, dict):
            name = person.get('name', '')
            affiliation = person.get('affiliation', '')
            if affiliation:
                return f"{name} ({affiliation})"
            return name
        return str(person)
    
    def extract_dates_from_timeline(self, timeline_text: str, reference_date: Optional[datetime] = None) -> Dict[str, Optional[str]]:
        """Extract start and end dates from timeline section."""
        if not self.available:
            return {"start_date": None, "end_date": None, "confidence": "low", "notes": "LLM not available"}
            
        if reference_date is None:
            reference_date = datetime.now()
        
        prompt = f"""Extract timeline dates from this text. Today's date is {reference_date.strftime('%Y-%m-%d')}.

Look for:
1. Explicit dates (e.g., "April 2025", "2025-04-01")
2. Relative dates (e.g., "one month in", "by Q2")
3. Project start dates or when work begins
4. Target completion dates or major milestone dates

Return a JSON object with:
- start_date: estimated start date in YYYY-MM-DD format (null if unclear)
- end_date: estimated end/target date in YYYY-MM-DD format (null if unclear)
- confidence: "high", "medium", or "low"
- notes: any important timeline notes

Text to analyze:
{timeline_text}

Return only valid JSON, no markdown formatting."""
        
        try:
            response = self.model.prompt(prompt)
            return json.loads(response.text())
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error extracting dates: {e}")
            return {"start_date": None, "end_date": None, "confidence": "low", "notes": ""}
    
    def determine_sponsorship_level(self, sponsors: Dict[str, List[str]], project_text: str) -> str:
        """Determine sponsorship level based on sponsors and project content.
        
        Note: The actual sponsorship level mapping from project names to levels
        is not straightforward. This uses heuristics and should be manually reviewed.
        """
        has_gc = len(sponsors.get("gc_sponsors", [])) > 0
        has_tc = len(sponsors.get("tc_sponsors", [])) > 0
        
        # Check for explicit mentions in text
        text_lower = project_text.lower()
        if "escalating" in text_lower:
            return "Escalating"
        elif "leading" in text_lower and "sponsor" in text_lower:
            return "Leading"
        elif "guiding" in text_lower and "sponsor" in text_lower:
            return "Guiding"
        
        # Heuristic based on sponsor presence
        # Note: This is approximate - actual levels require manual mapping
        if has_tc and has_gc:
            return "Leading"  # Projects with both types often have higher sponsorship
        elif has_tc:
            return "Guiding"  # TC sponsors typically indicate active guidance
        elif has_gc:
            return "Escalating"  # GC-only might need escalation
        else:
            return "None"  # No sponsors
    
    def extract_deliverables_summary(self, deliverables_text: str) -> str:
        """Create a concise summary of project deliverables."""
        if not self.available:
            return ""
            
        prompt = f"""Create a brief summary (2-3 sentences) of the key deliverables from this text.
Focus on the main outcomes and goals.

Text to analyze:
{deliverables_text}

Return only the summary text, no formatting."""
        
        try:
            response = self.model.prompt(prompt)
            return response.text().strip()
        except Exception as e:
            print(f"Error summarizing deliverables: {e}")
            return ""
    
    def extract_project_timeline(self, full_markdown: str, git_dates: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive timeline information from the full project markdown."""
        if not self.available:
            return {
                "start_date": None,
                "end_date": None,
                "milestones": [],
                "confidence": "low",
                "notes": "LLM not available"
            }
        
        # Include git dates in context for the LLM
        git_context = ""
        if git_dates.get("created"):
            git_context = f"\nNote: This project file was created in git on {git_dates['created'].strftime('%Y-%m-%d')}."
        if git_dates.get("moved_to_completed"):
            git_context += f"\nNote: This project was moved to 'completed' status on {git_dates['moved_to_completed'].strftime('%Y-%m-%d')}."
        if git_dates.get("moved_to_inactive"):
            git_context += f"\nNote: This project was moved to 'inactive' status on {git_dates['moved_to_inactive'].strftime('%Y-%m-%d')}."
        
        prompt = f"""Analyze this OpenTelemetry project document to extract timeline information.
{git_context}

Please extract:
1. Project start date or when work began/will begin
2. Project completion date, target date, or major milestone dates
3. Any intermediate milestones with dates
4. If the project is ongoing, estimate completion based on:
   - Mentioned quarters (Q1/Q2/Q3/Q4) and years
   - Phrases like "6 months", "by end of year", etc.
   - Progress indicators in the document

Important guidelines:
- Convert quarters to specific dates: Q1=March 31, Q2=June 30, Q3=September 30, Q4=December 31
- If you see "1H2024" use June 30, 2024; "2H2024" use December 31, 2024
- For ongoing projects without clear end dates, estimate based on typical project duration (6-12 months)
- If extremely uncertain about end date, use 2025-12-31

Return a JSON object with:
{{
  "start_date": "YYYY-MM-DD or null",
  "end_date": "YYYY-MM-DD or null", 
  "milestones": [
    {{"date": "YYYY-MM-DD", "description": "milestone description"}}
  ],
  "confidence": "high/medium/low",
  "reasoning": "Brief explanation of date extraction logic"
}}

Document to analyze:
{full_markdown}

Return only valid JSON, no markdown formatting."""
        
        try:
            response = self.model.prompt(prompt)
            result = json.loads(response.text())
            
            # Validate and clean the result
            if not isinstance(result.get('milestones'), list):
                result['milestones'] = []
            
            # Ensure dates are strings or None
            for field in ['start_date', 'end_date']:
                if result.get(field) and not isinstance(result[field], str):
                    result[field] = None
                    
            return result
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error extracting project timeline: {e}")
            return {
                "start_date": None,
                "end_date": None,
                "milestones": [],
                "confidence": "low",
                "reasoning": f"Error during extraction: {str(e)}"
            }