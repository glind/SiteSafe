import django_tables2 as tables
from .models import Folder, File

TEMPLATE = '''
   <a href="/folder/{{ record.id }}">{{ record.folder_name }}</a>
'''

class FolderTable(tables.Table):
    folder_name = tables.TemplateColumn(TEMPLATE)
    class Meta:
        model = Folder
        attrs = {"class": "paleblue"}
        fields = ("folder_path", "folder_name", "num_files", "create_date", "edit_date", "unverified_change")
        sequence = ("folder_path", "folder_name", "num_files", "create_date", "edit_date", "unverified_change")

TEMPLATE2 = '''
   <a href="/file/{{ record.id }}">{{ record.file_name }}</a>
'''

class FileTable(tables.Table):
    file_name = tables.TemplateColumn(TEMPLATE2)
    class Meta:
        model = File
        attrs = {"class": "paleblue"}
        fields = ("file_path", "file_name", "file_hash", "create_date", "edit_date", "unverified_change")
        sequence = ("file_path", "file_name", "file_hash", "create_date", "edit_date", "unverified_change")