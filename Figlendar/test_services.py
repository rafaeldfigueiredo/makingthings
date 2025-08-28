from events.services import CalendarService

def test_delete_event_should_return_true_if_successful(mocker):
    mock_repo = mocker.Mock()
    mock_repo.delete_event.return_value = True
    service = CalendarService(mock_repo)
    
    deleted_event = service.delete_event(1)

    assert deleted_event is True
    mock_repo.delete_event.assert_called_once_with(1)