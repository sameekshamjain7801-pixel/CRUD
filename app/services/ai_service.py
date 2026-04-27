"""
AI service for Ollama integration.
Handles AI-powered data analysis queries.
"""
import json
import requests
from app.utils.logger import get_logger
from app.utils.errors import ExternalServiceError
from app.config import get_config

logger = get_logger(__name__)


class AIService:
    """Service for AI operations using Ollama"""
    
    def __init__(self):
        """Initialize AI service with configuration"""
        config = get_config()
        self.ollama_url = config.OLLAMA_URL
        self.model = config.OLLAMA_MODEL
        self.timeout = config.OLLAMA_TIMEOUT
        logger.info(f"AI Service initialized with model: {self.model}")
    
    def query_ai(self, question, context_data):
        """
        Query AI with question based on provided context data.
        
        Args:
            question: User's question string
            context_data: List/dict of context data to analyze
            
        Returns:
            AI response string
            
        Raises:
            ExternalServiceError: If Ollama service is unavailable or fails
        """
        try:
            # Construct the prompt
            context_json = json.dumps(context_data, indent=2)
            prompt = self._build_prompt(question, context_json)
            
            # Call Ollama API
            response = self._call_ollama(prompt)
            logger.info("Successfully processed AI query")
            return response
            
        except requests.exceptions.ConnectionError:
            logger.error("Ollama service not available")
            raise ExternalServiceError(
                "Ollama",
                "Service is not running. Please start Ollama first."
            )
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            raise ExternalServiceError(
                "Ollama",
                "Request timeout. Try a simpler question or increase timeout."
            )
        except Exception as e:
            logger.error(f"AI service error: {str(e)}")
            raise ExternalServiceError("Ollama", str(e))
    
    def _build_prompt(self, question, context):
        """
        Build prompt for Ollama.
        
        Args:
            question: User's question
            context: JSON context data
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an AI assistant for a CRUD application.
Use the following database records (JSON format) to answer the user's question.

Database Records:
{context}

Rules:
1. ONLY use the provided database records to answer.
2. If the answer is not found in the data, return: "Data not available"
3. Keep answers short, clear, and direct.
4. You can count records, summarize data, find highest/lowest values, and detect patterns.

User Question: {question}

Answer:"""
        return prompt
    
    def _call_ollama(self, prompt):
        """
        Make API call to Ollama.
        
        Args:
            prompt: Prompt string to send to Ollama
            
        Returns:
            AI response text
            
        Raises:
            Various requests exceptions or ExternalServiceError
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                error_msg = f"Status {response.status_code}: {response.text}"
                logger.error(f"Ollama API error: {error_msg}")
                raise ExternalServiceError("Ollama", error_msg)
            
            result = response.json()
            ai_answer = result.get("response", "").strip()
            
            if not ai_answer:
                logger.warning("Empty response from Ollama")
                raise ExternalServiceError("Ollama", "Empty response from AI model")
            
            return ai_answer
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error when calling Ollama: {str(e)}")
            raise
