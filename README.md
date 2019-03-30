# icenews
Simple NLP for Icelandic News

This project is aimed at extracting themes / concepts from simple
icelandic news text - headlines and such.  This is used for example
by [helst.is](https://helst.is) for processing mainstream Icelandic 
news media.  

![travis](https://travis-ci.com/sverrirab/icenews.svg?token=xxFqtztRjZQMvihBaiGq&branch=master)

# How to use

```bash
$ pip install icenews
$ python -m icenews
```

And then when the web server is running -  analyze your text.  For example:

```bash
$ python
>>> import requests
>>> t = 'Áformað er að taka upp nýtt greiðslukerfi fyrir Strætó á næstunni.'
>>> r = requests.post('http://127.0.0.1:5000/v1/parse', json={'in': t}) 
>>> print(r.json())
{'important_words': ['greiðslukerfi', 'strætó', 'upp', 'á næstunni', 'áforma', 'áformaður', 'nýr', 'nýta']}
```

# Note on licensing

This project is released under the [Apache License](./LICENSE) because
that is compatible with all the other licenses for libraries it depends
on.  They are as time of writing: Public Domain, MIT, BSD, BSD-3 and GPLv3. 
