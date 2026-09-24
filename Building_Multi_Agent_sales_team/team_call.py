import asyncio
from html import escape
from pathlib import Path
from agents import Runner
from agents import Agent, ModelSettings
from Agents import model, tools
from email_services import send_email
from agents.extensions.visualization import draw_graph
from graphviz.backend import ExecutableNotFound
from PIL import Image, ImageDraw


def create_fallback_graph(filename: Path) -> None:
    image = Image.new("RGB", (1200, 760), "white")
    drawing = ImageDraw.Draw(image)

    nodes = {
        "manager": (410, 40, 790, 120, "Sales Manager"),
        "professional": (40, 260, 360, 350, "Professional Sales Agent"),
        "humorous": (440, 260, 760, 350, "Humorous Sales Agent"),
        "executive": (840, 260, 1160, 350, "Executive Sales Agent"),
        "email": (410, 560, 790, 650, "Send one email via SMTP"),
    }

    def draw_node(node):
        left, top, right, bottom, label = node
        drawing.rounded_rectangle((left, top, right, bottom), radius=14, outline="#1f4e79", width=3, fill="#eaf3f8")
        box = drawing.textbbox((0, 0), label)
        drawing.text(((left + right - (box[2] - box[0])) / 2, (top + bottom - (box[3] - box[1])) / 2), label, fill="#102a43")

    def draw_arrow(start, end):
        drawing.line((start[0], start[1], end[0], end[1]), fill="#52606d", width=3)
        drawing.polygon([(end[0], end[1]), (end[0] - 8, end[1] - 14), (end[0] + 8, end[1] - 14)], fill="#52606d")

    for node in nodes.values():
        draw_node(node)

    manager = nodes["manager"]
    for key in ("professional", "humorous", "executive"):
        node = nodes[key]
        draw_arrow(((manager[0] + manager[2]) // 2, manager[3]), ((node[0] + node[2]) // 2, node[1]))

    for key in ("professional", "humorous", "executive"):
        node = nodes[key]
        draw_arrow(((node[0] + node[2]) // 2, node[3]), ((nodes["email"][0] + nodes["email"][2]) // 2, nodes["email"][1]))

    image.save(filename)



instructions = """
You are a Sales Manager at ComplAI. Choose the strongest cold sales email.
After reviewing all three drafts, return only the single best draft.
Do not return the other drafts or commentary.
"""

task = """
Follow these steps:

1. Generate Drafts: Use each of the three sales_email_writer tools to generate different email drafts.
Just instruct each to write a sales email; no further details are needed.
Do not proceed until all three drafts are ready, one from each tool.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
 
3. Return only the best email draft.
"""

#alo we used the concept the hadoff techniqunes 

async def main():
    sales_manager = Agent(
        name="Sales Manager",
        instructions=instructions,
        tools=tools,
        model=model,
        model_settings=ModelSettings(max_tokens=400),
    )
    graph_file = Path(__file__).with_name("sales_team_graph")
    try:
        draw_graph(sales_manager, str(graph_file))
        print(f"Workflow graph saved to {graph_file}.png")
    except ExecutableNotFound:
        graph = draw_graph(sales_manager)
        dot_file = graph.save(str(graph_file.with_suffix(".dot")))
        png_file = graph_file.with_suffix(".png")
        create_fallback_graph(png_file)
        print(f"Graphviz 'dot' is not installed; graph definition saved to {dot_file}")
        print(f"Fallback workflow graph saved to {png_file}")
    result = await Runner.run(sales_manager, task, max_turns=8)
    selected_draft = result.final_output.strip()
    if not selected_draft:
        raise RuntimeError("The sales manager returned an empty email draft.")

    send_result = send_email(
        "ComplAI cold sales email",
        selected_draft,
        f"<html><body><pre>{escape(selected_draft)}</pre></body></html>",
    )
    print(selected_draft)
    print(send_result)


if __name__=="__main__":
    asyncio.run(main())


