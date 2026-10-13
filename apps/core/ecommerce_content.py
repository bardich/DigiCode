"""Bilingual Safaa presentation adapted from the supplied e-commerce brief."""
from urllib.parse import urlencode
from django.urls import reverse
from django.utils.translation import get_language


def text(fr, ar):
    return ar if get_language() == 'ar' else fr


def ecommerce_context(request, project):
    def inquiry_url(intent):
        return reverse('core:contact') + '?' + urlencode({'project': project.slug, 'intent': intent}) + '#project-form'
    return {
        'demo_url': inquiry_url('demo'), 'quote_url': inquiry_url('quote'),
        'commerce_features': [
            {
                'title': text('Une boutique à votre image', 'متجر يعكس هوية علامتك'),
                'description': text('Accueil accueillant, produits à la une, collections, histoire de marque et réponses aux questions courantes.', 'صفحة رئيسية جذابة ومنتجات مميزة ومجموعات وقصة علامتك وإجابات عن الأسئلة الشائعة.'),
                'items': [text('Contenus produits en français et arabe, avec navigation et formulaires adaptés à la lecture arabe.', 'محتوى المنتجات بالفرنسية والعربية، مع تنقل ونماذج تناسب اتجاه القراءة بالعربية.'), text('Parcours responsive et barre d’achat fixe sur les fiches mobiles.', 'تجربة متجاوبة وشريط شراء ثابت في صفحات المنتجات على الهاتف.'), text('Photos, formats, prix en dirhams, ingrédients, origine, disponibilité et livraison.', 'صور وأحجام وأسعار بالدرهم ومكونات ومنشأ ومعلومات التوفر والتوصيل.')],
            },
            {
                'title': text('Une recherche qui comprend votre catalogue', 'بحث يفهم كتالوجك'),
                'description': text('Aidez vos clients à trouver un produit sans parcourir tout votre stock.', 'ساعد عملاءك على الوصول إلى المنتج المناسب دون تصفح المخزون كله.'),
                'items': [text('Recherche dans les noms arabes et français, catégories, références et mots-clés définis par vos soins.', 'بحث في الأسماء العربية والفرنسية والفئات ومراجع المنتجات والكلمات التي تحددها.'), text('Filtres par catégorie et prix, tri et pagination.', 'تصفية حسب الفئة والسعر وترتيب النتائج وتقسيمها إلى صفحات.')],
            },
            {
                'title': text('Du panier à la commande, en toute clarté', 'من السلة إلى الطلب بوضوح'),
                'description': text('Un achat sans création de compte, avec paiement à la livraison.', 'شراء دون إنشاء حساب، مع الدفع عند الاستلام.'),
                'items': [text('Quantités modifiables, suppression de produits, code de réduction et choix de la ville.', 'تعديل الكميات وحذف المنتجات وتطبيق رمز خصم واختيار المدينة.'), text('Produits, remises applicables et frais de livraison calculés avant confirmation.', 'احتساب المنتجات والخصومات المناسبة ورسوم التوصيل قبل تأكيد الطلب.'), text('Nom, numéro marocain, ville, adresse et note de livraison facultative.', 'اسم ورقم هاتف مغربي ومدينة وعنوان وملاحظة توصيل اختيارية.')],
            },
            {
                'title': text('Un suivi privé et un contact accessible', 'متابعة خاصة وتواصل سهل'),
                'description': text('Le client conserve un lien privé pour suivre sa commande sans se connecter.', 'يحفظ العميل رابطاً خاصاً لمتابعة طلبه دون تسجيل الدخول.'),
                'items': [text('Les pages de suivi n’affichent ni adresse, ni téléphone, ni notes internes.', 'لا تعرض صفحات المتابعة العنوان أو الهاتف أو الملاحظات الداخلية.'), text('Téléphone, e-mail, réseaux sociaux et bouton de contact WhatsApp.', 'هاتف وبريد إلكتروني وشبكات اجتماعية وزر للتواصل عبر واتساب.'), text('Les achats se font sur le site ; la confirmation WhatsApp est gérée par votre équipe.', 'تتم المشتريات داخل الموقع، وتتولى فرقك التأكيد عبر واتساب.')],
            },
            {
                'title': text('Votre catalogue sous contrôle', 'كتالوجك تحت سيطرتك'),
                'description': text('Les personnes autorisées gèrent les produits et leurs formats depuis le tableau de bord.', 'تدير الفرق المصرح لها المنتجات وأحجامها من لوحة التحكم.'),
                'items': [text('Descriptions bilingues, photos, ingrédients, origines, catégories, recherche et mise en avant.', 'أوصاف ثنائية اللغة وصور ومكونات ومنشأ وفئات وبحث وإبراز المنتجات.'), text('Publication contrôlée : laissez un produit masqué pendant sa préparation.', 'نشر متحكم فيه: أبقِ المنتج مخفياً أثناء إعداد محتواه.'), text('Chaque format possède sa référence, son prix de vente, son coût, son poids et sa disponibilité.', 'لكل حجم مرجع وسعر بيع وتكلفة ووزن وحالة توفر، مثل 250 غ أو 500 غ أو 1 كغ.')],
            },
            {
                'title': text('Des commandes organisées pour l’équipe', 'طلبات منظمة لفريقك'),
                'description': text('Identifiez ce qui attend confirmation, préparation ou expédition.', 'اعرف ما ينتظر التأكيد أو التحضير أو الشحن.'),
                'items': [text('Coordonnées, ville, total, état de traitement, encaissement et responsable assigné.', 'بيانات العميل والمدينة والإجمالي وحالة المعالجة والتحصيل والموظف المكلف.'), text('Recherche, filtres, notes privées, impression des récapitulatifs et export des commandes.', 'بحث وتصفية وملاحظات خاصة وطباعة الملخصات وتصدير الطلبات.'), text('Correction des coordonnées et de l’adresse avant expédition ; historique des changements.', 'تصحيح بيانات التواصل والعنوان قبل الشحن، مع سجل للتغييرات.'), text('Actions encadrées pour annulation, échec de livraison, nouvelle tentative et retour.', 'إجراءات منظمة للإلغاء وفشل التوصيل وإعادة المحاولة والإرجاع.')],
            },
            {
                'title': text('Livraison et encaissement : deux suivis distincts', 'التوصيل والتحصيل: متابعتان منفصلتان'),
                'description': text('Une commande livrée ne signifie pas que l’argent est déjà parvenu à votre boutique.', 'توصيل الطلب لا يعني أن الأموال وصلت بالفعل إلى متجرك.'),
                'items': [text('Confirmation manuelle par téléphone ou WhatsApp et suivi dans le tableau.', 'تأكيد يدوي بالهاتف أو واتساب مع تسجيل المتابعة في اللوحة.'), text('Fonds non collectés, collectés par le livreur ou reversés au magasin.', 'أموال لم تُحصّل أو حصّلها الموزع أو حُوّلت إلى المتجر.'), text('Rapports séparant valeur des commandes, ventes livrées et fonds reversés.', 'تقارير تفصل قيمة الطلبات عن المبيعات المسلّمة والأموال المحولة.')],
            },
            {
                'title': text('Sachez où va votre stock', 'اعرف أين يذهب مخزونك'),
                'description': text('Les quantités commandées sont réservées ; le stock physique est déduit à l’expédition.', 'تُحجز الكميات المطلوبة، ويُخصم المخزون الفعلي عند الشحن.'),
                'items': [text('Réservations non confirmées : expiration après 48 heures. Réservations confirmées : maintien jusqu’à annulation ou expédition.', 'الحجوزات غير المؤكدة تنتهي بعد 48 ساعة. وتبقى المؤكدة حتى الإلغاء أو الشحن.'), text('Annulation : libération des réservations. Retour : remise en stock après contrôle par le personnel.', 'الإلغاء يحرر الكميات المحجوزة. وتُعاد المنتجات المرجعة إلى المخزون بعد فحص الموظفين.'), text('Historique des réceptions, ajustements, expéditions et retours avec motif ; seuils de stock bas par format.', 'سجل للاستلام والتعديلات والشحن والإرجاعات مع سبب كل حركة، وعتبات للمخزون المنخفض حسب الحجم.')],
            },
            {
                'title': text('Vos villes, vos règles de livraison', 'مدنك وقواعد توصيلك'),
                'description': text('Configurez la couverture selon le fonctionnement de votre activité au Maroc.', 'اضبط التغطية بما يناسب نشاطك في المغرب.'),
                'items': [text('Villes desservies, frais, délais estimés et coûts de transport.', 'مدن مدعومة ورسوم ومدد توصيل تقديرية وتكاليف نقل.'), text('Activation des destinations et seuils de livraison gratuite selon vos règles.', 'تفعيل الوجهات وضبط حدود التوصيل المجاني حسب قواعدك.')],
            },
            {
                'title': text('Des promotions utiles, des totaux vérifiés', 'عروض مفيدة وإجماليات متحقق منها'),
                'description': text('Créez des codes de réduction en pourcentage ou en montant fixe.', 'أنشئ رموز خصم بنسبة مئوية أو مبلغ ثابت.'),
                'items': [text('Produits ou catégories éligibles, minimum d’achat, dates et limites globales d’utilisation.', 'منتجات أو فئات مؤهلة وحد أدنى للطلب وتواريخ وحدود إجمالية للاستخدام.'), text('Un seul code par commande ; éligibilité et calculs vérifiés sur le serveur.', 'رمز واحد لكل طلب، مع التحقق من الأهلية والحسابات على الخادم.')],
            },
            {
                'title': text('Faites évoluer vos contenus vous-même', 'حدّث محتواك بنفسك'),
                'description': text('Les réglages courants de la boutique restent accessibles aux équipes autorisées.', 'تبقى إعدادات المتجر المعتادة متاحة للفرق المصرح لها.'),
                'items': [text('Identité, coordonnées, couleurs principales prises en charge, textes et image d’accueil.', 'هوية وتواصل وألوان رئيسية مدعومة ونصوص وصورة الصفحة الرئيسية.'), text('Ordre des sections prises en charge, produits à la une, FAQ et témoignages approuvés.', 'ترتيب الأقسام المدعومة والمنتجات المميزة والأسئلة الشائعة والشهادات المعتمدة.'), text('Pages d’information et politiques bilingues, titres et descriptions de référencement.', 'صفحات معلومات وسياسات ثنائية اللغة وعناوين وأوصاف لمحركات البحث.'), text('Règles de livraison, limites de commande, ouverture des achats et indexation du site.', 'قواعد التوصيل وحدود الطلبات وفتح الشراء وفهرسة الموقع.')],
            },
            {
                'title': text('Des indicateurs pour décider', 'مؤشرات تساعدك على القرار'),
                'description': text('Suivez l’activité, les produits et les villes sans confondre ventes et argent reçu.', 'تابع النشاط والمنتجات والمدن دون الخلط بين المبيعات والأموال المستلمة.'),
                'items': [text('Commandes du jour, confirmations et expéditions attendues, livraisons échouées et stock bas.', 'طلبات اليوم والتأكيدات والشحنات المنتظرة والتوصيلات الفاشلة والمخزون المنخفض.'), text('Valeur des commandes, ventes livrées, panier moyen et fonds COD reversés.', 'قيمة الطلبات والمبيعات المسلّمة ومتوسط الطلب والأموال المحولة من الدفع عند الاستلام.'), text('Produits les plus vendus, ventes livrées par ville, statuts et clients revenant acheter.', 'المنتجات الأكثر مبيعاً والمبيعات المسلّمة حسب المدينة والحالات والعملاء العائدون.'), text('Marge estimée selon les coûts produits et la livraison ; prix et coûts historiques conservés au moment de l’achat.', 'هامش تقديري حسب تكلفة المنتجات والتوصيل، مع حفظ الأسعار والتكاليف المسجلة وقت الشراء.')],
            },
        ],
        'commerce_statuses': [text('Reçue','مستلم'), text('À confirmer','بانتظار التأكيد'), text('Confirmée','مؤكد'), text('En préparation','قيد التحضير'), text('Expédiée','مشحون'), text('En livraison','قيد التوصيل'), text('Livrée','تم التوصيل')],
        'commerce_roles': [text('Propriétaire','مالك'), text('Administrateur','مدير النظام'), text('Manager','مسؤول الإدارة'), text('Commandes','فريق الطلبات'), text('Contenu','فريق المحتوى'), text('Entrepôt','فريق المستودع')],
        'commerce_audiences': [text('Produits naturels et marques du terroir marocain','المنتجات الطبيعية والعلامات المغربية المحلية'), text('Miel, amlou, huiles, dattes et produits alimentaires emballés','العسل وأملو والزيوت والتمور والمنتجات الغذائية المعبأة'), text('Beauté et soins personnels','منتجات التجميل والعناية الشخصية'), text('Artisanat et coffrets cadeaux','الحرف ومجموعات الهدايا'), text('Marques indépendantes présentes sur les réseaux sociaux','العلامات المستقلة الموجودة على الشبكات الاجتماعية'), text('Commerçants développant leur propre canal de vente','متاجر تطور قناة بيع خاصة بها')],
        'commerce_steps': [
            (text('Comprendre votre activité','نفهم نشاطك'),text('Catalogue, identité, couverture de livraison, processus COD et responsabilités de l’équipe.','الكتالوج والهوية وتغطية التوصيل والدفع عند الاستلام ومسؤوليات الفريق.')),
            (text('Préparer vos contenus','نجهز محتواك'),text('Logo, photos, descriptions bilingues, prix, stock initial, coordonnées et politiques approuvées.','الشعار والصور والأوصاف الثنائية اللغة والأسعار والمخزون الأولي والتواصل والسياسات المعتمدة.')),
            (text('Adapter la boutique','نخصص المتجر'),text('Personnalisation de l’expérience, produits, livraison, remises, contenus et accès du personnel.','تخصيص التجربة والمنتجات والتوصيل والخصومات والمحتوى وصلاحيات الموظفين.')),
            (text('Vérifier le parcours complet','نتحقق من المسار الكامل'),text('Vérification en préproduction de l’achat mobile, confirmation, expédition, suivi, stock et encaissement.','فحص الشراء على الهاتف والتأكيد والشحن والمتابعة والمخزون والتحصيل في بيئة تجريبية.')),
            (text('Préparer le lancement','نجهز الإطلاق'),text('Domaine, hébergement, stockage et suivi opérationnel, puis ouverture des commandes après vérification.','النطاق والاستضافة والتخزين والمراقبة التشغيلية، ثم فتح الطلبات بعد التحقق.')),
        ],
        'commerce_extensions': [text('Comptes clients et historique','حسابات العملاء وسجل الطلبات'),text('Paiements en ligne','الدفع الإلكتروني'),text('Messages WhatsApp ou SMS automatiques','رسائل واتساب أو رسائل نصية آلية'),text('Intégrations transporteurs','تكامل شركات التوصيل'),text('Avis publics sur les produits','تقييمات عامة للمنتجات'),text('Articles, recettes et conseils','مقالات ووصفات ومحتوى تعليمي'),text('Promotions avancées et lots','عروض متقدمة وحزم منتجات'),text('Paiements et livraisons internationaux','الدفع والشحن الدوليان'),text('Expérience de boutique installable','تجربة متجر قابلة للتثبيت')],
        'commerce_faq': [
            (text('Faut-il un compte client pour commander ?','هل يحتاج العميل إلى حساب للطلب؟'),text('Non. Le parcours actuel utilise un achat invité : le client renseigne la livraison et reçoit un lien privé de suivi. Les comptes clients constituent une phase supplémentaire.','لا. المسار الحالي يتيح الشراء كزائر: يدخل العميل معلومات التوصيل ويحصل على رابط متابعة خاص. حسابات العملاء مرحلة إضافية.')),
            (text('La boutique prend-elle en charge l’arabe ?','هل يدعم المتجر العربية؟'),text('Oui. La boutique propose l’arabe et le français, avec des mises en page adaptées à la lecture de droite à gauche.','نعم. يدعم المتجر العربية والفرنسية مع تخطيطات تناسب القراءة من اليمين إلى اليسار.')),
            (text('Puis-je gérer les produits moi-même ?','هل يمكنني إدارة المنتجات بنفسي؟'),text('Les personnes autorisées gèrent produits, formats, prix, images, catégories et disponibilités depuis le tableau de bord.','تدير الفرق المصرح لها المنتجات والأحجام والأسعار والصور والفئات والتوفر من لوحة التحكم.')),
            (text('Comment fonctionne le paiement à la livraison ?','كيف يعمل الدفع عند الاستلام؟'),text('Le client choisit COD. Votre équipe confirme et traite la commande, puis enregistre séparément la collecte par le livreur et le reversement au magasin.','يختار العميل الدفع عند الاستلام. يؤكد فريقك الطلب ويعالجه، ثم يسجل تحصيل الموزع وتحويل الأموال إلى المتجر بشكل منفصل.')),
            (text('La confirmation WhatsApp est-elle automatique ?','هل التأكيد عبر واتساب آلي؟'),text('La version actuelle utilise des liens de contact et une confirmation gérée par le personnel. Les messages automatiques nécessitent une intégration supplémentaire.','النسخة الحالية تعتمد روابط للتواصل وتأكيداً يديره الموظفون. تحتاج الرسائل الآلية إلى تكامل إضافي.')),
            (text('Peut-on varier les frais selon la ville ?','هل يمكن تحديد رسوم مختلفة حسب المدينة؟'),text('Oui : frais, délais estimés, destinations disponibles et seuils éventuels de livraison gratuite sont configurables.','نعم. يمكن ضبط الرسوم والمدد التقديرية والوجهات المتاحة وحدود التوصيل المجاني عند الحاجة.')),
            (text('Mon équipe peut-elle avoir des accès différents ?','هل يمكن لفريقي الحصول على صلاحيات مختلفة؟'),text('Oui. Les rôles couvrent commandes, contenu, entrepôt et administration. L’authentification du personnel prévoit une configuration multifacteur obligatoire et des codes de récupération.','نعم. تغطي الأدوار الطلبات والمحتوى والمستودع والإدارة. يتضمن دخول الموظفين إعداداً إلزامياً للمصادقة متعددة العوامل ورموز استرداد.')),
            (text('Safaa est-elle déjà une boutique ouverte au public ?','هل صفاء متجر مفتوح للجمهور بالفعل؟'),text('Non. Safaa est une démonstration avec produits, visuels et prix d’exemple. Les commandes publiques sont désactivées. Le lancement d’une entreprise nécessite contenus finaux, infrastructure et vérification en préproduction.','لا. صفاء عرض تجريبي بمنتجات وصور وأسعار نموذجية. الطلبات العامة معطلة. يتطلب إطلاق نشاط تجاري محتوى نهائياً وبنية تشغيلية وفحصاً في بيئة تجريبية.')),
            (text('Combien coûte une boutique ?','ما تكلفة متجر إلكتروني؟'),text('Nous préparons un devis selon votre catalogue, les personnalisations, intégrations, hébergement et besoins d’accompagnement. Contactez-nous pour en discuter.','نجهز عرض سعر حسب الكتالوج والتخصيص والتكاملات والاستضافة والمرافقة المطلوبة. تواصل معنا لمناقشتها.')),
        ],
    }
