# Description
This is a tool for flush the view count of csdn blog.

# Dependency
python3
numpy

# Usage
./flush_csdn_article.py --fast=file --slow=file

This tool seperate the article into two classify, one is fast, another is slow, the flush speed of the article that config in the fast will be more faster.

# How to write the fast/slow file
You can reference forsconfig_example.config

In that file, there are 3 field, aticle_url, flush_count_limit and single_article_flush_interval.
article_url: your article url
flush_count_limit: you want to flush the view count of your article up to?
single_article_flush_interval: because the continuous flush the view count have a great failed rate, so must set a suitable interval to flush the view count of single article

Now you can flush the view count of your blog!
