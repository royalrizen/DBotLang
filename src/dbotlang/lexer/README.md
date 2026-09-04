<div align="center">
  
<img src="https://github.com/royalrizen/DBotLang/blob/28684be2a4421e8efb2355e55980c34452b658b9/assets/logo.png" alt="DBotLang Logo" width="150">

# DBotLang Lexer

The lexer converts DBotLang source code into **tokens** for the parser.

</div>

## Currently has

- **Keywords** :: `bot`, `command`, `if`, `else`, `return`, etc.
- **Identifiers** :: variable, bot, and command names.
- **Strings** :: string literals such as `"Hello!"`.
- **Numbers**:: integer and decimal values.
- **Booleans & Null** :: `true`, `false`, `null`.
- **Operators & punctuation** :: `=`, `:`, and other defined symbols.
- **Newlines** :: represented as `NEWLINE` tokens.
- **Indentation** :: automatically produces `INDENT` and `DEDENT`.
- **EOF** :: marks the end of the source.
- **Error handling** :: reports invalid lexer input.

## Things to be added

- [ ] Unicode support
- [ ] Single quoted strings
- [ ] Complete operator set
- [ ] Strict float validation
- [ ] Bracket aware newline/indentation handling
