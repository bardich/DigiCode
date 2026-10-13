from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.models import Project


class Command(BaseCommand):
    help = 'Add the bilingual Safaa e-commerce portfolio project without an external URL.'

    @transaction.atomic
    def handle(self, *args, **options):
        project = Project.objects.filter(landing_page='ecommerce').first()
        if project is None:
            project = Project(slug='')
        if not project.pk:
            project.title_fr = 'Safaa · Boutique e-commerce et gestion commerciale'
            project.title_ar = 'صفاء · متجر إلكتروني وإدارة تجارية'
            project.short_description_fr = 'Une démonstration de boutique bilingue pour les entreprises marocaines : catalogue, commandes, stocks, livraison et suivi du paiement à la livraison.'
            project.short_description_ar = 'عرض تجريبي لمتجر ثنائي اللغة للشركات المغربية: كتالوج وطلبات ومخزون وتوصيل ومتابعة الدفع عند الاستلام.'
            project.full_description_fr = 'Safaa présente une boutique de produits naturels avec contenu d’exemple et commandes publiques désactivées. La solution réunit une vitrine arabe et française, un achat invité, le paiement à la livraison et la gestion du catalogue, des commandes, du stock, des livraisons et des accès du personnel. Les paiements en ligne et les messages automatisés sont des extensions à définir séparément. Contactez DigiCode pour une présentation ou un devis personnalisé.'
            project.full_description_ar = 'تعرض صفاء متجراً للمنتجات الطبيعية بمحتوى نموذجي وطلبات عامة معطلة. يجمع الحل واجهة عربية وفرنسية وشراء كزائر ودفعاً عند الاستلام وإدارة الكتالوج والطلبات والمخزون والتوصيل وصلاحيات الموظفين. الدفع الإلكتروني والرسائل الآلية إضافات تُحدد بشكل منفصل. تواصل مع ديجي كود لعرض توضيحي أو عرض سعر مخصص.'
            project.slug = 'safaa-ecommerce'
            if Project.objects.filter(slug=project.slug).exists():
                project.slug = ''
        project.link = ''
        project.landing_page = 'ecommerce'
        project.is_active = True
        project.is_featured = True
        project.save()
        self.stdout.write(self.style.SUCCESS(f'E-commerce project ready: {project.get_absolute_url()} (contact inquiries only)'))
