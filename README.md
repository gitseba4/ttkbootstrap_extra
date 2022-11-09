# ttkbootstrap_extra

Biblioteka rozszerza funkcjonalność 3 komponentów ttkbootstrap:
- Combobox
- Spinbox
- Tableview

oraz dodaje nowy komponent:
- ValuesEntry

Bibliotekę importujemy w następujący sposób:
```python
import ttkbootstrap_extra as ttke
```

### Combobox, Spinbox oraz ValuesEntry
Wszystkie 3 komponenty umożliwiają wybór jednej z wielu wartości przekazanych do komponentu. Przykładowo z bazy danych pobieramy listę producentów:
```python
[
  (1, 'Audi'),
  (2, 'Ford'),
  (3, 'Honda'),
  (4, 'Opel')
]
```
Teraz możemy utworzyć nowy komponent przekazując listę przez parametr `values_ext`, przykładowo:
```python
cb = ttke.Combobox(root, values_ext=producenci)
sb = ttke.Spinbox(root, values_ext=producenci)
ve = ttke.ValuesEntry(root, values_ext=producenci)
```
Dodatkowo w przypadku przekazania danych składających się z więcej niż dwóch kolumn możemy wskazać, która kolumna zawiera identyfikator z bazy danych (`column_id`), a która wartość do wyświetlenia w komponencie (`column_value`):
```python
cb = ttke.Combobox(root, values_ext=dane, column_id=2, column_value=5) # dla wartości w mysql cursor dictionary=False oraz named_tuple=False 
cb = ttke.Combobox(root, values_ext=dane, column_id='id', column_value='nazwa') # dla wartości w mysql cursor dictionary=True lub named_tuple=True 
```
Możemy także określić, czy dopuszczamy możliwość nie wybrania żadnej z wartości (NULL w MySQL, None w Python):
```python
cb = ttke.Combobox(root, values_ext=dane, allow_none=True)
```
