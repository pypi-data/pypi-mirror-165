# pdfdarkness
A command line tool for caluclating the darkness of the pages of PDF files.
Darkness is a scale from `pure_white_page=0.0` to `pure_black_page=1.0`.
This library is meant to be used with [`pdfmask`](https://github.com/hiroshi-matsuda/pdfmask) for calculating the darkness of the margin spaces of each page in PDF files.

## Installation

### Python libraries

```console
pip install pdfdarkness pdfmask
```

### Native libraries

You need to install [`poppler`](https://poppler.freedesktop.org/) in a different procedure for the OS environment. Please read [README in `Belval/pdf2image` repository](https://github.com/Belval/pdf2image#how-to-install) in detail.

We recommend using the Mac OS as the poppler installation step is very simple like below:

```console
$ brew install poppler
```

## Measuring the darkness of the PDF page margin spaces

### Example

```console
$ pdfmask_gen mask-A4-20_20_30_30.pdf A4 20 20 30 30
$ pdfmask mask-A4-20_20_30_30.pdf ./papers/*.pdf > pdfmask.log
$ pdfdarkness ./papers/*.masked.pdf

./papers/A1-1.pdf	1	0.00247536
./papers/A1-1.pdf	2	0.00083691
./papers/A1-1.pdf	3	0.00078953
./papers/A1-2.pdf	1	0.00245677
./papers/A1-2.pdf	2	0.00080773
...
```

### Usage

```
pdfdarkness target-pdf-path1 [target-pdf-path2 [...]]
```

The output format is the `tab separated value` and each record has three fields:
- PDF file name
- page number
- darkness

Please read [README in `hiroshi-matsuda/pdfmask` repository](https://github.com/hiroshi-matsuda/pdfmask#create-mask-pdf-file) for margin settings.

## License and Dependencies

- `pdfdarkness` is distributed under the terms of MIT License:
  - [MIT License](https://raw.githubusercontent.com/hiroshi-matsuda/pdfdarkness/main/LICENSE)
- `pdf2image` is distributed under the terms of MIT License:
  - See https://raw.githubusercontent.com/Belval/pdf2image/master/LICENSE

## Change Logs

### v0.1

#### v0.1.0
- 2022.09.01
- The first version
