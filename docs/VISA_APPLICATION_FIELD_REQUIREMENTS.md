# Visa Application Field Requirements for Telegram Bot

This document defines the expanded data-collection checklist that the Telegram bot should request from a user before creating a visa-application draft or sending a payload to the FastAPI backend.

> Scope: Germany VIDEX, France VFS Global, and U.S. DS-160 data-collection support. The project remains a safe dry-run / human-in-the-loop scaffold. Do not use this repository to bypass CAPTCHA, anti-bot controls, appointment systems, terms of service, or government/visa-provider access rules.

## Implementation summary

The current bot/backend should move from a minimal field set to country-specific questionnaires. Real forms can require 15-30 fields, including identity data, passport details, residence address, travel purpose, employment/education information, financial support, insurance, previous visas/travel history, and document uploads.

Recommended bot flow:

1. Ask the user to choose the route: `us_ds160`, `germany_videx`, or `france_vfs`.
2. Collect common personal and passport fields first.
3. Collect route-specific fields.
4. Show a review screen and ask the user to confirm.
5. Submit only after confirmation to the dry-run/mock API or a lawful human-in-the-loop workflow.
6. Store the returned `application_number` against `user_id`.

Recommended validation defaults:

| Field type | Validation rule |
|---|---|
| Dates | `YYYY-MM-DD` |
| Country codes | ISO 3166-1 alpha-2, for example `DE`, `FR`, `RU`, `US` |
| Passport number | Alphanumeric; Schengen examples use 6-9 symbols; DS-160 examples use 9 symbols |
| Phone | International format, for example `+4915112345678` |
| Email | Standard email format |
| Schengen stay length | `1-90` days |
| U.S. intended stay length | up to `365` days in the current data brief |
| Text input for portals | Prefer Latin characters/transliteration where the portal requires Latin input |

## 1. Germany — VIDEX field set

Context: Germany VIDEX / national visa route, generally long-stay `>90` days in the provided brief.

| # | Bot/API field key | Field label | Required | Format / allowed values | Example | Portal selector / block |
|---:|---|---|---|---|---|---|
| 1 | `surname` | Surname / Фамилия | Yes | Latin text | `Müller` | `#surname` |
| 2 | `given_name` | Given name / Имя | Yes | Latin text | `Anna` | `#givenName` |
| 3 | `other_names` | Other names / Отчество | No | Latin text | `Petrovich` | `#otherNames` |
| 4 | `sex` | Sex / Пол | Yes | `M` or `F` | `F` | `#sex` |
| 5 | `birth_date` | Date of birth / Дата рождения | Yes | `YYYY-MM-DD` | `1992-05-12` | `#dateOfBirth` |
| 6 | `place_of_birth_country` | Place of birth / Место рождения | Yes | ISO country code | `RU` | `#cityOfBirthCountry` |
| 7 | `passport_number` | Passport number / Номер паспорта | Yes | Alphanumeric, 6-9 symbols | `C1234567` | `#passportNumber` |
| 8 | `passport_issuing_country` | Passport issuing country / Страна выдачи | Yes | ISO country code | `DE` | `#passportIssuingCountry` |
| 9 | `passport_expiration` | Passport expiration date / Срок действия | Yes | `YYYY-MM-DD`; at least 3 months after planned exit | `2030-12-31` | `#passportExpirationDate` |
| 10 | `nationality` | Nationality / Гражданство | Yes | ISO country code | `DE` | `#nationality` |
| 11 | `address` | Current address / Текущий адрес | Yes | Latin text | `Musterstraße 12` | `#streetAddress` |
| 12 | `city` | City / Город | Yes | Latin text | `Berlin` | `#cityTown` |
| 13 | `zip_code` | Zip / Почтовый индекс | Yes | 5 digits for the example flow | `10115` | `#zipCode` |
| 14 | `country` | Country of residence / Страна проживания | Yes | ISO country code | `DE` | `#country` |
| 15 | `phone` | Phone number / Телефон | Yes | International format | `+4915112345678` | `#phoneNumber` |
| 16 | `email` | E-mail address / Электронная почта | Yes | Email | `anna.mueller@example.com` | `#emailAddress` |
| 17 | `purpose` | Purpose of travel / Цель поездки | Yes | `tourism`, `business`, `study`, `family`, `other` | `tourism` | `#purposeOfTravel` |
| 18 | `arrival_date` | Intended date of arrival / Планируемая дата въезда | Yes | `YYYY-MM-DD` | `2026-09-15` | `#intendedDateOfArrival` |
| 19 | `stay_length` | Intended length of stay / Планируемая длительность | Yes | Number of days | `14` | `#intendedLengthOfStay` |
| 20 | `occupation` | Occupation / Профессия | Yes | Controlled list, for example `student`, `employee`, `unemployed` | `student` | `#occupation` |
| 21 | `employer_name` | Employer / Работодатель | No | Organization name | `University of Berlin` | `#employerName` |
| 22 | `financial_means` | Financial means / Финансовые средства | Yes | Free text / structured notes | `Bank account, EUR 5 000` | Financial information block |
| 23 | `travel_insurance` | Travel insurance | Yes | Yes/no plus policy number | `Yes, 123456789` | Insurance block |
| 24 | `previous_schengen_visas` | Previous Schengen visas | No | List/details | `DE-2018-AB1234` | Previous visas block |
| 25 | `document_uploads` | Document upload | Yes | Passport scan, photo, insurance; PDF/JPG | `passport.pdf` | `#documentUpload` |

### Germany VIDEX sample payload

```json
{
  "user_id": "987654321",
  "target_country": "germany",
  "surname": "Muller",
  "given_name": "Anna",
  "other_names": "Petrovich",
  "sex": "F",
  "birth_date": "1992-05-12",
  "place_of_birth_country": "RU",
  "passport_number": "C1234567",
  "passport_issuing_country": "DE",
  "passport_expiration": "2030-12-31",
  "nationality": "DE",
  "address": "Musterstrasse 12",
  "city": "Berlin",
  "zip_code": "10115",
  "country": "DE",
  "phone": "+4915112345678",
  "email": "anna.mueller@example.com",
  "purpose": "tourism",
  "arrival_date": "2026-09-15",
  "stay_length": 14,
  "occupation": "student",
  "employer_name": "University of Berlin",
  "financial_means": "Bank account, EUR 5 000",
  "travel_insurance": "Yes, 123456789",
  "previous_schengen_visas": "DE-2018-AB1234"
}
```

## 2. France — VFS Global field set

Context: France VFS Global / Schengen short-stay route, generally up to 90 days in the provided brief.

| # | Bot/API field key | Field label | Required | Format / allowed values | Example |
|---:|---|---|---|---|---|
| 1 | `surname` | Surname | Yes | Latin text | `Dupont` |
| 2 | `given_name` | Given name | Yes | Latin text | `Jean` |
| 3 | `birth_date` | Date of birth | Yes | `YYYY-MM-DD` | `1990-02-28` |
| 4 | `place_of_birth_country` | Place of birth | Yes | ISO country code | `FR` |
| 5 | `passport_number` | Passport number | Yes | Alphanumeric, 6-9 symbols | `AB1234567` |
| 6 | `passport_issuing_country` | Passport issuing country | Yes | ISO country code | `FR` |
| 7 | `passport_expiration` | Passport expiry | Yes | `YYYY-MM-DD` | `2031-06-30` |
| 8 | `nationality` | Nationality | Yes | ISO country code | `FR` |
| 9 | `address` | Current address | Yes | Latin text | `12 Rue de Paris` |
| 10 | `city` | City | Yes | Latin text | `Paris` |
| 11 | `zip_code` | Zip / Postal code | Yes | 5 digits for the example flow | `75001` |
| 12 | `country` | Country of residence | Yes | ISO country code | `FR` |
| 13 | `phone` | Phone | Yes | International format | `+33612345678` |
| 14 | `email` | E-mail | Yes | Email | `jean.dupont@example.fr` |
| 15 | `purpose` | Purpose of travel | Yes | `tourism`, `business`, `visiting_family_friends`, `cultural`, `sport`, `official`, `other` | `tourism` |
| 16 | `arrival_date` | Intended arrival date | Yes | `YYYY-MM-DD` | `2026-07-10` |
| 17 | `stay_length` | Intended stay (days) | Yes | `1-90` | `10` |
| 18 | `number_of_entries` | Number of entries | Yes | `single`, `multiple` | `multiple` |
| 19 | `occupation` | Occupation | Yes | Controlled list | `employee` |
| 20 | `employer_or_school` | Employer / School | No | Organization name | `SNCF` |
| 21 | `annual_income_eur` | Annual income | No | Amount in EUR | `30000` |
| 22 | `travel_insurance` | Travel insurance | Yes | Yes/no plus policy number | `Yes - 123456789` |
| 23 | `previous_schengen_visas` | Previous Schengen visas | No | Yes/no plus details | `Yes - DE-2019-XY9876` |
| 24 | `document_uploads` | Document uploads | Yes | Passport, 35x45mm photo, insurance, bank statements | `passport.pdf` |
| 25 | `consulate` | Consulate / Embassy | Yes | Consulate by place of residence | `Paris Consulate` |

### France VFS sample payload

```json
{
  "user_id": "987654321",
  "target_country": "france",
  "surname": "Dupont",
  "given_name": "Jean",
  "birth_date": "1990-02-28",
  "place_of_birth_country": "FR",
  "passport_number": "AB1234567",
  "passport_issuing_country": "FR",
  "passport_expiration": "2031-06-30",
  "nationality": "FR",
  "address": "12 Rue de Paris",
  "city": "Paris",
  "zip_code": "75001",
  "country": "FR",
  "phone": "+33612345678",
  "email": "jean.dupont@example.fr",
  "purpose": "tourism",
  "arrival_date": "2026-07-10",
  "stay_length": 10,
  "number_of_entries": "multiple",
  "occupation": "employee",
  "employer_or_school": "SNCF",
  "annual_income_eur": 30000,
  "travel_insurance": "Yes - 123456789",
  "previous_schengen_visas": "Yes - DE-2019-XY9876",
  "consulate": "Paris Consulate"
}
```

## 3. United States — DS-160 field set

Context: U.S. DS-160 nonimmigrant visa application data-collection support.

| # | Bot/API field key | Field label | Required | Format / allowed values | Example |
|---:|---|---|---|---|---|
| 1 | `surname` | Surname | Yes | Latin text | `Smith` |
| 2 | `given_name` | Given name | Yes | Latin text | `John` |
| 3 | `other_names` | Other names | No | Latin text | `Edward` |
| 4 | `sex` | Sex | Yes | `M` or `F` | `M` |
| 5 | `birth_date` | Date of birth | Yes | `YYYY-MM-DD` | `1985-04-12` |
| 6 | `place_of_birth` | Place of birth | Yes | City, country in Latin characters | `Chicago, United States` |
| 7 | `nationality` | Nationality | Yes | ISO country code | `US` |
| 8 | `passport_number` | Passport number | Yes | Alphanumeric; brief example uses 9 symbols | `123456789` |
| 9 | `passport_issuance_date` | Passport issuance date | Yes | `YYYY-MM-DD` | `2015-05-01` |
| 10 | `passport_expiration` | Passport expiration date | Yes | `YYYY-MM-DD`; at least 6 months in the brief | `2025-05-01` |
| 11 | `home_address` | Home address | Yes | Full address in Latin characters | `123 Main St, Apt 4B, New York, NY 10001, USA` |
| 12 | `phone` | Phone number | Yes | International format | `+12125551234` |
| 13 | `email` | Email address | Yes | Email | `john.smith@example.com` |
| 14 | `passport_book_number` | Passport Book Number | No | Passport book identifier, if available | `AB1234567` |
| 15 | `purpose` | Travel purpose | Yes | `tourism`, `business`, `student`, `exchange`, `medical`, `other` | `tourism` |
| 16 | `arrival_date` | Intended date of arrival | Yes | `YYYY-MM-DD` | `2026-08-20` |
| 17 | `stay_length` | Intended length of stay | Yes | Number of days, max `365` in the brief | `30` |
| 18 | `previous_us_travel` | Previous U.S. travel | No | Yes/no plus dates/types | `Yes - B2-2018-06-15` |
| 19 | `us_contact_person` | U.S. contact person | Yes | Name, organization, phone | `Acme Corp, +1 212 555 0000` |
| 20 | `family_members_in_us` | Family members in U.S. | Yes | Yes/no plus relationship type | `No` |
| 21 | `work_education` | Work/Education | Yes | `student`, `employee`, `self-employed`, `unemployed` | `employee` |

### DS-160 sample payload

```json
{
  "user_id": "987654321",
  "surname": "Smith",
  "given_name": "John",
  "other_names": "Edward",
  "sex": "M",
  "birth_date": "1985-04-12",
  "place_of_birth": "Chicago, United States",
  "nationality": "US",
  "passport_number": "123456789",
  "passport_issuance_date": "2015-05-01",
  "passport_expiration": "2025-05-01",
  "home_address": "123 Main St, Apt 4B, New York, NY 10001, USA",
  "phone": "+12125551234",
  "email": "john.smith@example.com",
  "passport_book_number": "AB1234567",
  "purpose": "tourism",
  "arrival_date": "2026-08-20",
  "stay_length": 30,
  "previous_us_travel": "Yes - B2-2018-06-15",
  "us_contact_person": "Acme Corp, +1 212 555 0000",
  "family_members_in_us": "No",
  "work_education": "employee"
}
```

## 4. Recommended Telegram bot questionnaire structure

### Step 1 — Route selection

```text
Which application route do you want to prepare?
1. Germany — VIDEX
2. France — VFS Global
3. United States — DS-160
```

Save the selected route as one of:

```text
visa_route = germany_videx | france_vfs | us_ds160
```

### Step 2 — Common identity block

Ask these fields for all routes where applicable:

```text
surname
given_name
other_names
sex
birth_date
nationality
passport_number
passport_issuing_country
passport_expiration
phone
email
```

### Step 3 — Residence and travel block

Ask these fields for Schengen/VIDEX routes:

```text
address
city
zip_code
country
purpose
arrival_date
stay_length
occupation
```

For DS-160, ask:

```text
home_address
purpose
arrival_date
stay_length
previous_us_travel
us_contact_person
family_members_in_us
work_education
```

### Step 4 — Extra country-specific block

Germany VIDEX:

```text
place_of_birth_country
employer_name
financial_means
travel_insurance
previous_schengen_visas
document_uploads
```

France VFS:

```text
place_of_birth_country
number_of_entries
employer_or_school
annual_income_eur
travel_insurance
previous_schengen_visas
document_uploads
consulate
```

U.S. DS-160:

```text
place_of_birth
passport_issuance_date
passport_book_number
```

## 5. Data handling and privacy notes

Visa payloads contain highly sensitive personal data. The bot/backend should treat them as sensitive PII.

Minimum implementation notes:

- Do not log full passport numbers, addresses, phone numbers, or document-upload filenames in plaintext logs.
- Mask sensitive fields in debug logs, for example `C123****`.
- Store payloads encrypted at rest if a database is used.
- Use short retention periods for uploaded files.
- Keep document uploads out of public buckets.
- Add explicit user confirmation before sending data to any external system.
- Add a manual-review step before any production submission workflow.

## 6. Suggested repository integration

Recommended file location:

```text
docs/VISA_APPLICATION_FIELD_REQUIREMENTS.md
```

Recommended README link:

```markdown
- [Visa application field requirements](docs/VISA_APPLICATION_FIELD_REQUIREMENTS.md)
```

This keeps the requirement research separate from the API implementation and gives the colleague building the Telegram bot a clear field checklist.
