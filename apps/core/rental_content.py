"""Sales content adapted from the owner's supplied rental-project brief."""
from urllib.parse import urlencode
from django.urls import reverse
from django.utils.translation import get_language
from .utils import whatsapp_url


def text(fr, ar):
    return ar if get_language() == 'ar' else fr


def rental_context(request, project=None):
    from .models import SiteSettings
    service = None
    from apps.services.models import Service
    service = Service.objects.filter(is_active=True, slug__icontains='rental').first()
    params = {'project': project.slug} if project else {}
    if service:
        params['service'] = service.slug
    contact = reverse('core:contact')
    def inquiry_url(intent):
        return contact + '?' + urlencode({**params, 'intent': intent}) + '#project-form'
    message = text('Bonjour, je souhaite une démonstration de votre solution pour mon agence de location de voitures.', 'مرحباً، أود عرضاً توضيحياً لحل تأجير السيارات الخاص بكم لوكالتي.')
    return {
        'demo_url': inquiry_url('demo'), 'quote_url': inquiry_url('quote'),
        'rental_whatsapp_url': whatsapp_url(SiteSettings.load().whatsapp_number, message),
        'rental_external_url': project.link if project else 'https://rental.digicode.ma/',
        'rental_features': [
            {
                'title': text('Présentez chaque véhicule avec clarté', 'قدّم سياراتك بطريقة تساعد العميل على الاختيار'),
                'description': text('Des photos réelles, des caractéristiques utiles et des tarifs organisés pour faciliter le choix.', 'صور حقيقية ومواصفات واضحة وأسعار منظمة تساعد العميل على الاختيار قبل التواصل.'),
                'items': [text('Fiche par véhicule : galerie, marque, modèle, année et catégorie.', 'صفحة لكل سيارة: معرض صور وماركة وموديل وسنة الصنع والفئة.'), text('Transmission, carburant, places, portes, bagages et équipements renseignés par l’agence.', 'ناقل الحركة والوقود والمقاعد والأبواب والأمتعة والتجهيزات التي تضيفها الوكالة.'), text('Descriptions traduites, véhicules à la une et suggestions de la même catégorie.', 'أوصاف مترجمة وسيارات مميزة واقتراحات من الفئة نفسها.')],
            },
            {
                'title': text('Aidez vos clients à trouver le bon véhicule', 'سهّل البحث عن السيارة المناسبة'),
                'description': text('Des filtres et une recherche par dates pour consulter les options adaptées au séjour.', 'فلاتر وبحث حسب التواريخ للوصول إلى الخيارات المناسبة لفترة التأجير.'),
                'items': [text('Recherche par nom ; filtres par marque, catégorie, boîte et carburant.', 'بحث باسم السيارة وتصفية حسب الماركة والفئة وناقل الحركة والوقود.'), text('Tri par prix ou année et résultats répartis en pages.', 'ترتيب حسب السعر أو سنة الصنع وتقسيم النتائج إلى صفحات.'), text('Disponibilité sur la période choisie, ou prochaine date disponible lorsqu’elle peut être déterminée.', 'التوفر للفترة المختارة أو أقرب تاريخ متاح عند إمكانية تحديده.')],
            },
            {
                'title': text('Recevez la demande. Gardez la décision.', 'استقبل الطلب واحتفظ بقرار التأكيد'),
                'description': text('Le client choisit le véhicule et ses dates. Vous vérifiez sa demande avant de confirmer les arrangements.', 'يختار العميل السيارة والتواريخ. تراجع أنت الطلب قبل تأكيد الترتيبات.'),
                'items': [text('Nom, téléphone, e-mail facultatif et notes ; estimation des jours et du montant.', 'الاسم والهاتف والبريد الإلكتروني الاختياري والملاحظات، مع تقدير الأيام والقيمة.'), text('Demande enregistrée en attente et page de réception accessible par un lien unique.', 'حفظ الطلب بحالة قيد الانتظار وصفحة استلام عبر رابط فريد.'), text('Message WhatsApp prérempli avec véhicule, dates et référence sur la page de réception. Le client l’envoie lui-même.', 'رسالة واتساب جاهزة تتضمن السيارة والتواريخ ومرجع الطلب في صفحة الاستلام. يرسلها العميل بنفسه.')],
            },
            {
                'title': text('Suivez la disponibilité et les chevauchements', 'تابع التوفر وتعارض التواريخ'),
                'description': text('Le calendrier tient compte des demandes en attente, des réservations confirmées et des locations en cours.', 'يحتسب السجل الطلبات المعلقة والحجوزات المؤكدة والإيجارات الجارية ضمن الفترات المحجوزة.'),
                'items': [text('Vérification des dates qui se chevauchent pour un même véhicule.', 'التحقق من تداخل تواريخ الحجوزات للسيارة نفسها.'), text('Exclusion des véhicules en maintenance et libération des dates lors d’une annulation.', 'استبعاد السيارات في الصيانة وتحرير الفترة عند إلغاء الحجز.'), text('Une demande en attente bloque ses dates jusqu’au traitement par l’agence, sans expiration automatique.', 'الطلب المعلق يحتفظ بتواريخه إلى أن تعالجه الوكالة، دون مهلة انتهاء تلقائية.')],
            },
            {
                'title': text('Gérez votre flotte depuis un seul espace', 'أدِر أسطولك من لوحة خاصة'),
                'description': text('Mettez à jour les véhicules, les prix et les photos dans le tableau de bord de votre agence.', 'حدّث السيارات والأسعار والصور من لوحة إدارة وكالتك.'),
                'items': [text('Ajout et modification des caractéristiques, couleur, kilométrage et ville d’immatriculation.', 'إضافة وتعديل المواصفات واللون والكيلومترات ومدينة التسجيل.'), text('Import et classement des photos, choix de l’image principale, visibilité et mise en avant.', 'رفع الصور وترتيبها واختيار الصورة الرئيسية والتحكم في الظهور والسيارات المميزة.'), text('États disponible, réservé, loué ou en maintenance ; archivage des véhicules ayant un historique.', 'حالات متاحة ومحجوزة ومستأجرة وفي الصيانة، مع أرشفة السيارات ذات السجل.'), text('Gestion des catégories, marques et équipements, ces derniers depuis l’administration avancée.', 'إدارة الفئات والماركات والتجهيزات، والأخيرة من واجهة الإدارة المتقدمة.')],
            },
            {
                'title': text('Réunissez les réservations du site, du téléphone et du bureau', 'اجمع حجوزات الموقع والهاتف والمكتب'),
                'description': text('Conservez les demandes en ligne et les réservations saisies manuellement dans le même registre.', 'احتفظ بالطلبات الإلكترونية والحجوزات اليدوية في سجل واحد.'),
                'items': [text('Création manuelle ; modification du véhicule, des dates, du client et des notes.', 'إنشاء يدوي وتعديل السيارة والتواريخ وبيانات العميل والملاحظات.'), text('Confirmation, annulation, départ du véhicule et retour.', 'تأكيد الطلب وإلغاؤه وتسجيل التسليم والإرجاع.'), text('Recherche par client, téléphone ou véhicule ; filtres par statut et dates, et retours proches.', 'بحث بالعميل أو الهاتف أو السيارة وتصفية حسب الحالة والتواريخ ومتابعة الإرجاعات القريبة.')],
            },
            {
                'title': text('Gardez une vue sur l’activité quotidienne', 'شاهد ملخص نشاط الوكالة'),
                'description': text('Un aperçu des véhicules actifs, des demandes récentes et des locations en cours.', 'نظرة على السيارات النشطة والطلبات الحديثة والإيجارات الجارية.'),
                'items': [text('Répartition des véhicules et réservations selon leur statut.', 'توزيع السيارات والحجوزات حسب حالتها.'), text('Retours attendus dans les sept prochains jours.', 'الإرجاعات المنتظرة خلال الأيام السبعة المقبلة.'), text('Valeurs estimées des réservations confirmées, en cours et terminées : totaux et locations débutant ce mois jusqu’à aujourd’hui.', 'القيم التقديرية للحجوزات المؤكدة والجارية والمكتملة: الإجمالي والإيجارات التي يبدأ موعدها خلال الشهر حتى اليوم.')],
            },
            {
                'title': text('Faites vivre l’identité de votre agence', 'اجعل الموقع يحمل هوية وكالتك'),
                'description': text('Un site au nom de votre agence, avec vos coordonnées et vos conditions de location.', 'موقع باسم وكالتك وبيانات تواصلك وشروط تأجيرك.'),
                'items': [text('Nom, description, logo, icône du site et texte du pied de page.', 'اسم الوكالة ووصف الموقع والشعار والأيقونة ونص التذييل.'), text('Téléphone, e-mail, adresse, WhatsApp et réseaux sociaux.', 'الهاتف والبريد والعنوان وواتساب وروابط الشبكات الاجتماعية.'), text('Thème clair, sombre ou automatique avec mémorisation du choix ; conditions traduites.', 'مظهر فاتح أو داكن أو تلقائي مع حفظ اختيار الزائر وشروط تأجير مترجمة.')],
            },
            {
                'title': text('Parlez la langue de vos clients', 'تواصل مع العملاء بلغتهم'),
                'description': text('Interface client en arabe, français et anglais. Tableau de gestion de l’agence actuellement en français.', 'واجهة العملاء بالعربية والفرنسية والإنجليزية. لوحة إدارة الوكالة متاحة حالياً بالفرنسية.'),
                'items': [text('Mise en page de droite à gauche pour l’arabe et interface responsive.', 'اتجاه قراءة من اليمين إلى اليسار للعربية وتصميم متجاوب.'), text('Traductions saisies pour les catégories, descriptions et équipements ; contenu français d’origine si une traduction manque.', 'ترجمات مدخلة للفئات والأوصاف والتجهيزات، مع ظهور المحتوى الفرنسي الأصلي عند غياب ترجمة.')],
            },
            {
                'title': text('Gardez le contact avec vos visiteurs', 'حافظ على قناة واضحة للاستفسارات'),
                'description': text('WhatsApp, téléphone, e-mail et formulaire de contact pour recevoir les questions.', 'واتساب وهاتف وبريد ونموذج تواصل لاستقبال الأسئلة.'),
                'items': [text('Bouton WhatsApp lorsque le numéro de l’agence est configuré.', 'زر واتساب عند ضبط رقم الوكالة.'), text('Messages conservés dans l’administration avancée avec nom, e-mail, téléphone, sujet et message.', 'حفظ الرسائل في الإدارة المتقدمة مع الاسم والبريد والهاتف والموضوع والرسالة.'), text('Notification par e-mail possible après configuration du service de messagerie.', 'إشعار بريدي ممكن بعد إعداد خدمة البريد.')],
            },
        ],
        'rental_steps': [
            text('Ajoutez l’identité, les coordonnées et les conditions de votre agence.', 'تجهّز بيانات الوكالة: الهوية والتواصل وشروط التأجير.'),
            text('Publiez les véhicules, leurs photos, caractéristiques et tarifs.', 'تعرض أسطولك: السيارات والصور والمواصفات والأسعار.'),
            text('Le client consulte les véhicules, vérifie ses dates et son estimation.', 'يختار العميل: يتصفح السيارات ويتحقق من التواريخ والتقدير المالي.'),
            text('Vous recevez la demande et contactez le client pour confirmer.', 'تستقبل الطلب: تراجعه وتتواصل مع العميل لتأكيد الترتيبات.'),
            text('Vous suivez le départ, le retour et le statut de la réservation.', 'تتابع التأجير: تسجل التسليم والإرجاع وتحدث حالة الحجز.'),
        ],
        'rental_faq': [
            (text('Peut-on utiliser mon nom et mon logo ?', 'هل يمكن وضع اسم وكالتي وشعارها؟'), text('Oui. Le nom, le logo et les coordonnées se configurent depuis l’administration.', 'نعم، يمكنك ضبط الاسم والشعار ومعلومات التواصل من لوحة الإدارة.')),
            (text('Le client peut-il réserver depuis son téléphone ?', 'هل يستطيع العميل الحجز من الهاتف؟'), text('Il peut parcourir les véhicules, vérifier les dates et envoyer une demande via l’interface responsive.', 'يمكنه تصفح السيارات والتحقق من التواريخ وإرسال طلب عبر واجهة متجاوبة.')),
            (text('La réservation est-elle confirmée immédiatement ?', 'هل يُؤكد الحجز مباشرة؟'), text('Non. La demande arrive en attente. L’agence la vérifie et contacte le client avant de confirmer.', 'لا. يصل الطلب قيد الانتظار. تراجعه الوكالة وتتواصل مع العميل قبل التأكيد.')),
            (text('Quand une demande en attente libère-t-elle ses dates ?', 'متى يحرر الطلب المعلق تواريخه؟'), text('Elle conserve ses dates jusqu’au traitement par l’agence. La version actuelle ne prévoit pas d’expiration automatique.', 'يحتفظ بتواريخه حتى تعالجه الوكالة. لا توجد مهلة انتهاء تلقائية في النسخة الحالية.')),
            (text('Puis-je ajouter les réservations reçues au téléphone ?', 'هل أستطيع إضافة حجوزات الهاتف أو المكتب؟'), text('Oui, les réservations peuvent être créées, modifiées et suivies manuellement depuis le tableau de gestion.', 'نعم، يمكنك إنشاء الحجوزات يدوياً وتعديلها ومتابعتها من لوحة الإدارة.')),
            (text('Comment fonctionne WhatsApp ?', 'كيف يعمل واتساب؟'), text('Les liens ouvrent une conversation avec un message prérempli pour le véhicule ou la demande. Le client envoie lui-même le message.', 'تفتح الروابط محادثة برسالة جاهزة مرتبطة بالسيارة أو الطلب. يرسل العميل الرسالة بنفسه.')),
            (text('Y a-t-il un paiement en ligne ?', 'هل يدعم الدفع الإلكتروني؟'), text('Le paiement en ligne n’est pas disponible dans la version actuelle. Le site affiche une estimation et une caution ; les modalités de paiement sont convenues avec l’agence.', 'الدفع الإلكتروني غير موجود في النسخة الحالية. يعرض الموقع التقدير ومبلغ الضمان، وتُرتب إجراءات الدفع مع الوكالة.')),
            (text('Peut-on gérer plusieurs agences ou des succursales indépendantes ?', 'هل يمكن إدارة عدة وكالات أو فروع مستقلة؟'), text('La version actuelle est destinée à une seule agence. Elle ne propose pas de comptes indépendants pour plusieurs agences ou succursales.', 'النسخة الحالية مخصصة لوكالة واحدة ولا تتضمن حسابات مستقلة لعدة وكالات أو فروع.')),
            (text('Dans quelle langue est le tableau de gestion ?', 'بأي لغة تتوفر لوحة الإدارة؟'), text('Le tableau de gestion de l’agence est actuellement en français. L’interface client propose l’arabe, le français et l’anglais.', 'لوحة إدارة الوكالة متاحة حالياً بالفرنسية. واجهة العميل تدعم العربية والفرنسية والإنجليزية.')),
        ],
    }
