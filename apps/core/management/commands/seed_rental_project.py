from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.models import Project


class Command(BaseCommand):
    help = 'Add the bilingual rental project, reusing its untitled legacy entry when available.'

    @transaction.atomic
    def handle(self, *args, **options):
        project = Project.objects.filter(landing_page='car_rental').first()
        if project is None:
            project = Project.objects.filter(link__in=['https://rental.digicode.ma/', 'https://rental.digicode.ma', 'http://rental.digicode.ma/', 'http://rental.digicode.ma'], title_fr='', title_ar='').first()
        if project is None:
            project = Project(slug='')
        if not project.title_fr and not project.title_ar:
            project.title_fr = 'Solution de gestion pour agences de location de voitures'
            project.title_ar = 'موقع وإدارة لوكالات تأجير السيارات'
            project.short_description_fr = 'Un site au nom de votre agence et une gestion centralisée des véhicules, tarifs et demandes de réservation. Interface client en arabe, français et anglais.'
            project.short_description_ar = 'موقع باسم وكالتك وإدارة مركزية للسيارات والأسعار وطلبات الحجز. واجهة للعملاء بالعربية والفرنسية والإنجليزية.'
            project.full_description_fr = 'Une solution pour une seule agence, associant un site client et un tableau de gestion en français. Présentation des véhicules, recherche par dates, demandes de réservation, gestion manuelle des réservations et tarification selon la durée. Les demandes nécessitent une confirmation de l’agence. Le paiement en ligne n’est pas disponible dans la version actuelle.'
            project.full_description_ar = 'حل لوكالة واحدة يجمع بين موقع للعملاء ولوحة إدارة بالفرنسية. عرض السيارات والبحث حسب التواريخ وطلبات الحجز والحجوزات اليدوية والتسعير حسب المدة. تحتاج الطلبات إلى تأكيد الوكالة. الدفع الإلكتروني غير موجود في النسخة الحالية.'
        if not project.slug:
            project.slug = 'car-rental'
            if Project.objects.exclude(pk=project.pk).filter(slug=project.slug).exists():
                project.slug = ''  # Model generates a unique slug rather than changing another project.
        project.link = 'https://rental.digicode.ma/'
        project.landing_page = 'car_rental'
        project.is_active = True
        project.is_featured = True
        project.save()
        self.stdout.write(self.style.SUCCESS(f'Rental project ready: {project.get_absolute_url()}'))
