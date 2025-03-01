# Greek text to Greek Braille STL converter / Μετατροπέας ελληνικού κειμένου σε STL με κώδικα Μπράιγ

Αυτό είναι απλά ένα project που έφτιαξα για το σχολείο. Δέχεται ένα περιορισμένο εύρος χαρακτήρων, οπότε μην περιμένετε και πάρα πολλά

## Installation / Εγκατάσταση

1) Κατεβάστε την Python 3
2) (Προαιρετικό) Φτιάξτε ένα venv ώστε να μην γεμίσετε το global environment το υπολογιστή σας με προγράμματα που δεν θέλετε
3) `python3 -m pip install -r requirements.txt`
4) Είστε έτοιμοι

## Usage / Χρήση

```txt
$ python3 src/main.py  --help
usage: GRBrailleSTL [-h] [-r RADIUS] [--height HEIGHT] text dest

Ένα απλό πρόγραμμα μετατροπής κειμένου σε κώδικα Μπράιγ σε STL

positional arguments:
  text                  Το κείμενο που θέλετε να μεταφραστεί
  dest                  Η τοποθεσία του αρχείου εξόδου

options:
  -h, --help            show this help message and exit
  -r RADIUS, --radius RADIUS
                        Η ακτίνα των κουκίδων
  --height HEIGHT       Το συνολικό ύψος του STL μοντέλου
```

## License / Άδεια χρήσης

MIT
