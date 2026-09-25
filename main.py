from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.post("/generate-home")
def generate_home(
    request: Request,
    budget: int = Form(...),
    room: str = Form(...),
    style: str = Form(...)
):
    if budget <= 0:
        return {"error": "Budget must be greater than zero"}

    furniture = budget * 60 // 100
    lighting = budget * 15 // 100
    decor = budget * 15 // 100

    try:
        client = genai.Client()
        response = client.interactions.create(
            model="gemini-3.5-flash-lite",
                        input=(
                f"Give exactly three short decorating ideas for a {room} "
                f"in {style} style. The total budget is ₹{budget}: "
                f"furniture ₹{furniture}, lighting ₹{lighting}, "
                f"decor ₹{decor}, and reserve ₹{budget - furniture - lighting - decor}. "
                "Suggest items within those category limits. "
                "Use plain text only: no Markdown, asterisks, or headings. "
                "Do not claim that estimated prices are exact."
            ),
        )
        ai_suggestion = response.output_text or "No suggestion was returned."
    except Exception:
        ai_suggestion = "AI suggestions are temporarily unavailable."

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "room": room,
            "style": style,
            "total_budget": budget,
            "furniture": furniture,
            "lighting": lighting,
            "decor": decor,
            "reserve": budget - furniture - lighting - decor,
            "ai_suggestion": ai_suggestion,
        },
    )


@app.get("/party")
def party(request: Request):
    return templates.TemplateResponse(request=request, name="party.html")


@app.post("/generate-party")
def generate_party(
    request: Request,
    budget: int = Form(...),
    guests: int = Form(...),
    occasion: str = Form(...)
):
    food = budget * 40 // 100
    venue = budget * 25 // 100
    decorations = budget * 15 // 100
    entertainment = budget * 10 // 100
    reserve = budget - food - venue - decorations - entertainment
    try:
        client = genai.Client()
        response = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=(
                f"Give exactly three short, practical ideas for a {occasion} "
                f"with {guests} guests and a total budget of ₹{budget}. "
                f"The budget limits are food ₹{food}, venue ₹{venue}, "
                f"decorations ₹{decorations}, entertainment ₹{entertainment}, "
                f"and reserve ₹{reserve}. Stay within each category limit. "
                "Use plain text only, with no Markdown or asterisks. "
                "Treat any prices as estimates."
            ),
        )
        ai_suggestion = response.output_text or "No suggestion was returned."
    except Exception:
        ai_suggestion = "AI suggestions are temporarily unavailable."

    return templates.TemplateResponse(
        request=request,
        name="party_result.html",
        context= {"ai_suggestion": ai_suggestion,}
    )

@app.get("/jewelry")
def jewelry(request: Request):
    return templates.TemplateResponse(request=request, name="jewelry.html")


@app.post("/generate-jewelry")
def generate_jewelry(
    request: Request,
    budget: int = Form(...),
    item: str = Form(...),
    occasion: str = Form(...)
):
    item_budget = budget * 80 // 100
    making_charges = budget * 10 // 100
    reserve = budget - item_budget - making_charges
    try:
        client = genai.Client()
        response = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=(
                f"Give exactly three short, practical shopping tips for a {item} "
                f"for a {occasion}, with a total budget of ₹{budget}. "
                f"The item allowance is ₹{item_budget}, the making charges "
                f"allowance is ₹{making_charges}, and the reserve is ₹{reserve}. "
                "These are planning allowances, not actual jewelry prices or "
                "confirmed making charges. Do not invent current gold rates. "
                "Use plain text only, with no Markdown or asterisks."
            ),
        )
        ai_suggestion = response.output_text or "No suggestion was returned."
    except Exception:
        ai_suggestion = "AI suggestions are temporarily unavailable."

    return templates.TemplateResponse(
        request=request,
        name="jewelry_result.html",
        context={            "ai_suggestion": ai_suggestion,
        },
    )