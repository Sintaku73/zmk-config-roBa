# zmk-config-roBa

## convert_us2jis.py

### Usage

```mermaid
flowchart LR
rb[roBa]
kme[Keymap Editor]
bf[Build firmware]
rb--us2jis-->kme
kme--jis2us-->bf
bf--Flash-->rb
```
