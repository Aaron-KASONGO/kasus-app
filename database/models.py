from tortoise import fields
from tortoise.models import Model



class Utilisateur(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Dossier(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    dossier = fields.ForeignKeyField('models.Dossier', null=True, related_name="dossiers", on_delete=fields.CASCADE)
    utilisateur = fields.ForeignKeyField('models.Utilisateur', on_delete=fields.CASCADE, related_name="dossiers")

class Document(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    document_url = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    dossier = fields.ForeignKeyField('models.Dossier', on_delete=fields.CASCADE, related_name="documents")


class DocumentConverti(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    document = fields.TextField()
    format = fields.CharField(max_length=10)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    document = fields.ForeignKeyField('models.Document', on_delete=fields.CASCADE, related_name="documentConverties")

