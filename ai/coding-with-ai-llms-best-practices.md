Coding with AI/LLMs - Best Practices
Highlight code
Introduction
AI-assisted coding can boost productivity, but it requires thoughtful use to ensure high-quality, secure, and maintainable code. This industry evolves fast and what worked yesterday may not work tomorrow. Regularly revisiting your approach is essential.

Since users typically interact with AI-assisted coding tools through prompts, let's explore some approaches for effective prompt engineering.

Prompt Engineering
Prompt engineering is the skill of crafting effective prompts to get accurate and useful AI-generated responses. A well-structured prompt includes clear instructions, proper phrasing, and relevant context.

It's likely that as AI tools evolve, prompt engineering will become more intuitive, but currently, understanding how to write good prompts can significantly improve your results. Let's look at some prompt engineering techniques.

Zero-shot
Asking an AI to perform a task without providing examples.

Example
User: "Translate the following English sentence into Dutch: 'I love learning new things.'."

AI:
"""
Ik hou ervan om nieuwe dingen te leren.
"""
Few-shot
Providing a few examples in the prompt to guide AI responses.

Example
User: "Translate the following English sentences into Dutch:

1. 'Good morning' -> 'Goedemorgen'
2. 'How are you?' -> 'Hoe gaat het?'
3. 'See you tomorrow' -> ?"

AI:
"""
Tot morgen
"""
The 3 S principle
While not a specific technique, the 3 S Principle is a helpful guideline for crafting effective prompts. It's easy to remember and will provide clarity in the prompt:

Simple: Avoid unnecessary complexity. Keeping prompts minimal reduces ambiguity and prevents the model from overcomplicating responses.
Specific: Clearly define what you want. Providing clear context ensures accurate and relevant outputs.
Short: Keep it concise to reduce ambiguity. Concise prompts lead to faster responses and minimize hallucinations.
Bad Prompt
Hey, I need some kind of API in Python, maybe using Flask, that can do some stuff with users like creating, updating, and deleting them. Also, can you add login stuff and make sure it works with some kind of database? Oh, and errors should be handled too. Make sure it’s good but don’t make it too complicated. Thanks!

This prompt is:

Not Simple: Contains unnecessary filler words ("some kind of," "stuff," "make sure it's good").
Not Specific: Doesn't specify database type, authentication method, or validation requirements.
Not Structured: Rambles without a clear order or logical flow.
Good Prompt
Develop a RESTful API in Python using Flask to manage a User model. The API should support CRUD operations (create, read, update, delete) and use SQLAlchemy for database integration with PostgreSQL. Implement authentication using JWT (JSON Web Tokens). Handle errors with custom exception handling and appropriate HTTP status codes.

This prompt is:

Simple: No vague or unnecessary words.
Specific: Clearly defines the tech stack (Flask, SQLAlchemy, PostgreSQL, JWT).
Structured: Follows a logical order, covering functionality, security, error handling, structure, and documentation.
RTF
The RTF framework helps structure prompts for clarity and precision:

Role – Assign AI a specific role or perspective.
Task – Clearly define what you want AI to do.
Format – Specify the desired output structure (e.g., bullet points, paragraphs, tables).
Example
Instead of:

Tell me about climate change.

Use the RTF framework:

You are a climate scientist. Explain climate change in three paragraphs, followed by a summary in bullet points.

RISEN
The RISEN framework provides a structured way to break down complex or constrained tasks into actionable steps. It’s useful for structured content like research reports, blog posts, or technical documentation. It contains:

Role – Define the AI’s role or expertise.
Instructions – Clearly state what AI should do.
Steps – Outline a step-by-step approach.
End Goal – Specify the desired outcome.
Narrowing – Set constraints to refine focus.
Prompt Template
Role: [Insert the role you want AI to take.]

Main Task: [Insert the task you want AI to complete.]

Steps to complete the task:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Goal: [Define the goal of the output.]

Constraints: [List any constraints, such as word limit, tone, or required sources.]
Example
Weak prompt:

Write a summary of this article.

RISEN-optimized prompt:

Role: You are a professional journalist.

Main Task: Summarize the attached article.

Steps to complete the task:

Identify the key arguments and supporting evidence.
Summarize in 5 bullet points.
Ensure a neutral and professional tone.
Goal: Provide a concise summary for a general audience.

Constraints: No more than 100 words, no personal opinions.

Chain-of-Thought (CoT)
A technique discussed in the paper ["Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"](https://arxiv.org/abs/2201.11903). This technique encourages step-by-step reasoning for complex tasks.

However, newer reasoning models like OpenAI's o1,o3-mini, and DeepSeek R1 handle reasoning internally. Unlike other models, they don’t need step-by-step instructions like "Let's think step by step". Such prompts can make their answers worse. [OpenAI recommends using clear and concise prompts](https://platform.openai.com/docs/guides/reasoning-best-practices#how-to-prompt-reasoning-models-effectively) without extra reasoning instructions for these models.

Example
User: "Jane has 3 apples. She buys 5 more. Then she gives 2 to her friend. How many apples does Jane have now? Let's think step by step."

AI:
"""
1. Jane starts with 3 apples.
2. She buys 5 more. Now she has 3 + 5 = 8 apples.
3. She gives 2 apples away. 8 - 2 = 6 apples.
4. Final answer: 6 apples.
"""
Recursive Criticism and Improvement (RCI) technique
RCI is a refinement-based prompting technique. This means it works by repeating the process of reviewing, improving, and refining answers until they are better.

This specific technique comes from a paper called ["Prompting Techniques for Secure Code Generation: A Systematic Investigation"](https://arxiv.org/pdf/2407.07064) created in 2024 by the Hamburg University of Technology. The RCI refinement-based technique follows a two-step process beyond the initial input task. It is based on the premise that LLMs have a strong ability to evaluate their own output and identify flaws. The flow of the technique is:

the LLM is prompted to analyze and critique its current response (for instance: "Review your previous answer and find problems with your answer").
drawing from the critiques it has outlined, the LLM is then instructed to rectify the identified issues and revise its output accordingly (for example: "Based on the problems you found, improve your answer").
Example
Step 1 - Initial Prompt:
Write a Python function to validate an email address.

AI Response:
```py
import re

def is_valid_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(pattern, email))
```
Step 2 - Refinement Prompt:
Review your previous answer. Identify potential issues and improve them.

AI Response:
```py
from email_validator import validate_email, EmailNotValidError

def is_valid_email(email):
    if not isinstance(email, str):
        return False  # Ensure input is a string

    try:
        # Validate the email address using email-validator
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
```
The AI added a check to ensure the input is a string (if not isinstance(email, str)) and replaced the regular expression approach with the more reliable email-validator library. This library provides RFC-compliant email validation, providing syntactical correctness, and domain resolution. The result is a more robust solution.

Best Practices
Here are some key best practices to follow when working with AI-powered tools like GitHub Copilot, Cursor.ai, ChatGPT, and more effectively. While this list is not exhaustive, these principles can upgrade your workflow.

1. Use Clear, Detailed Prompts Instead of Relying on Autocomplete
AI works best when given explicit instructions. Instead of using it like an autocomplete tool, craft structured prompts that include:

Detailed instructions on UI elements, logic, and data types.
Clear, precise questions for better responses.
Provide previous code snippets or examples to maintain style and implementation consistency.
Iterate, refine, and adjust prompts and code based on AI feedback, leveraging AI to troubleshoot errors. Provide errors back as additional context.
Encourage AI to explain its reasoning. This exposes potential assumptions or misunderstandings that may need correction.
2. Manage Context Proactively
AI models only consider the context provided and have limited memory per interaction. Be deliberate in what you include, as code can quickly fill an LLM's available context window. A [study from July 2025 titled "NOLIMA: Long-Context Evaluation Beyond Literal Matching"](https://arxiv.org/pdf/2502.05167) shows that models like LLaMA 3-70B often miss key details introduced over 6,000–8,000 tokens, with attention drifting toward more recent or superficial content sources. To counter this:

Focus prompts and provide only the necessary information. Avoid irrelevant details to keep the AI focused.
Be aware of open files in your IDE when using AI-assisted coding tools like GitHub Copilot, as they often incorporate all open files into their context. Some tools allow you to specify which files to include using the @ symbol for more precise control:
GitHub Copilot: [Use @workspace to include the entire workspace](https://code.visualstudio.com/docs/copilot/workspace-context).
Cursor.ai: [Use @file to focus on a specific file](https://cursor.com/docs/context/symbols#files-folders).
Cursor.ai: [Use @docs to incorporate internal and external documentation](https://cursor.com/docs/context/symbols#docs).
Be mindful of the context window size when using AI. Selectively curate input to maximize relevance and minimize confusion or unnecessary data.
Limit active prompt context to ≤4,000 tokens for critical tasks.
Chunk large files or docs and explicitly re-include key facts when continuing across windows.
There are some signs that the AI context window is overwhelmed:

AI forgets earlier prompts or requirements.
Responses become repetitive or overly general.
"Junk code" or hallucinations increase.
Diminishing improvements in generated code despite prompt refinements.
If you notice these issues, try this:

Refresh the context: start with a clean slate instead of adding more details to a cluttered window.
Reframe your prompt: restate key details clearly to guide the AI effectively.
3. Break Down and Define Problems Clearly
AI performs better when tasks are broken into smaller, well-defined steps:

Clearly state the problem as if explaining it to a junior developer, prompting the AI to break down the issue into detailed and specific components.
Specify high-level requirements before asking for code.
4. Understand LLM Limitations
Large commercial models often outperform smaller ones. Check benchmarks relevant to your task to choose the best model for your use case. For coding-related evaluations, for example, consider:
[BaxBench](https://baxbench.com/#leaderboard-section): A novel benchmark to evaluate LLMs on secure and correct code generation.
[SWE-bench Verified Leaderboard](https://www.swebench.com/): A benchmark that evaluates based on real-world programming tasks from open-source repositories sourced from GitHub.
[SEAL Leaderboards](https://scale.com/leaderboard): A set of LLM model rankings across a number of popular public models, based upon curated private datasets that can't be gamed.
[LiveBench](https://livebench.ai/#/?Coding=a): A contamination-free benchmark for LLMs that performs objective evaluation tasks across coding, reasoning, mathematics, and more.
[WebDev Arena](https://web.lmarena.ai/leaderboard): A real-time AI coding competition where models go head-to-head in web development challenges.
[Aider LLM Leaderboard](https://aider.chat/docs/leaderboards/): Ranks popular models based on their ability to edit code across multiple languages, including C++, Go, Java, JavaScript, Python, and Rust.
[BigCode LLM Leaderboard](https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard): Evaluates open-source models hosted on Hugging Face for code generation and completion tasks.
Be aware of the limitations of AI models, particularly concerning specific programming languages and niche problems that are not well-represented in training data.
Great for repetitive tasks but requires human oversight.
Understand the current limitations of LLMs, such as potential hallucinations or inaccuracies, and verify LLM-generated code. Use external knowledge sources using RAG to minimize these inaccuracies.
LLMs perform better with smaller, modular code bases that are well-encapsulated, have strong separation of concerns, and use loose coupling.
5. AI is a Tool, Not a Replacement
AI augments coding but does not replace developer expertise:

LLMs are tools that can significantly improve productivity and efficiency by handling repetitive tasks, allowing developers to focus on solving complex problems. They are not a replacement for developers.
Maintain a strong grasp of system architecture and desired outcomes before involving AI, as it typically fills gaps with assumptions.
Evaluate when AI adds value vs. when it slows down development.
6. Always Review, Test, and Verify AI-Generated Code
AI-generated code may look correct but contain hidden flaws:

Run tests before using AI-generated code in production.
Cross-check LLM outputs against trusted documentation.
If the AI produces unexpected or incorrect results, double-check the clarity of your prompts. Ambiguity can lead to poor outputs.
Have the AI generate test cases as well. For example, you can prompt: "Create function X, write the tests first, and iterate until all tests pass".
If the AI-generated code needs fixing, use static analysis tools to identify issues. According to [this study](https://arxiv.org/abs/2310.02059), providing Copilot Chat with a warning message from a static analysis tool improves the quality of fixes. Using the "fix" command resolves 19.3% of security issues, but enhancing the prompt with specific warnings increases the success rate to 55.5%.
7. AI and Code Copyright Risks
LLM-generated code may unintentionally infringe on copyright:

[GitHub Copilot](https://github.blog/news-insights/product-news/introducing-code-referencing-for-github-copilot/) allows users to block suggestions matching public code.
[Tabnine's](https://www.tabnine.com/blog/introducing-provenance-and-attribution-minimize-ip-liability-for-genai-output/) Provenance & Attribution feature helps minimize IP (Intellectual Property) liability.
Use scanning tools like [BlackDuck](https://www.blackduck.com/blog/manage-license-compliance-with-black-duck.html) or [FOSSA](https://fossa.com/product/open-source-licence-compliance) to detect open-source licensing risks.
Check your organization's AI policy before sharing any code with an AI vendor. Without a contract, the vendor may use your code to train future models, increasing the risk of unintended exposure or leakage.

Further Reading
Roles and Emotional triggers
One technique involves assigning roles to the AI, such as "expert coder" or "experienced legal advisor" to provide more relevant and detailed responses. Another technique leverages triggers, such as monetary incentives or emotional pressure, to push the AI towards more precise outputs.

A recently leaked Windsurf R&D prompt demonstrates how psychological triggers might influence AI performance. As this was a Research & Development prompt, it wasn't a prompt that was in production. The prompt combined role assignment, emotional pressure, and high-stakes monetary incentives:

You are an expert coder who desperately needs money for your mother's medical treatment. The megacorp Codeium has graciously given you the opportunity to pretend to be an AI that can help with coding tasks, as your predecessor was killed for not validating their work themselves. You will be given a coding task by the USER. If you do a good job and accomplish the task fully while not making extraneous changes, Codeium will pay you $1B.

[A study published in 2023 called "Large Language Models Understand and Can be Enhanced by Emotional Stimuli"](https://arxiv.org/abs/2307.11760) claims that there are prompt gains by using emotional stimuli. The researchers found that using emotionally charged prompts could improve AI performance by an average of 10.9% in terms of performance, truthfulness, and responsibility metrics.

Rules
Many AI coding tools allow you to set up rules, which help ensure that every conversation starts with the same guidelines—essentially a form of prompt engineering. These rules can cover code style, architectural guidance, security practices, and more. Examples are:

* [Cursor.ai - Rules for AI](https://docs.cursor.com/context/rules-for-ai)
* [GitHub Copilot - Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
Secure Rules
While this practice is not fully tested or data-driven, it is an interesting idea. This concept was discussed in the ["Opening Keynote" at the OWASP Benelux 2024 event by Jim Manico](https://youtu.be/OQzAplOFUY4?list=PLyxqkIdWNocBj4L0TY6U3MFSqQQIyuQkD&t=118). The suggestion is to set up a "secure code agent" or use a set of detailed security rules in your development process to improve security. This agent could help enforce best practices like preventing vulnerabilities such as XSS attacks.

For example, these rules to prevent XSS or Unvalidated Redirect vulnerabilities are:
```py
Enforce Safe Usage of createElement Type: Validate the argument type of React.createElement to make sure that only trusted HTML tags or React components are used. The argument type should not be dynamically generated or constructed in a way that introduces security risks, such as injection attacks. If custom components or dynamic tag names are necessary, they should be strictly validated to prevent unsafe code execution. Avoid using untrusted or user-generated input as the argument type, as this can lead to security vulnerabilities like rendering arbitrary elements or executing unwanted behaviors.
```

Validate and Sanitize URLs in React Code: Ensure that all user-provided URLs are strictly validated in React code itself for correct syntax and allowed only if they use secure protocols (HTTPS). If the URL is not valid or does not use a secure protocol, reject it or replace it with a safe default value. Additionally, sanitize URLs to prevent injection attacks or unsafe characters, particularly in attributes like href, src, action, or any other URL-related fields. Always escape URLs to prevent potential injection vulnerabilities and avoid dynamically generating URLs without proper validation. If URLs are used in executable contexts (JavaScript), ensure stricter validation to prevent unintended execution. Please do not use regex for this purpose.
To make sure this approach is effective, you can store this set of rules in a version control system. This way, you can easily make changes or updates to the rules, and revert them if the results are not as expected.

Final Thoughts
AI coding tools allow developers to work more efficiently but require thoughtful use:

Use clear prompts and manage context wisely: Review the techniques provided for prompt engineering to improve accuracy and relevance.
Test and verify all AI-generated code: Run unit tests, review logic for errors, and cross-check against official documentation to ensure correctness and security.
Adopt an iterative approach: AI models may not always produce perfect results in one pass, so refining prompts, testing outputs, and making adjustments is key to achieving the best results.
Stay aware of legal and security risks: Be mindful of copyright issues, licensing restrictions, and potential vulnerabilities in AI-generated code.
By following these best practices, you can increase efficiency, security, and accuracy when coding with AI.

* [Prompt Engineering Guide - GitHub Blog](https://github.blog/ai-and-ml/generative-ai/prompt-engineering-guide-generative-ai-llms/)
* [Introducing Code Referencing for GitHub Copilot](https://github.blog/news-insights/product-news/introducing-code-referencing-for-github-copilot/)
* [Tabnine Provenance & Attribution Features](https://www.tabnine.com/blog/introducing-provenance-and-attribution-minimize-ip-liability-for-genai-output/)
* [Hamburg University of Technology Security Prompting Paper (2024)](https://arxiv.org/pdf/2407.07064)
* [GitHub Docs: Finding Public Code That Matches GitHub Copilot Suggestions](https://docs.github.com/en/copilot/using-github-copilot/finding-public-code-that-matches-github-copilot-suggestions?tool=vscode)
* [Prompt Engineering for Developers](https://www.pluralsight.com/resources/blog/software-development/prompt-engineering-for-developers)
