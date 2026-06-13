import json
import time
from langgraph.graph import StateGraph, END

# Mock AI functions for demonstration
def generate_cv_sections(user_input):
    """Simulates AI generating CV sections based on input."""
    print(f"AI: Generating sections for: {user_input}")
    time.sleep(0.5) # Simulate AI processing time
    sections = {
        "summary": f"Highly motivated professional with expertise in {user_input.split(' ')[-1]}.",
        "experience": "- Developed innovative solutions.\n- Led cross-functional teams.",
        "education": "- Bachelor's Degree in Computer Science."
    }
    return sections

def format_latex(cv_sections):
    """Simulates AI formatting CV sections into LaTeX."""
    print("AI: Formatting into LaTeX...")
    time.sleep(0.3)
    latex_output = "\\documentclass{article}\\usepackage{geometry}\\geometry{a4paper, margin=1in}\\title{Curriculum Vitae}\\date{}\\maketitle\n\n"
    for section, content in cv_sections.items():
        latex_output += f"\\section*{{{section.capitalize()}}}\\n{content}\\n\n"
    latex_output += "\\end{document}"
    return latex_output

def review_and_refine(latex_document):
    """Simulates AI reviewing and refining the LaTeX document."""
    print("AI: Reviewing and refining LaTeX...")
    time.sleep(0.4)
    # In a real scenario, this would involve parsing and checking for common errors
    refined_latex = latex_document.replace("\\section*", "\\section") # Simple refinement example
    return refined_latex

# Define the state for our graph
class CVState:
    def __init__(self, user_input=""):
        self.user_input = user_input
        self.cv_sections = {}
        self.latex_document = ""

def create_cv_graph():
    """Creates the LangGraph workflow for CV generation."""
    workflow = StateGraph(CVState)

    # Define nodes (AI functions)
    workflow.add_node("generate_sections", lambda state: {
        **state,
        "cv_sections": generate_cv_sections(state.user_input)
    })
    workflow.add_node("format_to_latex", lambda state: {
        **state,
        "latex_document": format_latex(state.cv_sections)
    })
    workflow.add_node("review_and_refine", lambda state: {
        **state,
        "latex_document": review_and_refine(state.latex_document)
    })

    # Define edges (workflow flow)
    workflow.set_entry_point("generate_sections")
    workflow.add_edge("generate_sections", "format_to_latex")
    workflow.add_edge("format_to_latex", "review_and_refine")
    workflow.add_edge("review_and_refine", END)

    return workflow.compile()

if __name__ == "__main__":
    # This part simulates the Hono/BullMQ integration by running the graph directly
    # In a real app, Hono would handle API requests, and BullMQ would queue tasks.

    print("--- TexFolio AI CV Generator Demo ---")
    user_query = input("Enter your core skill or field (e.g., 'Software Engineering'): ")

    # Initialize the graph
    cv_graph = create_cv_graph()

    # Run the graph
    initial_state = CVState(user_input=user_query)
    final_state = cv_graph.invoke(initial_state)

    print("\n--- Generated LaTeX CV ---")
    print(final_state.latex_document)
    print("\n--- Demo Complete ---")
