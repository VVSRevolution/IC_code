# Service::Base

It is expected to hold gems and configuration files that are shared by more than one service. Its main objective is to eliminate repetitions between services making maintenance easier.

This is not available to rubygems.org nad we do not expect it to be as it is intended for use within InterSCity's services context.

## Installation

Add this line to your application's Gemfile:

```ruby
gem 'service-base', path: '../gems/'
```

And then execute:

    $ bundle

## Usage

TODO: Write usage instructions here

## Development

After checking out the repo, run `bin/setup` to install dependencies. Then, run `rake spec` to run the tests. You can also run `bin/console` for an interactive prompt that will allow you to experiment.

To install this gem onto your local machine, run `bundle exec rake install`. To release a new version, update the version number in `version.rb`, and then run `bundle exec rake release`, which will create a git tag for the version, push git commits and tags, and push the `.gem` file to [rubygems.org](https://rubygems.org).
