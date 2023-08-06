import arches
import os
import shutil

from django.core.management.base import BaseCommand
from django.core import management
from django.db import connection
from arches.app.models.system_settings import settings


class Command(BaseCommand):
    """
    Command for migrating projects between versions

    """

    def handle(self, *args, **options):
        if "7.0.0" in arches.__version__:
            self.update_to_v7()

    def update_to_v7(self):
        # copy webpack config files to project
        project_webpack_path = os.path.join(settings.APP_ROOT, "webpack")

        if not os.path.isdir(project_webpack_path):
            shutil.copytree(os.path.join(settings.ROOT_DIR, "install", "arches-templates", "project_name", "webpack"), project_webpack_path)

        # publish graphs that were previously active
        with connection.cursor() as cursor:
            cursor.execute("select * from temp_graph_status;")
            rows = cursor.fetchall()
            graphs = []
            for row in rows:
                graphid = str(row[0])
                active = row[1]
                if active:
                    graphs.append(graphid)
            management.call_command("graph", operation="publish", update_instances=True, graphs=",".join(graphs))
            cursor.execute("drop table if exists temp_graph_status")
