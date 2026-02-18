# 🔐 Login Systeem - ConnectScript IDE

## 📋 Overzicht

Het ConnectScript IDE vereist nu **authenticatie** voordat gebruikers kunnen werken. Dit helpt bij het beheren van gebruikerssessies en het opslaan van projecten per gebruiker.

## 🔑 Wat is Toegevoegd?

### 1. **Login Scherm**
- Gebruikers moeten inloggen voordat de IDE toegankelijk is
- Scherm verschijnt automatisch bij het laden
- Eenvoudige maar veilige validatie

### 2. **Gebruikerssessies**
- Gebruikersnaam wordt opgeslagen in localStorage
- Automatisch inloggen bij volgende bezoek
- Logout functionaliteit beschikbaar

### 3. **Per-Gebruiker Projecten**
- Elk project wordt opgeslagen onder de gebruiker
- Andere gebruikers kunnen hun eigen projecten hebben
- Automatische opslag van wijzigingen

### 4. **Veiligheidsfuncties**
- Passwordvalidatie (minimaal 4 karakters)
- Gebruikersnaam validatie (minimaal 3 karakters)
- Sessie logout optie

---

## 🚀 Hoe Gebruiken?

### Eerste Keer Inloggen
1. Open `http://localhost:8000`
2. Je ziet het login scherm
3. Voer gebruikersnaam in (bijv: "alice")
4. Voer wachtwoord in (bijv: "password123")
5. Klik "Login"

**Demo mode:** In dit systeem accepteer je elk wachtwoord dat minimaal 4 karakters lang is. Dit is voor demo doeleinden!

### Automatische Inlog
- Volgende keer dat je de IDE opent, ben je automatisch ingelogd
- Je vorige projecten worden hersteld
- De logout knop staat rechtsboven in de header

### Projecten Opslaan
- Projecten worden **automatisch opgeslagen** in localStorage
- Telkens wanneer je code wijzigt, wordt het opgeslagen
- Je kunt ook handmatig downloaden met "Download" knop

### Uitloggen
- Klik "Uitloggen" rechtsboven
- Je huidige project wordt opgeslagen
- Je bent nu uitgelogd en moet opnieuw inloggen

---

## 📊 Opslagstructuur

### localStorage Keys

```
connectedUser          → Huidig ingelogde gebruiker
connectedScript_{user} → Project gegevens van gebruiker
```

### Project Structuur
```json
{
  "pages": {
    "Home": "page Home\n-background...",
    "Page2": "page Page2\n..."
  },
  "scripts": {
    "startScript": "on click\n...",
    "backScript": "on click\n..."
  },
  "lastSaved": "2024-02-18T10:30:00Z"
}
```

---

## 🔐 Validatie Regels

### Gebruikersnaam
- ✅ Minimaal 3 karakters
- ✅ Kan letters, cijfers, onderstrepingen bevatten
- ✅ Geen speciale karakters vereist

### Wachtwoord
- ✅ Minimaal 4 karakters
- ✅ Kan alles bevatten (letters, cijfers, symbolen)
- ✅ Casegevoelig

### Error Messages
- Duidelijke foutmeldingen indien validatie faalt
- Suggesties voor correctie
- Veld focusses op eerste fout

---

## 💾 Automatische Opslag

### Wanneer Wordt Opgeslagen?
- ✅ Bij item selectie (vorige item opgeslagen)
- ✅ Bij pagina/script toevoegen
- ✅ Bij pagina/script verwijderen
- ✅ Bij code wijziging en verlaten
- ✅ Bij uitloggen

### Geen Handmatig Opslaan Nodig!
Je project wordt voortdurend gesynchroniseerd met localStorage.

---

## 🔄 Workflow Voorbeeld

```
1. Gebruiker opent IDE
   ↓
2. Login scherm verschijnt
   ↓
3. Gebruiker voert credentials in
   ↓
4. Login succesvol
   ↓
5. IDE laadt vorige project
   ↓
6. Gebruiker kan werken
   ↓
7. Wijzigingen worden automatisch opgeslagen
   ↓
8. Gebruiker klikt uitloggen
   ↓
9. Project wordt opgeslagen
   ↓
10. Logout scherm verschijnt
```

---

## 🧠 Session Management Code

### Methoden Toegevoegd

#### `login()`
```javascript
// Valideert input
// Stelt gebruiker in
// Slaat gebruiker op in localStorage
// Laadt gebruikers project
```

#### `logout()`
```javascript
// Spaart huidig project op
// Verwijdert gebruiker uit session
// Verwijdert formuliergegevens
// Reset IDE
```

#### `loadUserProject()`
```javascript
// Haalt project van huidige gebruiker
// Herstelt pagina's en scripts
// Sluit terug naar standaardproject als niet gevonden
```

#### `saveUserProject()`
```javascript
// Slaat project op onder huidige gebruiker
// Voegt timestamp toe
// Werkt automatisch
```

---

## 🛡️ Beveiligingsnotities

### Current Implementation
- localStorage (client-side) - voor demo
- Geen backend authenticatie
- Geen wachtwoordencryptie (geen noodzaak in demo)

### Production Improvements
Wanneer je dit naar productie brengt:
- Implementeer backend authenticatie (OAuth, JWT)
- Voeg wachtwoordencryptie toe
- Voeg session tokens toe
- Zet HTTPS in
- Voeg 2FA in voor extra veiligheid

---

## 🧪 Test Login Accounts

Voor testen kun je deze accounts gebruiken (alle met elk wachtwoord van 4+ karakters):

| Gebruiker | Wachtwoord | Opmerking |
|-----------|-----------|----------|
| alice | demo1234 | Demo gebruiker 1 |
| bob | pass5678 | Demo gebruiker 2 |
| charlie | secret99 | Demo gebruiker 3 |
| admin | admin123 | Admin account |

---

## 📝 Opslaan & Herstellen

### Opslaan naar Bestand
```
Klik "💾 Download" om JSON download (kan later hersteld worden)
```

### Herstellen van Backup
```
// TODO: Voeg upload/import functionaliteit toe voor toekomst versies
```

---

## 🆘 Problemen & Oplossingen

### "Ik ben vergeten uit te loggen"
→ Verwijder cookies/localStorage of gebruik ander browser/apparaat

### "Mijn project is weg!"
→ Check localStorage in DevTools (F12 → Application → Local Storage)

### "Ik kan niet inloggen"
→ Check consolefout in DevTools
→ Zorg ervoor dat JavaScript ingeschakeld is

### "Login werkt, maar project komt niet terug"
→ Check browser console voor errors
→ Zorg ervoor dat localStorage niet vol is

---

## 🔧 Waarschuwingen voor Beheerders

### localStorage Beperkingen
- Maximaal ~5-10MB per domein
- Bij groot project kan dit vol raken
- Verwijder oude projecten als nodig

### Browser Privacy
- Private/Incognito mode wist localStorage bij sluiten
- Gebruikers moeten opslaan antes insluit

### Data Backup
- localStorage is niet persistent
- Gebruikers moeten projecten downloaden voor backup

---

## 🎯 Toekomstige Verbeteringen

- [ ] Backend authenticatie
- [ ] Wachtwoordherstel
- [ ] Projectsharing
- [ ] Teamworks
- [ ] Real-time synchronisatie
- [ ] Cloud opslag
- [ ] Twee-factor authenticatie

---

## 📞 Vragen?

Raadpleeg:
- [START_HERE.md](START_HERE.md) - Begin hier
- [IDE_USER_GUIDE.md](IDE_USER_GUIDE.md) - IDE gids
- [INDEX.md](INDEX.md) - Volledige navigationindex

---

**Login vereist is actief! Gebruik de IDE veilig! 🔐**
