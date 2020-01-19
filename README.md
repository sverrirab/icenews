# icenews
Simple NLP for Icelandic News

This project is aimed at extracting themes / concepts from simple
icelandic news text - headlines and such.  This is used for example
by [helst.is](https://helst.is) for processing mainstream Icelandic 
news media.  

[![travis](https://travis-ci.com/sverrirab/icenews.svg?token=xxFqtztRjZQMvihBaiGq&branch=master)](https://travis-ci.com/sverrirab/icenews)

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

# Use with container

If you prefer you can also load the prebuilt container and run locally:

```bash 
docker run -d -p 5000:5000 --rm --name icenews sverrirab/icenews
``` 

# Now with API documentation!

After you start the service visit `/docs` for detailed documentation!

```bash 
docker run -d -p 5000:5000 --rm --name icenews sverrirab/icenews
``` 

And the same request as above works...

# Note on licensing

This project is released under the [Apache License](./LICENSE) because
that is compatible with all the other licenses for libraries it depends
on.  They are as time of writing: Public Domain, MIT, BSD, BSD-3 and GPLv3. 
