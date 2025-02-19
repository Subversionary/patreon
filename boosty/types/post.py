from datetime import datetime

from pydantic import UUID4, HttpUrl

from .base import BaseObject
from .comment import CommentsResponse
from .content import Content
from .donator import DonatorsResponse
from .poll import Poll
from .reactions import Reactions
from .teaser import Teaser
from .users import BlogUser
from ..utils.post import render_text, Entity


class Currency(BaseObject):
    USD: int | float
    RUB: int | float


class Tag(BaseObject):
    id: int
    title: str
    """Tag name"""


class SubscriptionLevel(BaseObject):
    id: int
    createdAt: datetime
    """Creation timestamp"""
    price: int
    changePrice: int | None = None
    data: list[Teaser]
    """Could be Conent type"""
    deleted: bool
    isArchived: bool
    name: str
    ownerId: int
    """post.user.id"""

    currencyPrices: Currency

    promos: dict | list  # TODO


class React(BaseObject):
    actor: str


class Count(BaseObject):
    likes: int
    comments: int
    reactions: Reactions


class Post(BaseObject):
    id: UUID4
    createdAt: datetime
    """Creation timestamp"""
    updatedAt: datetime
    """Last update timestamp"""
    publishTime: datetime
    """Publication timestamp"""
    isPublished: bool
    """Is post published to users"""
    user: BlogUser
    """Blogger user object"""

    title: str
    """Post title"""
    data: list[Content]
    """List of contents, attached to post (text included)"""
    tags: list[Tag]

    hasAccess: bool
    """Is post available for you"""
    teaser: list[Teaser]
    """Post teaser for users which haven't access to post"""

    count: Count
    """Count of likes, comments, reactions"""
    comments: CommentsResponse
    isCommentsDenied: bool
    isLiked: bool
    price: int
    """Price to open post"""
    signedQuery: str
    """Query for media fetching"""
    subscriptionLevel: SubscriptionLevel | None = None
    """Subscription level for non-free posts"""

    poll: Poll | None = None
    reacted: React | None = None
    """Unknown"""
    isWaitingVideo: bool
    """Unknown, probably an indicator, which shows if video is incomplete"""
    currencyPrices: Currency
    """Unknown"""
    isRecord: bool
    """Is post a stream record"""
    donators: DonatorsResponse
    """List of sponsors of the post"""
    donations: float | dict  # TODO dict is appearing sometimes
    """Amount of donations"""
    int_id: int
    """Unknown, probably post.id to int"""

    isDeleted: bool
    """TODO"""

    @property
    def url(self) -> HttpUrl:
        return HttpUrl(f"https://boosty.to/{self.user.blogUrl}/posts/{self.id}")

    @property
    def text(self) -> tuple[str, list[Entity]]:
        return render_text(self.data)


class PostsResponseExtra(BaseObject):
    isLast: bool
    """Is last page"""
    offset: str
    """Value for pagination. Example: :code:`1654884900:923396`"""


class PostsResponse(BaseObject):
    data: list[Post]
    extra: PostsResponseExtra
