import unittest

from icenews.similar import _almost, important_words, similar, similar_article_wordlists


TEXT_1 = """
Hlutabréf í bandaríska netverslunarfyrirtækinu Amazon féllu um 4% í dag eftir harða gagnrýni Donalds Trump forseta 
Bandaríkjanna. Hann sagði Amazon borga bandarísku póstþjónustunni allt of lítið fyrir sendingar og boðaði Trump 
breytingar á því án þess þó að tilgreina þær nánar.
„Aðeins fávitar, eða eitthvað verra, trúa því að póstþjónustan hagnist á viðskiptum við Amazon,“ tísti Trump í dag.
„Póstþjónustan tapar stórfé og þetta mun breytast.“ Hann sagði að á meðan önnur smásölufyrirtæki berðust í bökkum 
þá keppti Amazon ekki á jafnréttisgrundvelli.
"""

TEXT_2 = """
Þreyta er komin í framhaldsskólakennara vegna stöðunnar í kjaraviðræðum þeirra við ríkið. Formaður Félags 
framhaldsskólakennara segir það ekki í boði að stéttin sé samningslaus svo mánuðum skiptir án þess að gripið sé til 
aðgerða.
"""

TEXT_3 = """
Winnie Mandela, fyrrum eiginkona Nelsons Mandela, fyrrum forseta Suður Afríku, er látin, 81 árs að aldri. 
Þetta staðfesti talskona Winnie Mandela í dag, en hún hafði lengi glímt við veikindi.  
Winnie var gift Nelson Mandela í 38 ár, en 27 af þeim sat Nelson í fangelsi.&nbsp;
"""

TEXT_4 = """
Hún var, líkt og eiginmaðurinn fyrrverandi, ötul baráttukona gegn aðskilnaði kynþátta í Suður Afríku og var handtekin 
árið 1969 fyrir að prenta og dreifa bæklingum þar sem aðskilnaðarstefnunni í Suður-Afríku var mótmælt.
"""

NEWS_0 = "Bréf í Amazon féllu eftir gagnrýni Trump"
NEWS_1 = "Kim Jong-un djúpt snortinn yfir suður-kóreskum söngatriðum"
NEWS_2 = "K-popp - tónleikar bræddu hjarta Kim Jong-un"
NEWS_3 = "Winnie Mandela látin"
NEWS_4 = "Winnie Mandela er látin"
NEWS_5 = "Tíu slasaðir eftir tvö umferðarslys"
NEWS_6 = "Tveimur vegum lokað vegna umferðarslysa"
NEWS_7 = "Fjórtán slösuðust eftir tvo árekstra"

NEWS_A_TITLE = "Bróðirinn grunaður um manndráp"
NEWS_A_DESCRIPTION = """
Bróðir mannsins, sem fannst látinn á bænum Gýgjarhóli II í uppsveitum Árnessýslu á laugardag, er grunaður um manndráp. Þetta staðfestir Oddur Árnason yfirlögregluþjónn í samtali við fréttastofu. Bráðabirgðaniðurstaða krufningar leiddi í ljós að áverkar voru á líkinu sem drógu manninn til dauða. Bróðirinn, sem er ábúandi á bænum,&nbsp;&nbsp;tilkynnti sjálfur um andlát bróður síns. Þegar lögregla kom á vettvang voru hann og þriðji bróðirinn handteknir og færðir til yfirheyrslu.&nbsp; Þriðja bróðurnum var sleppt að lokinni skýrslutöku en hinn úrskurðaður í gæsluvarðhald til 9. apríl.

Fram kom í tilkynningu frá lögreglunni á Suðurlandi á&nbsp;laugardag að ummerki hefðu&nbsp;verið um átök á vettvangi.&nbsp;&nbsp;Of snemmt væri að segja til um dánarorsök og því væri beðið eftir réttarkrufningu.&nbsp;

Sebastian Kuntz, eini starfandi réttarmeinafræðingurinn á landinu, kom til Íslands frá Salzburg&nbsp;í gærkvöld og niðurstaða bráðabirgðakrufningar hans var að áverkar væru á líkinu sem hafi&nbsp;leitt manninn til dauða.&nbsp;

Oddur Árnason, yfirlögregluþjónn, vildi sem minnst tjá sig um málið en staðfesti þó að bróðir mannsins væri nú grunaður um manndráp. Hann&nbsp;segir að hann&nbsp;hafi ekki verið yfirheyrður frá því á laugardag en hann er í gæsluvarðhaldi í fangelsinu á Hólmsheiði. Að öðru leyti yrðu ekki gefnar frekari upplýsingar um málið. Oddur vildi ekki svara því hvort atburðarásin lægi fyrir.

Fram kemur í tilkynningu frá lögreglunni í dag að rannsókn málsins sé umfangsmikil en hún er&nbsp;unnin í samvinnu lögreglunnar á Suðurlandi,&nbsp;tæknideildar lögreglunnar á&nbsp;höfuðborgarsvæðinu&nbsp;og réttarmeinafræðings Landspítala háskólasjúkrahúss.
"""

NEWS_B_TITLE = "Áverkar á líki mannsins sem leiddu hann til dauða"
NEWS_B_DESCRIPTION = "Fyrir liggur bráðabirgðaniðurstaða krufningar á líki manns sem fannst látinn að Gýgjarhóli II að morgni laugardagsins 31. mars s.l."

NEWS_C_DESCRIPTION = """
Donald Trump skortir siðferðið sem þarf til að gegna embætti forseta Bandaríkjanna. James Comey, fyrrverandi forstjóri bandarísku alríkislögreglunnar FBI sagði þetta í viðtali við George Stephanopolous sem sýnt var á ABC sjónvarpsstöðinni í Bandaríkjunum í gærkvöld. James Comey segist ekki hafa verið sammála þeim sem sögðu forsetann óhæfan vegna vanheilsu eða vitglapa. Hann sé ekki líkamlega ófær um að vera forseti en hann sé siðferðislega ófær um að vera forseti. Comey fór hörðum orðum um Donald Trump en þetta er fyrsta sjónvarpsviðtal hans eftir að Trump rak hann í maí í fyrra. Á næstunni verður gefin út sjálfsævisaga Comeys, þar sem hann fjallar opinskátt um samskipti sín við forsetann.
"""

NEWS_D_DESCRIPTION = """
<p>Starfshópur sem ríkið og Reykjavíkurborg skipaði 11. janúar sl. um uppbyggingu Laugardalsvallar hefur nú skilað af sér niðurstöðum. Hópurinn fór yfir hugmyndir um þjóðarleikvang fyrir knattspyrnu, lagði mat á þær og gerði tillögur um mögulega uppbyggingu.</p>
<p>Þá hefur ríkisstjórn, borgarráð og stjórn KSÍ samþykkt að stofna undirbúningsfélag um mögulega framkvæmd. Undirbúningi fyrir ákvörðun um uppbyggingu Laugardalsvallar skal lokið fyrir lok árs 2018.</p>
<p><a href="http://eyjan.dv.is/eyjan/2018/04/16/starfshopur-um-fjolnota-laugardalsvoll-ma-faera-fyrir-thvi-rok-ad-thad-se-ekki-rettlaetanleg-radstofun-opinberu-fe/" target="_blank" rel="noopener">Nánar má lesa um málið á Eyjunni.</a></p>
<p><strong>Helstu niðurstöður starfshópsins eru eftirfarandi:</strong><br />
Margt mælir með því að núverandi þjóðarleikvangur í Laugardal verði endurnýjaður.<br />
Ríkið, Reykjavíkurborg og KSÍ stofni undirbúningsfélag um mögulega framkvæmd og taki upp viðræður um eignarhald á þjóðarleikvangnum.<br />
Undirbúningsfélagið bjóði út samning um endanlega þarfagreiningu, skipulagningu verkefnisins, kostnaðaráætlun og gerð útboðsgagna.<br />
Þjóðarleikvangur getur hvort heldur sem er verið opinn knattspyrnuvöllur eða fjölnotaleikvangur með opnanlegu þaki.<br />
Kostnaður og áhætta við fjölnotaleikvang er vel umfram kostnað og áhættu við opinn knattspyrnuvöll.<br />
Ákvörðun um byggingu og eignarhald þjóðarleikvangs verði tekin með hliðsjón af niðurstöðu vinnu undirbúningsfélags og stöðu opinberra fjármála.<br />
Áætlað er að undirbúningi fyrir ákvörðun verði lokið í lok árs 2018.<br />
Verði tekin ákvörðun um byggingu þjóðarleikvangs getur útboðsferli framkvæmda tekið frá nokkrum mánuðum og upp undir eitt ár og framkvæmdatími verið að minnsta kosti tvö ár.<br />
Huga verður að mögulegu fordæmi ákvörðunar um byggingu þjóðarleikvangs fyrir aðrar íþróttagreinar með hliðsjón af væntanlegri reglugerð um þjóðarleikvanga.<br />
Hvetja ætti til opinnar umræðu um byggingu þjóðarleikvangs á grundvelli þeirra ítarlegu gagna sem tekin hafa verið saman á undanförnum misserum.</p>
<p>The post <a rel="nofollow" href="http://433.dv.is/433/2018/04/16/mun-liggja-fyrir-lok-ars-hvad-verdur-gert-vid-laugardalsvoll/">Mun liggja fyrir í lok árs hvað verður gert við Laugardalsvöll</a> appeared first on <a rel="nofollow" href="http://www.dv.is">DV</a>.</p>
"""


class TestSimilar(unittest.TestCase):
    def assertSameWords(self, a, b):
        self.assertSequenceEqual(sorted(a), sorted(b))

    def test_almost(self):
        self.assertTrue(_almost(10, 12, 14))
        self.assertTrue(_almost(7, 12, 14))
        self.assertFalse(_almost(3, 12, 14))

    def test_matching(self):
        # self.assertTrue(similar(important_words(TEXT_3), important_words(TEXT_4)))
        self.assertTrue(
            similar(
                important_words(NEWS_A_DESCRIPTION, NEWS_A_TITLE),
                important_words(NEWS_B_DESCRIPTION, NEWS_B_TITLE),
            )
        )
        # self.assertTrue(similar(NEWS_3, NEWS_4))

    def test_not_matching(self):
        # self.assertFalse(similar(NEWS_1, NEWS_3))
        # self.assertFalse(similar(NEWS_1, NEWS_6))
        # self.assertFalse(similar(NEWS_1, NEWS_6))
        pass

    def test_should_match_but_currently_dont(self):
        # self.assertFalse(similar(NEWS_1, NEWS_2))
        # self.assertFalse(similar(NEWS_5, NEWS_6))
        pass

    def test_important_words(self):
        # self.assertEqual(["Trump"], important_words(NEWS_C_DESCRIPTION))
        # self.assertEqual(["Trump"], important_words(NEWS_D_DESCRIPTION))
        pass

    def test_important_words_more(self):
        self.assertEqual(
            ["EFTA", "ESB", "Gangar", "ganga", "núinn", "núa", "gangur", "göng"],
            important_words("Göngum úr EFTA og í ESB núna!"),
        )
        self.assertEqual(
            ["NBA-deild", "fyrirtaksáhugamál", "fylgja"],
            important_words("Fylgjast með NBA-Deildinni er fyrirtaksáhugamál"),
        )
        self.assertEqual(
            ["http://helst.is", "www.helst.is", "skoða"],
            important_words("Skoðaðu http://helst.is eða www.Helst.is."),
        )
        self.assertEqual(
            ["samkomulag", "ná", "fela"],
            important_words("Samkomulag hefur náðst. Í samkomulaginu felst."),
        )
        self.assertEqual(
            ["Ásta F. Flosadóttir", "I", "Höfðar", "bóndi", "óttast"],
            important_words("Ásta F. Flosadóttir bóndi á Höfða I óttast."),
        )
        self.assertEqual(
            ["bók", "svanafólk", "nýútkominn", "nýútkoma", "heita", "heitur"],
            important_words("Í nýútkominni bók sem heitir Svanafólkið."),
        )
        self.assertEqual(
            ["gangur", "ganga"], important_words("Það er ekki neitt í gangi")
        )
        self.assertEqual(
            ["þegja", "heyra"], important_words("Þegar þú þegir þá heyrist ekkert")
        )
        self.assertEqual(
            ["þjóðaröryggisráð", "dagur", "funda"],
            important_words("Fundað var í þjóðaröryggisráði í dag."),
        )
        self.assertEqual(
            ["íhaldsflokkur", "þingmaður", "líkur", "bæta", "mikill", "mikla"],
            important_words(
                "Miklar líkur eru á að Íhaldsflokkurinn bæti við sig þingmönnum."
            ),
        )

    def test_need_to_fix_important_words(self):
        self.assertEqual(
            ["Tímamótasigur", "Boris"], important_words("Tímamótasigur Boris.")
        )
        self.assertEqual(
            [
                "sameining",
                "fjölmiðlamarkaður",
                "stó",
                "vænd",
                "stór",
                "væna",
                "fjölmiðlamarka",
            ],
            important_words("Stór sameining er í vændum á fjölmiðlamarkaði."),
        )

    def test_similar(self):
        self.assertSameWords(
            ["Baldur", "Konni", "sýning"],
            important_words("Baldur og Konni með sýningu"),
        )
        self.assertSameWords(
            ["Baldur", "Konni", "sýning"],
            important_words("", "Baldur og Konni með sýningu"),
        )
        self.assertSameWords(
            ["Álrisi", "hönd", "vandi", "vanda", "vandur", "venja"],
            important_words("Álrisi í vanda", "Vandi að höndum"),
        )
        self.assertSameWords(
            ["einn", "tveir", "þrír"], important_words("Einn, tveir og þrír")
        )

    def test_examples(self):
        self.assertTrue(
            similar_article_wordlists(
                "Ártúnsbrekka;Reykjavík;strætisvagn;reykur;vél;klukka;slökkvilið;höfuðborgarsvæði;tilkynna;skammur;skömmu",
                "Ártúnsbrekka;strætisvagn;bilun;slökkvilið;höfuðborgarsvæði;klukka;eldur;valda;út;í morgun;semja;sem",
            )
        )
        self.assertTrue(
            similar_article_wordlists(
                "Ögmundur;Steinar Skarphéðinn Jónsson;Ögmundur Kristinsson;Rússland;KSÍ;tengdafaðir;sena;blaðamannafundur;markvörður;gestur;höfuðstöðvar",
                "Rússland;Heimir;Ögmundur;Heimir Hallgrímsson;Steinar;Ögmundur Kristinsson;Rúnar Alex Rúnarsson;Hannes;Frederik Schram;maður;spurning;til",
            )
        )

    def test_gray_area(self):
        self.assertFalse(
            similar_article_wordlists(
                "Bretland;Ratcliffe;Grímsstaðir;Jim Ratcliffe;The Sunday Times;Manchester United;ár;maður;21,1;milljarður;2.933;18;65;eign;ær;ríkur;eiga;auðjöfur;úttekt;eigna;króna;blað",
                "Bretland;Ísland;Grímsstaðir;Fjöll;Hafralónsá;Þistilfjörður;Vopnafjörður;Sunday Times;ríkur;stóreignamaður;laxveiðijörð",
            )
        )
        self.assertFalse(
            similar_article_wordlists(
                "Jón G. Snædal;Íslendingur;Alzheimertilraun;Alzheimer;Ísland;lykilhlutverk;hópur;þáttur;lyfjarannsókn;þáttaskil;barátta;lyf;sjúkdómur;yfirmaður;rannsókn;yfirlæknir;öldrunarsvið",
                "Evrópusambandið;Ísland;Íslendingur;80%;á móti;orkutilskipun;könnun;þátttaka;meirihluti;tilskipun;sýn",
            )
        )

    def test_failure_examples(self):
        self.assertFalse(
            similar_article_wordlists(
                "Forvarnir;ferðaþjónusta;útsending;hjálp;samtak;starfsháttur;öryggismál;viðbragð;atburður;í dag;góður;óvæntur;upp;við;forvörn",
                "vika;stór;vinna;pottur;karlmaður;fimmtugsaldur;haf;lottóvinningur;lukkupottur;enn;tvisvar;talandi;ástralskur;því",
            )
        )
        self.assertFalse(
            similar_article_wordlists(
                "Ísland;Skarphéðinn Guðmundsson;Ari Ólafsson;Ísrael;Skarphéðinn;90;milljón;Ríkisútvarpið;Dagblaðið Vísir;Lissabon;Eurovisionævintýrið;Eurovision;króna;þátttaka",
                "Malavi;Ísland;Malaví;Mangochi;fimm;sjúkrabíll;sendiráð;stjórnvald;sjúkrabifreið;hérað;líf",
            )
        )
        self.assertFalse(
            similar_article_wordlists(
                "Suðurskautsland;117;Steve Plain;Everest;Vinon;dagur;ær;hár;fjallgöngumaður;toppur;sjö;eiga;fjall",
                "Reykjanes;Langanes;Ísland;land;ær;dagur;vestanátt;úrkomuskil;kólna;af;eiga;áfram;fram;fjall;landa;smálægð;húnn;hugleiðing;veðurfræðingur;veðurstofa;kjölfar;úrkoma;enn;úr;suðvestur;norður",
            )
        )
        self.assertFalse(
            similar_article_wordlists(
                "Berlín;Reykjavík;Ástarbrölt;Ástarbrölta;eð;rithöfundur;vestur;sonur;leikskóli;fútt;dagur;blað;kaffihús;borg;háttur;hugðarefni;stilla;ef;líf;ár;síða;borgaralegur;heimavinnandi;ýmist;upp;á milli;minna;mikill;snemma;heldri",
                "Karl Sigurðsson;100;ár;dagur;því;sé;stó;skipstjóri;vélstjóri;afmæli;verður;hundrað",
            )
        )
        self.assertFalse(
            similar_article_wordlists(
                "Evrópusambandið;Ísland;Íslendingur;80%;á móti;orkutilskipun;könnun;þátttaka;meirihluti;tilskipun;sýn",
                "Tékkland;Íslendingur;Evrópumeistaramót;Ísland;Mikill;kraftlyftingavor;gullverðlaun;verðlaunapeningur;kraftlyfting;meðbyr;íþrótt",
            )
        )


if __name__ == "__main__":
    unittest.main()
