# Filmbot

http://mhawryluk.pythonanywhere.com/

## Opis
Stworzony chatbot pełni rolę konsultanta firmy zajmującej się dystrybucją i oceną filmów. Potrafi znajdować informacje o pozycjach filmowych, jak również o celebrytach – aktorach i nie tylko.

## Użyte narzędzia
Bot został utworzony z wykorzystaniem platformy Dialogflow od Google. Integracja z zewnętrznymi API wymagała napisania własnego miniserwera, do czego posłużył moduł Flask do języka Python.

## Implementacja


### Interakcje
Na tę chwilę bot ma zdefiniowanych 30 interakcji, z których część korzysta z zewnętrznych API do udzielenia odpowiedzi.

### Encje
Dialogflow nie udostępnia typu encji będącego tytułem filmu, dlatego zdefiniowałem własny. Nazwa filmu jest rozpoznawana wyłącznie przez obecność cudzysłowu. Jest to pewien kompromis, innym rozwiązaniem byłoby dodatkowe uczenie sieci neuronowej sterującej botem rozpoznawania nazw filmów, jednak do tego potrzebne byłyby dane dużej wielkości i znaczny nakład obliczeniowy. 


## Integracja z API
Chatbot korzysta z dwóch zewnętrznych interfejsów:

* IMDB - Internet Movie Database (Unofficial) - znajduje informacje o wybranym filmie: rok produkcji, obsada, długość trwania, ocena na IMDB. Zna sporo polskich filmów, ale nie wszystkie.
* Celebrity By API-Ninjas – znajduje informacje o sławnych osobach.
  

## Przykład
<img width="723" alt="screenshot" src="https://user-images.githubusercontent.com/70582973/156233072-ee09788f-3f28-4d3c-b1ac-97a35a9386c7.png">
