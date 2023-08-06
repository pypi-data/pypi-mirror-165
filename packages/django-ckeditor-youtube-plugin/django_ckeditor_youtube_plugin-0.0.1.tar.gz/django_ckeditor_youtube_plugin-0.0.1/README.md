# Django CKEditor YouTube Plugin

```python
ckeditor__external_plugin_resources = [
    (
        "youtube",
        "/static/ckeditor/ckeditor/plugins/youtube/",
        "plugin.min.js",
    )
]
```

```python
CKEDITOR_CONFIGS["default"][
    "external_plugin_resources"
] = ckeditor__external_plugin_resources
```
