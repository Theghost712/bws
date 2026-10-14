"""Multilingual birthday message catalogue.

Each tone contains several *variants*; a variant is a list of sentences so the
generator can compose short, medium and long wishes precisely. Content is
written natively for every supported language rather than word-for-word
translated, and adding a language is a matter of adding a block here plus a
message catalogue under ``locale/`` for the interface.
"""

HELLO = {
    "en": "Happy birthday",
    "sw": "Heri ya kuzaliwa",
    "fr": "Joyeux anniversaire",
    "es": "Feliz cumpleaños",
    "ar": "عيد ميلاد سعيد",
}

GREETINGS = {
    "en": {
        "wife": "my darling wife", "husband": "my dear husband",
        "girlfriend": "my love", "boyfriend": "my love",
        "friend": "my dear friend", "mother": "Mum", "father": "Dad",
        "sister": "my dear sister", "brother": "my dear brother",
        "son": "my dear son", "daughter": "my dear daughter",
        "relative": "dearest one", "colleague": "my wonderful colleague",
        "teacher": "my dear teacher", "other": "my dear friend",
    },
    "sw": {
        "wife": "mke wangu mpendwa", "husband": "mume wangu mpendwa",
        "girlfriend": "mpenzi wangu", "boyfriend": "mpenzi wangu",
        "friend": "rafiki yangu mpendwa", "mother": "Mama", "father": "Baba",
        "sister": "dada yangu mpendwa", "brother": "kaka yangu mpendwa",
        "son": "mwanangu mpendwa", "daughter": "binti yangu mpendwa",
        "relative": "ndugu yangu mpendwa", "colleague": "mwenzangu mpendwa",
        "teacher": "mwalimu wangu mpendwa", "other": "rafiki yangu mpendwa",
    },
    "fr": {
        "wife": "ma chère épouse", "husband": "mon cher époux",
        "girlfriend": "mon amour", "boyfriend": "mon amour",
        "friend": "mon cher ami", "mother": "Maman", "father": "Papa",
        "sister": "ma chère sœur", "brother": "mon cher frère",
        "son": "mon cher fils", "daughter": "ma chère fille",
        "relative": "cher proche", "colleague": "cher collègue",
        "teacher": "cher professeur", "other": "mon cher ami",
    },
    "es": {
        "wife": "mi querida esposa", "husband": "mi querido esposo",
        "girlfriend": "mi amor", "boyfriend": "mi amor",
        "friend": "mi querido amigo", "mother": "Mamá", "father": "Papá",
        "sister": "mi querida hermana", "brother": "mi querido hermano",
        "son": "mi querido hijo", "daughter": "mi querida hija",
        "relative": "querido familiar", "colleague": "querido colega",
        "teacher": "querido profesor", "other": "mi querido amigo",
    },
    "ar": {
        "wife": "زوجتي العزيزة", "husband": "زوجي العزيز",
        "girlfriend": "حبيبتي", "boyfriend": "حبيبي",
        "friend": "صديقي العزيز", "mother": "أمي", "father": "أبي",
        "sister": "أختي العزيزة", "brother": "أخي العزيز",
        "son": "ابني العزيز", "daughter": "ابنتي العزيزة",
        "relative": "عزيزي القريب", "colleague": "زميلي العزيز",
        "teacher": "أستاذي العزيز", "other": "صديقي العزيز",
    },
}

SIGNOFF = {
    "en": "With love",
    "sw": "Kwa upendo",
    "fr": "Avec affection",
    "es": "Con cariño",
    "ar": "مع كل الحب",
}

LONG_CLOSERS = {
    "en": [
        "May this year bring you everything you quietly hope for.",
        "Here is to laughter, health and beautiful surprises.",
    ],
    "sw": [
        "Mwaka huu ukuletee kila unachotamani kwa faragha.",
        "Kwa vicheko, afya na mshangao mzuri.",
    ],
    "fr": [
        "Que cette année t'apporte tout ce que tu espères discrètement.",
        "Aux rires, à la santé et aux belles surprises.",
    ],
    "es": [
        "Que este año te traiga todo lo que esperas en silencio.",
        "Por las risas, la salud y las sorpresas hermosas.",
    ],
    "ar": [
        "ليأتِ لك هذا العام بكل ما تتمناه في سرك.",
        "إلى الضحك والصحة والمفاجآت الجميلة.",
    ],
}

AGE_LINE = {
    "en": "Here's to turning {age}!",
    "sw": "Heri ya kutimiza miaka {age}!",
    "fr": "Joyeux {age} ans !",
    "es": "¡Felicidades por tus {age}!",
    "ar": "عامك ال{age} سعيد!",
}

# BODIES[language][tone] -> list of variants; each variant is a list of sentences.
BODIES = {
    "en": {
        "romantic": [
            ["You are the reason my ordinary days feel like celebrations.", "I hope today wraps you in as much love as you give me.", "Happy birthday, my love."],
            ["Every year with you is my favourite year yet.", "May the candles remind you how brightly you light up my life.", "I love you endlessly."],
            ["If I could give you one gift, it would be a mirror so you could see how wonderful you are.", "Today I celebrate you with my whole heart.", "Happy birthday, darling."],
        ],
        "emotional": [
            ["Some people quietly make the world kinder just by being in it, and you are one of them.", "I am so grateful to know you.", "Happy birthday."],
            ["The years keep passing, but my appreciation for you only grows.", "Thank you for everything you bring into my life.", "Have a beautiful birthday."],
            ["Today my heart is full because you were born.", "I hope this year returns to you every bit of goodness you give away.", "Happy birthday."],
        ],
        "funny": [
            ["Happy birthday! You are not getting older, you are becoming a limited edition.", "Please save me a slice of cake the size of my enthusiasm."],
            ["You are officially at the age where the candles cost more than the cake.", "Happy birthday and enjoy your very important day."],
            ["Another trip around the sun and still no instruction manual.", "You are doing great. Now go claim the biggest piece of cake."],
        ],
        "inspirational": [
            ["May this new year open doors you did not even know existed.", "You have everything it takes to make it wonderful.", "Happy birthday."],
            ["Here is to another year of dreaming bigger and shining brighter.", "I cannot wait to see what you build next.", "Happy birthday."],
            ["The best chapters of your story are still unwritten.", "May this year be full of courage, joy and beautiful surprises."],
        ],
        "religious": [
            ["May the Lord bless you and keep you on this special day.", "May this new year be filled with grace, peace and abundant joy.", "Happy birthday."],
            ["I thank God for the gift of your life.", "May His favour follow you in everything you do.", "Happy birthday and many blessings."],
            ["May your birthday be covered in prayer and surrounded by love.", "May faith guide you gently through the year ahead."],
        ],
        "short": [
            ["Happy birthday! Wishing you a wonderful day."],
            ["Happy birthday! May this year be kind to you."],
            ["Happy birthday! So glad you were born."],
        ],
        "heartfelt": [
            ["You mean more to me than I can easily put into words.", "I hope today feels as warm as you make everyone around you feel.", "Happy birthday."],
            ["I am so thankful that our lives crossed.", "Wishing you a birthday filled with the little things that make your heart settle.", "Happy birthday."],
            ["You make ordinary days brighter just by being you.", "I hope this year brings that brightness right back to you."],
        ],
        "formal": [
            ["Please accept my warmest wishes on your birthday.", "May the year ahead bring you continued success, good health and happiness."],
            ["Wishing you a very happy birthday and a rewarding year ahead.", "May it be filled with prosperity and many reasons to celebrate."],
            ["On this special occasion, I extend my sincere congratulations.", "May the coming year bring you every success and lasting fulfilment."],
        ],
        "creative": [
            ["If birthdays were colours, today would be every shade of happy.", "Paint this year in whatever colours you love most."],
            ["Consider this message a tiny paper hat for your celebration.", "Wear your year proudly."],
            ["A year is a blank page and you hold the pen.", "Write something worth reading and make today the first line."],
        ],
    },
    "sw": {
        "romantic": [
            ["Wewe ndiye unayefanya siku zangu za kawaida zionekane kama sherehe.", "Nakutakia leo upendwe kama unavyonipenda mimi.", "Heri ya kuzaliwa, mpenzi wangu."],
            ["Kila mwaka nawe ni mwaka ninaoupenda zaidi.", "Mishumaa ikukumbushe jinsi unavyong'aa maishani mwangu.", "Nakupenda bila kikomo."],
            ["Laiti ningekupa kioo, ungejiona jinsi ulivyo mzuri.", "Leo nakuadhimisha kwa moyo wangu wote.", "Heri ya kuzaliwa, mpenzi."],
        ],
        "emotional": [
            ["Watu wengine hufanya dunia iwe na upole zaidi kwa kuwa tu maishani, na wewe ni mmoja wao.", "Nina furaha kubwa kukufahamu.", "Heri ya kuzaliwa."],
            ["Miaka inapita, lakini kuthamini kwangu wewe kunazidi kila siku.", "Asante kwa kila kitu unacholeta maishani mwangu.", "Uwe na siku nzuri ya kuzaliwa."],
            ["Leo moyo wangu umejaa kwa sababu ulizaliwa.", "Mwaka huu ukurudishie wema wote unaowapa wengine.", "Heri ya kuzaliwa."],
        ],
        "funny": [
            ["Heri ya kuzaliwa! Huzeeki, unazidi kuwa wa kipekee.", "Niokoe kipande cha keki kwa ukubwa wa shauku yangu."],
            ["Umefikia umri ambao mishumaa inagharimu zaidi ya keki.", "Heri ya kuzaliwa na ufurahie siku yako muhimu."],
            ["Mzunguko mwingine wa jua na bado hakuna mwongozo wa maisha.", "Unaendelea vizuri. Sasa kata kipande kikubwa cha keki."],
        ],
        "inspirational": [
            ["Mwaka huu mpya ukufungulie milango hata usingejua ipo.", "Una kila kitu kinachohitajika kuufanya uwe mzuri.", "Heri ya kuzaliwa."],
            ["Kwa mwaka mwingine wa kuota kwa ujasiri na kung'aa zaidi.", "Natarajia kuona unachojenga.", "Heri ya kuzaliwa."],
            ["Sura bora za hadithi yako bado hazijaandikwa.", "Mwaka huu uwe wa ujasiri, furaha na mshangao mzuri."],
        ],
        "religious": [
            ["Bwana akubariki na akulinde katika siku hii maalum.", "Mwaka huu ujae neema, amani na furaha tele.", "Heri ya kuzaliwa."],
            ["Namshukuru Mungu kwa zawadi ya maisha yako.", "Neema yake ikufuate katika kila unachofanya.", "Heri ya kuzaliwa na baraka nyingi."],
            ["Siku yako ya kuzaliwa iwe imefungwa kwa maombi na kuzungukwa na upendo.", "Imani ikuelekeze kwa upole mwaka huu."],
        ],
        "short": [
            ["Heri ya kuzaliwa! Nakutakia siku nzuri."],
            ["Heri ya kuzaliwa! Mwaka huu uwe mwema kwako."],
            ["Heri ya kuzaliwa! Nafurahi ulizaliwa."],
        ],
        "heartfelt": [
            ["Unamaanisha mengi kwangu zaidi ya ninavyoweza kusema.", "Natumai leo litakuwa joto kama unavyowafanya wengine wahisi.", "Heri ya kuzaliwa."],
            ["Nina shukrani kuwa maisha yetu yalikutana.", "Nakutakia siku yenye vitu vidogo vinavyotuliza moyo wako.", "Heri ya kuzaliwa."],
            ["Unafanya siku za kawaida ziwe nzuri kwa kuwa wewe.", "Mwaka huu ukurudishie mwanga huo."],
        ],
        "formal": [
            ["Pokea salamu zangu za dhati katika siku yako ya kuzaliwa.", "Mwaka ujao ukuletee mafanikio, afya na furaha."],
            ["Nakutakia heri ya kuzaliwa na mwaka wenye mafanikio.", "Ujae ustawi na sababu nyingi za kusherehekea."],
            ["Katika siku hii maalum, natoa pongezi zangu za dhati.", "Mwaka unaokuja ukuletee mafanikio na utimilifu wa kudumu."],
        ],
        "creative": [
            ["Kama siku za kuzaliwa ni rangi, leo ingekuwa kila aina ya furaha.", "Paka mwaka huu rangi unazozipenda zaidi."],
            ["Chukulia ujumbe huu kama kofia ndogo ya sherehe.", "Vaa mwaka wako kwa fahari."],
            ["Mwaka ni ukurasa mtupu na wewe unashikilia kalamu.", "Andika jambo la kusoma na uanze leo."],
        ],
    },
    "fr": {
        "romantic": [
            ["Tu es la raison pour laquelle mes journées ordinaires ressemblent à des fêtes.", "Que cette journée t'entoure d'autant d'amour que tu m'en donnes.", "Joyeux anniversaire, mon amour."],
            ["Chaque année à tes côtés est ma préférée.", "Que les bougies te rappellent à quel point tu illumines ma vie.", "Je t'aime infiniment."],
            ["Si je pouvais t'offrir un miroir, tu verrais combien tu es merveilleux.", "Aujourd'hui, je te célèbre de tout mon cœur.", "Joyeux anniversaire, mon chéri."],
        ],
        "emotional": [
            ["Certaines personnes rendent le monde plus doux simplement en y vivant, et tu en fais partie.", "Je suis si heureux de te connaître.", "Joyeux anniversaire."],
            ["Les années passent, mais mon admiration pour toi ne cesse de grandir.", "Merci pour tout ce que tu apportes à ma vie.", "Passe une belle journée d'anniversaire."],
            ["Aujourd'hui mon cœur déborde parce que tu es né.", "Que cette année te rende tout le bien que tu offres.", "Joyeux anniversaire."],
        ],
        "funny": [
            ["Joyeux anniversaire ! Tu ne vieillis pas, tu deviens une édition limitée.", "Garde-moi une part de gâteau à la hauteur de mon enthousiasme."],
            ["Tu as atteint l'âge où les bougies coûtent plus cher que le gâteau.", "Joyeux anniversaire et profite bien de ta journée."],
            ["Un autre tour du soleil et toujours pas de mode d'emploi.", "Tu t'en sors très bien. Va chercher la plus grosse part maintenant."],
        ],
        "inspirational": [
            ["Que cette nouvelle année t'ouvre des portes insoupçonnées.", "Tu as tout ce qu'il faut pour la rendre magnifique.", "Joyeux anniversaire."],
            ["À une autre année de rêves plus grands et de lumière plus vive.", "J'ai hâte de voir ce que tu construiras.", "Joyeux anniversaire."],
            ["Les plus beaux chapitres de ton histoire restent à écrire.", "Que cette année soit pleine de courage et de belles surprises."],
        ],
        "religious": [
            ["Que le Seigneur te bénisse et te garde en ce jour spécial.", "Que cette année soit remplie de grâce, de paix et de joie.", "Joyeux anniversaire."],
            ["Je remercie Dieu pour le cadeau de ta vie.", "Que Sa faveur t'accompagne partout.", "Joyeux anniversaire et mille bénédictions."],
            ["Que ton anniversaire soit entouré de prières et d'amour.", "Que la foi te guide doucement toute l'année."],
        ],
        "short": [
            ["Joyeux anniversaire ! Je te souhaite une merveilleuse journée."],
            ["Joyeux anniversaire ! Que cette année te soit douce."],
            ["Joyeux anniversaire ! Ravi que tu sois né."],
        ],
        "heartfelt": [
            ["Tu comptes plus pour moi que je ne saurais le dire.", "Que cette journée soit aussi chaleureuse que tu rends les autres.", "Joyeux anniversaire."],
            ["Je suis reconnaissant que nos chemins se soient croisés.", "Je te souhaite un anniversaire rempli de petites joies.", "Joyeux anniversaire."],
            ["Tu rends les jours ordinaires plus lumineux en étant toi.", "Que cette année te rende cette lumière."],
        ],
        "formal": [
            ["Veuillez accepter mes vœux les plus chaleureux à l'occasion de votre anniversaire.", "Que l'année à venir vous apporte succès, santé et bonheur."],
            ["Je vous souhaite un très joyeux anniversaire et une année enrichissante.", "Qu'elle soit remplie de prospérité et de belles occasions."],
            ["En cette occasion spéciale, je vous adresse mes sincères félicitations.", "Que l'année à venir vous apporte réussite et épanouissement."],
        ],
        "creative": [
            ["Si les anniversaires étaient des couleurs, aujourd'hui serait toutes les teintes du bonheur.", "Peins cette année des couleurs que tu aimes."],
            ["Considère ce message comme un petit chapeau de fête.", "Porte ton année avec fierté."],
            ["Une année est une page blanche et tu tiens la plume.", "Écris quelque chose de beau et commence aujourd'hui."],
        ],
    },
    "es": {
        "romantic": [
            ["Eres la razón por la que mis días comunes parecen celebraciones.", "Que hoy te envuelva tanto amor como el que me das.", "Feliz cumpleaños, mi amor."],
            ["Cada año a tu lado es mi año favorito.", "Que las velas te recuerden cuánto iluminas mi vida.", "Te quiero sin fin."],
            ["Si pudiera regalarte un espejo, verías lo maravilloso que eres.", "Hoy te celebro con todo mi corazón.", "Feliz cumpleaños, cariño."],
        ],
        "emotional": [
            ["Algunas personas hacen el mundo más amable solo con existir, y tú eres una de ellas.", "Me siento muy afortunado de conocerte.", "Feliz cumpleaños."],
            ["Los años pasan, pero mi cariño por ti solo crece.", "Gracias por todo lo que aportas a mi vida.", "Que tengas un hermoso cumpleaños."],
            ["Hoy mi corazón está lleno porque naciste.", "Que este año te devuelva todo el bien que das.", "Feliz cumpleaños."],
        ],
        "funny": [
            ["¡Feliz cumpleaños! No envejeces, te vuelves edición limitada.", "Guárdame un trozo de tarta del tamaño de mi entusiasmo."],
            ["Ya estás en la edad en que las velas cuestan más que la tarta.", "Feliz cumpleaños y disfruta tu gran día."],
            ["Otra vuelta al sol y todavía sin manual de instrucciones.", "Lo estás haciendo genial. Ve a por el trozo más grande."],
        ],
        "inspirational": [
            ["Que este nuevo año te abra puertas que ni imaginabas.", "Tienes todo para hacerlo maravilloso.", "Feliz cumpleaños."],
            ["Por otro año de soñar más alto y brillar más fuerte.", "Me muero por ver lo que construirás.", "Feliz cumpleaños."],
            ["Los mejores capítulos de tu historia aún están por escribir.", "Que este año sea de valentía y sorpresas hermosas."],
        ],
        "religious": [
            ["Que el Señor te bendiga y te guarde en este día especial.", "Que este año esté lleno de gracia, paz y alegría.", "Feliz cumpleaños."],
            ["Doy gracias a Dios por el regalo de tu vida.", "Que Su favor te acompañe en todo.", "Feliz cumpleaños y muchas bendiciones."],
            ["Que tu cumpleaños esté rodeado de oración y de amor.", "Que la fe te guíe durante todo el año."],
        ],
        "short": [
            ["¡Feliz cumpleaños! Te deseo un día maravilloso."],
            ["¡Feliz cumpleaños! Que este año sea bueno contigo."],
            ["¡Feliz cumpleaños! Qué alegría que hayas nacido."],
        ],
        "heartfelt": [
            ["Significas más para mí de lo que puedo expresar.", "Ojalá hoy sea tan cálido como haces sentir a los demás.", "Feliz cumpleaños."],
            ["Me alegra tanto que nuestros caminos se cruzaran.", "Te deseo un cumpleaños lleno de pequeñas alegrías.", "Feliz cumpleaños."],
            ["Haces los días comunes más brillantes con solo ser tú.", "Que este año te devuelva esa luz."],
        ],
        "formal": [
            ["Reciba usted mis más cordiales felicitaciones en su cumpleaños.", "Que el año venidero le traiga éxito, salud y felicidad."],
            ["Le deseo un muy feliz cumpleaños y un año muy provechoso.", "Que esté lleno de prosperidad y motivos para celebrar."],
            ["En esta ocasión especial, le envío mi más sincera enhorabuena.", "Que el próximo año le traiga grandes logros."],
        ],
        "creative": [
            ["Si los cumpleaños fueran colores, hoy sería todos los tonos de la felicidad.", "Pinta este año con los colores que más quieras."],
            ["Toma este mensaje como un pequeño gorro de fiesta.", "Lleva tu año con orgullo."],
            ["Un año es una página en blanco y tú tienes la pluma.", "Escribe algo que valga la pena y empieza hoy."],
        ],
    },
    "ar": {
        "romantic": [
            ["أنت السبب في أن تبدو أيامي العادية كأنها احتفالات.", "أتمنى أن يغمرك اليوم بحب بقدر ما تمنحني.", "عيد ميلاد سعيد يا حبيبي."],
            ["كل عام معك هو عامي المفضل.", "لتذكّرك الشموع بمدى إشراقك في حياتي.", "أحبك بلا حدود."],
            ["لو استطعت إهداءك مرآة لرأيت كم أنت رائع.", "اليوم أحتفل بك بكل قلبي.", "عيد ميلاد سعيد يا حبيبي."],
        ],
        "emotional": [
            ["بعض الناس يجعلون العالم ألطف بمجرد وجودهم، وأنت واحد منهم.", "أنا ممتن جداً لمعرفتك.", "عيد ميلاد سعيد."],
            ["تمر السنوات، لكن تقديري لك يزداد فقط.", "شكراً لكل ما تضيفه إلى حياتي.", "أتمنى لك عيد ميلاد جميلاً."],
            ["اليوم قلبي ممتلئ لأنك وُلدت.", "أتمنى أن يعيد لك هذا العام كل الخير الذي تمنحه.", "عيد ميلاد سعيد."],
        ],
        "funny": [
            ["عيد ميلاد سعيد! أنت لا تكبر، بل تصبح إصداراً محدوداً.", "احفظ لي قطعة من الكعكة بحجم حماسي."],
            ["لقد بلغت العمر الذي تصبح فيه الشموع أغلى من الكعكة.", "عيد ميلاد سعيد واستمتع بيومك المهم."],
            ["دورة أخرى حول الشمس وما زال لا يوجد دليل استخدام.", "أنت تبلي حسناً. اذهب الآن وخذ أكبر قطعة من الكعكة."],
        ],
        "inspirational": [
            ["أتمنى أن يفتح لك هذا العام أبواباً لم تكن تتخيلها.", "لديك كل ما تحتاجه لتصنعه رائعاً.", "عيد ميلاد سعيد."],
            ["إلى عام آخر من الحلم الأكبر والإشراق الأقوى.", "لا أطيق الانتظار لأرى ما ستبنيه.", "عيد ميلاد سعيد."],
            ["أجمل فصول قصتك لم تُكتب بعد.", "ليكن هذا العام مليئاً بالشجاعة والمفاجآت الجميلة."],
        ],
        "religious": [
            ["باركك الرب وحفظك في هذا اليوم المميز.", "ليكن هذا العام مليئاً بالنعمة والسلام والفرح.", "عيد ميلاد سعيد."],
            ["أشكر الله على هدية حياتك.", "لتتبعك نعمته في كل ما تفعل.", "عيد ميلاد سعيد وبركات كثيرة."],
            ["ليكن عيد ميلادك محاطاً بالدعاء والمحبة.", "ليرشدك الإيمان بلطف خلال العام القادم."],
        ],
        "short": [
            ["عيد ميلاد سعيد! أتمنى لك يوماً رائعاً."],
            ["عيد ميلاد سعيد! ليكن هذا العام لطيفاً معك."],
            ["عيد ميلاد سعيد! يسعدني أنك وُلدت."],
        ],
        "heartfelt": [
            ["أنت تعني لي أكثر مما يمكن أن أعبر عنه.", "أتمنى أن يكون اليوم دافئاً كما تجعل الآخرين يشعرون.", "عيد ميلاد سعيد."],
            ["أنا ممتن لأن طرقنا تقاطعت.", "أتمنى لك عيد ميلاد مليئاً بالتفاصيل الصغيرة التي تريح قلبك.", "عيد ميلاد سعيد."],
            ["تجعل الأيام العادية أكثر إشراقاً بمجرد كونك أنت.", "ليعد لك هذا العام ذلك الإشراق."],
        ],
        "formal": [
            ["تقبل أطيب تمنياتي بمناسبة عيد ميلادك.", "ليجلب لك العام القادم مزيداً من النجاح والصحة والسعادة."],
            ["أتمنى لك عيد ميلاداً سعيداً جداً وعاماً مثمراً.", "ليكن مليئاً بالازدهار والكثير من أسباب الاحتفال."],
            ["في هذه المناسبة الخاصة، أتقدم لك بخالص التهاني.", "ليجلب لك العام القادم كل النجاح والرضا الدائم."],
        ],
        "creative": [
            ["لو كانت أعياد الميلاد ألواناً، لكان اليوم كل درجات السعادة.", "لوّن هذا العام بالألوان التي تحبها أكثر."],
            ["اعتبر هذه الرسالة قبعة صغيرة لحفلك.", "ارتدِ عامك بفخر."],
            ["العام صفحة بيضاء وأنت تحمل القلم.", "اكتب شيئاً يستحق القراءة وابدأ اليوم."],
        ],
    },
}
