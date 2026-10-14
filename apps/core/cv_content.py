"""Sales copy and clearly fictional CV-demo content, localized without fallbacks."""
from urllib.parse import urlencode
from django.urls import reverse
from django.utils.translation import get_language
from apps.services.models import Service
from .models import Project, SiteSettings
from .utils import whatsapp_url


def text(fr, ar):
    return ar if get_language() == 'ar' else fr


def cv_context(request, project=None, service=None):
    service = service or Service.objects.filter(slug='cv-portfolio', is_active=True).first()
    params = {'service': service.slug} if service else {}
    if project:
        params.update(project=project.slug, intent='quote')
    quote_url = reverse('core:contact') + ('?' + urlencode(params) if params else '') + '#project-form'
    message = text('Bonjour DigiCode, je souhaite un devis pour transformer mon CV en site web professionnel.', 'مرحباً ديجي كود، أريد عرض سعر لتحويل سيرتي الذاتية إلى موقع مهني.')
    if project:
        message += text(f' Exemple choisi : {project.get_title()}.', f' النموذج المختار: {project.get_title()}.')
    return {
        'cv_service': service,
        'cv_service_url': service.get_absolute_url() if service else reverse('services:list'),
        'cv_quote_url': quote_url,
        'cv_whatsapp_url': whatsapp_url(SiteSettings.load().whatsapp_number, message),
        'cv_examples': Project.objects.filter(is_active=True, landing_page__in=['cv_professional', 'cv_creative']).order_by('display_order', 'pk'),
        'cv_steps': [
            (text('Parlons de votre parcours','نتحدث عن مسارك'), text('Objectif, audience et style souhaité : nous préparons un devis personnalisé.','الهدف والجمهور والأسلوب المطلوب: نجهز عرض سعر مخصصاً.')),
            (text('Rassemblez vos contenus','اجمع محتواك'), text('Après notre échange, partagez votre CV et les éléments approuvés par un canal privé convenu ensemble.','بعد المناقشة، شارك سيرتك الذاتية والمواد المعتمدة عبر قناة خاصة نتفق عليها.')),
            (text('Organisons votre histoire','ننظم قصتك'), text('Nous structurons vos expériences, compétences et réalisations, puis créons votre design.','ننظم خبراتك ومهاراتك وأعمالك، ثم نصمم موقعك.')),
            (text('Relisez et validez','راجع واعتمد'), text('Vous vérifiez les textes, les liens et la présentation avant la livraison.','تراجع النصوص والروابط والتصميم قبل التسليم.')),
            (text('Recevez votre site','استلم موقعك'), text('Livraison des fichiers HTML/CSS/JS. Domaine, hébergement, publication et mises à jour sont convenus séparément.','تسليم ملفات HTML/CSS/JS. النطاق والاستضافة والنشر والتحديثات تُحدد باتفاق منفصل.')),
        ],
        'cv_faq': [
            (text('Quelles langues sont possibles ?','ما اللغات المتاحة؟'),text('Français et arabe, avec une mise en page adaptée à chaque langue. Le contenu et les traductions sont validés avec vous dans le périmètre du devis.','الفرنسية والعربية مع تخطيط مناسب لكل لغة. يُعتمد المحتوى والترجمات معك ضمن نطاق عرض السعر.')),
            (text('Que dois-je fournir ?','ماذا أحتاج إلى تقديمه؟'),text('Votre CV à jour, vos liens professionnels et, si vous souhaitez les présenter, vos photos et projets autorisés. Nous ne publions que les coordonnées que vous approuvez.','سيرتك المحدثة وروابطك المهنية، وصورك وأعمالك المسموح بعرضها إن رغبت. ننشر فقط بيانات التواصل التي تعتمدها.')),
            (text('Puis-je adapter l’un des exemples ?','هل يمكنني تخصيص أحد النموذجين؟'),text('Oui. Ils servent de point de départ : couleurs, sections et présentation sont adaptés à votre profil selon le devis. Les identités affichées sont fictives.','نعم. هما نقطة بداية: تُخصص الألوان والأقسام والتصميم لمسارك حسب عرض السعر. الشخصيات المعروضة خيالية.')),
            (text('Le domaine et l’hébergement sont-ils inclus ?','هل النطاق والاستضافة مشمولان؟'),text('La livraison standard comprend les fichiers statiques. Domaine, hébergement et publication sont définis séparément ; nous pouvons discuter de leur mise en place.','يشمل التسليم القياسي الملفات الثابتة. يُحدد النطاق والاستضافة والنشر بشكل منفصل، ويمكننا مناقشة إعدادها.')),
            (text('Comment mettre mon CV à jour ensuite ?','كيف أحدث سيرتي لاحقاً؟'),text('Les fichiers peuvent être modifiés et republiés. Ce service ne comprend pas de tableau d’administration ; les mises à jour ou un accompagnement sont convenus séparément.','يمكن تعديل الملفات وإعادة نشرها. لا تشمل الخدمة لوحة إدارة، وتُحدد التحديثات أو المرافقة باتفاق منفصل.')),
            (text('Le site est-il généré automatiquement ?','هل يُنشأ الموقع تلقائياً؟'),text('Non. DigiCode organise votre contenu et réalise le site après échange et validation. Aucun téléversement de CV n’est demandé sur ce site.','لا. تنظم ديجي كود محتواك وتنجز الموقع بعد المناقشة والاعتماد. لا يُطلب رفع السيرة الذاتية على هذا الموقع.')),
        ],
        'professional_experience': [
            ('2022 — 2026', text('Consultante en organisation','مستشارة تنظيم'),text('Structure de conseil fictive','مكتب استشارات خيالي'),text('Clarifier les besoins, structurer les processus et accompagner les équipes dans leurs projets.','توضيح الاحتياجات وتنظيم الإجراءات ومرافقة الفرق في مشاريعها.')),
            ('2019 — 2022', text('Chargée de projets','مسؤولة مشاريع'),text('Organisation fictive','مؤسسة خيالية'),text('Préparer les plans de travail, coordonner les échanges et documenter les décisions.','إعداد خطط العمل وتنسيق التواصل وتوثيق القرارات.')),
            ('2017 — 2019', text('Analyste junior','محللة مبتدئة'),text('Équipe fictive','فريق خيالي'),text('Recueillir les informations, analyser les besoins et rédiger des synthèses utiles.','جمع المعلومات وتحليل الاحتياجات وإعداد خلاصات مفيدة.')),
        ],
        'professional_skills': [text('Gestion de projet','إدارة المشاريع'),text('Analyse des besoins','تحليل الاحتياجات'),text('Organisation des processus','تنظيم الإجراءات'),text('Animation d’ateliers','تنشيط ورش العمل'),text('Communication','التواصل'),text('Documentation','التوثيق')],
        'creative_skills': [text('Identité visuelle','هوية بصرية'),text('Design d’interfaces','تصميم واجهات'),text('Direction artistique','توجيه فني'),text('Typographie','تصميم طباعي'),text('Composition','تكوين بصري'),text('Prototypage','نماذج أولية')],
        'creative_work': [
            {'name':'FORMA', 'type':text('Identité visuelle','هوية بصرية'), 'description':text('Une recherche de formes, de rythme et de contraste pour une marque imaginaire.','بحث في الأشكال والإيقاع والتباين لعلامة خيالية.'), 'style':'forma'},
            {'name':'ATELIER 04', 'type':text('Design éditorial','تصميم تحريري'), 'description':text('Un concept de publication où la typographie devient le sujet principal.','تصور لمنشور تصبح فيه الحروف العنصر الرئيسي.'), 'style':'atelier'},
            {'name':'ORBIT', 'type':text('Interface numérique','واجهة رقمية'), 'description':text('Une exploration d’interface autour de la clarté, de l’espace et du mouvement.','تصور لواجهة تتمحور حول الوضوح والمساحة والحركة.'), 'style':'orbit'},
        ],
    }
