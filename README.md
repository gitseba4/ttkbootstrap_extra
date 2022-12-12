# ttkbootstrap_extra

Biblioteka rozszerza funkcjonalność 3 komponentów ttkbootstrap:
- Combobox
![Combobox](/img/cb.png "Combobox")
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
Teraz możemy utworzyć nowy komponent przekazując listę poprzez parametr `values_ext`, przykładowo:
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
Możemy także określić, czy dopuszczamy możliwość nie wybrania żadnej z wartości (NULL w MySQL, None w Python). Odpowiada za to parametr `allow_none`:
```python
cb = ttke.Combobox(root, values_ext=dane, allow_none=True)
```
Oprócz nowych parametrów komponenty wspierają także poprzednie funkcjonalności ttkbootstrap, jak np. opcjonalne `bootstyle` lub `width`.
```python
sb = ttke.Spinbox(root, values_ext=dane, bootstyle='success', width=30)
```
Konfiguracji już istniejącego komponentu możemy dokonać poprzez metodę `configure`, np:
```python
cb.configure(values_ext=dane, column_id='pracownik_id', bootstyle='danger')
```
Każdy z powyższych komponentów udostępnia także metody służące do pobrania informacji dotyczących wybranego elementu:
- `get_id()` - zwraca identyfikator z bazy danych dla zaznaczonej pozycji (na podstawie parametru `column_id`)
```python
cb.get_id() => 4
```
- `get_value()` - zwraca wartość dla zaznaczonej pozycji (na podstawie parametru `column_value`)
```python
cb.get_value() => 'Opel'
```
- `get_item()` - zwraca zaznaczony element (w zależności od mysql cursor krotkę, nazwaną krotkę lub słownik)
```python
cb.get_item() => {'id': 4, 'nazwa': 'Opel'}
```
- `set_by_id(id)` - ustawia wartość komponentu na podstawie identyfikatora z bazy
```python
cb.set_by_id(2)
```
- `set_by_value(value)` - ustawia wartość komponentu na podstawie nazwy
```python
cb.set_by_value('Ford')
```
### TableviewExt
Komponent umożliwia utworzenie tabeli na podstawie danych z bazy. Działa dla każdej konfiguracji mysql cursor (dictionary=True lub named_tuple=True lub żadne z powyższych). Aby utworzyć tabelę musimy w konstruktorze przekazać dane z bazy poprzez parametr `values_ext`, np:
```python
tv = ttke.TableviewExt(root, values_ext=dane)
```
Dodatkowo w przypadku danych typu krotki (dla mysql cursor dictionary=False i named_tuple=False) możemy przekazać listę kolumn poprzez parametr `coldata`:
```python
tv = ttke.TableviewExt(root, values_ext=dane, coldata=['id', 'nazwa', 'data'])
```
Możemy także wskazać, która z kolumn zawiera daną będącą identyfikatorem z bazy danych poprzez parametr `column_id`:
```python
tv = ttke.TableviewExt(root, values_ext=dane, column_id='pojazd_id')
```
Oprócz tego dysponujemy także standardowymi parametrami komponentu z biblioteki ttkbootstrap, np:
```python
tv = ttke.TableviewExt(root, values_ext=dane, 'bootstyle'='primary', autofit=True, height=15)
```
Konfiguracja komponentu odbywa się poprzez metodę `configure`, np:
```python
tv.configure(values_ext=dane, searchable=True)
```
Oprócz tego dysponujemy 3 nowymi metodami dla komponentu:
- `reload_data(values_ext)` - powoduje przeładowanie tabeli nowymi/zaktualizowanymi danymi
```python
tv.reload_data(dane)
```
- `get_selected_rows(only_one_row, raw_data)` - zwraca zaznaczone wiersze w tabeli lub zaznaczony wiersz, jeśli ustawiono only_one_row=True. Dla parametru raw_data=True zwraca dane dokładnie w takim formacie jak ustawiono w mysql cursor. W przypadku błędów wyświetlany jest stosowny komunikat Messagebox
```python
tv.get_selected_rows(False, True) => [{'id': 2, 'nazwa': 'Ford'}, {'id': 4, 'nazwa': 'Opel'}]
tv.get_selected_rows(True, False) => (2,'Ford')
```
- `get_selected_ids(only_one_row)` - zwraca identyfikatory zaznaczonych wierszy w tabeli lub zaznaczonego wiersza, jeśli ustawiono only_one_row=True. W przypadku błędów wyświetlany jest stosowny komunikat Messagebox. Konieczne jest ustalenie dla komponentu, która kolumna zawiera identyfikator (parametr `column_id`)
```python
tv.get_selected_ids(False) => [2,4]
tv.get_selected_ids(True) => 2
```
