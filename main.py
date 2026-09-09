"""CLI entry point for the AI HR Recruitment Assistant.

Usage (run from the project root, inside your venv):

    python main.py ingest
    python main.py screen --resume data/resumes/sample_resume_1.txt --jd data/job_descriptions/senior_backend_engineer.txt
    python main.py chat
"""
import argparse
import json

from rich.console import Console
from rich.panel import Panel

from src.rag.ingest import run_ingestion
from src.pipeline import screen_candidate
from src.agent.hr_agent import run_agent

console = Console()


def cmd_ingest(_args):
    run_ingestion()


def cmd_screen(args):
    console.print(f"[bold]Screening[/bold] {args.resume} against {args.jd} ...")
    result = screen_candidate(args.resume, args.jd)

    match = result["match"]
    console.print(
        Panel.fit(
            f"Overall score: [bold]{match['overall_score']}%[/bold]\n"
            f"Skill match: {match['skill_match_score']}%\n"
            f"Experience match: {match['experience_match_score']}%\n\n"
            f"Matched skills: {', '.join(match['matched_skills']) or '-'}\n"
            f"Missing skills: {', '.join(match['missing_skills']) or '-'}\n\n"
            f"{match['rationale']}",
            title="Match Result",
        )
    )

    q = result["interview_questions"]
    q_text = "[bold]Technical[/bold]\n" + "\n".join(f"- {x}" for x in q["technical_questions"])
    q_text += "\n\n[bold]Behavioral[/bold]\n" + "\n".join(f"- {x}" for x in q["behavioral_questions"])
    q_text += "\n\n[bold]Gap-probing[/bold]\n" + "\n".join(f"- {x}" for x in q["gap_probing_questions"])
    console.print(Panel.fit(q_text, title="Suggested Interview Questions"))

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2)
        console.print(f"[green]Full report saved to {args.output}[/green]")


def cmd_chat(_args):
    console.print("[bold cyan]AI HR Assistant[/bold cyan] (agent + tools + RAG) — type 'exit' to quit")
    console.print(
        "[dim]Try: \"Screen data/resumes/sample_resume_1.txt against "
        "data/job_descriptions/senior_backend_engineer.txt and give me interview questions\"[/dim]"
    )
    while True:
        try:
            query = console.input("\n[bold yellow]You:[/bold yellow] ")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("exit", "quit"):
            break
        response = run_agent(query)
        console.print(f"\n[bold green]Assistant:[/bold green] {response}")


def main():
    parser = argparse.ArgumentParser(description="AI HR Recruitment Assistant")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Ingest job descriptions & knowledge base into the RAG vector store")
    p_ingest.set_defaults(func=cmd_ingest)

    p_screen = sub.add_parser("screen", help="Screen a resume against a job description")
    p_screen.add_argument("--resume", required=True, help="Path to resume file")
    p_screen.add_argument("--jd", required=True, help="Path to job description file")
    p_screen.add_argument("--output", default=None, help="Optional path to save the full JSON report")
    p_screen.set_defaults(func=cmd_screen)

    p_chat = sub.add_parser("chat", help="Chat with the agent (free-form natural language)")
    p_chat.set_defaults(func=cmd_chat)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
