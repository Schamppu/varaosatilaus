# varaosatilaus
Varaosatilausjärjestelmä
	
	1. Asiakkaan kuvaus halutusta järjestelmästä
Sovellus tulee seuraavaan käyttötarkoituskuvaukseen, joka on saatu “asiakkaalta”:

Meillä on useampi myymälä ja yksi keskusvarasto. Myymälät tilaavat varaosia järjestelmän kautta keskusvarastolta, ja keskusvarasto täyttää ja merkitsee tilauksen käsitellyksi, mikäli niillä on varaosaa saatavilla. Mikäli varaosaa ei ole suoraan saatavilla, keskusvarasto tilaa varaosia lisää.

Varaosat koskevat erilaisia puhelinmalleja- ja merkkejä. Varaosalla on varaosakoodi, puhelinmalli ja  merkki sekä varaosan tyyppi, esimerkiksi piirilevy.

	2. Käsiteanalyysi
- myymälä
- keskusvarasto
- varaosa
- tilaus
- puhelinmalli
- puhelinmerkki
- varaosakoodi
- varaosan tyyppi

Seuraavaksi käydään käsitteet tarkemmin läpi ja mietitään niiden toimintaa tietokannassa.

	3. Käsitteiden avaaminen
Myymälä. Myymälöitä voi olla useampi, ja myymälän tulee toimia sisäänkirjautumistunnuksena, jolla tunnistetaan että mitä myymälää tarkastellaan. Myymälällä tulee olla ID, nimi, kirjautumistunnus ja salasana.

Keskusvarasto. Keskusvarastoja on vain yksi. Keskusvarasto toimii omana kirjautumistunnuksena, eli sillä tulee olla ainakin kirjautumistunnus ja salasana. Voidaan luoda myymälälle ja keskusvarastolle yhteinen “kirjautumistunnus”-taulu, jossa on erillisenä muuttujana että onko kyse keskusvarastosta vai myymälästä. Keskusvarasto voi selkeyden mukaan olla ID 1.

Varaosa. Järjestelmän kautta tilataan varaosia, ja niille oli määritelty käsiteanalyysissa jo valittuja termejä: varaosakoodi, varaosan tyyppi, puhelinmalli sekä puhelinmerkki. Näiden lisäksi varaosalla tulee olla ID. Uutta varaosaa ei luoda järjestelmään, jos sellainen on jo olemassa.

Tilaus. Tilaus sisältää varaosan, tai useampia varaosia. Tilaus voi olla eri tilassa: se voi olla käsittelemätön, käsitelty tai odottamassa varaosien saapumista (keskusvarasto on joutunut tilaamaan täydennyksiä). Tilauksella tulee siis olla liitostaulu varaosiin mitä se sisältää, sekä ID ja sen tila. Tämän lisäksi tilauksella tulee olla sen luonti-, käsittely-, sekä valmistumispäivämäärä. Luontipäivämäärä sisältää milloin tilaus on luotu, käsittelypäivämäärä milloin sitä on viimeksi käsitelty ja valmistumispäivämäärä milloin tilaus on valmis ja lähetetty myymälään.

Edellämainituista meillä syntyy kolme tietokantataulua (tunnus, varaosa, tilaus) sekä yksi liitostaulu (Tilaus-Varaosa). Avataan seuraavaksi tietokantataulut seuraavan linkin takaata löytyvästä tietokantakaaviosta:

https://drive.google.com/open?id=1Hph24yNAFZDf-kRXJ_KAXpfagFzMfLvC
Heroku: https://tsoha-varaosa.herokuapp.com/

Heroku: https://tsoha-varaosa.herokuapp.com/
Testitunnuksia: (tunnus, salasana)
admin, admin
user, user

Lisätty sisäänkirjautuminen, muokattu ohjelman toimintaa enemmän suunnitelman mukaiseksi kauemmaksi esimerkkimateriaalista.

