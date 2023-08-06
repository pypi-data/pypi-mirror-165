# AWS S3 Metadata Tagger
The S3 Metadata tagger adds information in the form of metadata to files saved in S3.

To do this, the central handler takes a file location and a metadata extracting function.
It first checks whether the file already contains the requested information via a `HEAD` request.
If it does not, it downloads the file, invokes extracting function, and adds the metadata to
the s3 object with a inplace `COPY, MetadataDirective="REPLACE"` operation.

This package comes with two optional variants for metadata extraction:
* PDF: for determining the number of pages in a pdf
* PICTURE: for determining the dimension of an image

## Structure
### `object_tagger` 
contains the higher-level orchestration:
* `object_tagger.py` contains all the logic for checking whether the file has already been tagged, downloading it, invoking the metadata script, creating the tag object, and adding it to the s3 resource. 

The metadata scripts are stored in their respective folders

### `pdf_tagger`
The pdf tagger uses [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) to determine the amount of pages in a pdf

### `picture_tagger`
Using [Pillow](https://python-pillow.org/), the script gets the `width` and `height` of the passed image