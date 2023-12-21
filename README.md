# Python-Crawler

This is a learning document about Python web crawlers, which includes two parts: learning examples and practical
operations. This project will involve web crawlers, big self, and artificial intelligence. Please regulate your own
operations and do not maliciously attack other people's web pages.When you need to crawl a webpage, please add/robots.
txt after the URL and follow the crawling protocol rules. We hope everyone can learn something from it.

## Directory Catalog

```
Python-Crawler:
--- catalog or file
	|--bin       -- start.py
	|--conf      -- settings.py
	|--core      -- code.py
	|--self      -- db/cache: self/sql
	|--docs      -- pdf,word,md
	|--env       -- environment.env
	|--example   -- example: other projects examples
	|--lib     -- common.py
	|--log       -- log.log
	|--model     -- entity.py
	|--out       -- output: something
	|--scripts   -- ptthon jdk: *.exe
	|--setup     -- setup: Scripts for installation, deployment, and packaging
	|--test      -- test.py
	|--quirements.txt
	|--README.md
```

## Contents

* [Quick start](#quick-start)

## Quick start

Start a Python-Crawler with a command

```bash
1. pip install -r requirements.txt
```

2. You need to download MySQL and Elasticsearch.If you don't download them,you can choose other db to save data.
3. Execute MySQL table creation statement from ../data/*.sql
4. Copy the files in the scripts' directory to Python/Scripts/
5. Execute Python files under the core package