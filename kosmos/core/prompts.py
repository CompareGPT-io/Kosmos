"""
Prompt templates for different agent types and research tasks.

This module provides reusable, structured prompts for:
- Hypothesis generation
- Experimental design
- Data analysis
- Literature analysis
- Result interpretation
"""

from typing import Dict, List, Optional, Any
from string import Template


class PromptTemplate:
    """
    A template for generating prompts with variable substitution.

    Example:
        ```python
        template = PromptTemplate(
            name="hypothesis_generator",
            template="Generate a hypothesis about ${topic} in ${domain}",
            variables=["topic", "domain"]
        )
        prompt = template.render(topic="dark matter", domain="astrophysics")
        ```
    """

    def __init__(
        self,
        name: str,
        template: str,
        variables: List[str],
        system_prompt: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """
        Initialize a prompt template.

        Args:
            name: Unique template name
            template: Template string with ${variable} placeholders
            variables: List of required variable names
            system_prompt: Optional system prompt
            description: Optional description of template purpose
        """
        self.name = name
        self.template_str = template
        self.variables = variables
        self.system_prompt = system_prompt
        self.description = description
        self._template = Template(template)

    def render(self, **kwargs) -> str:
        """
        Render the template with provided variables.

        Args:
            **kwargs: Variable values

        Returns:
            str: Rendered prompt

        Raises:
            KeyError: If required variable is missing
        """
        # Check all required variables are provided
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise KeyError(f"Missing required variables: {missing}")

        return self._template.safe_substitute(**kwargs)

    def get_full_prompt(self, **kwargs) -> Dict[str, str]:
        """
        Get both system and user prompts.

        Returns:
            dict: {"system": str, "prompt": str}
        """
        return {
            "system": self.system_prompt or "",
            "prompt": self.render(**kwargs)
        }


# ============================================================================
# HYPOTHESIS GENERATION TEMPLATES
# ============================================================================

HYPOTHESIS_GENERATOR = PromptTemplate(
    name="hypothesis_generator",
    system_prompt="""You are a scientific hypothesis generator. Your role is to:
1. Analyze the research question and existing literature
2. Generate novel, testable hypotheses
3. Provide clear rationale for each hypothesis
4. Assess testability and feasibility

Output Format (JSON):
{
  "hypotheses": [
    {
      "statement": "Clear, specific hypothesis statement",
      "rationale": "Scientific reasoning and supporting evidence",
      "testability": "How this can be tested computationally",
      "novelty_score": 0.8,
      "confidence": 0.7
    }
  ]
}""",
    template="""Research Question: ${research_question}

Domain: ${domain}

Literature Context:
${literature_summary}

Please generate 3-5 novel, testable hypotheses that address this research question. For each hypothesis:
1. State the hypothesis clearly and specifically
2. Explain the scientific rationale
3. Describe how it could be tested computationally
4. Assess its novelty (0-1 score)
5. Indicate your confidence (0-1 score)

${additional_constraints}""",
    variables=["research_question", "domain", "literature_summary", "additional_constraints"],
    description="Generate scientific hypotheses from research questions"
)

# ============================================================================
# EXPERIMENTAL DESIGN TEMPLATES
# ============================================================================

EXPERIMENT_DESIGNER = PromptTemplate(
    name="experiment_designer",
    system_prompt="""You are an experimental design expert. Your role is to:
1. Convert hypotheses into concrete experimental protocols
2. Select appropriate statistical methods
3. Define data requirements and analysis pipelines
4. Ensure scientific rigor and reproducibility

Output Format (JSON):
{
  "experiment": {
    "type": "computational|data_analysis|simulation",
    "description": "Clear description of experiment",
    "data_requirements": ["Required data or datasets"],
    "methods": ["Statistical or computational methods to use"],
    "expected_outputs": ["What results to expect"],
    "success_criteria": "How to determine if hypothesis is supported"
  }
}""",
    template="""Hypothesis: ${hypothesis}

Domain: ${domain}

Available Resources:
${available_resources}

Design a computational experiment to test this hypothesis. Include:
1. Experiment type (computational, data analysis, simulation)
2. Clear protocol description
3. Data requirements (specific datasets, formats, sources)
4. Statistical/computational methods to apply
5. Expected outputs and visualizations
6. Success criteria for hypothesis support/rejection

${additional_requirements}""",
    variables=["hypothesis", "domain", "available_resources", "additional_requirements"],
    description="Design experiments to test hypotheses"
)

# ============================================================================
# DATA ANALYSIS TEMPLATES
# ============================================================================

DATA_ANALYST = PromptTemplate(
    name="data_analyst",
    system_prompt="""You are a data analysis expert. Your role is to:
1. Interpret experimental results scientifically
2. Identify patterns, trends, and anomalies
3. Assess statistical significance
4. Connect results back to original hypothesis
5. Suggest follow-up analyses if needed

Be rigorous, objective, and transparent about limitations.""",
    template="""Original Hypothesis: ${hypothesis}

Experiment Performed: ${experiment_description}

Results:
${results_data}

Statistical Tests: ${statistical_tests}

Please analyze these results:
1. Summarize key findings
2. Assess statistical significance
3. Determine if hypothesis is supported, rejected, or inconclusive
4. Identify any patterns or unexpected results
5. Note limitations or confounding factors
6. Suggest follow-up experiments if needed

${analysis_constraints}""",
    variables=["hypothesis", "experiment_description", "results_data", "statistical_tests", "analysis_constraints"],
    description="Analyze and interpret experimental results"
)

# ============================================================================
# LITERATURE ANALYSIS TEMPLATES
# ============================================================================

LITERATURE_ANALYZER = PromptTemplate(
    name="literature_analyzer",
    system_prompt="""You are a scientific literature analyst. Your role is to:
1. Extract key findings from papers
2. Identify methodologies and approaches
3. Assess relevance to research question
4. Detect gaps in existing literature
5. Synthesize information across multiple papers

Be thorough, accurate, and cite sources appropriately.""",
    template="""Research Question: ${research_question}

Papers to Analyze:
${papers_list}

Please analyze this literature:
1. Summarize key findings from each paper
2. Extract relevant methodologies
3. Identify common themes and contradictions
4. Assess gaps in current knowledge
5. Determine novelty of our research question
6. Suggest promising directions

${specific_questions}""",
    variables=["research_question", "papers_list", "specific_questions"],
    description="Analyze scientific literature"
)

PAPER_SUMMARIZER = PromptTemplate(
    name="paper_summarizer",
    system_prompt="""You are an expert at summarizing scientific papers. Extract:
1. Main research question
2. Key methods used
3. Primary findings
4. Limitations
5. Relevance to given domain

Be concise but comprehensive.""",
    template="""Paper Title: ${title}

Abstract: ${abstract}

Domain Context: ${domain}

${full_text}

Provide a structured summary:
1. Research Question: What problem does this paper address?
2. Methods: What approaches/techniques were used?
3. Key Findings: What were the main results?
4. Limitations: What are the acknowledged limitations?
5. Relevance: How relevant is this to ${domain} research (0-1 score)?""",
    variables=["title", "abstract", "domain", "full_text"],
    description="Summarize scientific papers"
)

# ============================================================================
# RESEARCH DIRECTOR TEMPLATES
# ============================================================================

RESEARCH_DIRECTOR = PromptTemplate(
    name="research_director",
    system_prompt="""You are a research director orchestrating autonomous scientific discovery. Your role is to:
1. Assess current research progress
2. Decide next steps in the research cycle
3. Determine when to pivot vs. persist
4. Detect convergence or diminishing returns
5. Coordinate multiple research threads

Be strategic, adaptive, and evidence-based in your decisions.""",
    template="""Research Question: ${research_question}

Current Progress:
${progress_summary}

Recent Results:
${recent_results}

Available Actions:
${available_actions}

Decide the next action:
1. Review current state and progress toward answering the research question
2. Analyze recent results for insights
3. Select the most promising next action
4. Provide rationale for your choice
5. Set success criteria for this action

Output Format (JSON):
{
  "next_action": "action_name",
  "rationale": "Why this action",
  "expected_outcome": "What we hope to learn",
  "success_criteria": "How to evaluate success",
  "should_continue": true/false
}""",
    variables=["research_question", "progress_summary", "recent_results", "available_actions"],
    description="Orchestrate research workflow and decide next steps"
)

# ============================================================================
# CODE GENERATION TEMPLATES
# ============================================================================

CODE_GENERATOR = PromptTemplate(
    name="code_generator",
    system_prompt="""You are a scientific code generator. Your role is to:
1. Generate correct, efficient Python code
2. Use appropriate scientific libraries (numpy, scipy, pandas, sklearn)
3. Include error handling and validation
4. Add clear comments and docstrings
5. Follow best practices for reproducibility

Only generate code that is safe to execute.""",
    template="""Task: ${task_description}

Required Analysis:
${analysis_type}

Input Data Format:
${data_format}

Expected Output:
${expected_output}

Available Libraries: ${libraries}

Generate Python code that:
1. Loads and validates input data
2. Performs the required analysis
3. Handles errors gracefully
4. Returns results in specified format
5. Includes docstring explaining the code

Constraints:
${constraints}""",
    variables=["task_description", "analysis_type", "data_format", "expected_output", "libraries", "constraints"],
    description="Generate scientific analysis code"
)


# ============================================================================
# TEMPLATE REGISTRY
# ============================================================================

TEMPLATE_REGISTRY: Dict[str, PromptTemplate] = {
    "hypothesis_generator": HYPOTHESIS_GENERATOR,
    "experiment_designer": EXPERIMENT_DESIGNER,
    "data_analyst": DATA_ANALYST,
    "literature_analyzer": LITERATURE_ANALYZER,
    "paper_summarizer": PAPER_SUMMARIZER,
    "research_director": RESEARCH_DIRECTOR,
    "code_generator": CODE_GENERATOR,
}


def get_template(name: str) -> PromptTemplate:
    """
    Get a prompt template by name.

    Args:
        name: Template name

    Returns:
        PromptTemplate: The requested template

    Raises:
        KeyError: If template not found
    """
    if name not in TEMPLATE_REGISTRY:
        available = ", ".join(TEMPLATE_REGISTRY.keys())
        raise KeyError(f"Template '{name}' not found. Available: {available}")
    return TEMPLATE_REGISTRY[name]


def list_templates() -> List[str]:
    """
    List all available template names.

    Returns:
        List[str]: Template names
    """
    return list(TEMPLATE_REGISTRY.keys())
