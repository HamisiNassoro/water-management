import json

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    charset = "utf-8"

    ##function that overrides the JSONRenderer to render our data under a profile namespace
    def render(self, data, accepted_media_types=None, renderer_context=None):
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)

        return json.dumps({"profile": data})
