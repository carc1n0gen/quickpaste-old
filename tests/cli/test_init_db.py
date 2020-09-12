

def test_should_run_normally(app):
    runner = app.test_cli_runner()
    result = runner.invoke(args=['init-db'])
    assert result.exit_code == 0
