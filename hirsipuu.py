#TIE-02100
#13.2 Graafisen käyttöliittymän suunnitteleminen ja toteuttaminen
#Henri Pulkkinen
#oppnro 258141
#huhtikuu 2017

#Hirsipuupeli. Käyttäjä syöttää kirjaimia entry-kenttään
#tai arvaa koko sanan/lauseen. Vääriä arvauksia sallitaan 9.
#Väärästä arvauksesta ilmoitetaaan käyttäjälle tekstin lisäksi
#käyttöliittymän alalaidan asteikolla, missä punaisten ruutujen
#määrä indikoi väärin menneiden yritysten lukumäärää. Alussa
#kaikki ruudut ovat valkoisia. Kymmenen väärän arvauksen
#jälkeen peli on hävitty.
#Uuden pelin voi aloittaa milloin vain New game-nappulalla,
#jolloin myös arvotaaan uusi sana listasta.
#Uusia sanoja/lauseita on helppo lisätä peliin; riittää kun ne
#lisätään SANAT-listaan.
#Jos käyttäjä arvaa kaikki oikeat kirjaimet tai arvaa oikein koko
#sanan/lauseen, käyttäjä voittaa pelin ja siitä ilmoitetaan
#tekstillä. Lisäksi kaikki alalaidan ruudut muuttuvat vihreiksi.
#Mikäli käyttäjä syöttää yhden merkin, joka on jotain muuta kuin
#kirjain, ruutuun tulee teksti "Invalid input", eikä käyttäjä
#saa rangaistusta (alalaidan ruutujen tilanne ei muutu. Yli yhden
#merkin yritykset tulkitaan ratkaisuyrityksiksi, ja väärästä
#vastauksesta rangaistaan kuten väärän kirjaimen syöttämisestäkin.
#
#Työssä tähdättiin yksinkertaiseen toteutukseen, mutta mukaan tuli
#lopulta monia skaalautuvan version piirteitä.



from tkinter import *
import random

#MERKIT-listasta saadaan kirjainten, sekä välilyönnin ja tyhjän ruudun
#tiedostonimet.
MERKIT = { "A.gif", "B.gif","c.gif", "d.gif" ,"e.gif", "F.gif"
             ,"G.gif", "h.gif" ,"I.gif", "j.gif" ,"k.gif", "l.gif"
             ,"m.gif", "n.gif" ,"o.gif", "p.gif" ,"q.gif", "r.gif"
             ,"s.gif", "t.gif" ,"u.gif", "w.gif" ,"v.gif", "x.gif"
             ,"y.gif", "z.gif", "aa.gif", "ae.gif", "oe.gif", "valI.gif"
             ,"tyhja.gif"}

#VÄRIT-listasta saadaan alalaidan väriruutujen tiedostot.
VÄRIT= {"valkee.gif","punane.gif","vihree.gif"}


#SANAT-lista sisältää pelissä arvattavat sanat. Pitkiä
#lauseita voi rivittää /-merkillä. Käytössä ovat merkit A-Ö.
SANAT=["JOHDATUS/OHJELMOINTIIN","KALEVAN/PALLO",
       "KAHVIGALLUP","GRAAFISEN/KÄYTTÖLIITTYMÄN/SUUNNITTELEMINEN"
        "/JA TOTEUTTAMINEN","PEKKA SARAVO","PUFF THE MAGIC DRAGON"
        ,"YESTERDAY ALL/MY TROUBLES SEEMED/SO FAR AWAY",
        "VIHREÄN JOEN/RANNALLA", "YÖ KUIN SIELU/TEEKKARIN ON PIMIÄ"
       ,"HELMIPÖLLÖ ON/SUOMEN YLEISIN/PÖLLÖLAJI"]

class peli:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Hangman")

        self.__merkit = {}
        # Lisätään kuvatiedostot dictiin.
        for picfile in MERKIT:
            pic = PhotoImage(file=picfile)
            avain=picfile.strip(".gif").upper()
            self.__merkit[avain]=pic
        self.__merkit["Ö"]=PhotoImage(file="oe.gif")
        self.__merkit["Ä"]=PhotoImage(file="ae.gif")
        self.__merkit["Å"]=PhotoImage(file="aa.gif")


        self.__asteikkopics={}
        #Lisätään väriruudut omaan dictiinsä.
        for picfile in VÄRIT:
            pic = PhotoImage(file=picfile)
            avain=picfile.strip(".gif")
            self.__asteikkopics[avain]=pic

        self.initialize_game()

    def initialize_game(self):
        sanan_numero=random.randint(0,(len(SANAT)-1))
        self.__sana=SANAT[sanan_numero]
        self.__merkkilabels = []
        self.__asteikko=[]

        # Luodaan labelit arvotun sanan kirjaimille/merkeille.
        # /-merkin kohdalla vaihdetaan uudelle riville.
        sarake=1
        rivi=0
        for i in range(len(self.__sana)):
            if self.__sana[i]=="/":
                rivi+=1
                sarake=0
            new_label = Label(self.__window)
            new_label.grid(row=0+rivi, column=3+sarake,sticky=E)
            self.__merkkilabels.append(new_label)
            sarake+=1


        i=0
        #Luodaan labelit alalaidan asteikolle.
        for x in range (10):
            new_label = Label(self.__window,
                              image=self.__asteikkopics["valkee"])
            new_label.grid(row=5, column=4+i)
            self.__asteikko.append(new_label)
            i+=1


        indeksi = 0
        self.__asetetut_merkit=0
        #Lisätään labeleihin kuvatiedostot. Välilyönnit ovat
        #harmaita ruutuja ja vielä arvaamattomien kirjainten
        #paikalla on tyhjät valkoiset ruudut.
        #self.__asetetut_merkit-lukua tarvitaan, kun tarkastetaaan
        #onko kaikki kirjaimet arvattu oikein.
        for label in self.__merkkilabels:
            if self.__sana[indeksi] is not "/":
                if self.__sana[indeksi]==" ":
                    label.configure(image=self.__merkit["VALI"])
                    self.__asetetut_merkit+=1
                else:
                    label.configure(image=self.__merkit["TYHJA"])
            else: self.__asetetut_merkit+=1
            indeksi+=1

        self.__arvatut=[]
        self.__väärien_määrä=0


        self.__kirjain = Entry(self.__window)
        self.__kirjain.grid(row=3,column=1)
        self.__explanationtext = Label(self.__window,
                                       text="Start by entering a letter")
        self.__explanationtext.grid(row=2,column=1)
        Button(self.__window, text="new game", command=self.new_game)\
            .grid(row=6, column=1, sticky=E)
        Button(self.__window, text="stop", command=self.__window.destroy)\
            .grid(row=6, column=2)

        self.__quessButton = Button(self.__window,
                                    text="Quess",command=self.enter)
        self.__quessButton.grid(row=4, column=1, sticky=W+E)




    def enter(self):
        '''
        Tarkastaa syötteen laadun, eli onko syöte kirjain, koko lause vai
        "kielletty"-merkki. Mikäli kyseessä on virheellinen merkki
        tulostetaan virheilmoitus. Mikäli kyseessä yli yhden merkin mittainen
        merkkijono, tulkitaan käyttäjän yrittävän ratkaista koko sanaa/lausetta,
        jolloin kutsutaan koko_lause funktiota. Mikäli kyseessä on hyväksyttävissä
        oleva merkki, tarkastetaan ettei sitä ole jo arvattu. Tämän jälkeen
        kutsutaan joko väärin- tai oikea_kirjain-funktiota sen mukaan
        löytyykö kirjain kysytystä arvoituksesta.
        :return: 
        '''
        kirjain = self.__kirjain.get().upper()
        if kirjain !="":
            if len(kirjain)==1:
                if kirjain.isalpha()==False:
                    self.__explanationtext.configure(text="Invalid input")
                else:
                    if kirjain not in self.__arvatut:
                        if kirjain not in self.__sana:
                            self.väärin(kirjain)
                        else:
                            self.oikea_kirjain(kirjain)
                            self.__arvatut.append(kirjain)
                    else:
                        self.__explanationtext.configure\
                            (text="You have already entered this letter")
            else:
                self.koko_lause(kirjain)
        self.__kirjain.delete(0,END)
        self.tarkasta_lopetus()



    def oikea_kirjain(self,kirjain):
        '''
        Kun käyttäjä syöttää oikean kirjaimen, tämä metodi asettaa
        sen/ne näkyviin ruudulle.
        :param kirjain: arvattu kirjain
        :return:
        '''
        index=0
        avain=kirjain
        for kirjaimet in self.__sana:
            if kirjaimet==kirjain:
                self.__merkkilabels[index].configure(image=self.__merkit[avain])
                self.__asetetut_merkit += 1
            index+=1
        self.__explanationtext.configure(text="Correct!")


    def väärin(self,kirjain):
        '''
        Kun käyttäjä arvaa väärin, tämä metodi suorittaa
        vaadittavat toimenpiteet. Ikkunan alareunan ruudut
        muuttuvat punaisiksi, seliteteksti(explanationtext)
	    päivittyy ja käyttäjän mahdollinen häviö tarkistetaan.
        :param kirjain:
        :return:
        '''
        self.__arvatut.append(kirjain)
        self.__asteikko[self.__väärien_määrä].configure\
            (image=self.__asteikkopics["punane"])
        self.__väärien_määrä += 1
        self.__explanationtext.configure(text="Wrong!")
        if self.__väärien_määrä>len(self.__sana):
            self.__explanationtext.configure(text="You lose!")

    def koko_lause(self,mjono):
        '''
        Jos käyttäjä syöttää yli yhden merkin mittaisen arvauksen,
        tämä metodi tarkastaa, vastaako arvaus kysyttyä sanaa tai lausetta.
        :param mjono: käyttäjän syöttämä merkkijono
        :return: 
        '''
        vertailusana=""
        for kirjain in self.__sana:
            if kirjain is not "/":
                if kirjain is not " ":
                    vertailusana+=kirjain
        syötetty_sana=""
        for kirjain in mjono:
            if kirjain is not " ":
                syötetty_sana+=kirjain
        if syötetty_sana.upper()==vertailusana.upper():
            self.oikein()
        else:
            self.väärin(mjono)

    def ruudukon_täyttö(self):
        '''
        Käyttäjän arvatessa koko sanan oikein
        tämä metodi asettaa koko ko. sanan näkyviin ruudulle.
        :return: 
        '''
        indeksi=0
        for label in self.__merkkilabels:
            kuva=str(self.__sana[indeksi])
            if self.__sana[indeksi] is not "/":
                if self.__sana[indeksi]==(" "):
                    kuva="VALI"
                label.configure(image=self.__merkit[kuva])
            indeksi+=1


    def oikein(self):
        '''
        Käyttäjän arvatessa koko sanan oikein, tämä
        metodi suorittaa tarvittavat toimenpiteet sen
        ilmoittamiseen. Kysytyt kirjaimet ja onnitteluteksti
        ilmestyvät ruudulle. Alalaidan merkit muuttuvat vihreiksi.
        :return: 
        '''
        self.ruudukon_täyttö()
        self.__explanationtext.configure(text="Congratulations! "
                                "You won!")
        self.__quessButton.configure(state="disabled")
        for label in self.__asteikko:
            label.configure(image=self.__asteikkopics["vihree"])



    def tarkasta_lopetus(self):
        '''
        Tarkastaa, onko käyttäjä ratkaissut tehtävän
        arvaamalla kaikki kirjaimet oikein, tai onko
        sallittu väärien arvausten määrä ylitetty.
        :return: 
        '''
        if self.__asetetut_merkit==len(self.__sana):
            self.oikein()
        if self.__väärien_määrä==10:
            self.__explanationtext.configure(text="You lost!")
            self.ruudukon_täyttö()
            self.__quessButton.configure(state="disabled")

    def new_game(self):
        '''
        Nollaa pelin ja aloittaa uuden.
        :return: 
        '''
        for labels in self.__merkkilabels:
            labels.destroy()
        self.__explanationtext.configure(text="")
        self.initialize_game()


    def start(self):
        self.__window.mainloop()


def main():
    peli().start()
main()