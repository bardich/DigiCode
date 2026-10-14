from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.models import Project
from apps.services.models import Service


class Command(BaseCommand):
    help = 'Create the bilingual CV-to-website service and two unfeatured fictional demos.'

    @transaction.atomic
    def handle(self, *args, **options):
        service, created = Service.objects.get_or_create(slug='cv-portfolio', defaults={
            'title_fr':'Votre CV devient un site web', 'title_ar':'حوّل سيرتك الذاتية إلى موقع',
            'short_description_fr':'Un CV professionnel ou un portfolio créatif, présenté sur une page claire et responsive. Découvrez nos deux exemples et construisons votre présence en ligne.',
            'short_description_ar':'سيرة مهنية أو معرض أعمال إبداعي في صفحة واضحة ومتجاوبة. اكتشف النموذجين ولنصمم حضورك على الإنترنت.',
            'full_description_fr':'DigiCode transforme votre CV et vos contenus approuvés en une page web professionnelle. La livraison comprend les fichiers HTML/CSS/JS, une navigation par sections et des métadonnées de base. Le domaine, l’hébergement, la publication et les mises à jour sont convenus séparément. Devis personnalisé après un premier échange.',
            'full_description_ar':'تحول ديجي كود سيرتك الذاتية ومحتواك المعتمد إلى صفحة ويب مهنية. يشمل التسليم ملفات HTML/CSS/JS وتنقلاً بين الأقسام وبيانات أساسية لمحركات البحث. يُحدد النطاق والاستضافة والنشر والتحديثات باتفاق منفصل. عرض سعر مخصص بعد المناقشة الأولية.',
            'benefits_fr':['Un lien professionnel à partager','Une présentation claire de votre parcours','Une lecture confortable sur mobile et ordinateur'],
            'benefits_ar':['رابط مهني للمشاركة','عرض واضح لمسارك','قراءة مريحة على الهاتف والحاسوب'],
            'meta_title_fr':'Votre CV en site web et portfolio | DigiCode', 'meta_title_ar':'سيرتك الذاتية في موقع ومعرض أعمال | ديجي كود',
            'meta_description_fr':'Transformez votre CV en site web professionnel ou portfolio créatif. Deux exemples français/arabe, livraison de fichiers statiques et devis personnalisé.',
            'meta_description_ar':'حوّل سيرتك الذاتية إلى موقع مهني أو معرض أعمال إبداعي. نموذجان بالفرنسية والعربية وتسليم ملفات ثابتة وعرض سعر مخصص.',
            'is_active':True,'is_featured':True,'display_order':0,
        })
        profiles = [
            ('cv_professional','cv-professionnel','CV professionnel · Nadia Amrani','سيرة مهنية · نادية العمراني','Un exemple fictif de site CV pour une consultante : profil, expérience, compétences et formation dans une présentation éditoriale lumineuse.','نموذج خيالي لموقع سيرة مستشارة: نبذة وخبرات ومهارات وتعليم بتصميم تحريري فاتح.',10),
            ('cv_creative','portfolio-creatif','Portfolio créatif · Sami El Idrissi','معرض إبداعي · سامي الإدريسي','Un exemple fictif de portfolio de designer : compositions originales, compétences et parcours, dans une interface sombre et expressive.','نموذج خيالي لمعرض أعمال مصمم: تكوينات أصلية ومهارات ومسار مهني في واجهة داكنة ومعبرة.',11),
        ]
        for kind,slug,fr,ar,summary_fr,summary_ar,order in profiles:
            project = Project.objects.filter(landing_page=kind).first() or Project.objects.filter(slug=slug).first()
            if project:
                # Existing content and visibility are managed through the dashboard.
                if project.landing_page != kind:
                    self.stderr.write(f'Skipped reserved slug {slug}: belongs to another project.')
                continue
            Project.objects.create(slug=slug,landing_page=kind,title_fr=fr,title_ar=ar,
                short_description_fr=summary_fr,short_description_ar=summary_ar,
                full_description_fr=summary_fr+' Ce profil et ses expériences sont fictifs, créés pour illustrer le service CV-to-Portfolio de DigiCode. Le modèle est une page avec navigation interne, adaptée au français et à l’arabe. Contactez-nous pour adapter cette approche à votre propre parcours.',
                full_description_ar=summary_ar+' هذه الشخصية وخبراتها خيالية، أُعدت لتوضيح خدمة تحويل السيرة إلى موقع لدى ديجي كود. النموذج صفحة بتنقل داخلي يناسب الفرنسية والعربية. تواصل معنا لتخصيص هذا الأسلوب لمسارك.',
                link='',is_active=True,is_featured=False,display_order=order)
        self.stdout.write(self.style.SUCCESS(f'CV service {"created" if created else "preserved"}: {service.get_absolute_url()}; demos ready.'))
