import os
from fastapi.testclient import TestClient
from .app.server import app

os.chdir('app')
client = TestClient(app)

"""
We've built our web application, and containerized it with Docker.
But imagine a team of ML engineers and scientists that needs to maintain, improve and scale this service over time. 
It would be nice to write some tests to ensure we don't regress! 

  1. `Pytest` is a popular testing framework for Python. If you haven't used it before, take a look at https://docs.pytest.org/en/7.1.x/getting-started.html to get started and familiarize yourself with this library.

  2. How do we test FastAPI applications with Pytest? Glad you asked, here's two resources to help you get started:
    (i) Introduction to testing FastAPI: https://fastapi.tiangolo.com/tutorial/testing/
    (ii) Testing FastAPI with startup and shutdown events: https://fastapi.tiangolo.com/advanced/testing-events/
"""

PREDICT_WITHOUT_BODY_RESPONSE = {
  "detail": [
    {
      "loc": [
        "body",
        "source"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "body",
        "url"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "body",
        "title"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": [
        "body",
        "description"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

EN_REQUEST = {
  "source": "BBC Technology",
  "url": "http://news.bbc.co.uk/go/click/rss/0.91/public/-/2/hi/business/4144939.stm",
  "title": "System gremlins resolved at HSBC",
  "description": "Computer glitches which led to chaos for HSBC customers on Monday are fixed, the High Street bank confirms."
}

EN_RESPONSE = {
  "scores": {
    "Business": 0.4550814984508978,
    "Entertainment": 0.13000062451225236,
    "Health": 0.0325569891605281,
    "Music Feeds": 0.004118624567310023,
    "Sci/Tech": 0.3005427013839042,
    "Software and Developement": 0.01133333979071904,
    "Sports": 0.060413748539807494,
    "Toons": 0.005952473594580936
  },
  "label": "Business"
}

ES_REQUEST = {
  "source": "BBC Technology",
  "url": "http://news.bbc.co.uk/go/click/rss/0.91/public/-/2/hi/business/4144939.stm",
  "title": "System gremlins resolved at HSBC",
  "description": "Los fallos informáticos que provocaron el caos para los clientes de HSBC el lunes se han solucionado, confirma el banco High Street."
  }

ES_RESPONSE = {
  "scores": {
    "Business": 0.7239913595985465,
    "Entertainment": 0.02386727092723855,
    "Health": 0.008244287018147849,
    "Music Feeds": 0.002793750715946071,
    "Sci/Tech": 0.2029703176819705,
    "Software and Developement": 0.0106302002987647,
    "Sports": 0.026218109598776698,
    "Toons": 0.0012847041606089415
  },
  "label": "Business"
}


NON_ASCII_REQUEST = {
  "source": "BBC Technology",
  "url": "http://news.bbc.co.uk/go/click/rss/0.91/public/-/2/hi/business/4144939.stm",
  "title": "System gremlins resolved at HSBC",
  "description": "日本人 中國的 ~=[]()%+{}@;’#!$_&- éè ;∞¥₤€"
  }

NON_ASCII_RESPONSE = {
  "scores": {
    "Business": 0.1751583780666615,
    "Entertainment": 0.39429995840619075,
    "Health": 0.033783683220368295,
    "Music Feeds": 0.009004196701889535,
    "Sci/Tech": 0.30031416405344674,
    "Software and Developement": 0.024475878227799588,
    "Sports": 0.04004584817821076,
    "Toons": 0.022917893145432883
  },
  "label": "Entertainment"
}

def test_root():
    """
    [TO BE IMPLEMENTED]
    Test the root ("/") endpoint, which just returns a {"Hello": "World"} json response
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_predict_empty():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an empty request body
    """
    response = client.post("/predict", json={})
    assert response.status_code == 422
    assert response.json() == PREDICT_WITHOUT_BODY_RESPONSE 


def test_predict_en_lang():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an input text in English (you can use one of the test cases provided in README.md)
    """
    with TestClient(app) as client:
      response = client.post("/predict",json=EN_REQUEST)
      assert response.status_code == 200
      assert response.json() == EN_RESPONSE



def test_predict_es_lang():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an input text in Spanish. 
    Does the tokenizer and classifier handle this case correctly? Does it return an error?
    """
    with TestClient(app) as client:
      response = client.post("/predict",json=ES_REQUEST)
      assert response.status_code == 200
      assert response.json() == ES_RESPONSE 



def test_predict_non_ascii():
    """
    [TO BE IMPLEMENTED]
    Test the "/predict" endpoint, with an input text that has non-ASCII characters. 
    Does the tokenizer and classifier handle this case correctly? Does it return an error?
    """
    with TestClient(app) as client:
      response = client.post("/predict",json=NON_ASCII_REQUEST)
      assert response.status_code == 200
      assert response.json() == NON_ASCII_RESPONSE 