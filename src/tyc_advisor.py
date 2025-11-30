from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, List, Dict
import os

# Load environment variables from .env file
load_dotenv()

# Import system prompt from Python config file
try:
    from src.prompt_config import SYSTEM_PROMPT as TYC_SYSTEM_PROMPT
except ImportError:
    raise ImportError(
        "prompt_config.py not found. Please create src/prompt_config.py with a SYSTEM_PROMPT variable."
    )

# Import PDF knowledge base
try:
    from src.pdf_knowledge import get_aaoifi_context
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("Warning: pdf_knowledge module not available. PDF context will not be included.")


class TYCIslamicFinanceAdvisor:

    """

    Thin wrapper around the OpenAI Chat Completions API that turns a base model

    into the "TYC – Islamic Finance Advisor".

    """

    def __init__(

        self,

        api_key: Optional[str] = None,

        model: str = "gpt-5.1",

    ):
        """

        :param api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)

        :param model:   Base model to use, e.g. "gpt-5.1" or "gpt-4.1-mini"

        """

        self.client = OpenAI(api_key=api_key)

        self.model = model

    def ask(

        self,

        user_message: str,

        history: Optional[List[Dict]] = None,

        max_tokens: Optional[int] = None,

        temperature: float = 0.3,

        use_pdf_context: bool = True,

    ) -> str:
        """

        Send a question to the TYC Islamic Finance Advisor.



        :param user_message: The user's question or prompt (string).

        :param history: Optional chat history as a list of {"role", "content"} dicts.

                        Roles should be "user" or "assistant".

                        System messages will be prepended automatically.

        :param max_tokens: Optional max tokens for the reply.

        :param temperature: Sampling temperature (0 = more deterministic).

        :param use_pdf_context: Whether to include relevant AAOIFI Standards PDF context (default: True).

        :return: Assistant reply as a string.

        """

        # Build the user message with PDF context if available
        enhanced_message = user_message

        if use_pdf_context and PDF_AVAILABLE:
            try:
                pdf_context = get_aaoifi_context(user_message, max_chars=2000)
                if pdf_context and pdf_context.strip():
                    enhanced_message = f"""{user_message}

---
Relevant context from AAOIFI Standards:
{pdf_context}
---
Please use the above AAOIFI Standards context to inform your answer when relevant."""
            except (MemoryError, SystemExit) as e:
                # Critical errors - disable PDF for future requests
                print(f"Critical error with PDF: {e}. PDF context disabled.")
                # Continue without PDF context
            except Exception as e:
                # Silently continue without PDF context - app should work without it
                pass

        messages = [{"role": "system", "content": TYC_SYSTEM_PROMPT}]

        if history:

            # assume history already alternates between user/assistant

            messages.extend(history)

        messages.append({"role": "user", "content": enhanced_message})

        # Build request parameters, only including max_tokens if provided
        request_params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            request_params["max_tokens"] = max_tokens

        response = self.client.chat.completions.create(**request_params)

        return response.choices[0].message.content


if __name__ == "__main__":

    # Example usage:

    advisor = TYCIslamicFinanceAdvisor()

    question = "Can you explain whether a conventional fixed-rate bond is Sharia-compliant?"

    answer = advisor.ask(question)

    print("Q:", question)

    print("A:", answer)
