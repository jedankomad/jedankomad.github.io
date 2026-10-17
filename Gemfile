# frozen_string_literal: true

source "https://rubygems.org"

gemspec


# Lokalni pregled na Windows-u (bundle exec jekyll serve): Jekyll tamo traži podatke o vremenskim zonama.
# Na Linux-u (GitHub) se ne instaliraju.
platforms :windows, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
