# -*- encoding: utf-8 -*-
import unittest

from icenews.similar import important_words

NEWS_3 = "Winnie Mandela látin"
NEWS_4 = "Winnie Mandela er látin"
NEWS_5 = "Tíu slasaðir eftir tvö umferðarslys"
NEWS_7 = "Fjórtán slösuðust eftir tvo árekstra"
NEWS_8 = """Bæj­ar­ráð Akra­nes­kaupstaðar hef­ur óskað eft­ir leyfi frá Minja­stofn­un til þess að farga kútter
Sig­urfara sem staðið hef­ur við Byggðasafnið í Görðum á Akra­nesi und­an­farna ára­tugi. Bréf þessa efn­is var lagt
fram á fundi ráðsins á miðviku­dag­inn. Áður en skip­inu verði fargað, fá­ist til þess leyfi, verður áhuga­söm­um
gef­inn kost­ur á að eign­ast skipið."""
NEWS_9 = """Hlutabréf í bandaríska netverslunarfyrirtækinu Amazon féllu um 4% í dag eftir harða gagnrýni Donalds Trump
 forseta  Bandaríkjanna. Hann sagði Amazon borga bandarísku póstþjónustunni allt of lítið fyrir sendingar og boðaði Trump
 breytingar á því án þess þó að tilgreina þær nánar.
„Aðeins fávitar, eða eitthvað verra, trúa því að póstþjónustan hagnist á viðskiptum við Amazon,“ tísti Trump í dag.
„Póstþjónustan tapar stórfé og þetta mun breytast.“ Hann sagði að á meðan önnur smásölufyrirtæki berðust í bökkum
þá keppti Amazon ekki á jafnréttisgrundvelli."""


class TestImportant(unittest.TestCase):
    def assertSameWords(self, a, b):
        self.assertSequenceEqual(sorted(a), sorted(b))

    def assertAllIn(self, some_words, full_list):
        for word in some_words:
            self.assertIn(word, full_list)

    def test_important(self):
        self.assertSameWords(important_words(NEWS_3), important_words(NEWS_4))
        self.assertAllIn(["umferðarslys", "slasaður"], important_words(NEWS_5))
        self.assertAllIn(["fjórtán", "slasaður", "árekstur"], important_words(NEWS_7))
        self.assertAllIn(
            ["Akraneskaupstaður", "Garðar", "Akranes", "skip"], important_words(NEWS_8)
        )
        self.assertAllIn(
            ["Trump", "Amazon", "Donald Trump", "Bandaríkin", "póstþjónusta"],
            important_words(NEWS_9),
        )

    def test_names(self):
        self.assertAllIn(
            ["Winnie Mandela", "lát", "látinn", "láta"], important_words(NEWS_4)
        )
        self.assertAllIn(
            ["Google Inc.", "Gunnar J.", "vinna"],
            important_words("Gunnar J. vinnur hjá Google Inc."),
        )

    def test_more_names(self):
        self.assertAllIn(
            ["Jón Jónsson", "maður", "ár"],
            important_words("Jón Jónsson er maður ársins"),
        )
        self.assertAllIn(
            ["Jón Jónsson", "maður", "ár"],
            important_words("Maðurinn heitir Jón Jónsson og er maður ársins"),
        )
        self.assertAllIn(
            ["Jón Jónsson", "saga"],
            important_words("Sagan er um Jón Jónsson og leiðist mér"),
        )
        self.assertAllIn(
            ["Jón Jónsson", "gjöf"],
            important_words("Gjöfin er frá Jóni Jónssyni syni mínum"),
        )
        self.assertAllIn(
            ["Jón Jónsson", "saga"],
            important_words("Tengist sögum Jóns Jónssonar lítillega"),
        )


if __name__ == "__main__":
    unittest.main()
