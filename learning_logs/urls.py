from django.urls import path

from .views import (
    index,
    TopicList,
    TopicDetail,
    TopicCreate,
    TopicEdit,
    TopicDelete,
    EntryCreate,
    EntryEdit,
    EntryDelete,
)

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicList.as_view(), name="topics"),
    path("topics/<int:pk>/", TopicDetail.as_view(), name="topic"),
    path("new_topic/", TopicCreate.as_view(), name="new_topic"),
    path("edit_topic/<int:topic_id>/", TopicEdit.as_view(), name="edit_topic"),
    path("delete_topic/<int:topic_id>/", TopicDelete.as_view(), name="delete_topic"),
    path("new_entry/<int:topic_id>/", EntryCreate.as_view(), name="new_entry"),
    path("edit_entry/<int:entry_id>/", EntryEdit.as_view(), name="edit_entry"),
    path("delete_entry/<int:entry_id>/", EntryDelete.as_view(), name="delete_entry"),

]
