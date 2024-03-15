import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from .view import router
from unittest.mock import MagicMock, patch
from fastapi.exceptions import HTTPException

client = TestClient(router)

project_data = {
  "name": "string",
  "description": "string",
  "date_range": {
    "start": "2024-03-14T16:49:53.008Z",
    "end": "2024-03-14T16:49:53.008Z"
  },
  "area_of_interest": {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [
        5,
        5
      ]
    }
  }
}



@patch('app.tasks.create_project.delay')
def test_create_project(mock_create):
    mock_result = MagicMock()
    mock_result.get.return_value = {"id": 1, **project_data}
    mock_create.return_value = mock_result
    response = client.post("/projects/", json=project_data)
    assert response.status_code == 202
    assert response.json() == {"message": "Project created successfully"}
    mock_create.assert_called_once()

@patch('app.tasks.read_project.delay')
def test_read_project_success(mock_read):
    mock_result = MagicMock()
    mock_result.get.return_value = {"id": 1, **project_data}
    mock_read.return_value = mock_result

    response = client.get("/projects/1")
    assert response.status_code == 200
    assert {"id": 1, **project_data} == response.json()

@patch('app.tasks.read_project.delay')
def test_read_project_fail(mock_read):
    mock_result = MagicMock()
    mock_result.get.return_value = None
    mock_read.return_value = mock_result
    with pytest.raises(HTTPException) as exc_info:
        client.get("/projects/1")
    assert exc_info.value.status_code == 400
    assert str(exc_info.value.detail) == "404: Project not found"


@patch('app.tasks.update_project.delay')
def test_update_project_success(mock_update):
    mock_result = MagicMock()
    mock_result.get.return_value = None
    mock_update.return_value = mock_result
    with pytest.raises(HTTPException) as exc_info:
        client.put("/projects/1", json=project_data)
    assert exc_info.value.status_code == 400
    assert str(exc_info.value.detail) == "404: Project not found"

@patch('app.tasks.update_project.delay')
def test_update_project_fail(mock_update):
    mock_result = MagicMock()
    mock_result.get.return_value = {"id": 1, **project_data}
    mock_update.return_value = mock_result
    response = client.put("/projects/1", json=project_data)
    assert response.status_code == 200
    assert {"id": 1, **project_data} == response.json()

@patch('app.tasks.delete_project.delay')
def test_delete_project_success(mock_delete):
    mock_result = MagicMock()
    mock_result.get.return_value = True
    mock_delete.return_value = mock_result
    response = client.delete("/projects/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Project deleted successfully"}

@patch('app.tasks.delete_project.delay')
def test_delete_project_fail(mock_delete):
    mock_result = MagicMock()
    mock_result.get.return_value = False
    mock_delete.return_value = mock_result
    with pytest.raises(HTTPException) as exc_info:
        client.delete("/projects/1")
    assert exc_info.value.status_code == 400
    assert str(exc_info.value.detail) == "404: Project not found"

@patch('app.tasks.list_projects.delay')
def test_list_projects_success(mock_list_projects):
    mock_result = MagicMock()
    mock_result.get.return_value = [{"id": 1, **project_data}]
    mock_list_projects.return_value = mock_result
    response = client.get("/projects/")
    assert response.status_code == 200
    assert {"projects": [{"id": 1, **project_data}]} == response.json()


@patch('app.tasks.list_projects.delay')
def test_list_projects_fail(mock_list_projects):
    mock_result = MagicMock()
    mock_result.get.return_value = None
    mock_list_projects.return_value = mock_result
    with pytest.raises(HTTPException) as exc_info:
        client.get("/projects/")
    assert exc_info.value.status_code == 400
    assert str(exc_info.value.detail) == "404: Projects not found"
