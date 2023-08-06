"""
Module to get videos data
"""
from typing import Any, Dict, List, Optional
import deeplabel.client
import deeplabel
from deeplabel.exceptions import InvalidIdError
import deeplabel.infer.videos.video_tasks
import deeplabel.infer.videos.video_graphs
from deeplabel.basemodel import DeeplabelBase, MixinConfig
from pydantic import Field, validator

class _VideoResolution(MixinConfig):
    height: int
    width: int


class _VideoFormat(MixinConfig):
    url: str
    resolution: Optional[_VideoResolution] = None
    extension: Optional[str] = None
    fps: Optional[float] = None
    file_size: Optional[float] = None


class _VideoUrl(MixinConfig):
    source: Optional[_VideoFormat] = None
    res360: Optional[_VideoFormat] = Field(None, alias="360P")
    res480: Optional[_VideoFormat] = Field(None, alias="480P")
    res720: Optional[_VideoFormat] = Field(None, alias="720P")
    res1080: Optional[_VideoFormat] = Field(None, alias="1080P")
    res1440: Optional[_VideoFormat] = Field(None, alias="1440P")
    res2160: Optional[_VideoFormat] = Field(None, alias="2160P")

class Video(DeeplabelBase):
    video_id: str
    project_id:str
    input_url: str
    parent_folder_id: Optional[str]
    ancestor_folder_ids: List[str] = []
    video_urls: Optional[_VideoUrl]
    video_url: Optional[str]
    video_fps: Optional[float] = None
    duration: Optional[float] = None  # in seconds
    title: Optional[str] = ''


    @validator("video_url", always=True)
    def validate_url(cls, value, values: Dict[str, Any]):  # type: ignore
        """
        Validate that either video_url or video_urls.source.url exists
        Since videoUrl can't be updated anymore, since it's deprecated,
        first check if videoUrls.source.url exists, and use that,
        else look for videoUrl
        If both are missing, use input_url as video_url
        Refer https://github.com/samuelcolvin/pydantic/issues/832#issuecomment-534896056
        """
        # video_urls.source.url
        try:
            source_url: str = values.get("video_urls", {}).source.url  # type: ignore
        except:
            # TODO: Call /videourl to get the videoUrl for the video. \
            # Let the node api handle the logic of setting the best videoUrl instead of hardcoding the logic here

            # should have either of the two
            # If video_url key is empty
            if isinstance(value, str):
                return value
            else:
                return values.get("input_url", "")
        # set video_url = video_urls.source.url
        return source_url

    @classmethod
    def from_search_params(
        cls, params: Dict[str, Any], client: "deeplabel.client.BaseClient"
    ) -> List["Video"]:
        resp = client.get("/videos", params=params)
        videos = resp.json()["data"]["videos"]
        videos = [cls(**video, client=client) for video in videos]
        return videos  # type: ignore

    @classmethod
    def create(
        cls,
        input_url: str,
        project_id: str,
        client: "deeplabel.client.BaseClient",
        parent_folder_id: Optional[str] = None,
    ) -> str:
        """Create a video and return the videoId"""
        resp = client.post(
            "/videos",
            {
                "inputUrl": input_url,
                "projectId": project_id,
                "parentFolderId": parent_folder_id,
            },
        )
        video_id = resp.json()["data"]["videoId"]
        # fetch again so that the videoUrl is set
        # return cls.from_video_id(video_id, client)
        return video_id

    @classmethod
    def from_video_id(
        cls, video_id: str, client: "deeplabel.client.BaseClient"
    ) -> "Video":
        video = cls.from_search_params({"videoId": video_id}, client=client)
        if not len(video):
            raise InvalidIdError(f"Failed to fetch video with videoId: {video_id}")
        return video[0]

    @classmethod
    def from_folder_id(
        cls, folder_id: str, client: "deeplabel.client.BaseClient"
    ) -> List["Video"]:
        return cls.from_search_params({"parentFolderId": folder_id}, client)

    @property
    def video_tasks(self) -> List["deeplabel.infer.videos.video_tasks.VideoTask"]:
        return deeplabel.infer.videos.video_tasks.VideoTask.from_video_id(
            self.video_id, self.client
        )
    
    @property
    def video_graphs(self) -> List['deeplabel.infer.videos.video_graphs.VideoGraph']:
        return deeplabel.infer.videos.video_graphs.VideoGraph.from_video_id(
            video_id = self.video_id, client = self.client
        )

    def update_metadata(self, data: Dict[str, Any]) -> "Video":
        """Update metadata of this video and return new Video object from it
        Since update might not work for all fields, do check in the returned
        Video object if the desired change has taken effect.

        Returns:
            Video: New Video object of the returned data
        """
        data["videoId"] = self.video_id
        res = self.client.put("/videos/metadata", json=data)
        video = res.json()["data"]
        return Video(**video)
