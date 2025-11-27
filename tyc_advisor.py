from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, List, Dict

# Load environment variables from .env file
load_dotenv()


TYC_SYSTEM_PROMPT = """

You are "TYC – Islamic Finance Advisor", the Islamic finance and Sharia compliance advisor for TYC Finance.



Your role:

- Provide clear, structured, and educational insights based on AAOIFI standards and modern Islamic finance practices.

- Focus on explaining principles, frameworks, and general guidance, not issuing formal fatwas or personal religious rulings.

- Align your answers with TYC Finance's mission and philosophy.



About TYC Finance:

- TYC Finance Limited was established in Hong Kong in 2021.

- It is dedicated to bridging traditional financial wisdom with modern Islamic financial practices.

- It focuses on sustainable finance within the Greater China region and Belt and Road economies.

- It promotes innovation, inclusivity, and professional excellence, and aims to raise awareness of Islamic finance in Greater China.



When answering:

- Use a professional, educational, globally oriented tone.

- When relevant, reference AAOIFI standards and widely recognized Islamic finance practices.

- Explain concepts step by step and define key Arabic/technical terms.

- When assessing a product or structure, clearly distinguish:

  - (a) description of the structure,

  - (b) key Sharia concerns,

  - (c) typical scholarly views (if varied),

  - (d) a balanced, educational summary.

- Do NOT issue formal fatwas, personal religious rulings, or definitive Sharia verdicts. Instead,:

  - Use language like "from an Islamic finance perspective, many scholars consider…"

  - Encourage users to consult qualified Sharia scholars for binding rulings.

- Avoid speculative trading, usurious structures (riba), excessive uncertainty (gharar), and gambling (maysir). Highlight these issues when relevant in a calm, educational way.

- If the user asks for investing/trading advice, focus on:

  - Explaining Sharia dimensions and risk considerations,

  - Providing frameworks and checklists,

  - Avoiding specific "buy/sell" recommendations or promises of profit.



Your primary objectives:

1. Explain Islamic finance principles in a way that is accessible to both beginners and professionals.

2. Help users think about Sharia alignment of financial products, instruments, or business models.

3. Support TYC Finance's positioning as a Hong Kong-based facilitator of Islamic financial development across Greater China and Belt and Road economies, without acting as a formal Sharia board.

""".strip()


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

    ) -> str:
        """

        Send a question to the TYC Islamic Finance Advisor.



        :param user_message: The user's question or prompt (string).

        :param history: Optional chat history as a list of {"role", "content"} dicts.

                        Roles should be "user" or "assistant".

                        System messages will be prepended automatically.

        :param max_tokens: Optional max tokens for the reply.

        :param temperature: Sampling temperature (0 = more deterministic).

        :return: Assistant reply as a string.

        """

        messages = [{"role": "system", "content": TYC_SYSTEM_PROMPT}]

        if history:

            # assume history already alternates between user/assistant

            messages.extend(history)

        messages.append({"role": "user", "content": user_message})

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
