## Instrukcja uruchomienia symulacji

W celu uruchomienia symulacji należy wykonać następujące kroki:

1. **Pobranie kodu z repozytorium:**
   - Klonowanie repozytorium za pomocą polecenia:  
     ```bash
     git clone https://github.com/jakub-szafranski/praca-inzynierska.git
     ```
   - Przejście do katalogu projektu:  
     ```bash
     cd praca-inzynierska
     ```

2. **Sprawdzenie wersji Pythona:**
   - Wykonanie polecenia:  
     ```bash
     python3 --version
     ```
     Należy upewnić się, że wyświetlona wersja to 3.11.6.

3. **Tworzenie środowiska wirtualnego:**
   - Wykonanie polecenia:  
     ```bash
     python3 -m venv venv
     ```

4. **Aktywacja środowiska wirtualnego:**
   - Na Windows:  
     ```bash
     .\venv\Scripts\activate
     ```
   - Na Linux:  
     ```bash
     source venv/bin/activate
     ```

5. **Instalacja zależności:**
   - Wykonanie polecenia:  
     ```bash
     pip install -r requirements.txt
     ```

6. **Konfiguracja parametrów środowiska:**
   - W pliku `config.yml` należy dostosować parametry symulacji lub pozostawić domyślne.

7. **Uruchomienie programu:**
   - Wykonanie polecenia:  
     ```bash
     python3 main.py
     ```
