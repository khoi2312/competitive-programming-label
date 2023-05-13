# Codeforces Dataset 
Multi-label Classification / Tag predictions in Competitive Programming

## Installation

Clone this repository:

```sh
$ git clone https://github.com/khoi2312/tags-codeforces-dataset.git
```
Clone the [repository](https://github.com/Jur1cek/codeforces-dataset) (submissions dataset) and unzip files:

```sh
$ git clone https://github.com/Jur1cek/codeforces-dataset.git
$ cd codeforces-dataset/contests/
$ bzip2 -d *.bz2
```

## Build dataset
Use [Codeforces API](https://codeforces.com/apiHelp) to build tags dataset, run these scripts:

```sh
$ python3 codeforces-api.py
$ python3 make-tags-dataset.py
```

From [Jur1cek Submission Dataset](https://github.com/Jur1cek/codeforces-dataset), we use this metadata `['contest_id', 'submission_id', 'author', 'language', 'problem', 'source_code']` and just use `submission` which has `problem_id` in tags dataset and `language` in `['GNU C++17', 'GNU C++14', 'GNU C++11', 'GNU C++', 'GNU C++17 (64)', 'GNU C++20 (64)']`.

```sh
$ python3 make-submissons-dataset.py
```
## Data analysis

![](https://i.imgur.com/nE37aum.png)
![](https://i.imgur.com/NHJL7Qy.png)
