from unittest.mock import patch, mock_open


# TODO: revisit this since there are no required parameters anymore
# def test_should_exit_with_error_when_requried_parameters_missing(app):
#     runner = app.test_cli_runner()
#     result = runner.invoke(args=['export-db'])
#     assert result.exit_code == 1


# CLI tests need to be re-thought out now that mocks have changing dates in them. Makes it harder to assert the output
# def test_should_exit_normally_when_required_parameters_passed(app):
#     # read_data = '[{"_id": "CEX4l0Z", "created_at": 1599537703.259677, "delete_at": 1600142503.259681, "text": "Bork bork I am doggo"}, {"_id": "TfI6r3G", "created_at": 1599537703.259747, "delete_at": 1600142503.259747, "text": "Mooooooooo!"}, {"_id": "about", "created_at": 1599537703.259747, "delete_at": null, "text": "ABOUT PAGE"}]'
#     with patch('builtins.open', mock_open()):
#         runner = app.test_cli_runner()
#         result = runner.invoke(args=['export-db'])
#         assert result.exit_code == 0
#         print(result.stdout)
#         assert result.stdout == '{"_id": "6YrnrWA", "created_at": 1620970669.738594, "delete_at": 1621575469.738598, "text": "Bork bork I am doggo"}\n{"_id": "oNuzR-9", "created_at": 1620970669.73864, "delete_at": 1621575469.73864, "text": "Mooooooooo!"}'
