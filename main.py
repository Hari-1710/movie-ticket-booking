from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import datetime, os

from database import SessionLocal, engine
from models import Base, User, Admin, Movie, Booking
from auth import hash_password, verify_password
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- HOME ----------------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ---------------- USER AUTH ----------------
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db.add(User(username=username, password=hash_password(password)))
    db.commit()
    return RedirectResponse("/login", status_code=302)

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        return RedirectResponse("/movies", status_code=302)
    return RedirectResponse("/login", status_code=302)

# ---------------- ADMIN ----------------
@app.get("/admin")
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin")
def admin_auth(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "admin123":
        return RedirectResponse("/admin/dashboard", status_code=302)
    return RedirectResponse("/admin", status_code=302)

@app.get("/admin/dashboard")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "movies": movies})

@app.get("/admin/add_movie")
def add_movie_page(request: Request):
    return templates.TemplateResponse("add_movie.html", {"request": request})

@app.post("/admin/add_movie")
def add_movie(name: str = Form(...), time: str = Form(...), price: int = Form(...), db: Session = Depends(get_db)):
    db.add(Movie(name=name, time=time, price=price))
    db.commit()
    return RedirectResponse("/admin/dashboard", status_code=302)

# ---------------- BOOKING ----------------
@app.get("/movies")
def movies(request: Request, db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies})

@app.get("/seats/{movie_id}")
def seats(request: Request, movie_id: int):
    return templates.TemplateResponse("seats.html", {"request": request, "movie_id": movie_id})

@app.post("/payment")
def payment(movie_id: int = Form(...), seats: str = Form(...), db: Session = Depends(get_db)):
    movie = db.query(Movie).get(movie_id)
    amount = len(seats.split(",")) * movie.price

    booking = Booking(
        user="guest",
        movie=movie.name,
        seats=seats,
        amount=amount,
        date=str(datetime.date.today())
    )
    db.add(booking)
    db.commit()

    generate_invoice("guest", movie.name, seats, amount)
    return RedirectResponse("/invoice", status_code=302)

# ---------------- PDF INVOICE ----------------
def generate_invoice(user, movie, seats, amount):
    os.makedirs("invoices", exist_ok=True)
    file = f"invoices/{user}.pdf"

    c = canvas.Canvas(file, pagesize=A4)
    c.drawString(100,800,"🎬 Movie Ticket Invoice")
    c.drawString(100,760,f"User: {user}")
    c.drawString(100,740,f"Movie: {movie}")
    c.drawString(100,720,f"Seats: {seats}")
    c.drawString(100,700,f"Amount: ₹{amount}")
    c.drawString(100,680,f"Date: {datetime.date.today()}")
    c.save()

@app.get("/invoice")
def invoice():
    return FileResponse("invoices/guest.pdf", filename="invoice.pdf")
