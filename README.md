# ConnectScript IDE

🎨 Een volledig werkende IDE om je eigen visuele programmeertaal te ontwerpen en uit te voeren!

## ✨ Functies

- **Code Editor**: Schrijf ConnectScript code met syntaxondersteun
- **Live Preview**: Zie je pagina's en elementen direct verschijnen
- **Event System**: Klik, laden, start events
- **Variabelen & Acties**: Set, add, subtract operaties
- **Console Output**: Volgende al je programmalogica
- **Multi-page Navigation**: Navigeer tussen pagina's

## 📖 ConnectScript Syntaxis

### Pages definiëren

```
page <naam>
-background
--color <kleur>
```

### Elementen

#### Button
```
-button <naam>
--text "<tekst>"
--color <kleur>
--position <x> <y>
--size <breedte> <hoogte>
--corner <afronding>
--fontsize <grootte>
--script <scriptNaam>
```

#### Text
```
-text <naam>
--value "<tekst>"
--color <kleur>
--position <x> <y>
--fontsize <grootte>
```

#### Image
```
-image <naam>
--source "<bestandspad>"
--position <x> <y>
--size <breedte> <hoogte>
```

### Scripts & Events

```
on <event>
 <actie1>
 <actie2>
end
```

**Events**: `click`, `start`, `load`

**Acties**:
- `alert("<bericht>")` - Toon alert
- `connect.goto(<pagina>)` - Navigeer naar pagina
- `set <variabele> <waarde>` - Zet variabele
- `add <variabele> <waarde>` - Verhoog variabele
- `subtract <variabele> <waarde>` - Verlaag variabele
- `play("<geluid>")` - Speel geluid af
- `wait(<seconden>)` - Wacht X seconden

## 🚀 Aan de slag

1. Open `index.html` in je browser
2. Schrijf ConnectScript code in de linker editor
3. Klik **Run** om je app uit te voeren
4. Gebruik Live Preview rechts om je interface te zien
5. Klik op buttons om scripts uit te voeren
6. Check Console Output voor logs

## 📝 Voorbeeld

```
page Home
-background
--color lightblue

-text title
--value "Hallo Wereld!"
--color white
--position 50 50
--fontsize 28

-button nextBtn
--text "Volgende"
--color green
--position 100 150
--size 150 50
--script goNext

page Page2
-background
--color lightcoral

-text msg
--value "Pagina 2!"
--color white
--position 50 50

on click
 add counter 1
 alert("Counter: +1")
 connect.goto(Home)
end

on start
 set counter 0
end
```

## 💡 Tips

- Gebruik commentaar met `#` voor notities
- Kleuren kunnen zijn: `red`, `green`, `blue`, `yellow`, `white`, `black`, etc.
- Posities zijn in pixels (x, y)
- Alle tekst moet tussen aanhalingstekens: `"..."`

## 📦 Downloaden

Klik **Download** om je hele project op te slaan als JSON bestand.

---

**Veel plezier met programmeren!** 🎉
