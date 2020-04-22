# installation

## this project
just `pipenv install` with python 3.7.7

## general install
azure storage container
    guide 0th ref. https://docs.microsoft.com/en-us/python/api/overview/azure/storage-index?view=azure-python
        quickstart guide ref. https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python 
    
azure storage fileShare
    ref. https://pypi.org/project/azure-storage-file-share/

```bash
pip install azure-storage-blob
```


# note when coding with azure storage
dash _ not accepted in names
if used, we will have error  
> E azure.core.exceptions.HttpResponseError: The specified resource name contains invalid characters.
