"""Focused tests for the optional Atlas image provider."""

import io
from urllib.error import URLError

from PIL import Image

from scripts import generate_image


def _catalog():
    return {
        "data": [
            {
                "model": generate_image.DEFAULT_MODEL_ATLAS,
                "type": "Image",
                "display_console": True,
                "schema": "https://static.atlascloud.ai/model/schema/image.json",
                "price": {"actual": {"base_price": "0.028"}},
            }
        ]
    }


def _schema():
    return {
        "components": {
            "schemas": {
                "Input": {
                    "required": ["model", "prompt"],
                    "properties": {
                        "model": {"type": "string"},
                        "prompt": {"type": "string"},
                        "aspect_ratio": {"enum": ["1:1", "4:5", "16:9"]},
                        "resolution": {"enum": ["1k"]},
                    },
                }
            }
        },
        "paths": {"/api/v1/model/prediction/{request_id}": {"get": {}}},
    }


def _png_bytes():
    output = io.BytesIO()
    Image.new("RGB", (8, 10), "white").save(output, format="PNG")
    return output.getvalue()


def test_atlas_provider_submits_once_and_uses_schema_result_path():
    post_calls = []
    prediction_calls = []
    downloaded = []

    def get_json(url, _api_key=None):
        if url == generate_image.ATLAS_CATALOG_URL:
            return _catalog()
        if url.endswith("image.json"):
            return _schema()
        prediction_calls.append(url)
        return {
            "data": {
                "status": "completed",
                "outputs": ["https://cdn.example/ad.png?signature=temporary"],
            }
        }

    def post_json(url, _api_key, payload):
        post_calls.append((url, payload))
        return {"data": {"id": "prediction-1"}}

    result = generate_image.generate_atlas(
        "A studio product photo",
        1080,
        1350,
        "test-key",
        generate_image.DEFAULT_MODEL_ATLAS,
        get_json=get_json,
        post_json=post_json,
        get_bytes=lambda url: downloaded.append(url) or _png_bytes(),
        sleep_fn=lambda _seconds: None,
    )

    assert result == _png_bytes()
    assert len(post_calls) == 1
    assert post_calls[0][0].endswith("/api/v1/model/generateImage")
    assert post_calls[0][1]["aspect_ratio"] == "4:5"
    assert prediction_calls == [
        "https://api.atlascloud.ai/api/v1/model/prediction/prediction-1"
    ]
    assert downloaded == ["https://cdn.example/ad.png?signature=temporary"]


def test_atlas_prediction_get_retries_without_resubmitting():
    post_calls = []
    prediction_attempts = []

    def get_json(url, _api_key=None):
        if url == generate_image.ATLAS_CATALOG_URL:
            return _catalog()
        if url.endswith("image.json"):
            return _schema()
        prediction_attempts.append(url)
        if len(prediction_attempts) < 3:
            raise URLError("temporary")
        return {
            "data": {
                "status": "completed",
                "outputs": ["https://cdn.example/ad.png"],
            }
        }

    def post_json(_url, _api_key, _payload):
        post_calls.append(True)
        return {"data": {"id": "prediction-2"}}

    generate_image.generate_atlas(
        "A studio product photo",
        1080,
        1080,
        "test-key",
        generate_image.DEFAULT_MODEL_ATLAS,
        get_json=get_json,
        post_json=post_json,
        get_bytes=lambda _url: _png_bytes(),
        sleep_fn=lambda _seconds: None,
    )

    assert len(post_calls) == 1
    assert len(prediction_attempts) == 3


def test_atlas_schema_rejects_unsupported_ratio():
    payload = {
        "model": generate_image.DEFAULT_MODEL_ATLAS,
        "prompt": "A studio product photo",
        "aspect_ratio": "9:16",
        "resolution": "1k",
    }

    try:
        generate_image._atlas_validate_payload(_schema(), payload)
    except ValueError as exc:
        assert "aspect_ratio must be one of" in str(exc)
    else:
        raise AssertionError("unsupported Atlas ratio was accepted")


def test_atlas_jpeg_output_is_normalized_to_png():
    source = io.BytesIO()
    Image.new("RGB", (8, 10), "white").save(source, format="JPEG")

    result = generate_image._atlas_normalize_png(source.getvalue())

    assert result.startswith(b"\x89PNG\r\n\x1a\n")
    with Image.open(io.BytesIO(result)) as image:
        assert image.size == (8, 10)
