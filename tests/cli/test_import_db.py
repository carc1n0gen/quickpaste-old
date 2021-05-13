# from unittest.mock import patch, mock_open


# def test_should_exit_with_error_when_requried_parameters_missing(app):
#     runner = app.test_cli_runner()
#     result = runner.invoke(args=['import-db'])
#     assert result.exit_code == 1


# def test_should_exit_normally_when_required_parameters_passed(app):
#     read_data = '[{"_id": "CEX4l0Z", "created_at": 1599537703.259677, "delete_at": 1600142503.259681, "text": "Bork bork I am doggo"}, {"_id": "TfI6r3G", "created_at": 1599537703.259747, "delete_at": 1600142503.259747, "text": "Mooooooooo!"}, {"_id": "about", "created_at": 1599537703.259747, "delete_at": null, "text": "ABOUT PAGE"}]'
#     with patch('builtins.open', mock_open(read_data=read_data)):
#         runner = app.test_cli_runner()
#         result = runner.invoke(args=['import-db', '--input', 'output.json'])
#         assert result.exit_code == 0
#         assert result.stdout == 'Imported data from output.json\n'
