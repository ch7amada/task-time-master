from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
from database import engine, get_db

import csv
import io
from fastapi.responses import StreamingResponse

# create tables on startup
models.Base.metadata.create_all(bind=engine)

# fastapi app + jinja init
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static") # needed for css
templates = Jinja2Templates(directory="templates")

# HOME
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    entries = db.query(models.TimesheetEntry).order_by(models.TimesheetEntry.date).all()
    return templates.TemplateResponse(name="index.html", request=request, context={"timesheet":entries})
###

# Export route
@app.get("/export")
async def export_csv(db: Session = Depends(get_db)):
    entries = db.query(models.TimesheetEntry).order_by(models.TimesheetEntry.date).all()
    output = io.StringIO()
    writer = csv.writer(output)
    # Header row
    writer.writerow(["Date", "Type", "Task", "CostBearer", "Duration"])
    # Data rows
    for entry in entries:
        writer.writerow([
            entry.date.strftime("%d.%m.%Y %H:%M"),
            entry.type,
            entry.task,
            entry.costbearer,
            entry.duration,
        ])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=timesheet.csv"}
    )
###

# Delete Route
@app.delete("/{id}", response_class=HTMLResponse)
async def delete_row(id: int, db: Session = Depends(get_db)):
    entry = db.query(models.TimesheetEntry).filter(models.TimesheetEntry.id == id).first()
    if entry:
        db.delete(entry)
        db.commit()
    return ""
###

# Edit Route
@app.get("/{id}", response_class=HTMLResponse)
async def edit_row(request: Request, id: int, update_data: schemas.TimesheetUpdate = Depends(schemas.timesheet_update_params), db: Session = Depends(get_db)):
    db_entry = db.query(models.TimesheetEntry).filter(models.TimesheetEntry.id == id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_dict.items():
        setattr(db_entry, key, value)

    db.commit()
    db.refresh(db_entry)

    return templates.TemplateResponse(name="row.html", request=request, context={"entry": db_entry})
###

# Add Route
@app.post("/entry", response_class=HTMLResponse)
async def add_row(request: Request, db: Session = Depends(get_db)):
    last_entry = db.query(models.TimesheetEntry).order_by(models.TimesheetEntry.id.desc()).first()
    new_entry = models.TimesheetEntry(
        date=last_entry.date if last_entry else datetime.now(),
        type=last_entry.type if last_entry else 0,
        task="",
        costbearer=last_entry.costbearer if last_entry else 0,
        duration=0.0,
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return templates.TemplateResponse(name="row.html", request=request, context={"entry": new_entry})

###