from collections import namedtuple
from typing import Union
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from tkfontawesome import icon_to_image
from ttkbootstrap.dialogs.dialogs import Messagebox


class ExtendValuesWidget:
    """Klasa rozszerzająca funkcjonalość komponentów o możliwość korzystania ze słowników lub list złożonych"""

    def __init__(self, values_ext: Union[list, tuple, dict] = None, column_id: Union[str, int] = 0, column_value: Union[
        str, int] = 1,
                 allow_none: bool = False):
        self._set_config(values_ext, column_id, column_value, allow_none)

    def _set_config(self, values_ext: Union[list, tuple, dict], column_id: Union[str, int], column_value: Union[
        str, int],
                    allow_none: bool):
        """Konfiguracja komponentu"""

        self._source_values_data = values_ext
        self._column_id = column_id
        self._column_value = column_value
        self._allow_none = allow_none
        self._empty_source_data = False
        self._dict_rows = False
        self._namedtuple_rows = False

        """"Walidacja danych wejściowych"""
        self.__params_validation(values_ext)

        """Jeżeli brak danych wejściowych i niedopuszczalna wartość None to zwracamy błąd"""
        if self._empty_source_data and not self._allow_none:
            raise Exception("Dane wejściowe są puste a kontrolka nie umożliwia ustawienia wartości None!")

        """Jeżeli słownik to zamieniamy wartości na krotki"""
        if type(values_ext) == dict:
            self._values_lst = []

            for k, v in values_ext.items():
                self._values_lst.append((k, v))
        else:
            self._values_lst = values_ext[:]

        """Jeżeli dopuszczalny jest brak wartości (None) to dodajemy na początku listy"""
        if self._allow_none:
            if self._dict_rows:
                none_item = self._values_lst[-1]
                for i in none_item.keys():
                    none_item[i] = ''
                    if i == self._column_id:
                        none_item[i] = None
                self._values_lst.insert(0, none_item)
            elif self._namedtuple_rows:
                none_item = {}

                for i in self._values_lst[-1]._fields:
                    none_item[i] = ''
                    if i == self._column_id:
                        none_item[i] = None

                Row = namedtuple('Row', none_item.keys())
                self._values_lst.insert(0, Row(**none_item))
            else:
                first_row = []
                for i in range(max(self._column_id, self._column_value) + 1):
                    if i == self._column_id:
                        first_row.append(None)
                    else:
                        first_row.append('')
                self._values_lst.insert(0, tuple(first_row))

        self.__set_values_to_show()

    def __params_validation(self, values_ext):
        """Walidacja danych wejściowych"""

        if values_ext is None:
            raise Exception("Brak wymaganego parametru 'values_ext'!")

        if type(values_ext) not in (list, tuple, dict):
            raise Exception("Parametr 'values_lst' nie jest listą, krotką lub słownikiem!")

        """Jeśli dane słownikowe (dictionary=True) to ustawiamy odpowiednią flagę"""
        if type(values_ext) in (list, tuple) and len(values_ext) > 0 and type(values_ext[0]) == dict:
            self._dict_rows = True

        """Jeśli dane w nazwanych krotkach (named_tuple=True) to ustawiamy odpowiednią flagę"""
        if type(values_ext) in (list, tuple) and len(values_ext) > 0 and type(values_ext[0]).__name__ == 'Row':
            self._namedtuple_rows = True

        """Ustawiamy flagę, jeśli dane wejściowe są puste"""
        if len(values_ext) == 0:
            self._column_id = 0
            self._column_value = 1
            self._empty_source_data = True

        """Jeśli przekazano jakieś dane i nie mają one odpowiedniej struktury to zwracamy błąd"""
        if len(values_ext) > 0 and type(values_ext[0]) not in (list, tuple, dict) \
                and type(values_ext[0]).__name__ != 'Row':
            raise Exception("Niepoprawny format danych wejściowych 'values_ext'!")

        """Walidacja parametrów column_id i column_value dla danych słownikowych"""
        if self._dict_rows:
            if type(self._column_id) != str:
                raise Exception(f"Parametr 'column_id' musi być typu tekstowego!")
            if type(self._column_value) != str:
                raise Exception(f"Parametr 'column_value' musi być typu tekstowego!")

            if values_ext[-1].get(self._column_id) is None:
                raise Exception(f"Parametr column_id[{self._column_id}] nie występuje w przekazanych danych!")

            if values_ext[-1].get(self._column_value) is None:
                raise Exception(f"Parametr column_value[{self._column_value}] nie występuje w przekazanych danych!")

            return

        """Walidacja parametrów column_id i column_value dla danych w nazwanych krotkach"""
        if self._namedtuple_rows:
            if type(self._column_id) != str:
                raise Exception(f"Parametr 'column_id' musi być typu tekstowego!")
            if type(self._column_value) != str:
                raise Exception(f"Parametr 'column_value' musi być typu tekstowego!")

            try:
                getattr(values_ext[-1], self._column_id)
            except Exception:
                raise Exception(f"Parametr column_id[{self._column_id}] nie występuje w przekazanych danych!")

            try:
                getattr(values_ext[-1], self._column_value)
            except Exception:
                raise Exception(f"Parametr column_id[{self._column_value}] nie występuje w przekazanych danych!")

            return

        """Walidacja parametrów column_id i column_value dla zwykłych danych"""

        if type(self._column_id) != int:
            raise Exception(f"Parametr 'column_id' musi być typu liczbowego!")
        if type(self._column_value) != int:
            raise Exception(f"Parametr 'column_value' musi być typu liczbowego!")

        if not self._empty_source_data:
            if self._column_id > len(values_ext[-1]):
                raise Exception(f"Parametr 'column_id' ma wartość wyższą niż ilość kolumn w danych wejściowych!")

            if self._column_value > len(values_ext[-1]):
                raise Exception(f"Parametr 'column_value' ma wartość wyższą niż ilość kolumn w danych wejściowych!")

    def __set_values_to_show(self):
        """Ustawienie danych do wyświetlania w kontrolce"""

        self._values_show = []

        for item in self._values_lst:
            if len(item) < 2:
                raise Exception("Niepoprawny format danych wejściowych 'values_lst'!")

            if self._namedtuple_rows:
                self._values_show.append(getattr(item, self._column_value))
            else:
                self._values_show.append(item[self._column_value])

    def _config(self, values_ext: Union[list, tuple, dict], column_id: Union[str, int], column_value: Union[str, int],
                allow_none: bool):

        """Jeżeli cokolwiek zostało przekazane jako parametr to od nowa konfigurujemy komponent"""
        if values_ext is not None or column_id is not None or column_value is not None or allow_none is not None:
            values_ext = values_ext if values_ext is not None else self._source_values_data
            column_id = column_id if column_id is not None else self._column_id
            column_value = column_value if column_value is not None else self._column_value
            allow_none = allow_none if allow_none is not None else self._allow_none

            self._set_config(values_ext, column_id, column_value, allow_none)

    def get_id(self):
        """Zwrócenie identyfikatora zaznaczonego elementu, jeżeli nie znaleziono to błąd"""

        selected_value = self.get()

        for row in self._values_lst:
            if self._namedtuple_rows and getattr(row, self._column_value) == selected_value:
                return getattr(row, self._column_id)
            elif not self._namedtuple_rows and row[self._column_value] == selected_value:
                return row[self._column_id]

        raise Exception("Nie znaleziono identyfikatora dla wskazanego rekordu!")

    def get_value(self):
        """Zwrócenie wartości zaznaczonego elementu (to co wyświetlane w kontrolce)"""

        return self.get()

    def get_item(self):
        """Zwrócenie całego obiektu dla zaznaczonego elementu, jeżeli nie znaleziono to błąd"""

        selected_value = self.get()

        for row in self._values_lst:
            if self._namedtuple_rows and getattr(row, self._column_value) == selected_value:
                return row
            elif not self._namedtuple_rows and row[self._column_value] == selected_value:
                return row

        raise Exception("Nie znaleziono danych dla wskazanego rekordu!")

    def set_by_id(self, id: Union[int, str]):
        """Ustawienie wartości kontrolki na podstawie id (błąd jeśli nie znaleziono)"""

        for row in self._values_lst:
            if self._namedtuple_rows:
                r_id = getattr(row, self._column_id)
                r_value = getattr(row, self._column_value)
            else:
                r_id = row[self._column_id]
                r_value = row[self._column_value]

            if r_id == id:
                self.set(r_value)
                return

        raise Exception(f"Nie znaleziono wartości o identyfikatorze {id}!")

    def set_by_value(self, value):
        """Ustawienie wartości kontrolki na podstawie tekstu (błąd jeśli nie znaleziono)"""

        for row in self._values_lst:
            if self._namedtuple_rows:
                r_value = getattr(row, self._column_value)
            else:
                r_value = row[self._column_value]

            if r_value == value:
                self.set(value)
                return

        raise Exception(f"Nie znaleziono wartości {value}!")

    def set_first_value(self):
        """Ustawienie pierwszej wartości z kontrolki jako domyślnie wybranej"""

        if len(self._values_lst) == 0:
            return

        if self._namedtuple_rows:
            r_value = getattr(self._values_lst[0], self._column_value)
        else:
            r_value = self._values_lst[0][self._column_value]

        self.set(r_value)

class Combobox(ExtendValuesWidget, ttk.Combobox):
    """Definicja nowego komponentu Combobox umożliwiającego korzystanie ze słowników lub list złożonych"""

    def __init__(self, master=None, values_ext=None, column_id: Union[str, int] = None, column_value: Union[
        str, int] = None, allow_none: bool = False, bootstyle: str = 'primary', width: int = 20):
        ExtendValuesWidget.__init__(self, values_ext, column_id, column_value, allow_none)
        ttk.Combobox.__init__(self, master, values=self._values_show, bootstyle=bootstyle, width=width)
        self.set_first_value()

    def configure(self, cnf=None, values_ext: Union[list, tuple, dict] = None, column_id: Union[str, int] = None,
                  column_value: Union[str, int] = None,
                  allow_none: bool = None, **kw):
        """Konfiguracja komponentu"""

        ExtendValuesWidget._config(self, values_ext, column_id, column_value, allow_none)
        ttk.Combobox.configure(self, cnf, values=self._values_show, **kw)
        self.set_first_value()


class Spinbox(ExtendValuesWidget, ttk.Spinbox):
    """Definicja nowego komponentu Spinbox umożliwiającego korzystanie ze słowników lub list złożonych"""

    def __init__(self, master=None, values_ext=None, column_id: Union[str, int] = None, column_value: Union[
        str, int] = None, allow_none: bool = False, bootstyle: str = 'primary', width: int = 20):
        ExtendValuesWidget.__init__(self, values_ext, column_id, column_value, allow_none)
        ttk.Spinbox.__init__(self, master, values=self._values_show, bootstyle=bootstyle, width=width)
        self.set_first_value()

    def configure(self, cnf=None, values_ext: Union[list, tuple, dict] = None, column_id: Union[str, int] = None,
                  column_value: Union[str, int] = None,
                  allow_none: bool = None, **kw):
        """Konfiguracja komponentu"""

        ExtendValuesWidget._config(self, values_ext, column_id, column_value, allow_none)
        ttk.Spinbox.configure(self, cnf, values=self._values_show, **kw)
        self.set_first_value()


class ValuesEntry(ExtendValuesWidget, ttk.Frame):

    def __init__(self, master=None, values_ext=None, column_id: Union[str, int] = None, column_value: Union[
        str, int] = None, allow_none: bool = False, bootstyle: str = 'primary', width: int = 10):
        ExtendValuesWidget.__init__(self, values_ext, column_id, column_value, allow_none)
        ttk.Frame.__init__(self, master)

        """Wyzerowanie zmiennych"""
        self.__ret_id = None
        self.__ret_value = None
        self.__ret_item = None

        self.__bootstyle = bootstyle
        self.__list_icon = icon_to_image("list", scale_to_height=16)

        """Dodanie pola typu entry w celu wyświetlania aktualnie ustawionej wartości"""
        self.__entry = ttk.Entry(self, state='disabled', bootstyle=self.__bootstyle, width=width)
        self.__entry.pack(side='left', fill='x', expand='yes')
        self.__entry.configure(foreground=ttk.Style().colors.inputfg)

        """Dodanie przycisku który utworzy okno z listą wartości do wyboru"""
        self.__button = ttk.Button(self, bootstyle=self.__bootstyle, image=self.__list_icon,
                                   command=self.__show_list_window)
        self.__button.pack(side='left')
        self.set_first_value()

    def __show_list_window(self):
        """Utworzenie okna z listą wartości do wyboru"""

        self.__list_window = ttk.Toplevel(title='Wybierz wartość')
        self.__list_window.geometry('270x270')
        self.__list_window.resizable(0, 0)

        columns = []
        rows = []

        if self._dict_rows:
            """Jeżeli dane z bazy jako słownik to wczytujemy nagłówki kolumn i wiersze konwertujemy na krotki"""
            i = 0

            for column in self._source_values_data[-1].keys():
                columns.append({'text': column, 'width': 125})

                if column == self._column_id:
                    self._id_order_nr = i
                if column == self._column_value:
                    self._val_order_nr = i

                i += 1
            for row in self._values_lst:
                rows.append(tuple(row.values()))

        elif self._namedtuple_rows:
            """Jeżeli dane z bazy jako obiekty typu Rows to wczytujemy nagłówki kolumn i wiersze konwertujemy na krotki"""
            i = 0

            for column in self._source_values_data[-1]._fields:
                columns.append({'text': column, 'width': 125})

                if column == self._column_id:
                    self._id_order_nr = i
                if column == self._column_value:
                    self._val_order_nr = i

                i += 1

            for row in self._values_lst:
                rows.append(tuple(row))

        else:
            """Jeżeli dane jako krotki to dodajemy tyle kolumn ile będzie wartości, jeśli dwie to nazywamy je 'id' oraz 'Wartość'"""
            if len(self._values_lst[-1]) == 2:
                columns.append({'text': 'id', 'width': 125})
                columns.append({'text': 'Wartość', 'width': 125})
            else:
                for i in range(len(self._values_lst[-1])):
                    columns.append({'text': f'col{i + 1}', 'width': 125})
            rows = self._values_lst

            self._id_order_nr = self._column_id
            self._val_order_nr = self._column_value

        """Rysujemy tabelę w oknie"""
        self.__table = Tableview(self.__list_window, bootstyle=self.__bootstyle, coldata=columns, rowdata=rows,
                                 searchable=True, height=5)
        self.__table.pack(fill='both', expand='yes', padx=10, pady=10)

        """Dodajemy przycisk, który ustawi wybraną wartość"""
        self.__set_value_button = ttk.Button(self.__list_window, bootstyle='success', text='Ustaw',
                                             command=self.__set_value_from_list)
        self.__set_value_button.pack(pady=(5, 15))

    def __set_value_from_list(self):
        """Ustawienie wybranej wartości z listy"""

        """Sprawdzenie czy na pewno wybrany został tylko jeden rekord"""
        selected_rows = self.__table.view.selection()
        if len(selected_rows) != 1:
            Messagebox.show_error(parent=self.__list_window, message='Należy zaznaczyć jedną wartość z listy!',
                                  title='Błąd')
            return

        """Ustawienie wartości na podstawie wybranego rekordu"""
        row = self.__table.get_row(iid=selected_rows[0]).values
        self.__set_values_by_row(row)

        """Zamknięcie okna z listą wartości do wyboru"""
        self.__table.destroy()
        self.__set_value_button.destroy()
        self.__list_window.destroy()

    def __set_values_by_row(self, tbl_row):
        """Ustawienie zmiennych komponentu na podstawie wybranego elementu"""

        self.__ret_id = tbl_row[self._id_order_nr]

        for row in self._values_lst:
            if self._namedtuple_rows and getattr(row, self._column_id) == self.__ret_id:
                self.__ret_value = getattr(row, self._column_value)
                self.__ret_item = row
                break
            elif not self._namedtuple_rows and row[self._column_id] == self.__ret_id:
                self.__ret_value = row[self._column_value]
                self.__ret_item = row
                break

        self.__entry.configure(state='normal')
        self.__entry.delete(0, 'end')
        self.__entry.insert(0, self.__ret_value)
        self.__entry.configure(state='disabled')

    def get_id(self):
        """Zwrócenie identyfikatora zaznaczonego elementu"""

        return self.__ret_id

    def get_value(self):
        """Zwrócenie wartości zaznaczonego elementu (to co wyświetlane w kontrolce)"""

        return self.__ret_value

    def get_item(self):
        """Zwrócenie całego obiektu dla zaznaczonego elementu"""

        return self.__ret_item

    def set_by_id(self, id: Union[int, str]):
        """Ustawienie wartości kontrolki na podstawie id (błąd jeśli nie znaleziono)"""

        self.__show_list_window()

        for row in self.__table.get_rows():
            if row.values[self._id_order_nr] == id:
                self.__set_values_by_row(row.values)
                self.__list_window.destroy()
                return

        self.__list_window.destroy()

        raise Exception(f"Nie znaleziono wartości o identyfikatorze {id}!")

    def set_by_value(self, value):
        """Ustawienie wartości kontrolki na podstawie tekstu (błąd jeśli nie znaleziono)"""

        self.__show_list_window()

        for row in self.__table.get_rows():
            if row.values[self._val_order_nr] == value:
                self.__set_values_by_row(row.values)
                self.__list_window.destroy()
                return

        self.__list_window.destroy()

        raise Exception(f"Nie znaleziono wartości {value}!")

    def set_first_value(self):
        """Ustawienie pierwszej wartości z kontrolki jako domyślnie wybranej"""

        if len(self._values_lst) == 0:
            return

        if self._namedtuple_rows:
            r_id = getattr(self._values_lst[0], self._column_id)
        else:
            r_id = self._values_lst[0][self._column_id]

        self.set_by_id(r_id)


class TableviewExt(Tableview):
    """Komponent tabelki generowanej na podstawie danych z bazy"""

    def __init__(self,
                 master=None,
                 coldata: Union[list, tuple] = [],
                 values_ext: Union[list, tuple] = [],
                 column_id: Union[int, str] = None,
                 bootstyle='default',
                 paginated=False,
                 searchable=False,
                 autofit=False,
                 autoalign=True,
                 stripecolor=None,
                 pagesize=10,
                 height=10,
                 delimiter=",",
                 ):
        
        coldata = coldata[:]
        values_ext = values_ext[:]
        
        coldata, rowdata = self._config(coldata, values_ext, column_id)

        """Inicjalizujemy komponent tabeli"""
        Tableview.__init__(self, master=master,
                           bootstyle=bootstyle,
                           coldata=coldata,
                           rowdata=rowdata,
                           paginated=paginated,
                           searchable=searchable,
                           autofit=autofit,
                           autoalign=autoalign,
                           stripecolor=stripecolor,
                           pagesize=pagesize,
                           height=height,
                           delimiter=delimiter)

    def _config(self, coldata, values_ext, column_id) -> (list, list):
        """Konfiguracja kolumn i wierszy do tabelki"""

        coldata = coldata
        rowdata = []
        self._coldata = None
        if type(coldata) in (tuple, list):
            self._coldata = coldata[:]
        self._source_values_data = values_ext[:]
        self._column_id = column_id
        self._column_id_name = column_id

        if len(values_ext) > 0:
            """Sprawdzenie typu danych"""
            first_row = values_ext[0]
            data_type = type(first_row).__name__

            if data_type not in ('tuple', 'list', 'dict', 'Row'):
                raise Exception(f"Niepoprawny typ danych: {data_type}!")

            self._raw_data_type = data_type

            """Obsługa krotek i list"""
            if data_type in ('tuple', 'list'):
                if column_id is not None and type(column_id) != int:
                    raise Exception("Parametr 'column_id' musi być typu liczbowego!")

                if len(coldata) == 0:
                    for i in range(len(first_row)):
                        coldata.append(f'col{i + 1}')
                rowdata = values_ext

            """Obsługa słowników"""
            if data_type == 'dict':
                if len(coldata) == 0:
                    for i in first_row.keys():
                        coldata.append(i)
                for row in values_ext:
                    rowdata.append([])
                    for column in row.keys():
                        rowdata[-1].append(row[column])

                if column_id is not None and type(column_id) == str:
                    i = 0
                    for column in values_ext[0].keys():
                        if column_id == column:
                            column_id = i
                            break
                        i += 1
                    if type(column_id) != int:
                        raise Exception(f"Wskazana kolumna {column_id} nie znajduje się w przekazanych danych!")

            """Obsługa nazwanych krotek"""
            if data_type == 'Row':
                if len(coldata) == 0:
                    for i in first_row._fields:
                        coldata.append(i)
                for row in values_ext:
                    rowdata.append([])
                    for column in row._fields:
                        rowdata[-1].append(getattr(row, column))

                if column_id is not None and type(column_id) == str:
                    i = 0
                    for column in values_ext[0]._fields:
                        if column_id == column:
                            column_id = i
                            break
                        i += 1
                    if type(column_id) != int:
                        raise Exception(f"Wskazana kolumna {column_id} nie znajduje się w przekazanych danych!")

            if column_id is not None and column_id >= len(rowdata[0]):
                raise Exception(
                    f"Parametr 'column_id' spoza zakresu przekazanych danych: {column_id} > {len(rowdata[0])}!")

        self.__column_id = column_id

        return coldata, rowdata

    def _get_raw_data(self, selected_row_id):
        """Pobranie źródłowych danych z bazy (w formie słownika, nazwanych krotek itp)"""

        if self._raw_data_type == 'Row':
            """namedtuples"""
            for i in self._source_values_data:
                if getattr(i, self._column_id_name) == selected_row_id:
                    return i
        elif self._raw_data_type == 'dict':
            """dict"""
            for i in self._source_values_data:
                if i[self._column_id_name] == selected_row_id:
                    return i
        else:
            """lists, tuples"""
            for i in self._source_values_data:
                if i[self._column_id] == selected_row_id:
                    return i

        raise Exception(f"Nie znaleziono źródłowych danych o identyfikatorze: {selected_row_id}!")

    def configure(self, coldata: Union[list, tuple, None] = None, values_ext: Union[list, tuple, None] = None,
                  column_id: Union[int, str] = None, cnf=None,
                  **kwargs):
        """Konfiguracja komponentu"""

        if coldata is not None or values_ext is not None or column_id is not None:
            coldata = coldata if coldata is not None else self._coldata
            values_ext = values_ext if values_ext is not None else self._source_values_data
            column_id = column_id if column_id is not None else self._column_id

            coldata, rowdata = self._config(coldata, values_ext, column_id)
            self.build_table_data(coldata, rowdata)

        Tableview.configure(self, cnf, **kwargs)

    def reload_data(self, values_ext: Union[list, tuple]):
        """Przeładowanie tabeli na podstawie nowego/zaktualizowanego zestawu danych"""

        self.configure(values_ext=values_ext)

    def get_selected_rows(self, only_one_row: bool = False, raw_data: bool = False):
        """Zwrócenie wartości zaznaczonego wiersza/wierszy"""

        if raw_data and self.__column_id is None:
            raise Exception("Dla parametru raw_data=True konieczne jest ustawienie parametru 'column_id'!")

        selected_rows = self.view.selection()

        """Błąd jeśli nic nie zostało zaznaczone"""
        if len(selected_rows) == 0:
            Messagebox.show_error(parent=self, message='Nie zaznaczono żadnego rekordu!',
                                  title='Błąd')
            return

        """Błąd jeśli zaznaczonych jest więcej rekordów a miał być tylko jeden"""
        if only_one_row and len(selected_rows) > 1:
            Messagebox.show_error(parent=self, message='Zaznaczono więcej niż jeden rekord!',
                                  title='Błąd')
            return

        """Zwrócenie jednego rekordu"""
        if only_one_row:
            if raw_data:
                selected_row_id = self.get_row(iid=selected_rows[0]).values[self.__column_id]
                return self._get_raw_data(selected_row_id)
            else:
                return self.get_row(iid=selected_rows[0]).values

        """Zwrócenie wielu rekordów"""
        res_rows = []

        for i in selected_rows:
            if raw_data:
                selected_row_id = self.get_row(iid=i).values[self.__column_id]
                res_rows.append(self._get_raw_data(selected_row_id))
            else:
                res_rows.append(self.get_row(iid=i).values)

        return res_rows

    def get_selected_ids(self, only_one_id: bool = False):
        """Zwrócenie identyfikatorów zaznaczonych rekordów (jeśli ustawiono parametr column_id)"""

        if self.__column_id is None:
            raise Exception("Nie ustawiono parametru 'column_id'!")

        selected_rows = self.get_selected_rows(only_one_id)

        if selected_rows is None:
            return

        """Zwrócenie jednego id"""
        if only_one_id:
            return selected_rows[self.__column_id]

        """Zwrócenie wielu id"""
        res_ids = []

        for i in selected_rows:
            res_ids.append(i[self.__column_id])

        return res_ids
