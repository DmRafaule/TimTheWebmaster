from rest_framework import serializers
from .models import Feed, FeedId, FeedGroup

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('__all__')
    # create # update #save method implementation herer

class FeedIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedId
        fields = ('user_id', 'similar_user_id', 'sort', 'posts_per_page', 'with_previews')

class FeedGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model =  FeedGroup
        fields = ('__all__')