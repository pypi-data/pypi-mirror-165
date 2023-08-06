from unfolded.map_sdk.api import filter_api

DUMMY_MESSAGE_UUID = "ede3fafc-4945-41b7-ac64-16faa896a47a"
DATASET_UUID = "0e939627-8ea7-4db6-8c92-3dd943166a01"
LAYER_UUID = "997c21eb-604b-49df-add9-b2fcc615a243"
FILTER_UUID = "e02b67ea-20d4-4613-808e-9a8fdbd81e6f"

ACTION_FIXTURES = [
    (
        filter_api.GetFiltersAction(),
        {
            "type": "v1/map-sdk-get-filters",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [],
        },
    ),
    (
        filter_api.GetFilterByIdAction(filter_id=FILTER_UUID),
        {
            "type": "v1/map-sdk-get-filter-by-id",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [FILTER_UUID],
        },
    ),
    (
        filter_api.AddFilterAction(
            filter={
                "type": filter_api.FilterType.RANGE,
                "sources": [{"data_id": DATASET_UUID, "field_name": "test"}],
                "value": (0, 100),
            }
        ),
        {
            "type": "v1/map-sdk-add-filter",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                {
                    "type": "range",
                    "sources": [{"dataId": DATASET_UUID, "fieldName": "test"}],
                    "value": [0, 100],
                }
            ],
        },
    ),
    (
        filter_api.UpdateFilterAction(
            filter_id=FILTER_UUID,
            values={
                "value": (0, 50),
                "sources": [{"data_id": DATASET_UUID, "field_name": "test-2"}],
            },
        ),
        {
            "type": "v1/map-sdk-update-filter",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [
                FILTER_UUID,
                {
                    "type": "range",
                    "value": [0, 50],
                    "sources": [{"dataId": DATASET_UUID, "fieldName": "test-2"}],
                },
            ],
        },
    ),
    (
        filter_api.RemoveFilterAction(filter_id=FILTER_UUID),
        {
            "type": "v1/map-sdk-remove-filter",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [FILTER_UUID],
        },
    ),
    (
        filter_api.UpdateTimelineAction(
            filter_id=FILTER_UUID, values={"view": "side", "is_animating": True}
        ),
        {
            "type": "v1/map-sdk-update-timeline",
            "messageId": DUMMY_MESSAGE_UUID,
            "args": [FILTER_UUID, {"view": "side", "isAnimating": True}],
        },
    ),
]
