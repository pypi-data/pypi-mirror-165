from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import AnyHttpUrl
from pydantic import Field as PydanticField
from pydantic import StrictStr

from unfolded.map_sdk.api.base import Action, CamelCaseBaseModel, Number
from unfolded.map_sdk.api.enums import (
    ActionType,
    BasicFieldType,
    DatasetType,
    FieldType,
    TimestampFieldType,
    VectorTileAttributeType,
)
from unfolded.map_sdk.transport.base import (
    BaseInteractiveTransport,
    BaseNonInteractiveTransport,
)
from unfolded.map_sdk.utils.validators import validate_kwargs

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import geopandas as gpd
except ImportError:
    gpd = None


RGBColor = Tuple[Number, Number, Number]
"""Red, green and blue channels of a color in [0-255] range."""


class BaseField(CamelCaseBaseModel):

    name: StrictStr
    """Unique identifier of the field."""

    label: StrictStr
    """User facing field label."""

    type: FieldType
    """Type of the field."""


class BasicField(BaseField):
    """Contains semantics around a single field in a dataset table."""

    type: BasicFieldType


class TimestampField(BaseField):
    """Contains semantics around a single timestamp field in a dataset table."""

    type: TimestampFieldType = TimestampFieldType.TIMESTAMP
    time_format: StrictStr
    """moment.js time format of this field data."""


Field = Union[BasicField, TimestampField]
"""Union of available field types."""


class BaseDataset(CamelCaseBaseModel):

    id: StrictStr
    """Unique identifier of the dataset."""

    type: DatasetType
    """Type of dataset."""

    label: StrictStr
    """Displayable dataset label."""

    color: RGBColor
    """Color label of the dataset."""

    fields: List[Field]
    """Schema describring the fields of the dataset."""


class LocalDataset(BaseDataset):
    """Dataset record representing a local dataset, with data provided by the caller."""

    type = DatasetType.LOCAL


class DatasetWithData(LocalDataset):

    data: List[List[Any]]
    """Tabular data backing the dataset, where the order of fields matches the order in `Dataset.fields`."""


class VectorTileBaseMetadata(CamelCaseBaseModel):
    """Vector tileset base metadata."""

    class Config(CamelCaseBaseModel.Config):
        extra = "ignore"

    data_url: AnyHttpUrl
    """URL template for tiles, with {x}/{y}/{z} placeholders"""


class _VectorAttributes(CamelCaseBaseModel):
    """Attributes of a Vector layer."""

    class Config(CamelCaseBaseModel.Config):
        extra = "ignore"

    attribute: StrictStr
    """The name of this attribute."""

    type: VectorTileAttributeType
    """The type of this attribute's values."""

    min: Optional[Number]
    """The minimum value of this attribute (if numeric)."""

    max: Optional[Number]
    """The maximum value of this attribute (if numeric)."""


class _VectorLayer(CamelCaseBaseModel):
    """Layer attribute of the Vector TileJSON."""

    class Config(CamelCaseBaseModel.Config):
        extra = "ignore"

    attributes: List[_VectorAttributes]
    """Attributes in the layer."""


class _VectorTilestats(CamelCaseBaseModel):
    """Tilestats attribute of the Vector TileJSON."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(num_layers={len(self.layers)})"

    class Config(CamelCaseBaseModel.Config):
        extra = "ignore"

    layers: List[_VectorLayer]
    """Layers in the tileset."""


class VectorTileEmbeddedMetadata(CamelCaseBaseModel):
    """Minimal shape for the embedded JSON metadata in a Tippecanoe vector
    tileset metadata file.
    """

    class Config(CamelCaseBaseModel.Config):
        extra = "ignore"

    tilestats: _VectorTilestats
    """The tilestats for this tileset."""


class VectorTileLocalMetadata(VectorTileBaseMetadata):
    """Vector tileset metadata, following the metadata format generated
    by Tippecanoe. This metadata shape can be passed to the
    map to synchronously add a vector tileset.
    see https://github.com/mapbox/tippecanoe
    """

    # JSON metadata has multiple names in different contexts
    # maxzoom and minzoom are returned by studio in camelCase
    def __init__(self, **data):
        super().__init__(
            _json=data.pop("metaJson", None) or data.pop("json", None),
            maxzoom=data.pop("maxzoom", None) or data.pop("maxZoom", None),
            minzoom=data.pop("minzoom", None) or data.pop("minZoom", None),
            **data,
        )

    class Config(VectorTileBaseMetadata.Config):
        extra = "ignore"

    metadata_url: Optional[AnyHttpUrl]
    """URL for tileset metadata."""

    bounds: Optional[Union[StrictStr, List[Number]]]
    """Tileset bounds, as an array or comma-delimited string in format "w,s,e,n"."""

    center: Optional[Union[StrictStr, List[Number]]]
    """Tileset center, as an array or comma-delimited string in format "lng,lat"."""

    maxzoom: Optional[Number]
    """Maximum zoom supported by the tileset."""

    minzoom: Optional[Number]
    """Minimum zoom supported by the tileset."""

    _json: Union[StrictStr, VectorTileEmbeddedMetadata, None] = PydanticField(
        ..., alias="json"
    )
    """Metadata for the tileset, as a JSON string or object."""


class VectorTileRemoteMetadata(VectorTileBaseMetadata):
    """Vector tileset metadata with a remote metadata URL. The remote metadata file
    should follow the metadata format generated by Tippecanoe. This metadata can
    be passed to the map to asynchronously load a vector tileset.
    see https://github.com/mapbox/tippecanoe
    """

    metadata_url: AnyHttpUrl
    """URL for tileset metadata."""


VectorTileMetadata = Union[VectorTileLocalMetadata, VectorTileRemoteMetadata]


class VectorTileDataset(BaseDataset):
    """Dataset record representing a vector tileset."""

    type = DatasetType.VECTOR_TILE

    metadata: VectorTileMetadata
    """Metadata about the vector tileset."""


class RasterTileBaseMetadata(CamelCaseBaseModel):
    """Raster tileset base metadata."""

    class Config(CamelCaseBaseModel.Config):
        extra = "ignore"


class RasterTileLocalMetadata(RasterTileBaseMetadata):
    """Raster tileset metadata in STAC Item format. STAC version must be >= 1.0.0,
    and the EO and Raster STAC extensions are required. This metadata shape can
    be passed to the map to synchronously add a raster tileset.
    see https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md
    """

    metadata_url: Optional[AnyHttpUrl]
    """URL for tileset metadata."""

    type: StrictStr = "Feature"
    """Type of the raster tileset."""

    stac_version: StrictStr = PydanticField(..., alias="stac_version")
    """STAC version for tileset."""

    stac_extensions: List[StrictStr] = PydanticField(..., alias="stac_extensions")
    """A list of extensions the Item implements."""

    assets: Dict[StrictStr, Any]
    """Dictionary of asset objects that can be downloaded, each with a unique key."""


class RasterTileRemoteMetadata(RasterTileBaseMetadata):
    """Raster tileset metadata with a remote metadata URL. This metadata can
    be passed to the map to asynchronously load a raster tileset.
    """

    metadata_url: AnyHttpUrl
    """URL for tileset metadata."""


RasterTileMetadata = Union[RasterTileLocalMetadata, RasterTileRemoteMetadata]


class RasterTileDataset(BaseDataset):
    """Dataset record representing a raster tileset."""

    type = DatasetType.RASTER_TILE

    metadata: RasterTileMetadata
    """Metadata about the raster tileset."""


Dataset = Union[LocalDataset, VectorTileDataset, RasterTileDataset]


class _BaseDatasetCreationProps(CamelCaseBaseModel):

    id: Optional[StrictStr]
    """Unique identifier of the dataset."""

    type: DatasetType
    """Type of dataset."""

    label: Optional[StrictStr]
    """Displayable dataset label."""

    color: Optional[RGBColor]
    """Color label of the dataset."""


class _LocalDatasetCreationProps(_BaseDatasetCreationProps):
    """A set of properties used to create a dataset with inline data."""

    type: DatasetType = PydanticField(default=DatasetType.LOCAL)

    data: Union[StrictStr, dict, List[List[Any]]]
    """Data used to create a dataset, in CSV, JSON, GeoJSON format."""


class _VectorTileDatasetCreationProps(_BaseDatasetCreationProps):
    """A set of properties used to create a vector tile dataset with provided metadata."""

    type: DatasetType = DatasetType.VECTOR_TILE

    metadata: VectorTileLocalMetadata
    """Metadata about the vector tileset."""


class _VectorTileDatasetRemoteCreationProps(_BaseDatasetCreationProps):
    """A set of properties used to create a vector tile dataset with remote metadata."""

    type: DatasetType = DatasetType.VECTOR_TILE

    metadata: VectorTileRemoteMetadata
    """Metadata about the vector tileset."""


class _RasterTileDatasetCreationProps(_BaseDatasetCreationProps):
    """A set of properties used to create a raster tile dataset with provided metadata."""

    type: DatasetType = DatasetType.RASTER_TILE

    metadata: RasterTileLocalMetadata
    """Metadata about the raster tileset."""


class _RasterTileDatasetRemoteCreationProps(_BaseDatasetCreationProps):
    """A set of properties used to create a raster tile dataset with remote metadata."""

    type: DatasetType = DatasetType.RASTER_TILE

    metadata: RasterTileRemoteMetadata
    """Metadata about the raster tileset."""


_DatasetCreationProps = Union[
    _LocalDatasetCreationProps,
    _VectorTileDatasetCreationProps,
    _RasterTileDatasetCreationProps,
]


_TileDatasetCreationProps = Union[
    _VectorTileDatasetRemoteCreationProps, _RasterTileDatasetRemoteCreationProps
]


class _DatasetUpdateProps(CamelCaseBaseModel):
    """A set of properties used to update a dataset."""

    label: Optional[StrictStr]
    """Displayable dataset label."""

    color: Optional[RGBColor]
    """Color label of the dataset."""


###########
# ACTIONS #
###########


class GetDatasetsAction(Action):
    """Action payload sent with `get_datasets` calls"""

    type = ActionType.GET_DATASETS


class GetDatasetByIdAction(Action):
    """Action payload sent with `get_dataset_by_id` calls"""

    class Meta(Action.Meta):
        args = ["dataset_id"]

    type = ActionType.GET_DATASET_BY_ID
    dataset_id: StrictStr


class AddDatasetAction(Action):
    """Action payload sent with `add_dataset` calls"""

    class Meta(Action.Meta):
        args = ["dataset"]
        options = ["auto_create_layers", "center_map"]

    type = ActionType.ADD_DATASET
    dataset: _DatasetCreationProps
    auto_create_layers: bool
    center_map: bool


class AddTileDatasetAction(Action):
    """Action payload sent with `add_tile_dataset` calls"""

    class Meta(Action.Meta):
        args = ["dataset"]
        options = ["auto_create_layers", "center_map"]

    type = ActionType.ADD_TILE_DATASET
    dataset: _TileDatasetCreationProps
    auto_create_layers: bool
    center_map: bool


class UpdateDatasetAction(Action):
    """Action payload sent with `update_dataset` calls"""

    class Meta(Action.Meta):
        args = ["dataset_id", "values"]

    type = ActionType.UPDATE_DATASET
    dataset_id: StrictStr
    values: _DatasetUpdateProps


class RemoveDatasetAction(Action):
    """Action payload sent with `remove_dataset` calls"""

    class Meta(Action.Meta):
        args = ["dataset_id"]

    type = ActionType.REMOVE_DATASET
    dataset_id: StrictStr


class ReplaceDatasetAction(Action):
    """Action payload sent with `replace_dataset` calls"""

    class Meta(Action.Meta):
        args = ["this_dataset_id", "with_dataset"]

    type = ActionType.REPLACE_DATASET
    this_dataset_id: StrictStr
    with_dataset: _DatasetCreationProps


class GetDatasetWithDataAction(Action):
    """Action payload sent with `get_dataset_with_data` calls"""

    class Meta(Action.Meta):
        args = ["dataset_id"]

    type = ActionType.GET_DATASET_WITH_DATA
    dataset_id: StrictStr


#########
# UTILS #
#########


def normalize_dataset(
    dataset: Union[Dataset, Dict, None],
    kwargs: Dict[str, Any],
    fields_to_exclude: Optional[List[str]] = None,
) -> Dict:
    # convert to dict to make transformations
    if isinstance(dataset, BaseDataset):
        dataset_dict = dataset.dict(exclude_none=True)
    elif dataset is not None and isinstance(dataset, dict):
        dataset_dict = dataset
    else:
        dataset_dict = kwargs

    if fields_to_exclude:
        for field in fields_to_exclude:
            if field in dataset_dict:
                del dataset_dict[field]

    return dataset_dict


def normalize_data(
    data: Union[str, dict, List[List[Any]], "pd.DataFrame", "gpd.GeoDataFrame"]
) -> Union[str, dict, List[List[Any]]]:

    if pd is not None and isinstance(data, pd.DataFrame):
        # convert to CSV string
        return data.to_csv()
    elif gpd is not None and isinstance(data, gpd.GeoDataFrame):
        # convert to GeoJSON FeatureCollection
        return data.to_json()
    else:
        return data


###########
# METHODS #
###########


class BaseDatasetApiMethods:
    @abstractmethod
    def add_dataset(
        self,
        dataset: Union[Dataset, Dict, None] = None,
        *,
        auto_create_layers: bool = True,
        center_map: bool = True,
        **kwargs: Any,
    ) -> Optional[Dataset]:
        ...

    @abstractmethod
    def add_tile_dataset(
        self,
        dataset: Union[Dataset, Dict, None] = None,
        *,
        auto_create_layers: bool = True,
        center_map: bool = True,
        **kwargs: Any,
    ) -> Optional[Dataset]:
        ...

    @abstractmethod
    def update_dataset(
        self, dataset_id: str, values: Union[Dataset, Dict, None] = None, **kwargs: Any
    ) -> Optional[Dataset]:
        ...

    @abstractmethod
    def remove_dataset(self, dataset_id: str) -> None:
        ...

    @abstractmethod
    def replace_dataset(
        self, this_dataset_id: str, with_dataset: Optional[dict] = None, **kwargs: Any
    ) -> Optional[Dataset]:
        ...


class BaseInteractiveDatasetApiMethods:
    @abstractmethod
    def get_datasets(self) -> List[Dataset]:
        ...

    @abstractmethod
    def get_dataset_by_id(self, dataset_id: str) -> Optional[Dataset]:
        ...

    @abstractmethod
    def get_dataset_with_data(self, dataset_id: str) -> Optional[DatasetWithData]:
        ...


class DatasetApiNonInteractiveMixin(BaseDatasetApiMethods):
    """Dataset methods that are supported in non-interactive (i.e. pure HTML) maps"""

    transport: BaseNonInteractiveTransport

    @validate_kwargs(positional_only=["dataset"])
    def add_dataset(
        self,
        dataset: Union[Dataset, Dict, None] = None,
        *,
        auto_create_layers: bool = True,
        center_map: bool = True,
        **kwargs: Any,
    ) -> None:
        """Adds a new dataset to the map.

        Args:
            dataset:
                A dictionary with the following format. Unused if these attributes are provided through kwargs.
                    id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
                    label (Optional[str]): Displayable dataset label.
                    color: (Optional[Tuple[float, float, float]]): Color label of the dataset
                    data: (Union[str, dict, List[List[Any]]]): Data used to create a dataset, in CSV, JSON, or GeoJSON format (for local datasets).
                    metadata: (Dict): Object containing tileset metadata (for tiled datasets).

        Kwargs:
            auto_create_layers:
                Whether to attempt and create new layer(s) when adding a dataset. Defaults to True.
            center_map:
                Whether to center the map to fit the new layer bounds. Defaults to True.
            id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
            label (Optional[str]): Displayable dataset label.
            color: (Optional[Tuple[float, float, float]]): Color label of the dataset
            data: (Union[str, dict, List[List[Any]]]): Data used to create a dataset, in CSV, JSON, or GeoJSON format (for local datasets).
            metadata: (Dict): Object containing tileset metadata (for tiled datasets).
        """

        dataset = normalize_dataset(dataset, kwargs, ["fields"])

        if "data" in dataset:
            dataset["data"] = normalize_data(dataset["data"])

        action = AddDatasetAction(
            dataset=dataset,
            auto_create_layers=auto_create_layers,
            center_map=center_map,
        )
        self.transport.send_action(action=action, response_class=None)

    @validate_kwargs(positional_only=["dataset"])
    def add_tile_dataset(
        self,
        dataset: Union[Dataset, Dict, None] = None,
        *,
        auto_create_layers: bool = True,
        center_map: bool = True,
        **kwargs: Any,
    ) -> None:
        """Adds a new dataset to the map.

        Args:
            dataset:
                A dictionary with the following format. Unused if these attributes are provided through kwargs.
                    id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
                    label (Optional[str]): Displayable dataset label.
                    color: (Optional[Tuple[float, float, float]]): Color label of the dataset
                    metadata: (Dict): Object containing tileset metadata.

        Kwargs:
            auto_create_layers:
                Whether to attempt and create new layer(s) when adding a dataset. Defaults to True.
            center_map:
                Whether to center the map to fit the new layer bounds. Defaults to True.
            id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
            label (Optional[str]): Displayable dataset label.
            color: (Optional[Tuple[float, float, float]]): Color label of the dataset
            metadata: (Dict): Object containing tileset metadata.
        """

        dataset = normalize_dataset(dataset, kwargs, ["fields", "data"])

        action = AddTileDatasetAction(
            dataset=dataset,
            auto_create_layers=auto_create_layers,
            center_map=center_map,
        )
        self.transport.send_action(action=action, response_class=None)

    @validate_kwargs(positional_only=["dataset_id", "values"])
    def update_dataset(
        self,
        dataset_id: str,
        values: Union[_DatasetUpdateProps, dict, None] = None,
        **kwargs: Any,
    ) -> None:
        """Updates an existing dataset with given values.

        Args:
            dataset_id: The identifier of the dataset to update.
            values: The values to update.

        Kwargs:
            label: Displayable dataset label.
            color: Color label of the dataset.

        Returns:
            Updated dataset record.
        """

        action = UpdateDatasetAction(
            dataset_id=dataset_id, values=values if values else kwargs
        )
        self.transport.send_action(action=action, response_class=None)

    @validate_kwargs(positional_only=["dataset_id"])
    def remove_dataset(self, dataset_id: str) -> None:
        """Removes a dataset from the map.

        Args:
            dataset_id: The identifier of the dataset to remove

        Returns:
            None
        """
        action = RemoveDatasetAction(dataset_id=dataset_id)
        self.transport.send_action(action=action, response_class=None)

    @validate_kwargs(positional_only=["this_dataset_id", "with_dataset"])
    def replace_dataset(
        self,
        this_dataset_id: str,
        with_dataset: Union[Dataset, Dict, None] = None,
        **kwargs: Any,
    ) -> None:
        """Replaces a given dataset with a new one.

        Args:
            this_dataset_id: Identifier of the dataset to replace.
            with_dataset: Dataset details to replace the dataset with.

        Returns:
            The dataset that's now in use.
        """
        with_dataset = normalize_dataset(with_dataset, kwargs, ["fields", "data"])

        action = ReplaceDatasetAction(
            this_dataset_id=this_dataset_id,
            with_dataset=with_dataset,
        )
        self.transport.send_action(action=action, response_class=None)


class DatasetApiInteractiveMixin(
    BaseDatasetApiMethods, BaseInteractiveDatasetApiMethods
):

    transport: BaseInteractiveTransport

    def get_datasets(self) -> List[Dataset]:
        """Gets all the datasets currently available in the map.

        Returns:
            An array of datasets.
        """
        action = GetDatasetsAction()
        return self.transport.send_action_non_null(
            action=action, response_class=List[Dataset]
        )

    @validate_kwargs(positional_only=["dataset_id"])
    def get_dataset_by_id(self, dataset_id: str) -> Optional[Dataset]:
        """Retrieves a dataset by its identifier if it exists.

        Args:
            dataset_id: Identifier of the dataset to get.

        Returns:
            Dataset with a given identifier, or null if one doesn't exist.
        """
        action = GetDatasetByIdAction(dataset_id=dataset_id)
        return self.transport.send_action(action=action, response_class=Dataset)  # type: ignore

    @validate_kwargs(positional_only=["dataset"])
    def add_dataset(
        self,
        dataset: Optional[dict] = None,
        *,
        auto_create_layers: bool = True,
        center_map: bool = True,
        **kwargs: Any,
    ) -> Dataset:
        """Adds a new dataset to the map.

        Args:
            dataset:
                A dictionary with the following format. Unused if these attributes are provided through kwargs.
                    id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
                    label (Optional[str]): Displayable dataset label.
                    color: (Optional[Tuple[float, float, float]]): Color label of the dataset
                    data: (Union[str, dict, List[List[Any]]]): Data used to create a dataset, in CSV, JSON, or GeoJSON format (for local datasets).
                    metadata: (Dict): Object containing tileset metadata (for tiled datasets).

        Kwargs:
            auto_create_layers:
                Whether to attempt and create new layer(s) when adding a dataset. Defaults to True.
            center_map:
                Whether to center the map to fit the new layer bounds. Defaults to True.
            id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
            label (Optional[str]): Displayable dataset label.
            color: (Optional[Tuple[float, float, float]]): Color label of the dataset
            data: (Union[str, dict, List[List[Any]]]): Data used to create a dataset, in CSV, JSON, or GeoJSON format (for local datasets).
            metadata: (Dict): Object containing tileset metadata (for tiled datasets).
        """

        dataset = normalize_dataset(dataset, kwargs, ["fields"])

        if "data" in dataset:
            dataset["data"] = normalize_data(dataset["data"])

        action = AddDatasetAction(
            dataset=dataset,
            auto_create_layers=auto_create_layers,
            center_map=center_map,
        )
        return self.transport.send_action_non_null(
            action=action, response_class=Dataset  # type: ignore
        )

    @validate_kwargs(positional_only=["dataset"])
    def add_tile_dataset(
        self,
        dataset: Union[Dataset, Dict, None] = None,
        *,
        auto_create_layers: bool = True,
        center_map: bool = True,
        **kwargs: Any,
    ) -> Dataset:
        """Adds a new dataset to the map.

        Args:
            dataset:
                A dictionary with the following format. Unused if these attributes are provided through kwargs.
                    id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
                    label (Optional[str]): Displayable dataset label.
                    color: (Optional[Tuple[float, float, float]]): Color label of the dataset
                    metadata: (Dict): Object containing tileset metadata.

        Kwargs:
            auto_create_layers:
                Whether to attempt and create new layer(s) when adding a dataset. Defaults to True.
            center_map:
                Whether to center the map to fit the new layer bounds. Defaults to True.
            id (Optional[str]): Unique identifier of the dataset. If not provided, a random id will be generated.
            label (Optional[str]): Displayable dataset label.
            color: (Optional[Tuple[float, float, float]]): Color label of the dataset
            metadata: (Dict): Object containing tileset metadata.
        """

        dataset = normalize_dataset(dataset, kwargs, ["fields", "data"])

        action = AddTileDatasetAction(
            dataset=dataset,
            auto_create_layers=auto_create_layers,
            center_map=center_map,
        )
        return self.transport.send_action_non_null(
            action=action, response_class=Dataset  # type: ignore
        )

    @validate_kwargs(positional_only=["dataset_id", "values"])
    def update_dataset(
        self,
        dataset_id: str,
        values: Union[_DatasetUpdateProps, dict, None] = None,
        **kwargs: Any,
    ) -> Dataset:
        """Updates an existing dataset with given values.

        Args:
            dataset_id: The identifier of the dataset to update.
            values: The values to update.

        Kwargs:
            label: Displayable dataset label.
            color: Color label of the dataset.

        Returns:
            Updated dataset record.
        """

        action = UpdateDatasetAction(
            dataset_id=dataset_id, values=values if values else kwargs
        )
        return self.transport.send_action_non_null(
            action=action, response_class=Dataset  # type: ignore
        )

    @validate_kwargs(positional_only=["dataset_id"])
    def remove_dataset(self, dataset_id: str) -> None:
        """Removes a dataset from the map.

        Args:
            dataset_id: The identifier of the dataset to remove

        Returns:
            None
        """
        action = RemoveDatasetAction(dataset_id=dataset_id)
        self.transport.send_action(action=action, response_class=None)

    @validate_kwargs(positional_only=["this_dataset_id", "with_dataset"])
    def replace_dataset(
        self,
        this_dataset_id: str,
        with_dataset: Union[Dataset, Dict, None] = None,
        **kwargs: Any,
    ) -> Dataset:
        """Replaces a given dataset with a new one.

        Args:
            this_dataset_id: Identifier of the dataset to replace.
            with_dataset: Dataset details to replace the dataset with.

        Returns:
            The dataset that's now in use.
        """
        with_dataset = normalize_dataset(with_dataset, kwargs, ["fields", "data"])

        action = ReplaceDatasetAction(
            this_dataset_id=this_dataset_id,
            with_dataset=with_dataset,
        )
        return self.transport.send_action_non_null(
            action=action, response_class=Dataset  # type: ignore
        )

    @validate_kwargs(positional_only=["dataset_id"])
    def get_dataset_with_data(self, dataset_id: str) -> Optional[DatasetWithData]:
        """Retrieves a dataset record with its data for a given dataset if it exists.

        Args:
            dataset_id: Identifier of the dataset to get the record for.

        Returns:
            Dataset record with its data based on an identifier, or None if one doesn't exist.
        """
        action = GetDatasetWithDataAction(dataset_id=dataset_id)
        return self.transport.send_action(action=action, response_class=DatasetWithData)
