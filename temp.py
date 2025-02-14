import openai

# OpenAI API Key
OPENAI_API_KEY = "your-openai-api-key"

# Define file paths for original markdown reports and AI-generated summaries
projects = {
    "PROJECT1": {
        "report_file": "PROJECT1_sprint_report.md",
        "summary_file": "PROJECT1_sprint_summary_ai.md"
    },
    "PROJECT2": {
        "report_file": "PROJECT2_sprint_report.md",
        "summary_file": "PROJECT2_sprint_summary_ai.md"
    }
}

# Function to generate AI-powered sprint summaries
def generate_ai_summary(project_name, report_content):
    prompt = f"""
    You are an experienced Business Analyst with a software development background, adept at creating concise and structured release notes.
    Given the sprint report for project {project_name}, generate a professional summary in markdown format with the following sections:
    
    ## 🏆 Key Achievements
    - Summarize major features or improvements.
    
    ## 🐛 Bug Fixes
    - List major bugs resolved with their impact.
    
    ## 🔄 Carryover & Pending Work
    - Highlight any unfinished work or stories that moved to the next sprint.
    
    ## 📌 Notes for Stakeholders
    - Any crucial business updates, technical risks, or dependencies to be aware of.
    
    **Sprint Report Content:**
    {report_content}

    Provide a well-structured summary in markdown format.
    """
    
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You create structured and business-friendly sprint summaries for software development teams."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    
    return response["choices"][0]["message"]["content"]

# Process each project
for project, paths in projects.items():
    try:
        # Read the original sprint report
        with open(paths["report_file"], "r") as f:
            report_content = f.read()

        # Generate AI summary
        ai_summary = generate_ai_summary(project, report_content)

        # Save the AI-generated summary
        with open(paths["summary_file"], "w") as f:
            f.write(f"# {project} Sprint Summary\n\n")
            f.write(ai_summary)
        
        print(f"✅ AI-generated summary saved: {paths['summary_file']}")
    
    except Exception as e:
        print(f"❌ Error processing {project}: {str(e)}")
