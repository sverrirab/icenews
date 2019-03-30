# -*- encoding: utf-8 -*-
from reynir import Reynir
from reynir.bintokenizer import tokenize, TOK
from collections import defaultdict

_NLP = Reynir()
_INDENT = " " * 8
_VERBOSE = 1

_DEFAULT_IMPORTANT_THRESHOLD = 0.7
_DEFAULT_MAX_TOKENS = 100
_DEFAULT_MAX_WORDS = 30
_MIN_WORD_COUNT = 10

_UNCLASSIFIED_WEIGHT = 0.25
_UNCLASSIFIED_NAME = 2.5
_NORMAL_WEIGHT = 0.5
_KVKHK_WEIGHT = 0.75
_NUMBER_WEIGHT = 1.5
_DATE_WEIGHT = 3.0
_TITLE_WEIGHT = 3.0
_LOCATION_WEIGHT = 4.0
_ENTITY_WEIGHT = 5.0

_STOP_CONCEPTS = {
    "á",
    "að",
    "ekki",
    "fara",
    "fer",
    "fyrir",
    "get",
    "hafa",
    "í",
    "koma",
    "með",
    "og",
    "segja",
    "taka",
    "um",
    "var",
    "ver",
    "vera",
    "verða",
    "verður",
    "þannig",
    "þar",
    "úr",
    "sjá",
    "við",
    "því",
    "eiga",
    "ær",
    "haf",
    "húnn",
    "tak",
    "til",
    "sem",

}


def get_lemma(token):
    result = set()
    for val in token.val:
        result.add(val.stofn)
    return result


def simplify_val(vals):
    """
    Remove stopwords, personal pronouns etc
    Reduce the number of results to the first in each "class" - e.g. one ao, one lo etc
    :param vals:
    :return:
    """
    result = {}
    for val in vals:
        unique = "{}/{}".format(val.ordfl, val.fl)
        if unique in result:
            if _VERBOSE > 2:
                print("simplify_val - ignoring:", val)
            continue
        if val.ordfl in ["fs", "fn", "uh", "pfn", "st"]:
            continue
        elif val.stofn in _STOP_CONCEPTS:
            continue
        result[unique] = val

    return result.values()


def remove_hyphen(text):
    return text.replace("-", "")


def is_name(text):
    """
    Checks if text sounds like a name or abbreviation (title or upper case).
    :param text: the text to check.
    :return: True if it might be a name.
    """
    return text.istitle() or text.isupper()


class Concept(object):
    def __init__(self, concept, weight=1.0):
        self.concept = concept
        self.weight = weight


class Concepts(object):
    def __init__(self):
        self._concepts = defaultdict(int)
        self._count = 0

    def extract(self, text, max_tokens=_DEFAULT_MAX_TOKENS):
        tokens = 0
        for sent in text.split("\n"):
            if _VERBOSE > 1:
                print("Parsing sentence:", sent)

            unclassified_names = []

            for t in tokenize(sent):
                add_unclassified_name = False
                if _VERBOSE > 2:
                    print("Parsing token:", t)
                if t.kind > TOK.UNKNOWN:
                    # ignoring end/start line/paragraph etc
                    pass
                elif t.kind == TOK.PUNCTUATION:
                    pass
                elif t.kind in [TOK.DATE, TOK.YEAR, TOK.TIME]:
                    if _VERBOSE > 1:
                        print(_INDENT, "DATE:", t)
                    self.add(t.txt, _DATE_WEIGHT)
                elif t.kind in [TOK.NUMBER, TOK.ORDINAL, TOK.AMOUNT, TOK.PERCENT]:
                    if _VERBOSE > 1:
                        print(_INDENT, "NUMBER:", t)
                    self.add(t.txt, _NUMBER_WEIGHT)
                elif t.kind == TOK.PERSON:
                    if _VERBOSE > 1:
                        print(_INDENT, "PERSON:", t)
                    self.add(t.val[0].name, _ENTITY_WEIGHT)
                elif t.kind == TOK.WORD:
                    if _VERBOSE > 1:
                        print(_INDENT, "WORD:", t.txt)

                    if not t.val:
                        if is_name(t.txt):
                            add_unclassified_name = True
                        else:
                            if _VERBOSE > 1:
                                print(_INDENT, "UNCLASSIFIED:", t.txt)
                            self.add(t.txt, _UNCLASSIFIED_WEIGHT)
                    else:
                        self._add_token_concepts(t)
                else:
                    if _VERBOSE > -1:
                        print(_INDENT, "UNHANDLED:", t)

                if add_unclassified_name:
                    unclassified_names.append(t.txt)
                else:
                    self._handle_unclassified_names(unclassified_names)
                tokens += 1
                if tokens > max_tokens:
                    break

            # If the sentence ends with unclassified names.
            self._handle_unclassified_names(unclassified_names)

    def _handle_unclassified_names(self, names):
        if len(names) > 0:
            full = " ".join(names)
            if _VERBOSE > 1:
                print(_INDENT, "UNCLASSIFIED NAMES:", full)

            self.add(full, _UNCLASSIFIED_NAME)
            names.clear()

    def _add_token_concepts(self, t):
        if _VERBOSE > 2:
            for val in t.val:
                print("   VAL:", val.fl, val)
        simplified = simplify_val(t.val)

        if len(simplified) == 0:
            if _VERBOSE > 1:
                print(_INDENT * 2, "Ignored", t.txt)
            return

        for val in simplified:
            stofn = remove_hyphen(val.stofn)
            if val.fl == "lönd":
                weight = _LOCATION_WEIGHT
            elif is_name(stofn):
                weight = _TITLE_WEIGHT
            elif val.ordfl in ["kk", "hk", "kvk"]:
                if val.fl in ["fyr"]:
                    weight = _ENTITY_WEIGHT
                else:
                    weight = _KVKHK_WEIGHT
            else:
                weight = _NORMAL_WEIGHT
            self.add(stofn, weight / len(simplified))

    def add(self, concept, weight=1.0):
        self._count += 1
        if _VERBOSE > 1:
            print("adding weight", concept, weight)
        self._concepts[concept] += weight

    def count(self):
        self._count += 1

    def important(self, max_count=_DEFAULT_MAX_WORDS, threshold=_DEFAULT_IMPORTANT_THRESHOLD):
        result = []
        total = sum(self._concepts.values())
        cap = total * threshold
        running = 0.0
        for c in sorted(self._concepts, key=self._concepts.get, reverse=True)[:max_count]:
            w = self._concepts[c]
            if running > cap:
                if len(result) > _MIN_WORD_COUNT:
                    break
            running += w
            result.append(c)
        return result

    def report(self, max_count=_DEFAULT_MAX_WORDS, threshold=_DEFAULT_IMPORTANT_THRESHOLD):
        print("Concepts report for {} items:".format(self._count))
        print("Sum:", sum(self._concepts.values()))
        print("Len:", len(self._concepts))
        print(self._concepts)
        for c in self.important(max_count, threshold):
            w = self._concepts[c]
            print("  {:.2f} {}".format(w, c))
        print(" -" * 20)


T1 = """Höfða mál vegna vopnasölu til Sádi-Arabíu
Mannréttindasamtök á Ítalíu, Þýskalandi og Jemen hafa höfðað mál á hendur ítölskum yfirvöldum og evrópskum vopnaframleiðendum fyrir meinta aðild að loftárásum Sádi-Araba og bandamanna þeirra í Jemen. Þar berjast þeir gegn Houthi uppreisnarmönnum. Þúsundir almennra borgara hefur fallið í árásunum undanfarin þrjú ár. Mannréttindasamtökin European Center for Constitutional and Human Rights (ECCHR) í Berlín, Mwatana Organisation for Human Rights í Jemen og Reta Italiana per il Disarmo á Ítalíu lögðu fram sameiginlega ákæru til saksóknara í Róm í gær. Hún beinist gegn embættismönnum í utanríkisráðuneyti Ítalíu og æðstu stjórnendum útibús þýsku vopnasamsteypunnar Rheinmetall á Ítalíu, RWM Italia.
Greint er frá málinu á vef Guardian. Þar segir að tilraunir mannréttindasamtaka í Bretlandi og víðar til fá embættismenn og vopnaframleiðendur sakfellda, hafi ekki borið árangur þar sem ákærurnar hafi náð yfir of breitt svið. Ákæran sem var lögð fram í gær er vegna sprengjuárásar 8. október 2016. Í henni var sex manna fjölskylda drepin, þar af fjögur börn. Forsvarsfólk mannréttindasamtakanna vonar að með því að leggja fram kæru vegna eins ákveðins máls séu meiri líkur á sakfellingu.
Sprengjuleifar fundust á vettvangi þar sem árásin var gerð árið 2016. Á þeim er númer sem gefur til kynna að þær hafi verið framleiddar í júní 2014 hjá RWM Itala. Linde Bryn, hollenskur lögfræðingur sem áður starfaði í Kósóvó, segir að málið sé sérstakt þar sem merktar sprengjuleifar hafi fundist á vettvangi. „Þetta mál er táknrænt þar sem það snertir ekki aðeins embættismenn og yfirmenn vopnaframleiðanda á Ítalíu. Það snertir almennt ábyrgð ríkisstjórna í Evrópu og evrópska vopnaframleiðendur og hver þeirra ábyrgð er á afleiðingum útflutnings vopna sem eru notuð af Sádi-Aröbum og bandamönnum þeirra,“ segir hún.
Greint var frá því í fréttaskýringaþættinum Kveik í febrúar síðastliðnum að flugvélar á vegum íslenska flugfélagsins Atlanta hafi á undanförnum árum flutt vopn til Sádi-Arabíu. Til þess fengu þau heimild frá Samgöngustofu. Vopnin gætu hafa verið borist til stríðshrjáðra landa eins og Jemens og Sýrlands. Samkvæmt vopnasáttmála Sameinuðu þjóðanna frá árinu 2014 er bannað að afhenda bardagasveitum, sem brjóta gegn stríðsrétti, vopn. Tveir þingmenn Vinstri grænna og þingmenn stjórnarandstöðuflokka óskuðu 11. apríl síðastliðinn eftir skýrslu frá utanríkisráðherra um það hvort íslenska ríkið hafi brotið gegn banni Öryggisráðs Sameinuðu þjóðanna um vopnaflutning."""

T2 = """
Stjórnarslitin í júní 2017 urðu til þess að skólpmál í Mývatnssveit tóku nýja stefnu og nú er gerbreytt og mun ódýrari umbótaáætlun nær tilbúin. Sveitarstjóri Skútustaðahrepps segir að stefnt sé að samningum við ríkisvaldið í næstu viku. Umbótaáætlun í skólpmálum hefur verið í vinnslu hjá Skútustaðahreppi frá því snemma á síðasta ári. Upphaflega var gert ráð fyrir lokuðu kerfi með hreinsistöðvum sem átti að kosta um einn milljarð króna. 
Ríkisstjórnin sprakk daginn fyrir fund um skólpmálin
Þorsteinn Gunnarsson, sveitarstjóri, sagði á Morgunvaktinni á Rás 1 í morgun, að þannig áætlun hafi verið nánast tilbúin í júní 2017. „Við áttum þá í samningaviðræðum við ríkið. Þetta var á fimmtudagskvöldi og við áttum bókaðan fund með umhverfisráðherra og fjármálaráðherra á mánudeginum á eftir. Og við vorum mjög bjartsýn og töldum að það eina sem myndi koma í veg fyrir að við myndum klára samningaviðræður við ríkið, væri ef ríkisstjórnin myndi springa. Og það gerðist þetta sama kvöld."
Allt fór á byrjunarreit og ný hugmynd fæddist
En þetta var lán í óláni, segir Þorsteinn, því að allt fór á byrjunarreit og ný hugmynd, sem nú er unnið út frá, fæddist. Hún felst í stuttu máli í því að safna saman úrgangi úr salernum í Mývatnssveit og nýta til landgræðslu. „Það sem fer í salernin, sem er svartvatnið, það fer í lokaða tanka. Það sem kemur úr sturtum, vöskum og annað, heldur bara áfram í gegnum rotþróa siturbeð. Síðan kemur tankbíll, dælir svartvatninu úr þessum lokuðu tönkum og fer með það upp á Hólasand þar sem verður reistur safntankur og grófhreinsistöð.  Og svartvatnið er þetta næringarríka efni sem verður síðan notað til uppgræðslu á Hólasandi." 
Vonandi gengið frá samingum við ríkið eftir helgi
Heilbrigðiseftirlitið hefur nú samþykkt þessa nýju áætlun og aftur þurfa Mývetningar að treysta á ríkisstjórnina. „Og við erum núna á lokasprettinum í samningaviðræðum við ríkið. Og það verður vonandi gengið frá því ekki seinna en í næstu viku. Þannig að það yrðu ansi stórar fréttir."""

T3 = """
Ef hægt verður að vinna orku úr borholum við Eldvörp á Reykjanesi, gætu verið lagðir allt að 7.000 fermetra stórir borteigar. Nú stenda yfir rannsóknarboranir á vegum HS Orku. Samkvæmt framkvæmdaleyfi til þeirra er heimild til að gera fimm borteiga sem eru 4.200 til 5.700 fermetrar hver. Ekki er víst hvort þeir verði allir lagðir. Í umhverfismatsskýrslu frá VSÓ ráðgjöf frá 2014 segir að áætlað rask á hrauni vegna framkvæmda við rannsóknarboranir sé 23.000 fermetrar verði öll borplönin lögð. Líklegra sé þó að rask verði á um 15.000 fermetrum.
Hugmyndir um fleiri en eina holu á borteig
Ein hola er boruð á hverjum teig í rannsóknaborunum en ef þær bera góðan árangur og orkuvinnsla hefst gæti svo farið að HS Orka vilji hafa tvær til þrjár borholur á teig. Þeir borteigar verða 3.500 til 7.000 fermetrar, að sögn Ásgeirs Margeirssonar, forstjóra HS Orku. „Stærð fer eftir því hve margar holur eru boraðar frá sama teig. Með því að hafa fleiri en eina holu á borteig, gjarnan tvær til þrjár, er unnt að fækka borteigum. Með því móti minnka umhverfisáhrif við gerð borteiga auk þess sem vegagerð verður minni og gufulagnir einnig ef til orkunýtingar kemur. Verkefnið nú heimilar allt að fimm borteiga og er ráðgert að bora í fyrstu tvær til þrjár rannsóknarholur,“ segir hann. Ekki sé hægt að segja til um það núna hvort gerðir verði fimm borteigar. Boruð sé ein hola í einu og niðurstöður rannsókna á henni ráði því hvert framhaldið verði.
HS Orka er með framkvæmdaleyfi frá Grindavíkurbæ til rannsóknaborana og til að gera borteiga sem eru 5.700 fermetrar að stærð. Ef hægt verður að vinna orku úr borholunum og HS Orka vill láta stækka borteigana í allt að 7.000 fermetra þarf að sækja um leyfi til Grindavíkurbæjar og fá deiliskipulagi breytt.
Fyrsti borteigurinn er 5.500 fermetrar
Fyrsti borteigurinn er tilbúinn fyrir tilraunaborun og er 5.500 fermetrar. Þar er áætlað að bora 2.000 til 2.500 metra djúpa holu. Ætlunin er að bora eina holu til að byrja með, prófa holuna og meta þær niðurstöður. Áætlað er að hefja borun í haust og ljúka henni á sex til átta vikum. Síðan taka við prófanir og rannsóknir fram á vor 2019, samkvæmt upplýsingum frá HS Orku. Áætlað er að meta það næsta sumar hvar heppilegt væri að staðsetja næstu holu.
Náttúruverndarsinnar gegn tilraunaborunum
Eldvörp eru gígaröð sem myndaðist á 13. öld. Náttúruverndarsinnar hafa lagst gegn raski á hrauni og tilraunaborunum HS Orku á svæðinu. Meðal þeirra sem sendu inn athugasemdir á sínum tíma voru Náttúruverndarsamtök Suðvesturlands. Í umsögn þeirra segir að gildi svæðisins til ferðaþjónustu og útvistar sé gríðarlega mikið. Mikið rask hafi orðið á náttúru Reykjanesskaga vegna jarðhitavinnslu og mál sé að linni. Ekki síst í því ljósi sé mikilvægt að halda Eldvörpum ósnortnum. Landvernd lagðist gegn rannsóknaborunum í Eldvörpum vegna neikvæðra áhrifa framkvæmdarinnar á náttúru og"""

T4 = """Telja að álverð gæti farið í 3.000 dali
Í byrjun apríl var verðið í kringum 2.000 dali og hafði þá farið lækkandi en hefur nú hækkað upp í tæplega 2.460 hækkunin hefur því numerið tæpum 25% í mánuðinum. Rætist spá Goldman þýðir það hækkunin yrði 50% á mjög skömmum tíma."""

T5 = """Ein hola er boruð á hverjum teig í rannsóknaborunum en ef þær bera góðan árangur og orkuvinnsla hefst gæti svo farið að HS Orka vilji hafa tvær til þrjár borholur á teig. Þeir borteigar verða 3.500 til 7.000 fermetrar, að sögn Ásgeirs Margeirssonar, forstjóra HS Orku."""

T6 = """"
Risavaxin viðskipti Guðmundar Kristjánssonar í Granda
Guðmundur Kristjánsson, forstjóri útgerðarfélagsins Brims, hefur keypt 34,1% eignarhlut Kristjáns Loftssonar og Halldórs Teitssonar í HB Granda. Heildarupphæð viðskiptanna nemur tæplega 21,7 milljörðum króna, en markaðsvirði HB Granda við lokun markaða í gær nam 54,7 milljörðum króna.Kristján og Halldór eru báðir stjórnarmenn í HB Granda. Þeir áttu eignarhlutinn í gegnum félögin Vogun hf. og Fiskiveiðahlutafélagið Venus hf. Þeir hafa verið stærstu ...
"""

T7 = """Stærsta verkefni Stóra Fíkniefnakóngsins er að borga KSÍ fyrir Rússlandsferðina og ganga í ÍSÍ."""

T8 = """Embiid snéri aftur í sigri 76ers
Úrslitakeppnin í NBA körfuboltanum vestanhafs eru í fullum gangi, í nótt fóru fram þrír leikir. Philadelphia 76ers vann góðan sigur á útivelli gegn Miami Heat og þá unnu Golden State Warriors og New Orleans Pelicans sína leiki og eru nú einum sigurleik frá því að sópa andstæðingum sínum í sumarfrí.
Philadelphia 76ers hafa verið á mikilli siglingu undanfarin misseri en áður en úrslitakeppnin hófst höfðu þeir borið sigur úr býtum í 15 leikjum í röð. Í nótt endurheimti liðið svo einn af sínum betri leikmönnum úr meiðslum, Kamerúnann Joel Embiid, hann lék á als oddi og var stigahæstur í sigri sinna manna með 23 stig. Leiknum lauk með öruggum sigri 76ers 128-108 en stigahæstur hjá Miami Heat var Slóveninn Goran Dragic með 23 stig. 76ers leiða einvígið 2-1 en vinna þarf fjóra leiki til að komast áfram."""

if __name__ == "__main__":
    for t in [T1, T2, T3, T4, T5, T6, T7, T8]:
        c = Concepts()
        c.extract(t)
        c.report(threshold=1.0)

