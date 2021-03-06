# frozen_string_literal: true

class CatchJsonParseErrors
  def initialize(app)
    @app = app
  end

  def call(env)
    @app.call(env)
  rescue ActionDispatch::Http::Parameters::ParseError => e
    error_output = "There was a problem in the JSON you submitted: #{e}"
    [
      400, { 'Content-Type' => 'application/json' },
      [{ status: 400, error: error_output }.to_json]
    ]
  end
end
