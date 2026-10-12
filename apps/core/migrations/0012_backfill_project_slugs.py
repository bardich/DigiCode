from django.db import migrations
from django.utils.text import slugify


def backfill_project_slugs(apps, schema_editor):
    Project = apps.get_model('core', 'Project')
    projects = Project.objects.using(schema_editor.connection.alias)
    for project in projects.filter(slug='').order_by('pk').iterator():
        title = project.title_fr or project.title_ar
        base = slugify(title)[:80].rstrip('-') or f'project-{project.pk}'
        candidate = base
        suffix = 1
        while projects.exclude(pk=project.pk).filter(slug=candidate).exists():
            candidate = f'{base}-{suffix}'
            suffix += 1
        projects.filter(pk=project.pk).update(slug=candidate)


class Migration(migrations.Migration):
    dependencies = [('core', '0011_project_display_order_project_is_featured_and_more')]
    operations = [migrations.RunPython(backfill_project_slugs, migrations.RunPython.noop)]
