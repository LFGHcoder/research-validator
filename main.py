import os
import re
from typing import List, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from search_service import search_claim

# Optional imports for embeddings
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

try:
    import google.generativeai as genai
    HAS_GEMINI_LIB = True
except ImportError:
    HAS_GEMINI_LIB = False
    genai = None

try:
    from openai import OpenAI
    HAS_OPENAI_LIB = True
except ImportError:
    HAS_OPENAI_LIB = False
    OpenAI = None

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Research Validator API",
    description="Validates factual claims using web search and AI embeddings",
    version="1.0.0"
)

# Allow CORS for frontend (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client (optional - preferred for free tier)
gemini_api_key = os.getenv("GEMINI_API_KEY", "")
if HAS_GEMINI_LIB and HAS_NUMPY and gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_client = genai
    except Exception:
        gemini_client = None
else:
    gemini_client = None

# Initialize OpenAI client (optional - fallback)
openai_api_key = os.getenv("OPENAI_API_KEY", "")
if HAS_OPENAI_LIB and HAS_NUMPY and openai_api_key:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
    except Exception:
        openai_client = None
else:
    openai_client = None


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Research Validator API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    gemini_key_set = bool(os.getenv("GEMINI_API_KEY"))
    openai_key_set = bool(os.getenv("OPENAI_API_KEY"))
    you_key_set = bool(os.getenv("YOU_API_KEY"))
    
    # Service is healthy if YOU_API_KEY is set (required)
    # Embeddings are optional (uses fallback if missing)
    status = "healthy" if you_key_set else "degraded"
    
    # Determine which similarity method will be used
    if gemini_key_set:
        similarity_method = "Gemini embeddings (free tier)"
    elif openai_key_set:
        similarity_method = "OpenAI embeddings"
    else:
        similarity_method = "text-based matching"
    
    return {
        "status": status,
        "gemini_api_key": "set" if gemini_key_set else "missing",
        "openai_api_key": "set" if openai_key_set else "missing",
        "you_api_key": "set" if you_key_set else "missing (required)",
        "similarity_method": similarity_method
    }


def split_into_factual_sentences(text: str, max_sentences: int = 5) -> list[str]:
    """
    Split input text into up to max_sentences factual sentences.
    
    Args:
        text: Input text to split
        max_sentences: Maximum number of sentences to return (default: 5)
    
    Returns:
        List of factual sentences (up to max_sentences)
    """
    # Split text into sentences using regex
    # Pattern matches sentence endings (. ! ?) followed by space or end of string
    sentence_pattern = r'(?<=[.!?])\s+'
    sentences = re.split(sentence_pattern, text.strip())
    
    # Also split on newlines if no punctuation found
    if len(sentences) == 1 and '\n' in sentences[0]:
        sentences = [s.strip() for s in sentences[0].split('\n') if s.strip()]
    
    # Clean sentences and filter out empty ones
    cleaned_sentences = [s.strip() for s in sentences if s.strip()]
    
    # If no sentences found with punctuation, treat entire text as one sentence
    if not cleaned_sentences:
        cleaned_sentences = [text.strip()]
    
    # Very lenient filtering - accept almost everything as factual
    factual_sentences = []
    
    for sentence in cleaned_sentences:
        # Only skip if it's a pure question (ends with ? and is short)
        if sentence.strip().endswith('?') and len(sentence.split()) < 3:
            continue
        
        # Only skip if it's a single word
        if len(sentence.split()) < 1:
            continue
        
        factual_sentences.append(sentence)
        
        # Stop once we have enough sentences
        if len(factual_sentences) >= max_sentences:
            break
    
    # If we don't have enough, add remaining sentences
    if len(factual_sentences) < max_sentences:
        remaining = [s for s in cleaned_sentences if s not in factual_sentences]
        factual_sentences.extend(remaining[:max_sentences - len(factual_sentences)])
    
    # Final fallback: if absolutely nothing, return the original text as one claim
    if not factual_sentences and text.strip():
        factual_sentences = [text.strip()]
    
    return factual_sentences[:max_sentences] if factual_sentences else []


def compute_similarity_simple(claim: str, snippet: str) -> float:
    """
    Simple text-based similarity using keyword matching (fallback when OpenAI not available).
    
    Args:
        claim: The claim text to compare
        snippet: The snippet text to compare against
    
    Returns:
        Similarity score between 0 and 1 (higher is more similar)
    """
    # Normalize text
    claim_lower = claim.lower()
    snippet_lower = snippet.lower()
    
    # Split into words
    claim_words = set(claim_lower.split())
    snippet_words = set(snippet_lower.split())
    
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    claim_words = claim_words - stop_words
    snippet_words = snippet_words - stop_words
    
    if not claim_words:
        return 0.5  # If claim has no meaningful words, give medium score
    
    # Calculate Jaccard similarity (intersection over union)
    intersection = len(claim_words & snippet_words)
    union = len(claim_words | snippet_words)
    
    if union == 0:
        return 0.0
    
    jaccard = intersection / union
    
    # Boost score if key phrases match
    claim_phrases = claim_lower.split()
    snippet_lower_full = snippet_lower
    phrase_matches = sum(1 for phrase in claim_phrases if len(phrase) > 3 and phrase in snippet_lower_full)
    
    # Combine Jaccard similarity with phrase matching
    similarity = min(1.0, jaccard * 0.7 + (phrase_matches / max(len(claim_phrases), 1)) * 0.3)
    
    return float(similarity)


def compute_similarity(claim: str, snippet: str) -> float:
    """
    Compute similarity between claim and snippet.
    Tries Gemini (free tier) first, then OpenAI, then falls back to simple text matching.
    
    Args:
        claim: The claim text to compare
        snippet: The snippet text to compare against
    
    Returns:
        Similarity score between 0 and 1 (higher is more similar)
    """
    # Try Gemini embeddings first (free tier - preferred for hackathons)
    if gemini_client and HAS_NUMPY:
        try:
            # Get embeddings using Gemini's embedding model
            claim_result = gemini_client.embed_content(
                model="models/embedding-001",
                content=claim
            )
            snippet_result = gemini_client.embed_content(
                model="models/embedding-001",
                content=snippet
            )
            
            claim_embedding = np.array(claim_result['embedding'])
            snippet_embedding = np.array(snippet_result['embedding'])
            
            # Calculate cosine similarity
            dot_product = np.dot(claim_embedding, snippet_embedding)
            norm_claim = np.linalg.norm(claim_embedding)
            norm_snippet = np.linalg.norm(snippet_embedding)
            
            # Avoid division by zero
            if norm_claim == 0 or norm_snippet == 0:
                # Fall through to next method
                raise ValueError("Zero norm")
            
            similarity = dot_product / (norm_claim * norm_snippet)
            return float(similarity)
        except Exception as e:
            # Fall through to OpenAI or text matching
            pass
    
    # Try OpenAI embeddings as fallback
    if openai_client and HAS_NUMPY:
        try:
            # Get embeddings for both texts
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=[claim, snippet]
            )
            
            # Extract embeddings
            claim_embedding = np.array(response.data[0].embedding)
            snippet_embedding = np.array(response.data[1].embedding)
            
            # Calculate cosine similarity
            dot_product = np.dot(claim_embedding, snippet_embedding)
            norm_claim = np.linalg.norm(claim_embedding)
            norm_snippet = np.linalg.norm(snippet_embedding)
            
            # Avoid division by zero
            if norm_claim == 0 or norm_snippet == 0:
                return compute_similarity_simple(claim, snippet)
            
            similarity = dot_product / (norm_claim * norm_snippet)
            return float(similarity)
        except Exception as e:
            # Fall back to simple similarity if OpenAI fails
            return compute_similarity_simple(claim, snippet)
    else:
        # Use simple text-based similarity
        return compute_similarity_simple(claim, snippet)


def map_similarity_to_confidence(similarity_score: float) -> str:
    """
    Map similarity score to confidence level.
    
    Args:
        similarity_score: Cosine similarity score between 0 and 1
    
    Returns:
        Confidence level: "High", "Medium", or "Low"
    """
    if similarity_score >= 0.8:
        return "High"
    elif similarity_score >= 0.5:
        return "Medium"
    else:
        return "Low"


class ValidateRequest(BaseModel):
    text: str


class ClaimResult(BaseModel):
    claim: str
    similarity_score: float
    confidence: str
    best_match_snippet: Optional[str] = None
    best_match_url: Optional[str] = None


class ValidateResponse(BaseModel):
    validated: bool
    claims: List[ClaimResult]
    message: str


@app.post("/validate", response_model=ValidateResponse)
async def validate(request: ValidateRequest):
    """
    Validate input text by:
    1. Splitting into factual sentences
    2. Searching for evidence for each claim
    3. Computing similarity scores
    4. Mapping to confidence levels
    """
    try:
        # Validate required API key (YOU_API_KEY is required for search)
        if not os.getenv("YOU_API_KEY"):
            return ValidateResponse(
                validated=False,
                claims=[],
                message="Error: YOU_API_KEY not set in environment variables. This is required for web search."
            )
        
        # Check which embedding service is available
        use_gemini = bool(os.getenv("GEMINI_API_KEY"))
        use_openai = bool(os.getenv("OPENAI_API_KEY"))
        
        # Validate input
        if not request.text or not request.text.strip():
            return ValidateResponse(
                validated=False,
                claims=[],
                message="Error: Input text cannot be empty."
            )
        
        # Split text into factual sentences
        factual_sentences = split_into_factual_sentences(request.text, max_sentences=5)
        
        # Debug: Always return at least the input text as a claim if nothing found
        if not factual_sentences:
            # Fallback: use the entire text as one claim
            factual_sentences = [request.text.strip()] if request.text.strip() else []
        
        if not factual_sentences:
            return ValidateResponse(
                validated=False,
                claims=[],
                message=f"No text provided. Please provide text to validate."
            )
        
        # Debug output (remove in production)
        print(f"DEBUG: Found {len(factual_sentences)} sentences: {factual_sentences}")
        
        claim_results = []
        
        # Process each factual sentence
        for claim in factual_sentences:
            try:
                # Search for evidence
                search_results = search_claim(claim)
                
                if not search_results:
                    # No search results found - still add the claim with Low confidence
                    claim_results.append(ClaimResult(
                        claim=claim,
                        similarity_score=0.0,
                        confidence="Low",
                        best_match_snippet=None,
                        best_match_url=None
                    ))
                    continue
                
                # Compute similarity with each snippet and find the best match
                best_similarity = 0.0
                best_snippet = None
                best_url = None
                
                for result in search_results:
                    snippet = result.get("snippet", "")
                    if snippet:
                        similarity = compute_similarity(claim, snippet)
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_snippet = snippet
                            best_url = result.get("url")
                
                # Map similarity to confidence
                confidence = map_similarity_to_confidence(best_similarity)
                
                claim_results.append(ClaimResult(
                    claim=claim,
                    similarity_score=round(best_similarity, 4),
                    confidence=confidence,
                    best_match_snippet=best_snippet,
                    best_match_url=best_url
                ))
            except Exception as e:
                # If processing a claim fails, add it with Low confidence
                claim_results.append(ClaimResult(
                    claim=claim,
                    similarity_score=0.0,
                    confidence="Low",
                    best_match_snippet=None,
                    best_match_url=None
                ))
        
        # Determine overall validation status
        # Validated = true only if we have at least one Medium / High confidence claim.
        # This way, obviously wrong claims with only Low confidence will show validated = false.
        has_strong_evidence = any(
            result.confidence in ["High", "Medium"] for result in claim_results
        ) if claim_results else False
        overall_validated = has_strong_evidence
        
        # Build message with info about similarity method used
        if use_gemini:
            similarity_method = "Gemini embeddings (free tier)"
        elif use_openai:
            similarity_method = "OpenAI embeddings"
        else:
            similarity_method = "text-based matching"
        
        # Ensure we always return claims if we processed any text at all
        if not claim_results and request.text.strip():
            # Fallback: treat the input text itself as one Low-confidence claim
            claim_results.append(
                ClaimResult(
                    claim=request.text[:200],
                    similarity_score=0.0,
                    confidence="Low",
                    best_match_snippet=None,
                    best_match_url=None,
                )
            )
            overall_validated = False
        
        # Build informative message
        if has_strong_evidence:
            msg = f"Processed {len(claim_results)} claim(s) using {similarity_method}. Found strong evidence for some claims."
        elif overall_validated:
            msg = f"Processed {len(claim_results)} claim(s) using {similarity_method}. Claims found but need stronger evidence."
        else:
            msg = f"Processed {len(claim_results)} claim(s) using {similarity_method}."
        
        return ValidateResponse(
            validated=overall_validated,  # True only if strong evidence was found
            claims=claim_results,
            message=msg,
        )
    
    except Exception as e:
        # Catch any unexpected errors - but still try to return something useful
        import traceback
        error_details = str(e)
        print(f"ERROR in validate endpoint: {error_details}")
        print(traceback.format_exc())
        
        # Try to return at least the input text as a claim
        fallback_claim = ClaimResult(
            claim=request.text[:200] if request.text else "Error processing",
            similarity_score=0.0,
            confidence="Low",
            best_match_snippet=None,
            best_match_url=None
        )
        
        return ValidateResponse(
            validated=False,
            claims=[fallback_claim],
            message=f"Error processing request: {error_details}. Returning input as claim."
        )


# Windows multiprocessing guard
if __name__ == "__main__":
    import uvicorn
    # Try port 8000, if busy use 8001
    import socket
    port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        print(f"Port {port} is in use, trying port 8001...")
        port = 8001
    
    uvicorn.run(app, host="127.0.0.1", port=port)
