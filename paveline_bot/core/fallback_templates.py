from typing import Dict, List, Tuple

# Translated templates for English, Kiswahili, French, Spanish and Arabic
RELATIONSHIPS = {
    "wife": {"en": "my dear wife", "sw": "mke wangu mpendwa", "fr": "ma chère épouse", "es": "mi querida esposa", "ar": "زوجتي العزيزة"},
    "husband": {"en": "my dear husband", "sw": "mume wangu mpendwa", "fr": "mon cher époux", "es": "mi querido esposo", "ar": "زوجي العزيز"},
    "girlfriend": {"en": "my love", "sw": "mpenzi wangu", "fr": "mon amour", "es": "mi amor", "ar": "حبيبتي"},
    "boyfriend": {"en": "my love", "sw": "mpenzi wangu", "fr": "mon amour", "es": "mi amor", "ar": "حبيبي"},
    "friend": {"en": "my dear friend", "sw": "rafiki yangu mpendwa", "fr": "mon cher ami", "es": "mi querido amigo", "ar": "صديقي العزيز"},
    "mother": {"en": "Mom", "sw": "Mama", "fr": "Maman", "es": "Mamá", "ar": "أمي"},
    "father": {"en": "Dad", "sw": "Baba", "fr": "Papa", "es": "Papá", "ar": "أبي"},
    "sister": {"en": "my dear sister", "sw": "dada yangu mpendwa", "fr": "ma chère sœur", "es": "mi querida hermana", "ar": "أختي العزيزة"},
    "brother": {"en": "my dear brother", "sw": "kaka yangu mpendwa", "fr": "mon cher frère", "es": "mi querido hermano", "ar": "أخي العزيز"},
    "son": {"en": "my dear son", "sw": "mwanangu mpendwa", "fr": "mon cher fils", "es": "mi querido hijo", "ar": "ابني العزيز"},
    "daughter": {"en": "my dear daughter", "sw": "binti yangu mpendwa", "fr": "ma chère fille", "es": "mi querida hija", "ar": "ابنتي العزيزة"},
    "relative": {"en": "dearest one", "sw": "ndugu yangu mpendwa", "fr": "cher proche", "es": "querido familiar", "ar": "عزيزي القريب"},
    "colleague": {"en": "my wonderful colleague", "sw": "mwenzangu mpendwa", "fr": "cher collègue", "es": "querido colega", "ar": "زميلي العزيز"},
    "teacher": {"en": "my dear teacher", "sw": "mwalimu wangu mpendwa", "fr": "cher professeur", "es": "querido profesor", "ar": "أستاذي العزيز"},
    "other": {"en": "my dear friend", "sw": "rafiki yangu mpendwa", "fr": "mon cher ami", "es": "mi querido amigo", "ar": "صديقي العزيز"},
}

HELLO = {
    "en": "Happy birthday",
    "sw": "Heri ya kuzaliwa",
    "fr": "Joyeux anniversaire",
    "es": "Feliz cumpleaños",
    "ar": "عيد ميلاد سعيد",
}

SIGNOFF = {
    "en": "With love",
    "sw": "Kwa upendo",
    "fr": "Avec affection",
    "es": "Con cariño",
    "ar": "مع كل الحب",
}

TEMPLATES = {
    "en": {
        "heartfelt": ["Wishing you a birthday filled with love and happiness. You make the world a better place.", 
                      "You mean so much to me. I hope this new year brings you joy and peace.", 
                      "So grateful to have you in my life. May your birthday be as wonderful as you are."],
        "romantic": ["Every day with you is a gift. Today we celebrate you with all my love.", 
                     "You make ordinary moments extraordinary. Happy birthday, my love.", 
                     "My heart is full of love for you on your special day and always."],
        "funny": ["Another trip around the sun and still looking fabulous! Enjoy your special day!", 
                  "You're not getting older, you're just increasing in value like fine wine. Happy birthday!", 
                  "Cake, candles and fun - you deserve all of them today!"],
        "formal": ["Wishing you a very happy birthday and a year of continued success and good health.", 
                   "May this birthday mark the beginning of another wonderful year for you.", 
                   "Best wishes on your birthday and for the year ahead."],
        "religious": ["May God bless you with health, happiness, and peace on your birthday and always.", 
                      "I thank God for you. May He grant you many more blessed years.", 
                      "May the Lord's blessings be with you today and throughout the coming year."],
    },
    "sw": {
        "heartfelt": ["Nakutakia heri ya kuzaliwa iliyojaa furaha na upendo. Unafanya dunia kuwa bora zaidi.", 
                      "Unamaanisha mengi kwangu. Nakutakia mwaka huu mpya ujae furaha na amani.", 
                      "Nina shukrani kubwa kuwa nawe katika maisha yangu. Heri ya kuzaliwa."],
        "romantic": ["Kila siku nawe ni zawadi. Leo nakuadhimisha kwa upendo wangu wote.", 
                     "Unafanya mambo ya kawaida yawe ya ajabu. Heri ya kuzaliwa, mpenzi wangu.", 
                     "Moyo wangu umejaa upendo kwako katika siku hii maalum na daima."],
        "funny": ["Mzunguko mwingine wa jua na bado unaonekana mzuri sana! Furahia siku yako maalum!", 
                  "Haujazeeka, unaendelea kuwa bora kama divai nzuri. Heri ya kuzaliwa!", 
                  "Keki, mishumaa na furaha - unastahili vyote leo!"],
        "formal": ["Nakutakia heri ya kuzaliwa na mwaka mwingine wa mafanikio na afya njema.", 
                   "Heri ya kuzaliwa na baraka nyingi kwa mwaka unaokuja.", 
                   "Nawatakia kila la heri katika siku yako ya kuzaliwa na mwaka ujao."],
        "religious": ["Mungu akubariki kwa afya njema, furaha na amani siku ya kuzaliwa na daima.", 
                      "Namshukuru Mungu kwa ajili yako. Akubariki kwa miaka mingi zaidi.", 
                      "Baraka za Bwana ziwe nawe leo na katika mwaka wote ujao."],
    },
    "fr": {
        "heartfelt": ["Je te souhaite un joyeux anniversaire rempli d'amour et de bonheur. Tu rends le monde meilleur.", 
                      "Tu comptes beaucoup pour moi. Que cette nouvelle année t'apporte joie et sérénité.", 
                      "Je suis si heureux de t'avoir dans ma vie. Joyeux anniversaire !"],
        "romantic": ["Chaque jour à tes côtés est un cadeau. Aujourd'hui je te célèbre avec tout mon amour.", 
                     "Tu fais des moments ordinaires des moments extraordinaires. Joyeux anniversaire, mon amour.", 
                     "Mon cœur déborde d'amour pour toi en ce jour spécial et toujours."],
        "funny": ["Un nouveau tour du soleil et tu es toujours aussi rayonnant ! Profite de ta journée spéciale !", 
                  "Tu ne vieillis pas, tu prends de la valeur comme un bon vin. Joyeux anniversaire !", 
                  "Gâteau, bougies, amusement - tu mérites tout ça aujourd'hui !"],
        "formal": ["Je te souhaite un très joyeux anniversaire et une année pleine de succès et de bonne santé.", 
                   "Que cet anniversaire marque le début d'une nouvelle année merveilleuse.", 
                   "Meilleurs vœux pour ton anniversaire et pour l'année à venir."],
        "religious": ["Que Dieu te bénisse de santé, de bonheur et de paix en ce jour et toujours.", 
                      "Je remercie Dieu pour toi. Qu'Il te donne encore de nombreuses années bénies.", 
                      "Que les bénédictions du Seigneur t'accompagnent aujourd'hui et toute l'année."],
    },
    "es": {
        "heartfelt": ["Feliz cumpleaños lleno de amor y felicidad. Haces el mundo mejor.", 
                      "Significas mucho para mí. Que este nuevo año te traiga alegría y paz.", 
                      "Me alegro tanto de tenerte en mi vida. Feliz cumpleaños."],
        "romantic": ["Cada día contigo es un regalo. Hoy te celebro con todo mi amor.", 
                     "Haces de los momentos ordinarios momentos extraordinarios. Feliz cumpleaños, mi amor.", 
                     "Mi corazón rebosa de amor por ti en este día especial y siempre."],
        "funny": ["Otra vuelta al sol y sigues tan radiante como siempre. ¡Disfruta tu día especial!", 
                  "No envejeces, te mejoras con el tiempo como un buen vino. ¡Feliz cumpleaños!", 
                  "Pastel, velas y diversión - ¡te lo mereces todo hoy!"],
        "formal": ["Feliz cumpleaños y que el año que viene sea de éxito y buena salud.", 
                   "Que este cumpleaños marque el inicio de un año maravilloso para ti.", 
                   "Mis mejores deseos en tu cumpleaños y para el año venidero."],
        "religious": ["Que Dios te bendiga con salud, felicidad y paz en tu cumpleaños y siempre.", 
                      "Doy gracias a Dios por ti. Que te conceda muchos años más de bendiciones.", 
                      "Que las bendiciones del Señor te acompañen hoy y durante todo el año."],
    },
    "ar": {
        "heartfelt": ["عيد ميلاد سعيد مليء بالحب والسعادة. أنت تجعل العالم مكانًا أفضل.", 
                      "أنت تعني لي الكثير. أتمنى أن يجلب لك هذا العام الجديد السعادة والسلام.", 
                      "أنا ممتن جدًا لوجودك في حياتي. عيد ميلاد سعيد."],
        "romantic": ["كل يوم معك هو هدية. اليوم أحتفل بك بكل حبي.", 
                     "تجعل اللحظات العادية لحظات استثنائية. عيد ميلاد سعيد يا حبيبي.", 
                     "قلبي ممتلئ بالحب لك في هذا اليوم المميز ودائمًا."],
        "funny": ["دورة أخرى حول الشمس وما زلت تبدو رائعًا. استمتع بيومك المميز!", 
                  "أنت لا تكبر، أنت تتحسن مع الوقت مثل النبيذ الجيد. عيد ميلاد سعيد!", 
                  "كعكة، شموع، ومرح - تستحق كل ذلك اليوم!"],
        "formal": ["أتمنى لك عيد ميلاد سعيدًا وعامًا مليئًا بالنجاح والصحة الجيدة.", 
                   "ليكن عيد ميلادك هذا بداية عام رائع آخر لك.", 
                   "أطيب التمنيات بعيد ميلادك وللعام القادم."],
        "religious": ["باركك الله بالصحة والسعادة والسلام في عيد ميلادك ودائمًا.", 
                      "أشكر الله من أجلك. باركك الله بالعديد من السنوات المباركة.", 
                      "لتكن بركات الرب معك اليوم وخلال العام القادم."],
    },
}


def generate_fallback_wish(
    name: str = "",
    relationship: str = "friend",
    language: str = "en",
    style: str = "heartfelt",
    sender: str = "",
    extra: str = "",
    variation: int = 0,
) -> str:
    lang = language if language in HELLO else "en"
    rel = relationship if relationship in RELATIONSHIPS else "friend"
    sty = style if style in TEMPLATES[lang] else "heartfelt"
    
    templates = TEMPLATES[lang][sty]
    idx = variation % len(templates) if templates else 0
    base = templates[idx]
    
    # Simple composition
    greeting = f"{HELLO[lang]}, {name or RELATIONSHIPS[rel][lang]}!"
    wish = base
    signoff = f"{SIGNOFF[lang]}, {sender}" if sender else SIGNOFF[lang]
    
    parts = [greeting, wish, signoff]
    return " ".join(p for p in parts)
