from peewee import Model, CharField, \
      DateTimeField, AutoField, SQL
from db import get_db
from datetime import datetime

# Use the singleton database instance
database = get_db()


class BaseModel(Model):
    class Meta:
        database = database


class SampleTable(BaseModel):
    id = AutoField(primary_key=True)  # Auto-incrementing primary key
    name = CharField()
    record_type = CharField()    
    created_at = DateTimeField(default=datetime.now, null=False)
    updated_at = DateTimeField(default=None, null=True)

    class Meta:
        table_name = 'sample_table'
        constraints = [
            SQL('UNIQUE(name, record_type)')  # Enforce uniqueness
        ]

    def save(self, *args, **kwargs):
        # Automatically update `updated_at` field on save
        self.updated_at = datetime.now()
        return super(SampleTable, self).save(*args, **kwargs)
