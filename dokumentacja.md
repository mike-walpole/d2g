# Dokumentacja Deploymentu - Dock2Gdansk (d2g)

Niniejszy dokument opisuje proces wdrożenia aplikacji Dock2Gdansk na własnej infrastrukturze AWS oraz platformie Vercel.

## Spis Treści

1. [Wymagania Wstępne](#wymagania-wstępne)
2. [Konfiguracja Konta AWS](#konfiguracja-konta-aws)
3. [Deploy Infrastruktury AWS](#deploy-infrastruktury-aws)
4. [Konfiguracja Cloudflare Turnstile (CAPTCHA)](#konfiguracja-cloudflare-turnstile-captcha)
5. [Deploy Aplikacji na Vercel](#deploy-aplikacji-na-vercel)
6. [Konfiguracja Po Deploymencie](#konfiguracja-po-deploymencie)
7. [Inicjalizacja Danych](#inicjalizacja-danych)
8. [Zarządzanie Użytkownikami](#zarządzanie-użytkownikami)
9. [Troubleshooting](#troubleshooting)

---

## Wymagania Wstępne

### Narzędzia

Przed rozpoczęciem należy zainstalować następujące narzędzia:

- **Node.js** (wersja 18 lub nowsza): [https://nodejs.org/](https://nodejs.org/)
- **Python** (wersja 3.11 lub nowsza): [https://www.python.org/](https://www.python.org/)
- **AWS CLI**: [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)
- **AWS CDK**: `npm install -g aws-cdk`
- **Git**: [https://github.com/](https://github.com/)

### Konta

Potrzebne będą następujące konta:

- **Konto AWS** z uprawnieniami administratora
- **Konto Vercel**: [https://vercel.com/](https://vercel.com/)
- **Konto Cloudflare** (do CAPTCHA Turnstile): [https://cloudflare.com/](https://cloudflare.com/)

### Weryfikacja Instalacji

```bash
# Sprawdź wersje zainstalowanych narzędzi
node --version          # Powinno wyświetlić v18.x lub nowszą
python3 --version       # Powinno wyświetlić 3.11.x lub nowszą
aws --version           # AWS CLI
cdk --version           # AWS CDK
```

---

## Konfiguracja Konta AWS

### 1. Konfiguracja AWS CLI

```bash
# Uruchom konfigurację AWS CLI
aws configure

# Wprowadź dane:
# AWS Access Key ID: [Twój Access Key]
# AWS Secret Access Key: [Twój Secret Key]
# Default region name: ap-east-1
# Default output format: json
```

**WAŻNE**: Aplikacja domyślnie używa regionu **ap-east-1** (Hong Kong). Możesz zmienić region w pliku `infra/app.py`, ale upewnij się, że wszystkie serwisy AWS są dostępne w wybranym regionie.

### 2. Weryfikacja Dostępu

```bash
# Sprawdź, czy masz dostęp do AWS
aws sts get-caller-identity
```

Powinno zwrócić informacje o Twoim koncie AWS.

### 3. Bootstrap AWS CDK

CDK wymaga jednorazowego bootstrapu w każdym regionie:

```bash
# Bootstrap CDK w regionie ap-east-1
cdk bootstrap aws://ACCOUNT-ID/ap-east-1
```

Zastąp `ACCOUNT-ID` swoim numerem konta AWS (można go uzyskać z poprzedniej komendy).

---

## Deploy Infrastruktury AWS

### 1. Przygotowanie Środowiska

```bash
# Przejdź do katalogu infra
cd infra

# Utwórz virtual environment dla Python
python3 -m venv venv

# Aktywuj virtual environment
# Na macOS/Linux:
source venv/bin/activate
# Na Windows:
# venv\Scripts\activate

# Zainstaluj wymagane pakiety
pip install -r requirements.txt
```

### 2. Przegląd Infrastruktury

Stack AWS CDK utworzy następujące zasoby:

- **DynamoDB Tables**:
  - `d2g-form-submissions` - przechowuje zgłoszenia formularzy
  - `d2g-form-schemas` - przechowuje schematy formularzy i konfigurację

- **Cognito User Pool**:
  - `d2g-user-pool` - zarządzanie użytkownikami i autentykacja
  - Grupa `admin` - dla użytkowników z dostępem do panelu kapitanat

- **Lambda Functions**:
  - `d2g-submit-form` - obsługa zgłoszeń formularzy
  - `d2g-get-schema` - pobieranie schematów formularzy
  - `d2g-get-config` - pobieranie konfiguracji i tłumaczeń
  - `d2g-manage-schema` - zarządzanie schematami (CRUD)
  - `d2g-admin-kapitanat` - panel administracyjny

- **API Gateway**: HTTP API z endpointami REST

### 3. Deploy Stack

```bash
# Upewnij się, że jesteś w katalogu infra z aktywnym venv

# Zsyntetyzuj stack (opcjonalnie, aby sprawdzić konfigurację)
cdk synth

# Deploy stack
cdk deploy

# CDK wyświetli zmiany i poprosi o potwierdzenie
# Wpisz 'y' i naciśnij Enter
```

### 4. Zapisz Outputy

Po zakończeniu deployu CDK wyświetli ważne wartości:

```
Outputs:
D2GStack.ApiEndpoint = https://xxxxxxxxxx.execute-api.ap-east-1.amazonaws.com
D2GStack.UserPoolId = ap-east-1_xxxxxxxxx
D2GStack.UserPoolClientId = xxxxxxxxxxxxxxxxxxxxxxxxxx
D2GStack.DynamoDBTableName = d2g-form-submissions
D2GStack.SchemasTableName = d2g-form-schemas
```

**Zapisz te wartości** - będą potrzebne do konfiguracji aplikacji frontend.

### 5. Weryfikacja Deployu

```bash
# Sprawdź, czy API działa
curl https://TWOJ-API-ENDPOINT/config?type=all&lang=en

# Powinieneś otrzymać odpowiedź JSON (może być pusta na początku)
```

---

## Konfiguracja Cloudflare Turnstile (CAPTCHA)

Aplikacja używa Cloudflare Turnstile do ochrony formularzy przed botami.

### 1. Utwórz Widget Turnstile

1. Zaloguj się na [https://dash.cloudflare.com/](https://dash.cloudflare.com/)
2. Przejdź do **Turnstile**
3. Kliknij **Add Site**
4. Wprowadź:
   - **Site Name**: Dock2Gdansk
   - **Domain**: Twoja domena Vercel (np. `d2g.vercel.app`) lub własna domena
   - **Widget Mode**: Managed (zalecane)
5. Kliknij **Create**

### 2. Zapisz Klucze

Po utworzeniu otrzymasz:
- **Site Key** (Public) - dla aplikacji frontend
- **Secret Key** (Private) - dla backend

---

## Deploy Aplikacji na Vercel

### 1. Przygotowanie Projektu

```bash
# Wróć do głównego katalogu projektu
cd ..

# Zainstaluj zależności Node.js
npm install
```

### 2. Konfiguracja Zmiennych Środowiskowych

Utwórz plik `.env` w głównym katalogu projektu:

```bash
# Cloudflare Turnstile CAPTCHA
PUBLIC_TURNSTILE_SITE_KEY=twoj-site-key-z-cloudflare
TURNSTILE_SECRET_KEY=twoj-secret-key-z-cloudflare
```

**UWAGA**: Plik `.env` jest w `.gitignore` i nie powinien być commitowany do repozytorium.

### 3. Aktualizacja API Endpoint

Edytuj plik `src/lib/stores/config.js` i zaktualizuj `apiBaseUrl`:

```javascript
// Zamień na swój API Gateway endpoint z outputów CDK
export let apiBaseUrl = $state('https://TWOJ-API-ENDPOINT');
```

### 4. Deploy na Vercel

#### Opcja A: Za pomocą CLI Vercel

```bash
# Zainstaluj Vercel CLI
npm install -g vercel

# Zaloguj się do Vercel
vercel login

# Deploy
vercel

# Postępuj zgodnie z instrukcjami:
# - Set up and deploy? Y
# - Which scope? (wybierz swoje konto)
# - Link to existing project? N
# - What's your project's name? d2g
# - In which directory is your code located? ./
# - Auto-detected SvelteKit. Continue? Y
# - Want to modify settings? N

# Po zakończeniu otrzymasz URL preview
# Aby zdeployować do produkcji:
vercel --prod
```

#### Opcja B: Za pomocą Dashboard Vercel

1. Zaloguj się na [https://vercel.com/](https://vercel.com/)
2. Kliknij **Add New Project**
3. Importuj repozytorium Git lub upload folder
4. Skonfiguruj:
   - **Framework Preset**: SvelteKit
   - **Root Directory**: `./`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.svelte-kit` (automatycznie)
5. Dodaj **Environment Variables**:
   - `PUBLIC_TURNSTILE_SITE_KEY`: Twój Site Key z Cloudflare
   - `TURNSTILE_SECRET_KEY`: Twój Secret Key z Cloudflare
6. Kliknij **Deploy**

### 5. Weryfikacja Deploymentu

Po zakończeniu deployu:

1. Odwiedź URL aplikacji (np. `https://d2g.vercel.app`)
2. Sprawdź, czy strona się ładuje
3. Sprawdź konsolę przeglądarki (F12) pod kątem błędów

---

## Konfiguracja Po Deploymencie

### 1. Aktualizacja CORS w API Gateway

Jeśli masz własną domenę, zaktualizuj konfigurację CORS w `infra/d2g_stack.py`:

```python
cors_preflight=apigatewayv2.CorsPreflightOptions(
    allow_headers=["Content-Type", "Authorization"],
    allow_methods=[apigatewayv2.CorsHttpMethod.ANY],
    allow_origins=["https://twoja-domena.com"],  # Zmień na swoją domenę
    max_age=Duration.days(1)
)
```

Następnie ponownie zdeployuj stack:

```bash
cd infra
source venv/bin/activate
cdk deploy
```

### 2. Konfiguracja Własnej Domeny (Opcjonalnie)

#### W Vercel:

1. Przejdź do **Project Settings** → **Domains**
2. Dodaj swoją domenę
3. Skonfiguruj rekordy DNS zgodnie z instrukcjami Vercel

#### Aktualizacja Turnstile:

1. Wróć do Cloudflare Dashboard → Turnstile
2. Edytuj swój widget
3. Dodaj nową domenę do listy dozwolonych

---

## Inicjalizacja Danych

### 1. Tworzenie Pierwszego Użytkownika Admin

```bash
# Ustaw zmienne środowiskowe
export USER_POOL_ID=ap-east-1_xxxxxxxxx  # Z outputów CDK
export AWS_DEFAULT_REGION=ap-east-1

# Utwórz użytkownika
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username admin@twojadomena.com \
  --user-attributes Name=email,Value=admin@twojadomena.com Name=email_verified,Value=true \
  --temporary-password TymczasoweHaslo123! \
  --message-action SUPPRESS

# Dodaj użytkownika do grupy admin
aws cognito-idp admin-add-user-to-group \
  --user-pool-id $USER_POOL_ID \
  --username admin@twojadomena.com \
  --group-name admin
```

### 2. Zaloguj się i Zmień Hasło

1. Przejdź do `https://twoja-domena.vercel.app/kapitanat`
2. Zaloguj się używając:
   - Email: `admin@twojadomena.com`
   - Hasło: `TymczasoweHaslo123!`
3. System poprosi o zmianę hasła - ustaw nowe bezpieczne hasło

### 3. Dodanie Początkowych Danych Konfiguracyjnych

#### Opcja A: Za pomocą AWS CLI

```bash
# Ustaw zmienną środowiskową
export SCHEMAS_TABLE="d2g-form-schemas"

# Dodaj przykładową konfigurację
aws dynamodb put-item \
  --table-name $SCHEMAS_TABLE \
  --item '{
    "formId": {"S": "config"},
    "version": {"S": "1.0"},
    "data": {"M": {
      "cargoTypes": {"L": [
        {"S": "Container"},
        {"S": "Bulk"},
        {"S": "Break Bulk"},
        {"S": "Ro-Ro"}
      ]},
      "translations": {"M": {
        "en": {"M": {
          "welcome": {"S": "Welcome to Dock2Gdansk"},
          "submitForm": {"S": "Submit Form"}
        }},
        "zh": {"M": {
          "welcome": {"S": "欢迎来到格但斯克码头"},
          "submitForm": {"S": "提交表格"}
        }}
      }}
    }},
    "createdAt": {"S": "2025-01-15T00:00:00Z"},
    "updatedAt": {"S": "2025-01-15T00:00:00Z"}
  }'
```

#### Opcja B: Za pomocą Panelu Kapitanat

1. Zaloguj się do panelu kapitanat
2. Użyj interfejsu do zarządzania schematami formularzy i konfiguracją
3. Dodaj typy ładunków, tłumaczenia i inne dane konfiguracyjne

### 4. Weryfikacja

```bash
# Sprawdź, czy dane zostały dodane
curl "https://TWOJ-API-ENDPOINT/config?type=all&lang=en"
```

Powinieneś otrzymać konfigurację z dodanymi danymi.

---

## Zarządzanie Użytkownikami

### Dodawanie Nowych Użytkowników Admin

```bash
export USER_POOL_ID=ap-east-1_xxxxxxxxx
export AWS_DEFAULT_REGION=ap-east-1

# Utwórz użytkownika
aws cognito-idp admin-create-user \
  --user-pool-id $USER_POOL_ID \
  --username nowy.admin@domena.com \
  --user-attributes Name=email,Value=nowy.admin@domena.com Name=email_verified,Value=true \
  --temporary-password TymczasoweHaslo456!

# Dodaj do grupy admin
aws cognito-idp admin-add-user-to-group \
  --user-pool-id $USER_POOL_ID \
  --username nowy.admin@domena.com \
  --group-name admin
```

### Usuwanie Użytkowników

```bash
aws cognito-idp admin-delete-user \
  --user-pool-id $USER_POOL_ID \
  --username uzytkownik@domena.com
```

### Lista Użytkowników

```bash
aws cognito-idp list-users \
  --user-pool-id $USER_POOL_ID
```

---

## Troubleshooting

### Problem: CDK Deploy kończy się błędem

**Rozwiązanie:**

```bash
# Sprawdź logi
cdk synth --verbose

# Upewnij się, że region jest poprawnie skonfigurowany
aws configure get region

# Sprawdź, czy masz wystarczające uprawnienia
aws iam get-user
```

### Problem: API zwraca błąd 502 lub 503

**Możliwe przyczyny:**

1. Lambda function timeout - zwiększ timeout w `d2g_stack.py`
2. Brak uprawnień Lambda do DynamoDB - sprawdź IAM policies
3. Błąd w kodzie Lambda - sprawdź CloudWatch Logs

**Sprawdź logi Lambda:**

```bash
# Lista log groups
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/d2g

# Wyświetl najnowsze logi
aws logs tail /aws/lambda/d2g-submit-form --follow
```

### Problem: CORS Error w przeglądarce

**Rozwiązanie:**

1. Sprawdź konfigurację CORS w `d2g_stack.py`
2. Upewnij się, że domena Vercel jest w `allow_origins`
3. Ponownie zdeployuj stack: `cdk deploy`

### Problem: Cloudflare Turnstile nie działa

**Rozwiązanie:**

1. Sprawdź, czy `PUBLIC_TURNSTILE_SITE_KEY` jest poprawnie ustawiony w Vercel
2. Sprawdź, czy domena Vercel jest dodana w ustawieniach Turnstile w Cloudflare
3. Sprawdź konsolę przeglądarki pod kątem błędów

### Problem: Nie można zalogować się do panelu kapitanat

**Rozwiązanie:**

1. Sprawdź, czy użytkownik istnieje:
   ```bash
   aws cognito-idp admin-get-user \
     --user-pool-id $USER_POOL_ID \
     --username twoj@email.com
   ```

2. Sprawdź, czy użytkownik jest w grupie admin:
   ```bash
   aws cognito-idp admin-list-groups-for-user \
     --user-pool-id $USER_POOL_ID \
     --username twoj@email.com
   ```

3. Zresetuj hasło:
   ```bash
   aws cognito-idp admin-set-user-password \
     --user-pool-id $USER_POOL_ID \
     --username twoj@email.com \
     --password NoweHaslo123! \
     --permanent
   ```

### Problem: Formularz nie wysyła danych

**Rozwiązanie:**

1. Sprawdź Network tab w DevTools (F12)
2. Sprawdź, czy API endpoint jest poprawny w `config.js`
3. Sprawdź CloudWatch Logs dla Lambda `d2g-submit-form`
4. Sprawdź, czy schemat formularza istnieje w DynamoDB

---

## Koszty i Maintenance

### Szacunkowe Koszty AWS (niski ruch)

- **DynamoDB**: Pay-per-request (~$1-5/miesiąc)
- **Lambda**: Free tier obejmuje 1M requestów/miesiąc
- **API Gateway**: Free tier obejmuje 1M wywołań/miesiąc
- **Cognito**: Free tier do 50,000 MAU
- **CloudWatch Logs**: ~$0.50-2/miesiąc

**Całkowity szacunek**: $2-10/miesiąc dla małego ruchu

### Koszty Vercel

- **Hobby Plan**: $0/miesiąc (z limitami)
- **Pro Plan**: $20/miesiąc (dla produkcji)

### Backup i Recovery

#### Backup DynamoDB

AWS Point-in-Time Recovery jest włączony automatycznie. Możesz także tworzyć snapshoty:

```bash
# Utwórz backup
aws dynamodb create-backup \
  --table-name d2g-form-submissions \
  --backup-name d2g-backup-$(date +%Y%m%d)
```

#### Restore z Backupu

```bash
aws dynamodb restore-table-from-backup \
  --target-table-name d2g-form-submissions-restored \
  --backup-arn arn:aws:dynamodb:region:account-id:table/d2g-form-submissions/backup/01234567890
```

### Monitoring

Zalecane monitorowanie:

1. **CloudWatch Alarms** dla:
   - Lambda errors
   - API Gateway 5xx errors
   - DynamoDB throttling

2. **Vercel Analytics** dla:
   - Page load times
   - Deployment status
   - Error tracking

---

## Usuwanie Infrastruktury

Jeśli chcesz całkowicie usunąć zasoby AWS:

```bash
cd infra
source venv/bin/activate

# UWAGA: To usunie wszystkie dane!
cdk destroy

# Potwierdź usunięcie wpisując 'y'
```

**UWAGA**: Przed usunięciem upewnij się, że masz backup danych z DynamoDB!

---

## Wsparcie i Kontakt

W przypadku problemów:

1. Sprawdź sekcję [Troubleshooting](#troubleshooting)
2. Sprawdź logi w AWS CloudWatch
3. Sprawdź deployment logs w Vercel
4. Skontaktuj się z zespołem programistów projektu

---

## Changelog

- **v1.0**: Pierwsza wersja dokumentacji
