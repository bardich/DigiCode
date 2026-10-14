"""Equivalent French/Arabic sales content from the supplied AutoMaroc brief."""
from django.urls import reverse
from django.utils.translation import get_language
from .models import SiteSettings
from .utils import whatsapp_url


def text(fr, ar):
    return ar if get_language() == 'ar' else fr


def usedcars_context(request, project=None):
    message = text('Bonjour DigiCode, je souhaite un devis pour l’achat unique et l’installation d’AutoMaroc pour mon showroom automobile, avec personnalisation et formation.', 'مرحباً ديجي كود، أريد عرض سعر لشراء أوتوماروك لمرة واحدة وتركيبه لمعرض سياراتي، مع تخصيص الهوية والتدريب.')
    sales_url = whatsapp_url(SiteSettings.load().whatsapp_number, message)
    rows = [
        ('Recherche et filtres', 'البحث والتصفية', 'Aider le client à trouver un véhicule adapté.', 'مساعدة العميل على إيجاد سيارة مناسبة.'),
        ('Fiches et jusqu’à 15 photos', 'تفاصيل وحتى 15 صورة', 'Présenter les caractéristiques et l’état du véhicule.', 'عرض المواصفات وحالة السيارة.'),
        ('Disponibilité visible', 'حالة توفر ظاهرة', 'Distinguer disponible, réservé et vendu.', 'التمييز بين المتاح والمحجوز والمباع.'),
        ('Favoris et comparaison de 3 voitures', 'المفضلة ومقارنة 3 سيارات', 'Préparer un choix sans inscription, sur l’appareil du visiteur.', 'تسهيل الاختيار دون تسجيل، على جهاز الزائر.'),
        ('Véhicules similaires', 'سيارات مشابهة', 'Proposer d’autres options dans votre catalogue.', 'عرض بدائل ضمن كتالوجك.'),
        ('WhatsApp, téléphone et formulaires', 'واتساب وهاتف ونماذج', 'Faciliter le contact direct avec votre équipe.', 'تسهيل التواصل المباشر مع فريقك.'),
        ('Création, modification, publication et masquage', 'إنشاء وتعديل ونشر وإخفاء', 'Préparer les annonces et choisir leur mise en ligne.', 'تجهيز الإعلانات والتحكم في نشرها.'),
        ('Véhicules à la une et ordre des photos', 'سيارات مميزة وترتيب الصور', 'Soigner la présentation de votre stock.', 'تحسين عرض مخزونك.'),
        ('Marques, catégories et équipements', 'علامات وفئات وتجهيزات', 'Garder un catalogue cohérent et facile à parcourir.', 'تنظيم كتالوج متناسق وسهل التصفح.'),
        ('Demandes et notes internes', 'طلبات وملاحظات داخلية', 'Centraliser le suivi des échanges pour le personnel.', 'توحيد متابعة المحادثات للموظفين.'),
        ('Stock, ajouts mensuels et ventes datées', 'مخزون وإضافات شهرية ومبيعات مؤرخة', 'Suivre les mouvements enregistrés dans le tableau.', 'متابعة الحركات المسجلة في اللوحة.'),
        ('Vues et nombre de demandes', 'مشاهدات وعدد الطلبات', 'Observer l’activité enregistrée sur les annonces.', 'ملاحظة النشاط المسجل على الإعلانات.'),
        ('Valeur annoncée estimée des véhicules vendus', 'قيمة معلنة تقديرية للسيارات المباعة', 'Disposer d’un repère opérationnel, sans assimiler ce total au revenu encaissé.', 'الحصول على مؤشر تشغيلي دون اعتباره إيراداً محصلاً.'),
        ('Français, arabe et lecture RTL', 'فرنسية وعربية واتجاه من اليمين', 'Accueillir vos clients dans les deux langues.', 'استقبال عملائك باللغتين.'),
        ('Beiruti, modes clair/sombre et écrans responsive', 'خط بيروتي ووضع فاتح وداكن وشاشات متجاوبة', 'Offrir une lecture confortable sur téléphone et ordinateur.', 'توفير قراءة مريحة على الهاتف والحاسوب.'),
        ('Identité, coordonnées et réseaux sociaux', 'هوية وبيانات تواصل وشبكات اجتماعية', 'Présenter votre établissement avec sa propre marque.', 'تقديم معرضك بعلامته الخاصة.'),
    ]
    faqs = [
        ('Puis-je gérer les annonces au quotidien ?', 'هل يمكنني إدارة الإعلانات يومياً؟', 'Oui. Votre équipe crée, modifie, publie ou masque les véhicules et met à jour leurs disponibilités depuis le tableau. La prise en main fait partie de la formation initiale.', 'نعم. ينشئ فريقك السيارات ويعدلها وينشرها أو يخفيها ويحدث توفرها من اللوحة. يشمل التدريب الأولي شرح الاستخدام.'),
        ('Combien de photos par véhicule ?', 'كم صورة لكل سيارة؟', 'La galerie accepte jusqu’à 15 photos par véhicule. Vous pouvez organiser leur ordre pour présenter les détails utiles.', 'تقبل الصور حتى 15 صورة لكل سيارة. يمكنك ترتيبها لإبراز التفاصيل المفيدة.'),
        ('Les descriptions sont-elles traduites automatiquement ?', 'هل تُترجم الأوصاف تلقائياً؟', 'Les interfaces sont en français et arabe. Votre personnel renseigne les descriptions des véhicules dans chaque langue ; la traduction automatique n’est pas incluse.', 'الواجهات بالفرنسية والعربية. يدخل موظفوك أوصاف السيارات بكل لغة، ولا يشمل الحل ترجمة آلية.'),
        ('Le client doit-il créer un compte ?', 'هل يحتاج العميل إلى إنشاء حساب؟', 'Non. Les favoris et la comparaison de trois voitures sont enregistrés sur son appareil, sans inscription. Ils ne constituent pas un compte synchronisé entre appareils.', 'لا. تُحفظ المفضلة ومقارنة ثلاث سيارات على جهازه دون تسجيل. وهي ليست حساباً متزامناً بين الأجهزة.'),
        ('Puis-je utiliser mon identité visuelle ?', 'هل يمكنني استخدام هويتي البصرية؟', 'Oui. La personnalisation initiale couvre l’identité de votre établissement, ses coordonnées et ses liens sociaux. Le périmètre est confirmé dans le devis.', 'نعم. يغطي التخصيص الأولي هوية معرضك وبيانات تواصله وروابطه الاجتماعية. يُؤكد النطاق في عرض السعر.'),
        ('Que comprend l’achat unique ?', 'ماذا يشمل الشراء لمرة واحدة؟', 'Le site installé, le tableau de gestion, la configuration initiale, la personnalisation de l’identité et la formation. Contactez DigiCode sur WhatsApp pour un devis adapté.', 'الموقع المركب ولوحة الإدارة والإعداد الأولي وتخصيص الهوية والتدريب. تواصل مع ديجي كود عبر واتساب لعرض سعر مناسب.'),
        ('L’hébergement et le support sont-ils inclus ?', 'هل الاستضافة والدعم مشمولان؟', 'L’hébergement et l’accompagnement continu sont convenus séparément. Nous précisons leurs conditions avec vous avant la livraison.', 'تُحدد الاستضافة والمرافقة المستمرة باتفاق منفصل. نوضح شروطهما معك قبل التسليم.'),
        ('Les demandes sont-elles un CRM ou une intégration WhatsApp ?', 'هل الطلبات نظام علاقات عملاء أو تكامل واتساب؟', 'Il s’agit d’une boîte de suivi avec notes internes. Les liens WhatsApp facilitent un contact manuel ; ils n’envoient pas de messages automatiques.', 'هي صندوق لمتابعة الطلبات مع ملاحظات داخلية. تسهل روابط واتساب التواصل اليدوي، ولا ترسل رسائل آلية.'),
    ]
    return {
        'cars_sales_url': sales_url or reverse('core:contact') + '#project-form',
        'cars_has_whatsapp': bool(sales_url),
        'cars_external_url': (project.link if project and project.link else 'https://cars.digicode.ma/'),
        'cars_benefits': [(text(a,b),text(c,d)) for a,b,c,d in [
            ('Votre propre showroom','معرضك الرقمي الخاص','Votre nom et votre stock au même endroit, pour un seul établissement.','اسمك ومخزونك في مكان واحد لمعرض واحد.'),
            ('Un choix plus simple','اختيار أسهل','Recherche, photos et comparaison pour préparer un échange utile.','بحث وصور ومقارنة لتهيئة محادثة مفيدة.'),
            ('Des disponibilités claires','توفر واضح','Mettez à jour les voitures disponibles, réservées ou vendues.','حدث السيارات المتاحة والمحجوزة والمباعة.'),
            ('Un suivi centralisé','متابعة موحدة','Retrouvez les demandes et les notes de votre équipe dans le tableau.','اعثر على الطلبات وملاحظات فريقك داخل اللوحة.')]],
        'cars_rows': [(text(a,b),text(c,d)) for a,b,c,d in rows],
        'cars_faq': [(text(a,b),text(c,d)) for a,b,c,d in faqs],
        'cars_steps': [text('Échange sur WhatsApp : présentez votre établissement et vos besoins.','محادثة عبر واتساب: عرفنا بمعرضك واحتياجاتك.'),text('Périmètre et devis : validez les fonctionnalités, la personnalisation et les services séparés.','النطاق وعرض السعر: حدد المميزات والتخصيص والخدمات المنفصلة.'),text('Configuration : nous préparons le site et votre identité.','الإعداد: نجهز الموقع وهويتك.'),text('Préparation du stock : rassemblez photos, caractéristiques et descriptions bilingues.','تجهيز المخزون: اجمع الصور والمواصفات والأوصاف باللغتين.'),text('Formation et livraison : votre équipe apprend à utiliser le tableau de gestion.','التدريب والتسليم: يتعلم فريقك استخدام لوحة الإدارة.')],
    }
