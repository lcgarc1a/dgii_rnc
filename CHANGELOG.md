# Changelog

## [0.6] - 2024-12-17

### 🐞 Fixes

- Fix `IncompleteRead` error.

## [0.5] - 2024-03-11

### ✨ Enhancements

- Add `web_search` method to open a headless browser to lookup the `Cédula/RNC` numeric string. This new method shows the full available text of the `Actividad Economica` column, and shows the `Administracion Local` column not present in the `search` method

### 🐞 Fixes

- Fix missing rows. Set `quote_char` to `None` in `read_csv()` and remove `.filter(pl.col('x1').is_not_null())`

### 🛠️ Other improvements

- Change `getctime()` to `getmtime()` in the `check_file()` method. The csv file isn't daily updated, so it doesn't make sense to check for creation date. Now it's going to be downloaded once a day when called

- Rename `dgii_search` method to `search`

## [0.4] - 2024-02-21

### 📖 Documentation

- Add `changelog`
- Fix typos in `README.md`

### 🐞 Fixes

- Fix folder structure

[0.4]: https://github.com/lcgarc1a/dgii_rnc/releases/tag/0.4
[0.5]: https://github.com/lcgarc1a/dgii_rnc/releases/tag/0.5
[0.6]: https://github.com/lcgarc1a/dgii_rnc/releases/tag/0.6
