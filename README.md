# mCaptcha-solver
it was too easy cuz there is JavaScript worker instead WebAssembly worker for browser that doesn't support WASM.<br>
# usage
```py
import mcap

# mcap.solve("sitekey", "endpoint")
mcap.solve("pHy0AktWyOKuxZDzFfoaewncWecCHo23","https://demo.mcaptcha.org") # uDYNeVoNBAvRUMjEqpQso9QpFNQcxqTW
mcap.solve("abcdef","https://discord.gg/Wh279Ryt65") # returns response.text when its failed
```
