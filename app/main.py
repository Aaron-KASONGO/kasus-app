from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise

from .database.models import Utilisateur, Dossier, Document, DocumentConverti


app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['app.database.models', 'app.main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

Tortoise.init_models(['app.database.models', 'app.main'], 'models')

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
async def welcome():
    return await {'detail': "welcome to kasus-app"}



####################################
#  Api controller for Utilisateur  #
####################################

@app.post('/get-create-user')
async def create_user(user: Utilisateur_creator_pydantic):
    user_obj = await Utilisateur.create(**user.model_dump(exclude_unset=True))
    return await Utilisateur_read_pydantic.from_tortoise_orm(user_obj)

@app.get('/get-users')
async def create_user():
    return await Utilisateur_read_pydantic.from_queryset(Utilisateur.all())

################################
#  Api controller for Dossier  #
################################

@app.get('/dossiers/{user_id}')
async def get_dossiers(user_id: int):
    dossiers = Dossier.filter(utilisateur_id=user_id)
    return await Dossier_read_pydantic.from_queryset(dossiers)

# Create Dossier 
@app.post('/dossiers')
async def create_dossier(dossier: Dossier_creator_pydantic):
    dossier = await Dossier.create(**dossier.model_dump(exclude_unset=True))
    return await Dossier_read_pydantic.from_tortoise_orm(dossier)

# Get a dossier by id
@app.get('/dossiers/{user_id}/{dossier_id}')
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
