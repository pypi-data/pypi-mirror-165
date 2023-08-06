from unfolded.map_sdk.api import layer_api

DUMMY_MESSAGE_UUID = "ede3fafc-4945-41b7-ac64-16faa896a47a"
LAYER_UUID = "997c21eb-604b-49df-add9-b2fcc615a243"

ACTION_FIXTURES = [
    (
        layer_api.GetLayersAction(),
        {
            "type": "v1/map-sdk-get-layers",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
    (
        layer_api.GetLayerByIdAction(layer_id="layer-id"),
        {
            "type": "v1/map-sdk-get-layer-by-id",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": ["layer-id"],
        },
    ),
    (
        layer_api.AddLayerAction(
            layer={
                "id": "layer-id",
                "data_id": "data-1",
                "fields": {"field-1": "value-1"},
            }
        ),
        {
            "type": "v1/map-sdk-add-layer",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                {"id": "layer-id", "dataId": "data-1", "fields": {"field-1": "value-1"}}
            ],
        },
    ),
    (
        layer_api.UpdateLayerAction(
            layer_id="layer-id", values={"fields": {"field-1": "value-1"}}
        ),
        {
            "type": "v1/map-sdk-update-layer",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                "layer-id",
                {"fields": {"field-1": "value-1"}},
            ],
        },
    ),
    (
        layer_api.RemoveLayerAction(layer_id="layer-id"),
        {
            "type": "v1/map-sdk-remove-layer",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": ["layer-id"],
        },
    ),
    (
        layer_api.GetLayerTimelineAction(),
        {
            "type": "v1/map-sdk-get-layer-timeline",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
    (
        layer_api.UpdateLayerTimelineAction(values={"current_time": 0}),
        {
            "type": "v1/map-sdk-update-layer-timeline",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [{"currentTime": 0}],
        },
    ),
]
