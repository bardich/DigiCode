from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.models import Project


class Command(BaseCommand):
    help = 'Add the bilingual AutoMaroc dealership project and its external website.'

    @transaction.atomic
    def handle(self, *args, **options):
        project = Project.objects.filter(landing_page='used_cars').first()
        if project is None:
            project = Project(slug='')
        if not project.pk:
            project.title_fr = 'AutoMaroc · Site de vente de voitures d’occasion'
            project.title_ar = 'أوتوماروك · موقع بيع السيارات المستعملة'
            project.short_description_fr = 'Un showroom numérique bilingue pour votre établissement : catalogue automobile, comparaison, demandes clients et tableau de gestion. Achat unique avec installation, identité et formation.'
            project.short_description_ar = 'معرض رقمي ثنائي اللغة لنشاطك: كتالوج سيارات ومقارنة وطلبات عملاء ولوحة إدارة. شراء لمرة واحدة يشمل التركيب والهوية والتدريب.'
            project.full_description_fr = 'AutoMaroc réunit le site d’un seul établissement automobile et son tableau de gestion. Les visiteurs filtrent les véhicules, consultent jusqu’à 15 photos, sauvegardent des favoris et comparent trois voitures sans compte. Votre équipe gère les annonces, disponibilités, demandes et notes internes. Les indicateurs sont opérationnels et les valeurs de vente estimées. L’achat unique comprend installation, personnalisation de l’identité et formation ; hébergement et accompagnement continu sont convenus séparément. Les descriptions arabes sont saisies par votre équipe.'
            project.full_description_ar = 'يجمع أوتوماروك موقعاً لمعرض سيارات واحد ولوحة إدارته. يصفي الزوار السيارات ويستعرضون حتى 15 صورة ويحفظون المفضلة ويقارنون ثلاث سيارات دون حساب. يدير فريقك الإعلانات والتوفر والطلبات والملاحظات الداخلية. المؤشرات تشغيلية وقيم البيع تقديرية. يشمل الشراء لمرة واحدة التركيب وتخصيص الهوية والتدريب، وتُحدد الاستضافة والمرافقة المستمرة باتفاق منفصل. يدخل فريقك الأوصاف العربية.'
            project.slug = 'automaroc-usedcars'
            if Project.objects.filter(slug=project.slug).exists():
                project.slug = ''
        project.link = 'https://cars.digicode.ma/'
        project.landing_page = 'used_cars'
        project.is_active = True
        project.is_featured = True
        project.save()
        self.stdout.write(self.style.SUCCESS(f'AutoMaroc project ready: {project.get_absolute_url()}'))
