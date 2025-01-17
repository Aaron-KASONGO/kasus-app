from typing import Annotated

from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise

from .database.models import Utilisateur, Dossier, Document, DocumentConverti
import cloudinary
import cloudinary.uploader


app = FastAPI()

origins = [
    "https://kasusapp1-i1u1jey1.b4a.run"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url="postgres://cmvyyavg:PqrM5Qn1BhiZEz0Mf4DTgRLw2Y4MWJEz@motty.db.elephantsql.com/cmvyyavg",
    modules={'models': ['app.database.models', 'app.main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

Tortoise.init_models(['app.database.models', 'app.main'], 'models')

#result = cloudinary.uploader.upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", 
#  public_id = "kasus_app/olympic_flag")

#print(result.get('url'))

# Pydantic model for Utilisateur
Utilisateur_read_pydantic = pydantic_model_creator(Utilisateur)
Utilisateur_creator_pydantic = pydantic_model_creator(Utilisateur, exclude_readonly=True, name="UtilisateurCreator", exclude=('created_at', 'id'))

# Pydantic model for Dossier
Dossier_read_pydantic = pydantic_model_creator(Dossier)
Dossier_creator_pydantic = pydantic_model_creator(Dossier, exclude_readonly=True, name="DossierCreator", exclude=('created_at', "modified_at", 'id'))
Dossier_creator_racine_pydantic = pydantic_model_creator(Dossier, exclude_readonly=True, name="DossierCreator", exclude=('created_at', "modified_at", 'id', 'dossier_id'))

# Pydantic model for Document
Document_read_pydantic = pydantic_model_creator(Document)
Document_creator_pydantic = pydantic_model_creator(Document, exclude_readonly=True, name="DocumentCreator", exclude=('created_at', "modified_at", 'id'))

DocumentConverti_read_pydantic = pydantic_model_creator(DocumentConverti)
DocumentConverti_creator_pydantic = pydantic_model_creator(DocumentConverti, exclude_readonly=True, name="DocumentConvertiCreator", exclude=("created_at", "modified_at", "id"))


############################
#  Api welcome controller  #
############################
@app.get('/')
def welcome():
    return {'detail': "welcome to kasus-app"}



####################################
#  Api controller for Utilisateur  #
####################################

@app.post('/create-user')
async def create_user(user: Utilisateur_creator_pydantic):
    user_obj = await Utilisateur.create(**user.model_dump(exclude_unset=True))
    await Dossier.create(name="__base__", dossier=None, utilisateur=user_obj)
    return await Utilisateur_read_pydantic.from_tortoise_orm(user_obj)

@app.get('/get-users')
async def create_user():
    return await Utilisateur_read_pydantic.from_queryset(Utilisateur.all())

################################
#  Api controller for Dossier  #
################################

@app.get('/get-dossiers/{user_id}')
async def get_dossiers(user_id: int):
    dossiers = Dossier.filter(utilisateur_id=user_id)
    return await Dossier_read_pydantic.from_queryset(dossiers)

@app.get('/get-clear-dossiers/{user_id}')
async def get_dossiers(user_id: int):
    dossiers = Dossier.filter(utilisateur_id=user_id)
    return await Dossier_read_pydantic.from_queryset(dossiers)

# Create Dossier 
@app.post('/create-dossier')
async def create_dossier(dossier: Dossier_creator_pydantic):
    dossier = await Dossier.create(**dossier.model_dump(exclude_unset=True))
    return await Dossier_read_pydantic.from_tortoise_orm(dossier)

# Get a dossier by id
@app.get('/get-content-dossier/{user_id}/{dossier_id}')
async def get_dossier_by_id(user_id, dossier_id):
    dossier = await Dossier.get(utilisateur_id=user_id, id=dossier_id)
    return await Dossier_read_pydantic.from_tortoise_orm(dossier)

#################################
#  Api controller for Document  #
#################################

@app.get('/documents/{dossier_id}')
async def get_docuemnts(dossier_id: int):
    documents = Document.filter(dossier_id=dossier_id)
    return await Document_read_pydantic.from_queryset(documents)

@app.post('/upload-image')
async def upload_image(id_dossier: int, name: str, file: Annotated[bytes, File()]):
    result = cloudinary.uploader.upload(file, public_id = "kasus_app/olympic_flag")
    dossier = await Dossier.get(id=id_dossier)
    document = await Document.create(name=name, document_url=result.get('url'), dossier=dossier)
    return await document
