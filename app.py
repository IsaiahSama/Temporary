from datetime import datetime
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from controller import GeneratorController
from os.path import exists
from os import mkdir

app = FastAPI()

templates = Jinja2Templates(directory="./templates")

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    location: str = Form(...),
    sales: UploadFile = File(...),
    payments: UploadFile = File(...),
):
    file_date = sales.filename.split("-")[-1].split(".")[0]
    date_obj = datetime.strptime(file_date, "%Y%m%d")
    
    try:
        controller = GeneratorController()
        controller.set_generator(location, date_obj.strftime("%m/%d/%Y"))
        controller.upload_file(sales.file, "Sales")
        controller.upload_file(payments.file, "Payments")
        result_file_path = controller.generate_report()

        print("Report generated and stored in " + result_file_path)
    except KeyError as e:
        print("KeyError", e)
        return {"error": e}
    except Exception as e:
        print(e)
        return {"error": e}
    
    restaurant_name = controller.generator.restaurant_name.upper()

    if not exists(f"./static/{restaurant_name}"):
        mkdir("./static/" + restaurant_name)

    static_filepath = f"./static/{restaurant_name}/" + result_file_path.split('/')[-1]
    with open(result_file_path, "rb") as f:
        with open(static_filepath, "wb") as f2:
            f2.write(f.read())
    print(static_filepath)
    return {"message": "Files uploaded Successfully", "file": FileResponse(path=static_filepath, filename=result_file_path.split('/')[-1])}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)