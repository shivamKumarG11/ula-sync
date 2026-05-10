import uuid

from sqlalchemy import Column, ForeignKey, Index, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID

from app.extensions import db
from app.models.mixins import TimestampMixin


class CommunityPost(TimestampMixin, db.Model):
    __tablename__ = "community_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="SET NULL"),
        nullable=True,
    )
    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id", ondelete="SET NULL"),
        nullable=True,
    )
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    image_urls = Column(JSONB, nullable=False, default=list)
    likes_count = Column(Integer, nullable=False, default=0)
    comments_count = Column(Integer, nullable=False, default=0)

    user = db.relationship("User", back_populates="community_posts")
    trip = db.relationship("Trip", back_populates="community_posts")
    city = db.relationship("City", back_populates="community_posts")
    comments = db.relationship(
        "CommunityComment",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="CommunityComment.created_at",
        lazy="dynamic",
    )
    likes = db.relationship(
        "CommunityLike", back_populates="post", cascade="all, delete-orphan", lazy="dynamic"
    )

    __table_args__ = (
        Index("community_posts_user_id_idx", "user_id"),
        Index("community_posts_city_id_idx", "city_id"),
        Index("community_posts_trip_id_idx", "trip_id"),
        Index("community_posts_created_at_idx", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<CommunityPost {self.title[:30]}>"


class CommunityComment(TimestampMixin, db.Model):
    __tablename__ = "community_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("community_posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(Text, nullable=False)

    post = db.relationship("CommunityPost", back_populates="comments")
    user = db.relationship("User")

    __table_args__ = (Index("community_comments_post_id_idx", "post_id"),)

    def __repr__(self) -> str:
        return f"<CommunityComment post={self.post_id}>"


class CommunityLike(db.Model):
    __tablename__ = "community_likes"

    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("community_posts.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    liked_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ),
    )

    post = db.relationship("CommunityPost", back_populates="likes")

    __table_args__ = (
        PrimaryKeyConstraint("post_id", "user_id", name="pk_community_likes"),
    )

    def __repr__(self) -> str:
        return f"<CommunityLike post={self.post_id} user={self.user_id}>"
