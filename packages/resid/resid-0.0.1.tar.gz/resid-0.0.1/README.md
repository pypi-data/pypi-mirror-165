# resid

### Description
**Resid** is a python library for analysing resource identifiers 
for extracting valuable information. This can include guessing content 
type, encoding, wheather contents are available locally or if it 
resembles file path, url, etc.

In this library, _source_ is defined as similar to _uri_ but source
can be anything including file object. 'source' is defined as anything
that can be used to access/locate contents. That can include _url_, 
_file path_, _file object_ and others depending on wheather
they can be used to access data or get information about it.

Any object can be used as source but not all of them will be supported.
This library helps in extracting information about source such as wheather
source is supported or guessing its content type.

> Only urls, file-paths, dir-paths, file-like-objects, path-like-objects are
currenly supported. 

### Install
Enter this on your command-line application:  
```bash 
pip install resid
```

### Usage
#### Importing resid
```python
import resid
```
> resid -> Resource Identifier

#### Check support of source
View _supported source_ as a valid file path and resembled as file path
that may not be valid but looks like file path.
```python
>>> resid.is_supported("https://stackoverflow.com/")
True
>>> resid.is_supported("not_exists.txt")
False
>>> resid.is_resembled("not_exists.txt")
True
>>> resid.is_supported(io.BytesIO())
True
>>> resid.is_resembled(object)
False
```
> Most functions will return `None` if source is not supported.

#### Check if source falls in category
```python
>>> resid.is_url("https://example.com/")
True
>>> resid.is_web_url("https://example.com/")
True
>>> resid.is_file_path("https://example.com/")
False
>>> resid.is_file_path("sample.txt")
True
>>> resid.is_file_path(object)
False
>>> resid.is_file_like(io.BytesIO())
True
>>> resid.is_path_like(pathlib.Path("sample.txt"))
True
```


#### Guess content type
```python
>>> resid.guess_content_type("sample.txt")
'text/plain'
>>> resid.guess_content_type("https://example.com/")
'text/html'
>>> resid.guess_content_type("https://example.com/files/sample.pdf")
'application/pdf'
>>> resid.guess_content_type(open("sample.txt"))
'text/plain'
```

#### Check if contents are hosted locally or remotely
```python
>>> resid.locally_hosted("sample.txt")
True
>>> resid.locally_hosted("https://example.com/")
False
>>> resid.locally_hosted("http://127.0.0.1/")
True
>>> resid.guess_content_type(open("sample.txt"))
True
>>> resid.remotely_hosted("sample.txt")
False
>>> resid.remotely_hosted("https://example.com/")
True
>>> resid.remotely_hosted("file:///home/sample.txt")
False
```

#### Guess type of source
```python
>>> resid.guess_type("sample.txt")
'file-path'
>>> resid.guess_type("contents/")
'dir-path'
>>> resid.guess_type("https://example.com/")
'web-url'
>>> resid.guess_type(io.BytesIO())
'file-like-object'
>>> resid.guess_type(pathlib.Path("sample.txt"))
'file-path-like-object'
>>> resid.guess_type("file:///home/sample.txt")
'local-file-url'
```

#### Convert source to string
```python
>>> resid.to_string(open("setup.py"))
'setup.py'
>>> resid.to_string(pathlib.Path("sample.txt"))
'sample.txt'
>>> resid.to_string("https://example.com/")
'https://example.com/'
```


### Alternate Usage
#### File path example
```python
>>> file_res = resid.find_resource("setup.py")
>>> file_res.supported
True
>>> file_res.content_type
'text/plain'
>>> file_res.path
'setup.py'
>>> file_res.size
41
>>> file_res.mod_time
1661489762.1989822
```

#### Directory example
```python
>>> dir_res = resid.find_resource("https://example.com/")
>>> list(dir_res.files)
['.venv\\pyvenv.cfg']
>>> list(dir_res.dirs)
['.venv\\Include', '.venv\\Lib', '.venv\\Scripts']
>>> list(dir_res.files_recursive)
...
>>> list(dir_res.dirs_recursive)
...
```

#### URL example
```python
>>> url_res = resid.find_resource("https://example.com/")
>>> url_res.content_type
'text/html'
>>> url_res.scheme
'https'
>>> url_res.hostname
'example.com'
>>> list(dir_res.files)
['.venv\\pyvenv.cfg']
>>> list(dir_res.dirs)
['.venv\\Include', '.venv\\Lib', '.venv\\Scripts']
>>> list(dir_res.files_recursive)
...
>>> list(dir_res.dirs_recursive)
...
```

### About
_Resid_ was developed based on [navaly](https://github.com/Sekgobela-Kevin/naval) 
library to be used with navaly. It relect a portion of navaly which is 
split to its own project for reuse. Resid can still be used with other 
python projects as seen in the examples above.