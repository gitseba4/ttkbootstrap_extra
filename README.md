# ttkbootstrap_extra

Biblioteka rozszerza funkcjonalność 3 komponentów ttkbootstrap:
- Combobox
- Spinbox
- Tableview

oraz dodaje nowy komponent:
- ValuesEntry

Biliotekę importujemy w następujący sposób:
```
import ttkbootstrap_extra as ttke
```

### Combobox, Spinbox oraz ValuesEntry
Wszystkie 3 komponenty umożliwiają wybór jednej z wielu wartości przekazanych do komponentu. Przykładowo z bazy danych pobieramy listę producentów:
```
[
  (1, 'Audi'),
  (2, 'Ford'),
  (3, 'Honda'),
  (4, 'Opel')
]
```
Teraz możemy utworzyć nowy komponent przekazując listę przez parametr `values_ext`, przykładowo:
```
cb = ttke.Combobox(root, values_ext=producenci)
sb = ttke.Spinbox(root, values_ext=producenci)
ve = ttke.ValuesEntry(root, values_ext=producenci)
```
