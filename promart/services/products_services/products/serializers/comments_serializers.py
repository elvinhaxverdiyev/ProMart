from rest_framework import serializers
from products.models.comments import Comment
from typing import List, Dict


class CommentSerializer(serializers.ModelSerializer):
   
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", 
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            "id", 
            "product",  
            "user", 
            "text", 
            "created_at", 
        ]
        read_only_fields = ["id", "user"] 
        

    def get_user(self, obj: Comment) -> Dict[str, str]:
        """
        Returns the data of the user who made the comment.

        Args:
            obj (Comment): The comment object.

        Returns:
            dict: A dictionary containing the user's ID and email.
        """
        return {
            "id": obj.user.id,
            "email": obj.user.email,
            "name": obj.user.get_full_name() 
        }


    def get_poduct(self, obj: Comment) -> Dict[str, str]:
        """
        Returns the post's image and caption for the given comment.

        Args:
            obj (Comment): The comment object.

        Returns:
            dict: A dictionary containing the post's image and caption.
        """
        if obj.post:
            return {
                "image": obj.post.image.url if obj.post.image else None, 
                "caption": obj.post.caption
            }
        return {}

    def validate_text(self, value: str) -> str:
        """
        Validates that the comment text is not empty.

        Args:
            value (str): The comment text.

        Returns:
            str: The validated comment text.

        Raises:
            serializers.ValidationError: If the comment text is empty or only 
            contains whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value