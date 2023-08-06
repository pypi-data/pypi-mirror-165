from unfolded.map_sdk.api import map_api

DUMMY_MESSAGE_UUID = "ede3fafc-4945-41b7-ac64-16faa896a47a"
DATASET_UUID = "0e939627-8ea7-4db6-8c92-3dd943166a01"
LAYER_UUID = "997c21eb-604b-49df-add9-b2fcc615a243"
FILTER_UUID = "e02b67ea-20d4-4613-808e-9a8fdbd81e6f"

ACTION_FIXTURES = [
    (
        map_api.GetViewAction(index=0),
        {
            "type": "v1/map-sdk-get-view",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [0],
        },
    ),
    (
        map_api.SetViewAction(
            view={"latitude": 47.271057, "longitude": 8.650367, "zoom": 5},
            index=0,
        ),
        {
            "type": "v1/map-sdk-set-view",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                {
                    "longitude": 8.650367,
                    "latitude": 47.271057,
                    "zoom": 5.0,
                }
            ],
            "options": {"index": 0},
        },
    ),
    (
        map_api.GetViewLimitsAction(index=0),
        {
            "type": "v1/map-sdk-get-view-limits",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [0],
        },
    ),
    (
        map_api.SetViewLimitsAction(
            view_limits={"min_zoom": 3, "max_zoom": 8}, index=0
        ),
        {
            "type": "v1/map-sdk-set-view-limits",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                {
                    "minZoom": 3,
                    "maxZoom": 8,
                }
            ],
            "options": {"index": 0},
        },
    ),
    (
        map_api.GetMapControlVisibilityAction(),
        {
            "type": "v1/map-sdk-get-map-control-visibility",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
    (
        map_api.SetMapControlVisibilityAction(
            visibility={"legend": False, "toggle_3d": True}
        ),
        {
            "type": "v1/map-sdk-set-map-control-visibility",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                {
                    "legend": False,
                    "toggle-3d": True,
                }
            ],
        },
    ),
    (
        map_api.GetSplitModeAction(),
        {
            "type": "v1/map-sdk-get-split-mode",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
    (
        map_api.SetSplitModeAction(
            split_mode="swipe",
            options={
                "layers": [[LAYER_UUID], []],
                "is_view_synced": True,
                "is_zoom_synced": True,
            },
        ),
        {
            "type": "v1/map-sdk-set-split-mode",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                "swipe",
                {
                    "layers": [[LAYER_UUID], []],
                    "isViewSynced": True,
                    "isZoomSynced": True,
                },
            ],
        },
    ),
    (
        map_api.SetThemeAction(
            theme={"preset": "light", "options": {"background_color": "blue"}}
        ),
        {
            "type": "v1/map-sdk-set-theme",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [{"preset": "light", "options": {"backgroundColor": "blue"}}],
        },
    ),
    (
        map_api.GetMapConfigAction(),
        {
            "type": "v1/map-sdk-get-map-config",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
    (
        map_api.SetMapConfigAction(
            config={"map": "config"},
            options={
                "additional_datasets": [
                    {"id": "dataset-id", "type": "local", "data": "dataset-data"}
                ]
            },
        ),
        {
            "type": "v1/map-sdk-set-map-config",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                {"map": "config"},
                {
                    "additionalDatasets": [
                        {"id": "dataset-id", "type": "local", "data": "dataset-data"}
                    ]
                },
            ],
        },
    ),
    (
        map_api.GetMapStylesAction(),
        {
            "type": "v1/map-sdk-get-map-styles",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
]
