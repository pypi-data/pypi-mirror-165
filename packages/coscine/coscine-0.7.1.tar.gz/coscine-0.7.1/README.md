# Coscine Python SDK

![Coscine] ![Python]  
[Coscine](https://coscine.rwth-aachen.de/), short for Collaborative Scientific
Integration Environment is a platform for research data management (RDM).  
For more information on Coscine visit the [Coscine Landing Page].

[Coscine]: ./data/coscine_logo_rgb.png
[Python]: ./data/python-powered-w-200x80.png
[Coscine Landing Page]: https://www.coscine.de/

## About

The *Coscine Python SDK* is an open source python package providing
a pythonic client interface to the Coscine REST API. It is compatible
with Python versions 3.7+.  
Features (to name a few):  
- Project Management
	- Create, modify or delete a project
	- Add/Invite members to a project and set their roles
	- Download a project and all of its contents
- Resource Management
	- Create, modify or delete a resource
	- Download a resource and all of its contents
- File and Metadata Management
	- Upload, download and delete files
	- Interact with metadata in an intuitive pythonic manner
	- Fetch S3 access credentials

> **Note**  
> Please note that this python module is developed and maintained
> by the scientific community and even though Copyright remains with  
> RWTH Aachen, it is not an official service that RWTH Aachen
> provides support for.  

## Code example

Shown below is a small code snippet highlighting some functionality
offered by this package.  

```python
import coscine

cfg = coscine.Config()
client = coscine.Client(cfg.token)
project = client.project("My Project")
resource = project.resource("My Resource")
resource.upload("file.txt", "C:/databases/file.txt")
for file in resource.objects():
	print(file.name)
	print(file.metadata())
	if file.size > 4096: file.delete()
metadata = resource.object("path/to/file.csv").form()
metadata["Author"] = "John Doe"
resource.object("path/to/file.csv").update(metadata)
project.download("/home/datascience", metadata=True)
```

## Installation

### via the Python Package Index (PyPi)

The *Coscine Python SDK* is hosted on the *Python Package Index (PyPi)*:  
https://pypi.org/project/coscine/  

You can download and install the package with *pip*:  
```bash
py -m pip install coscine
```

### via Conda

The package version hosted on the *Python Package Index (PyPi)* is
automatically mirrored in the community driven packaging for *Conda*.

You can download and install the package with *conda*:  
```bash
conda install -c conda-forge coscine
```

### via Git

Manual installation:  
```bash
git clone https://git.rwth-aachen.de/coscine/community-features/coscine-python-sdk.git
cd ./coscine-python-sdk
py setup.py
```

## Documentation

The source code has been thorougly documented with *Python DOCstrings*.
Documentation can be generated via a variety of tools that take advantage
of these *DOCstrings*, such as [pydoc] or [pdoc3].  
Use the following script to generate documentation with *pdoc3*:  
```bash
cd ./coscine-python-sdk
py -m pip install pdoc3
py -m pdoc --html -o docs ./src/coscine
```  
The documentation inside of this repository is automatically deployed to
a [GitLab-Pages instance] for online access.  
In addition to the general documentation, many more examples and tutorials
in the form of short code snippets and interactive notebooks have been
provided in the [src/examples](./src/examples) directory.

[GitLab-Pages instance]:https://coscine.pages.rwth-aachen.de/community-features/coscine-python-sdk/coscine
[pydoc]:https://docs.python.org/3/library/pydoc.html
[pdoc3]:https://pypi.org/project/pdoc3/

## Contact

To report bugs, request features or resolve questions open an issue inside
of the current git repository.  
Contributions and any help on improving this package are appreciated. To
contribute source code you may fork the repository and open a merge request
or simply submit a short and relevant snippet or fix inside of an issue.

## License

This project is Open Source Software and licensed under the terms of
the [MIT License](./LICENSE.txt).

> **MIT License**
> 
> Copyright (**c**) 2018-2022 *RWTH Aachen University*
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy  
> of this software and associated documentation files (the "Software"), to deal  
> in the Software without restriction, including without limitation the rights  
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
> copies of the Software, and to permit persons to whom the Software is  
> furnished to do so, subject to the following conditions:  
>   
> The above copyright notice and this permission notice shall be included in all  
> copies or substantial portions of the Software.  
>   
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  
> SOFTWARE.
